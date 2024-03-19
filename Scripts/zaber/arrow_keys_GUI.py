import sys
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox
from PyQt6.QtCore import Qt
from zaber_motion import Units
from zaber_motion.ascii import Connection

class ArrowsGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.x_coord = 0
        self.y_coord = 0
        self.z_coord = 0
        self.selected_port = None
        self.speed = 8.99
        self.sleep_time = 0.1

        self.setWindowTitle("Zaber Stage Controller")
        self.initUI()

    def initUI(self):
        # Create arrow key buttons
        self.up_button = QPushButton("↑")
        self.down_button = QPushButton("↓")
        self.left_button = QPushButton("←")
        self.right_button = QPushButton("→")

        # Create buttons for vertical movement control
        self.move_up_button = QPushButton("Move Up")
        self.move_down_button = QPushButton("Move Down")

        # Setup
        self.setup_button = QPushButton("Setup")
        self.info_button = QPushButton("Info")

        # Speed input
        self.speed_label = QLabel("Speed: " + str(self.speed) + " mm/step")
        self.speed_edit = QLineEdit()
        self.speed_edit.returnPressed.connect(self.update_speed)
        self.speed_edit.setText(str(self.speed))

        # Connect arrow key buttons to functions
        self.up_button.clicked.connect(self.move_up)
        self.down_button.clicked.connect(self.move_down)
        self.left_button.clicked.connect(self.move_left)
        self.right_button.clicked.connect(self.move_right)
        self.move_up_button.clicked.connect(self.move_vertical_up)
        self.move_down_button.clicked.connect(self.move_vertical_down)

        # misc buttons
        self.setup_button.clicked.connect(self.setup)
        self.info_button.clicked.connect(self.info)

        # Set layout and add buttons to it
        layout = QGridLayout()
        layout.addWidget(self.move_up_button, 0, 3)
        layout.addWidget(self.move_down_button, 1, 3)
        layout.addWidget(self.up_button, 0, 1)
        layout.addWidget(self.down_button, 1, 1)
        layout.addWidget(self.left_button, 1, 0)
        layout.addWidget(self.right_button, 1, 2)
        layout.addWidget(self.setup_button, 1, 6)
        layout.addWidget(self.info_button, 2, 6)
        layout.addWidget(self.speed_label, 2, 1)
        layout.addWidget(self.speed_edit, 2, 2)

        for col in range(layout.columnCount()):
            layout.setColumnStretch(col, 1)

        comboBox = QComboBox()
        comboBox.addItem("")
        comboBox.addItem("COM1")
        comboBox.addItem("COM2")
        comboBox.addItem("COM3")
        comboBox.addItem("COM4")
        comboBox.addItem("COM5")
        comboBox.addItem("COM6")
        comboBox.currentIndexChanged.connect(self.selectionChanged)
        layout.addWidget(comboBox, 0, 6)

        port_label = QLabel('Port Selection: ')
        layout.addWidget(port_label, 0, 5)

        coord = QLabel('Coordinates (mm): ')
        coordX = QLabel('X: ' + str(self.x_coord))
        coordY = QLabel('Y: ' + str(self.y_coord))
        coordZ = QLabel('Z: ' + str(self.z_coord))
        layout.addWidget(coord, 3, 0)
        layout.addWidget(coordX, 3, 1)
        layout.addWidget(coordY, 3, 2)
        layout.addWidget(coordZ, 3, 3)
        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def move_up(self):
      try:
        axis_x.move_relative(-1*self.speed, Units.LENGTH_MILLIMETRES)
        updateCoords()
        print("Moving Up")
      except:
        print("X out of range")
      time.sleep(self.sleep_time)

    def move_down(self):
      try:
        axis_x.move_relative(self.speed, Units.LENGTH_MILLIMETRES)
        updateCoords()
        print("Moving Down")
      except:
        print("X Out of Range")
        time.sleep(self.sleep_time)

    def move_left(self):
        try:
          axis_y.move_relative(self.speed, Units.LENGTH_MILLIMETRES)
          updateCoords()
          print("Moving Left")
        except:
          print("Y out of range")
        time.sleep(self.sleep_time)

    def move_right(self):
      try:
        axis_y.move_relative(-1*self.speed, Units.LENGTH_MILLIMETRES)
        updateCoords()
        print("Moving Right")
      except:
        print("Y out of range")
      time.sleep(self.sleep_time)

    def move_vertical_down(self):
      try:
        axis_z.move_relative(self.speed, Units.LENGTH_MILLIMETRES)
        updateCoords()
      except:
        print("Z out of range")
      time.sleep(self.sleep_time)

    def move_vertical_up(self):
      try:
        axis_z.move_relative(-1*self.speed, Units.LENGTH_MILLIMETRES)
        updateCoords()
      except:
        print("Z out of range")
      time.sleep(self.sleep_time)

    def update_speed(self):
      try:
          speed = float(self.speed_edit.text())
          self.speed = speed
          self.speed_label.setText("Speed: " + str(self.speed) + " mm/step")  # Update the speed_label text
      except ValueError:
          # Handle invalid input
          pass

    def setup(self):
        if (self.selected_port is None):
            dialog = QDialog()
            dialog.setWindowTitle('Warning')

            layout = QVBoxLayout()

            label = QLabel('You must select a serial port before testing the connection.')
            layout.addWidget(label)

            ok_button = QPushButton('OK')
            ok_button.clicked.connect(dialog.accept)
            layout.addWidget(ok_button)

            dialog.setLayout(layout)
            dialog.exec()

            return False
        else:
            try:
                with Connection.open_serial_port(self.selected_port) as connection:
                    connection.enable_alerts()

                    device_list = connection.detect_devices()

                    return True
            except Exception as e:
                return False

    def info(self):
      dialog = QDialog()
      dialog.setWindowTitle('Instructions')

      layout = QVBoxLayout()

      label = QLabel(('Controls: \n'
                      '-> Control X/Y-Axis: Arrows\n'
                      '-> Control Z Axis Up/Down\n'
                      'Input COM port and press setup before moving stage\n'))

      layout.addWidget(label)

      ok_button = QPushButton('OK')
      ok_button.clicked.connect(dialog.accept)
      layout.addWidget(ok_button)

      dialog.setLayout(layout)
      dialog.exec()

    def selectionChanged(self, index):
        if index != 0:
            self.selected_port = "COM" + str(index)
        else:
            self.selected_port = None

    def updateCoords():
      self.x_coord = axis_x.get_position(Units.LENGTH_MILLIMETRES)
      self.y_coord = axis_y.get_position(Units.LENGTH_MILLIMETRES)
      self.z_coord = axis_z.get_position(Units.LENGTH_MILLIMETRES)

      self.coordX.setText('X: ' + str(self.x_coord))  
      self.coordY.setText('Y: ' + str(self.y_coord))  
      self.coordZ.setText('Z: ' + str(self.z_coord))  

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ArrowsGUI()
    window.show()
    sys.exit(app.exec())
