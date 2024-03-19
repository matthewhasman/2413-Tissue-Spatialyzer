import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QSize

from zaber.move_to_well import WellPlateGUI
from zaber.arrow_keys_GUI import ArrowsGUI

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tissue Spatialyzer")
        self.setFixedSize(QSize(400, 300))

        # Create three buttons
        self.wells = QPushButton("96-Well Microplate")
        self.arrows = QPushButton("Control Zaber Stage")
        self.fluidics = QPushButton("Control Fluigent Hardware")

        # Set layout and add buttons to it
        layout = QVBoxLayout()
        layout.addWidget(self.wells)
        layout.addWidget(self.arrows)
        layout.addWidget(self.fluidics)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Connect button signals to functions
        self.wells.clicked.connect(self.move_wells)
        self.arrows.clicked.connect(self.arrows_start)

        # Attribute to hold the instance of ArrowsGUI
        self.arrows_window = None

    def move_wells(self):
        # Instantiate and show the new window
        new_window = WellPlateGUI()
        new_window.show()

    def arrows_start(self):
        # Create an instance of ArrowsGUI and store it in self.arrows_window
        self.arrows_window = ArrowsGUI()
        self.arrows_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
