import sys
from PyQt6.QtWidgets import *
from zaber_motion import Units
from zaber_motion.ascii import Connection
from time import sleep

WELL_SPACING_mm = 8.99

class WellPlateGUI(QWidget):

    def __init__(self):
        super().__init__()
        self.x_coord = None
        self.y_coord = None
        self.selected_port = None
        self.connection = None
        self.x_axis = None
        self.y_axis = None
        self.z_axis = None
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

            # Remove seal before moving to new well
            self.z_axis.move_absolute(90, Units.LENGTH_MILLIMETRES)

            try:
                self.x_axis.move_absolute(x_coord, Units.LENGTH_MILLIMETRES, wait_until_idle=False)
                self.y_axis.move_absolute(y_coord, Units.LENGTH_MILLIMETRES, wait_until_idle=False)
            except Exception as e:
                dialog = QDialog()
                dialog.setWindowTitle(type(e).__name__)

                layout = QVBoxLayout()

                label = QLabel(str(e))
                layout.addWidget(label)

                ok_button = QPushButton('OK')
                ok_button.clicked.connect(dialog.accept)
                layout.addWidget(ok_button)

                dialog.setLayout(layout)
                dialog.exec()


    def handle_x_input(self, line_edit):
        self.x_coord = float(line_edit.text())
        self.grid.itemAtPosition(0,13).widget().setText('Top Left X Position: ' + str(self.x_coord))

    def handle_y_input(self, line_edit):
        self.y_coord = float(line_edit.text())
        self.grid.itemAtPosition(0,14).widget().setText('Top Left X Position: ' + str(self.y_coord))

    def testAll(self):
        # Add labels for rows (A-H)
        rows_label = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

        # Add labels for columns (1-12)
        columns_label = [str(i) for i in range(1, 13)]

        # Add buttons for each well
        for row in range(len(rows_label)):
            for col in range(len(columns_label)):
                self.move_to_well(rows_label[row] + str(col+1))
                self.x_axis.wait_until_idle()
                self.y_axis.wait_until_idle()
                self.z_axis.wait_until_idle()
                self.create_seal()
                sleep(.25)

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
            except Exception as e:
                dialog = QDialog()
                dialog.setWindowTitle(type(e).__name__)

                layout = QVBoxLayout()

                label = QLabel(str(e))
                layout.addWidget(label)

                ok_button = QPushButton('OK')
                ok_button.clicked.connect(dialog.accept)
                layout.addWidget(ok_button)

                dialog.setLayout(layout)
                dialog.exec()

                self.connection = None
                self.grid.itemAtPosition(2,14).widget().setText("Connection Status: Disconnected")
        else:
            self.connection.close()
            self.selected_port = None
            self.grid.itemAtPosition(2,14).widget().setText("Connection Status: Disconnected")
        
    def create_seal(self):
        self.z_axis.wait_until_idle()
        self.z_axis.move_absolute(105, Units.LENGTH_MILLIMETRES)

    def initGUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

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
                grid.addWidget(button, row, col)


        x_line_edit = QLineEdit()
        x_line_edit.returnPressed.connect(lambda: self.handle_x_input(x_line_edit))
        grid.addWidget(x_line_edit, 1, 13)

        y_line_edit = QLineEdit()
        y_line_edit.returnPressed.connect(lambda: self.handle_y_input(y_line_edit))
        grid.addWidget(y_line_edit, 1, 14)

        # Add label for the QLineEdit
        label = QLabel('Top Left X Position:')
        grid.layout().addWidget(label, 0, 13)

        label = QLabel('Top Left Y Position:')
        grid.layout().addWidget(label, 0, 14)

        comboBox = QComboBox()
        comboBox.addItem("")
        comboBox.addItem("COM1")
        comboBox.addItem("COM2")
        comboBox.addItem("COM3")
        comboBox.addItem("COM4")
        comboBox.addItem("COM5")
        comboBox.addItem("COM6")
        comboBox.currentIndexChanged.connect(self.selectionChanged)
        grid.layout().addWidget(comboBox, 3, 13)

        label = QLabel('Port Selection')
        grid.layout().addWidget(label, 2, 13)

        label = QLabel("Connection Status: Unknown")
        grid.layout().addWidget(label, 2, 14)

        label = QLabel("Seal Status: Unknown")
        grid.layout().addWidget(label, 4, 13)

        seal_well_button = QPushButton("Seal Well")
        seal_well_button.clicked.connect(self.create_seal)
        grid.layout().addWidget(seal_well_button, 5, 13)

        test_all_button = QPushButton("Run All Well Test")
        test_all_button.clicked.connect(self.testAll)
        grid.layout().addWidget(test_all_button, 5, 14)

        self.grid = grid

        self.setWindowTitle('96-Well Microplate GUI')
        self.setGeometry(100, 100, 800, 600)
        self.show()

    def closeEvent(self, event):
        self.connection.close()
        return super().closeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    well_plate_gui = WellPlateGUI()
    app.exec()