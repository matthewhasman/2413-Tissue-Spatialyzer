import sys

from PyQt6.QtGui import QCloseEvent
from move_once import move_once
from create_seal import create_seal
from PyQt6.QtWidgets import *
from zaber_motion import Units
from zaber_motion.ascii import Connection

WELL_SPACING_mm = 8.99

class WellPlateGUI(QWidget):

    def __init__(self):
        super().__init__()
        self.initGUI()
        self.x_coord = None
        self.y_coord = None
        self.selected_port = None

    def well_button_clicked(self, button_name):
        
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
        elif (self.selected_port == None):
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
            number = int(button_name[1])

            x_coord = self.x_coord + WELL_SPACING_mm * character_id
            y_coord = self.y_coord - WELL_SPACING_mm * (number-1)

            self.x_axis.wait_until_idle()
            self.y_axis.wait_until_idle()
            self.z_axis.wait_until_idle()

            # Remove seal before moving to new well
            self.z_axis.move_absolute(50, Units.LENGTH_MILLIMETRES, wait_until_idle=False)

            try:
                self.x_axis.move_absolute(x_coord, Units.LENGTH_MILLIMETRES, wait_until_idle=False)
                self.y_axis.move_absolute(y_coord, Units.LENGTH_MILLIMETRES, wait_until_idle=False)
                self.x_axis.wait_until_idle()
                self.y_axis.wait_until_idle()
                self.z_axis.wait_until_idle()
            except:
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
        self.x_coord = int(line_edit.text())

    def handle_y_input(self, line_edit):
        self.y_coord = int(line_edit.text())

    def selectionChanged(self, index):
        if index != 0:
            self.selected_port = "COM" + str(index)
            self.connection = Connection.open_serial_port(self.selected_port)
            self.connection.enable_alerts()

            device_list = self.connection.detect_devices()
            device = device_list[0]

            self.x_axis = device.get_lockstep(1)
            self.y_axis = device.get_axis(3)
            self.z_axis = device.get_axis(4)

            self.x_axis.home(wait_until_idle=False)
            self.y_axis.home(wait_until_idle=False)
            self.z_axis.home(wait_until_idle=False)
        else:
            self.connection.close()
            self.selected_port = None

    def test_connection(self):
        if self.check_zaber_connection():
            self.grid.itemAtPosition(2,14).widget().setText("Connection Status: Connected")
        else:
            self.grid.itemAtPosition(2,14).widget().setText("Connection Status: Disconnected")

    def check_zaber_connection(self):
        if (self.selected_port == None):
            dialog = QDialog()
            dialog.setWindowTitle('Warning')

            layout = QVBoxLayout()

            label = QLabel('You must selected a serial port before testing the connection.')
            layout.addWidget(label)

            ok_button = QPushButton('OK')
            ok_button.clicked.connect(dialog.accept)
            layout.addWidget(ok_button)

            dialog.setLayout(layout)
            dialog.exec()

            return False
        else:
            try:
                with Connection.open_serial_port(self.port) as connection:
                    connection.enable_alerts()

                    device_list = connection.detect_devices()

                    return True
            except Exception as e:
                return False
        
    def create_seal(self):
        if create_seal(self.selected_port):
            self.grid.itemAtPosition(4,13).widget().setText("Seal Status: Successful")
        else:
            self.grid.itemAtPosition(4,13).widget().setText("Seal Status: Failed")

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

        test_button = QPushButton("Test Connection")
        test_button.clicked.connect(self.test_connection)
        grid.layout().addWidget(test_button, 3, 14)

        label = QLabel("Seal Status: Unknown")
        grid.layout().addWidget(label, 4, 13)

        seal_well_button = QPushButton("Seal Well")
        seal_well_button.clicked.connect(self.create_seal)
        grid.layout().addWidget(seal_well_button, 5, 13)

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