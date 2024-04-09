import sys
import serial.tools.list_ports
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import *
from PyQt6 import QtCore
from zaber_motion import Units
from zaber_motion.ascii import Connection
from time import sleep
import random

WELL_SPACING_mm = 8.99
DEFUALT_X_COORD_mm = 71.55
DEFUALT_Y_COORD_mm = 404.95

class ExceptionDialog:
    @staticmethod
    def show_exception_dialog(exception):
        dialog = QDialog()
        dialog.setWindowTitle(type(exception).__name__)

        layout = QVBoxLayout()

        label = QLabel(str(exception))
        layout.addWidget(label)

        ok_button = QPushButton('OK')
        ok_button.clicked.connect(dialog.accept)
        layout.addWidget(ok_button)

        dialog.setLayout(layout)
        dialog.exec()

class TaskProgressWindow(QMainWindow):
        def __init__(self):
            super().__init__()

            self.setWindowTitle("Task Progress")
            self.setGeometry(200, 200, 400, 150)

            main_widget = QWidget()
            self.setCentralWidget(main_widget)

            # Create a main layout for the central widget
            main_layout = QVBoxLayout()
            main_widget.setLayout(main_layout)

            # Create a widget to hold the progress bar and label
            progress_widget = QWidget()
            progress_layout = QVBoxLayout()
            progress_widget.setLayout(progress_layout)

            # Add a label above the progress bar
            label = QLabel("Task Completion Percentage")
            label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)  # Align text horizontally to the center
            progress_layout.addWidget(label)

            # Add the progress bar
            self.progress_bar = QProgressBar()
            self.progress_bar.setRange(0, 100)  # Set the range from 0 to 100
            progress_layout.addWidget(self.progress_bar)

            # Add the progress widget to the main layout
            main_layout.addStretch(1)  # Add stretchable space above the progress widget
            main_layout.addWidget(progress_widget)
            main_layout.addStretch(1)  # Add stretchable space below the progress widget


        def update_progress(self, percent):
            self.progress_bar.setValue(percent)

class StartupPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Startup Page")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.run_button = QPushButton("Run Experiment")
        self.run_button.setEnabled(False)  # Button starts as grayed out
        layout.addWidget(self.run_button)

        self.debug_button = QPushButton("Debugging")
        layout.addWidget(self.debug_button)
        self.debug_button.clicked.connect(self.open_debug_window)

        self.setLayout(layout)

    def open_debug_window(self):
        self.debug_window = DebugWindow()  # Keep a reference to the debug window
        self.debug_window.show()

    def close_debug_window(self):
        if hasattr(self, 'debug_window'):
            self.debug_window.close()

    def closeEvent(self, event):
        self.close_debug_window()
        return super().closeEvent(event)

class DebugWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Debugging Window")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)

        self.zaber_xyz_tab = ZaberWidget()
        self.fluigent_tab = QWidget()
        self.camera_tab = QWidget()
        self.scripting_tab = QWidget()

        self.central_widget.addTab(self.zaber_xyz_tab, "Zaber XYZ Stage")
        self.central_widget.addTab(self.fluigent_tab, "Fluigent")
        self.central_widget.addTab(self.camera_tab, "Microscope Camera")
        self.central_widget.addTab(self.scripting_tab, "Scripting")

        self.setup_fluigent_tab()
        self.setup_camera_tab()
        self.setup_scripting_tab()

    def setup_fluigent_tab(self):
        layout = QVBoxLayout()
        label = QLabel("This is a work in progress.")
        layout.addWidget(label)
        self.fluigent_tab.setLayout(layout)

    def setup_camera_tab(self):
        layout = QVBoxLayout()
        label = QLabel("This is a work in progress.")
        layout.addWidget(label)
        self.camera_tab.setLayout(layout)

    def setup_scripting_tab(self):
        layout = QVBoxLayout()
        label = QLabel("This is a work in progress.")
        layout.addWidget(label)
        self.scripting_tab.setLayout(layout)

class ZaberWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.x_coord = DEFUALT_X_COORD_mm
        self.y_coord = DEFUALT_Y_COORD_mm
        self.selected_port = None
        self.connection = None
        self.x_axis = None
        self.y_axis = None
        self.z_axis = None
        self.speed = 8.99
        self.sleep_time = 0.1
        self.curr_x = 0
        self.curr_y = 0
        self.curr_z = 0
        self.initGUI()

    def well_button_clicked(self, button_name):
        self.move_to_well(button_name)

    def move_to_well(self, button_name):
        if (self.x_coord == None or self.y_coord == None):
            dialog = QDialog()
            dialog.setWindowTitle('Warning')

            layout = QVBoxLayout()

            label = QLabel('You must set both the x and y coordinates of the top left well before moving the stage.')
            layout.addWidget(label)

            ok_button = QPushButton('OK')
            ok_button.clicked.connect(dialog.accept)
            layout.addWidget(ok_button)

            dialog.setLayout(layout)
            dialog.exec()
        elif (self.selected_port == None or self.connection == None):
            dialog = QDialog()
            dialog.setWindowTitle('Warning')

            layout = QVBoxLayout()

            label = QLabel('You must selected a serial port before using the stage.')
            layout.addWidget(label)

            ok_button = QPushButton('OK')
            ok_button.clicked.connect(dialog.accept)
            layout.addWidget(ok_button)

            dialog.setLayout(layout)
            dialog.exec()
        else:
            letter = button_name[0].lower()
            character_id = ord(letter) - ord('a')
            number = int(button_name[1:])

            x_coord = self.x_coord + WELL_SPACING_mm * character_id
            y_coord = self.y_coord - WELL_SPACING_mm * (number-1)

            self.x_axis.wait_until_idle()
            self.y_axis.wait_until_idle()

            try:
                # Remove seal before moving to new well
                self.z_axis.move_absolute(90, Units.LENGTH_MILLIMETRES)
                self.x_axis.move_absolute(x_coord, Units.LENGTH_MILLIMETRES, wait_until_idle=False)
                self.y_axis.move_absolute(y_coord, Units.LENGTH_MILLIMETRES, wait_until_idle=False)
                self.grid.itemAtPosition(4, 13).widget().setText("Seal Status: Unsealed")
                self.updateCoords()
            except Exception as e:
                ExceptionDialog.show_exception_dialog(e)


    def handle_x_input(self, line_edit):
        try:
            self.x_coord = float(line_edit.text())
            self.grid.itemAtPosition(0,13).widget().setText('Top Left X Position (mm): ' + str(self.x_coord))
        except Exception as e:
            ExceptionDialog.show_exception_dialog(e)


    def handle_y_input(self, line_edit):
        try:
            self.y_coord = float(line_edit.text())
            self.grid.itemAtPosition(0,14).widget().setText('Top Left Y Position (mm): ' + str(self.y_coord))
        except Exception as e:
            ExceptionDialog.show_exception_dialog(e)

    def testAll(self):
        # Add labels for rows (A-H)
        rows_label = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

        # Add labels for columns (1-12)
        columns_label = [str(i) for i in range(1, 13)]

        progress = 0
        total_wells = len(rows_label) * len(columns_label)
        test_progress_window = TaskProgressWindow()
        test_progress_window.show()

        test_progress_window.update_progress(0)

        try:
            # Add buttons for each well
            for row in range(len(rows_label)):
                for col in range(len(columns_label)):
                    self.move_to_well(rows_label[row] + str(col+1))
                    self.x_axis.wait_until_idle()
                    self.y_axis.wait_until_idle()
                    self.z_axis.wait_until_idle()
                    self.create_seal()
                    sleep(.25)
                    progress = progress + 1
                    test_progress_window.update_progress(round(progress/total_wells))
                    test_progress_window.close()

        except Exception as e:
            test_progress_window.close()
            ExceptionDialog.show_exception_dialog(e)

    def randomMove(self):
        # Add labels for rows (A-H)
        rows_label = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

        # Add labels for columns (1-12)
        columns_label = [str(i) for i in range(1, 13)]

        test_progress_window = TaskProgressWindow()
        test_progress_window.show()

        test_progress_window.update_progress(0)

        try:
            # Add buttons for each well
            for i in range(10):
                row = random.choice(rows_label)
                col = random.choice(columns_label)
                self.move_to_well(row + str(col))
                self.x_axis.wait_until_idle()
                self.y_axis.wait_until_idle()
                self.z_axis.wait_until_idle()
                self.create_seal()
                sleep(.25)
                test_progress_window.update_progress( (i+1) * 10)
                test_progress_window.close()
        except Exception as e:
            test_progress_window.close()
            ExceptionDialog.show_exception_dialog(e)

    def selectionChanged(self, index):
        if index != 0:
            try:
                self.selected_port = "COM" + str(index)
                self.connection = Connection.open_serial_port(self.selected_port)
                self.connection.enable_alerts()

                device_list = self.connection.detect_devices()
                device = device_list[0]

                self.x_axis = device.get_lockstep(1)
                self.y_axis = device.get_axis(3)
                self.z_axis = device.get_axis(4)

                self.z_axis.home()
                self.x_axis.home(wait_until_idle=False)
                self.y_axis.home(wait_until_idle=False)

                self.grid.itemAtPosition(2,14).widget().setText("Connection Status: Connected")
                self.grid.itemAtPosition(4, 13).widget().setText("Seal Status: Unsealed")
            except Exception as e:
                ExceptionDialog.show_exception_dialog(e)

                self.connection = None
                self.grid.itemAtPosition(2,14).widget().setText("Connection Status: Disconnected")
                self.grid.itemAtPosition(4, 13).widget().setText("Seal Status: Unknown")
        else:
            self.connection.close()
            self.selected_port = None
            self.grid.itemAtPosition(2,14).widget().setText("Connection Status: Disconnected")
            self.grid.itemAtPosition(4, 13).widget().setText("Seal Status: Unknown")
        
    def create_seal(self):
        try:
            self.z_axis.wait_until_idle()
            self.z_axis.move_absolute(105, Units.LENGTH_MILLIMETRES)
            self.grid.itemAtPosition(4, 13).widget().setText("Seal Status: Sealed")
            self.updateCoords()
        except Exception as e:
            ExceptionDialog.show_exception_dialog(e)

    def remove_seal(self):
        try:
            self.z_axis.wait_until_idle()
            self.z_axis.move_absolute(90, Units.LENGTH_MILLIMETRES)
            self.grid.itemAtPosition(4, 13).widget().setText("Seal Status: Unsealed")
            self.updateCoords()
        except Exception as e:
            ExceptionDialog.show_exception_dialog(e)

    def initGUI(self):
        microwell_grid = QGridLayout()
        main_grid = QGridLayout()
        self.setLayout(main_grid)

        main_grid.addLayout(microwell_grid, 0, 0)

        # Add labels for rows (A-H)
        rows_label = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

        # Add labels for columns (1-12)
        columns_label = [str(i) for i in range(1, 13)]


        # Add buttons for each well
        for row in range(len(rows_label)):
            for col in range(len(columns_label)):
                button_name = f'{rows_label[row]}{columns_label[col]}'
                button = QPushButton(button_name)
                button.clicked.connect(lambda checked, name=button_name: self.well_button_clicked(name))
                microwell_grid.addWidget(button, row, col)

        x_line_edit = QLineEdit()
        x_line_edit.returnPressed.connect(lambda: self.handle_x_input(x_line_edit))
        microwell_grid.addWidget(x_line_edit, 1, 13)

        y_line_edit = QLineEdit()
        y_line_edit.returnPressed.connect(lambda: self.handle_y_input(y_line_edit))
        microwell_grid.addWidget(y_line_edit, 1, 14)

        # Add label for the QLineEdit
        label = QLabel('Top Left X Position (mm): ' + str(self.x_coord))
        microwell_grid.layout().addWidget(label, 0, 13)

        label = QLabel('Top Left Y Position (mm): ' + str(self.y_coord))
        microwell_grid.layout().addWidget(label, 0, 14)

        comboBox = QComboBox()
        comboBox.addItem("")
        comboBox.addItem("COM1")
        comboBox.addItem("COM2")
        comboBox.addItem("COM3")
        comboBox.addItem("COM4")
        comboBox.addItem("COM5")
        comboBox.addItem("COM6")
        comboBox.currentIndexChanged.connect(self.selectionChanged)
        microwell_grid.layout().addWidget(comboBox, 3, 13)

        label = QLabel('Port Selection')
        microwell_grid.layout().addWidget(label, 2, 13)

        label = QLabel("Connection Status: Unknown")
        microwell_grid.layout().addWidget(label, 2, 14)

        label = QLabel("Seal Status: Unknown")
        microwell_grid.layout().addWidget(label, 4, 13)

        seal_well_button = QPushButton("Seal Well")
        seal_well_button.clicked.connect(self.create_seal)
        microwell_grid.layout().addWidget(seal_well_button, 5, 13)

        test_all_button = QPushButton("Run All Well Test")
        test_all_button.clicked.connect(self.testAll)
        microwell_grid.layout().addWidget(test_all_button, 5, 14)

        unseal_button = QPushButton("Remove Seal")
        unseal_button.clicked.connect(self.remove_seal)
        microwell_grid.layout().addWidget(unseal_button, 6, 13)

        random_button = QPushButton("Random Wells")
        random_button.clicked.connect(self.randomMove)
        microwell_grid.layout().addWidget(random_button, 6, 14)

        self.grid = microwell_grid

        width = 100

        # Create arrow key buttons
        up_button = QPushButton("↑")
        up_button.setFixedSize(width, 20)
        down_button = QPushButton("↓")
        down_button.setFixedSize(width,20)
        left_button = QPushButton("←")
        left_button.setFixedSize(width, 20)
        right_button = QPushButton("→")
        right_button.setFixedSize(width, 20)

        # Create buttons for vertical movement control
        move_up_button = QPushButton("Move Up")
        move_up_button.setFixedSize(width, 20)
        move_down_button = QPushButton("Move Down")
        move_down_button.setFixedSize(width, 20)

        # Speed input
        self.speed_label = QLabel(str(self.speed) + " mm/step")
        self.speed_label.setFixedSize(width,20)
        self.speed_edit = QLineEdit()
        self.speed_edit.setFixedSize(width,20)
        self.speed_edit.returnPressed.connect(self.update_speed)

        # Connect arrow key buttons to functions
        up_button.clicked.connect(self.move_up)
        down_button.clicked.connect(self.move_down)
        left_button.clicked.connect(self.move_left)
        right_button.clicked.connect(self.move_right)
        move_up_button.clicked.connect(self.move_vertical_up)
        move_down_button.clicked.connect(self.move_vertical_down)

        # Set layout and add buttons to it
        arrow_key_grid = QGridLayout()

        main_grid.addLayout(arrow_key_grid, 1, 0)

        arrow_key_grid.addWidget(QLabel(''),0,8)

        arrow_key_grid.addWidget(move_up_button, 1, 8)
        arrow_key_grid.addWidget(move_down_button, 2, 8)
        arrow_key_grid.addWidget(up_button, 1, 6)
        arrow_key_grid.addWidget(down_button, 2, 6)
        arrow_key_grid.addWidget(left_button, 2, 5)
        arrow_key_grid.addWidget(right_button, 2, 7)
        arrow_key_grid.addWidget(self.speed_label, 3, 6)
        arrow_key_grid.addWidget(self.speed_edit, 3, 7)

        for col in range(arrow_key_grid.columnCount()):
            arrow_key_grid.setColumnStretch(col, 0)

        coord = QLabel('Coordinates (mm): ')
        coord.setFixedSize(width,20)
        self.coordX = QLabel('X: ' + str(self.curr_x))
        self.coordY = QLabel('Y: ' + str(self.curr_y))
        self.coordZ = QLabel('Z: ' + str(self.curr_z))
        self.coordX.setFixedSize(width,20)
        self.coordY.setFixedSize(width,20)
        self.coordZ.setFixedSize(width,20)
        arrow_key_grid.addWidget(coord, 4, 5)
        arrow_key_grid.addWidget(self.coordX, 4, 6)
        arrow_key_grid.addWidget(self.coordY, 4, 7)
        arrow_key_grid.addWidget(self.coordZ, 4, 8)

        arrow_key_grid.addWidget(QLabel(''), 2, 1)
        arrow_key_grid.addWidget(QLabel(''), 2, 14)

    def move_up(self):
      try:
        self.x_axis.wait_until_idle()
        self.y_axis.wait_until_idle()
        self.x_axis.move_relative(-1*self.speed, Units.LENGTH_MILLIMETRES)
        self.updateCoords()
      except Exception as e:
        ExceptionDialog.show_exception_dialog(e)
      sleep(self.sleep_time)

    def move_down(self):
      try:
        self.x_axis.wait_until_idle()
        self.y_axis.wait_until_idle()
        self.x_axis.move_relative(self.speed, Units.LENGTH_MILLIMETRES)
        self.updateCoords()
      except Exception as e:
        ExceptionDialog.show_exception_dialog(e)
        sleep(self.sleep_time)

    def move_left(self):
        try:
          self.x_axis.wait_until_idle()
          self.y_axis.wait_until_idle()
          self.y_axis.move_relative(self.speed, Units.LENGTH_MILLIMETRES)
          self.updateCoords()
        except Exception as e:
          ExceptionDialog.show_exception_dialog(e)
        sleep(self.sleep_time)

    def move_right(self):
      try:
        self.x_axis.wait_until_idle()
        self.y_axis.wait_until_idle()
        self.y_axis.move_relative(-1*self.speed, Units.LENGTH_MILLIMETRES)
        self.updateCoords()
      except Exception as e:
          ExceptionDialog.show_exception_dialog(e)
      sleep(self.sleep_time)

    def move_vertical_down(self):
      try:
        self.x_axis.wait_until_idle()
        self.y_axis.wait_until_idle()
        self.z_axis.move_relative(self.speed, Units.LENGTH_MILLIMETRES)
        self.updateCoords()
      except Exception as e:
        ExceptionDialog.show_exception_dialog(e)
      sleep(self.sleep_time)

    def move_vertical_up(self):
      try:
        self.x_axis.wait_until_idle()
        self.y_axis.wait_until_idle()
        self.z_axis.move_relative(-1*self.speed, Units.LENGTH_MILLIMETRES)
        self.updateCoords()
      except Exception as e:
        ExceptionDialog.show_exception_dialog(e)
      sleep(self.sleep_time)

    def update_speed(self):
      try:
          speed = float(self.speed_edit.text())
          self.speed = speed
          self.speed_label.setText(str(self.speed) + " mm/step")  # Update the speed_label text
      except ValueError:
          # Handle invalid input
          pass

    def updateCoords(self):
        try:
            self.x_axis.wait_until_idle()
            self.y_axis.wait_until_idle()

            self.curr_x = self.x_axis.get_position(Units.LENGTH_MILLIMETRES)
            self.curr_y = self.y_axis.get_position(Units.LENGTH_MILLIMETRES)
            self.curr_z = self.z_axis.get_position(Units.LENGTH_MILLIMETRES)

            self.coordX.setText('X: ' + str(self.curr_x))  
            self.coordY.setText('Y: ' + str(self.curr_y))  
            self.coordZ.setText('Z: ' + str(self.curr_z))      
        except Exception as e:
            ExceptionDialog.show_exception_dialog(e)


    def closeEvent(self, event):
        self.connection.close()
        return super().closeEvent(event)
    

def main():
    app = QApplication(sys.argv)
    startup_page = StartupPage()
    startup_page.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
