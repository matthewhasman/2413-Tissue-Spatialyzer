from zaber_motion import Units
from zaber_motion.ascii import Connection
from PyQt6.QtWidgets import *
import sys

# Constants
WELL_SPACING_MM = 8.99

def move_once(well="A1", port="COM1", ref_x_coord = 0, ref_y_coord = 200):
    """Moves to the given well based off of A1 reference x and y coordinates by connection to the Zaber stage with the input port.

    Args:
        well (string): Desired well to move to.
        port (string): Port that Zaber stage is connected to.
        ref_x_coord (int): X coordinate of the A1 well.
        ref_y_coord (int): Y coordinate of the A1 well.
    """

    with Connection.open_serial_port(port) as connection:
        connection.enable_alerts()

        device_list = connection.detect_devices()
        print("Found {} devices".format(len(device_list)))

        device = device_list[0]

        x_axis = device.get_lockstep(1)
        y_axis = device.get_axis(3)
        z_axis = device.get_axis(4)

        x_axis.home(wait_until_idle=False)
        y_axis.home(wait_until_idle=False)
        z_axis.home(wait_until_idle=False)

        letter = well[0].lower()
        character_id = ord(letter) - ord('a')
        number = int(well[1])

        x_coord = ref_x_coord + WELL_SPACING_MM * character_id
        y_coord = ref_y_coord - WELL_SPACING_MM * (number-1)

        x_axis.wait_until_idle()
        y_axis.wait_until_idle()
        z_axis.wait_until_idle()

        # Remove seal before moving to new well
        z_axis.move_absolute(100, Units.LENGTH_MILLIMETRES, wait_until_idle=False)

        try:
            x_axis.move_absolute(x_coord, Units.LENGTH_MILLIMETRES, wait_until_idle=False)
            y_axis.move_absolute(y_coord, Units.LENGTH_MILLIMETRES, wait_until_idle=False)
            x_axis.wait_until_idle()
            y_axis.wait_until_idle()
            z_axis.wait_until_idle()
        except Exception as e:
                #If an exception is raised show the user the exception
                
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
   

# If script is called from terminal check for optional arguments and set default values
if __name__ == "__main__":
    if len(sys.argv) > 1:
        well = sys.argv[1]
    else:
        well = "A1"
    
    if len(sys.argv) > 2:
        port = sys.argv[2]
    else:
        port = "COM1"

    if len(sys.argv) > 3:
        ref_x_coord = int(sys.argv[3])
    else:
        ref_x_coord = 0
    
    if len(sys.argv) > 4:
        ref_y_coord = int(sys.argv[4])
    else:
        ref_y_coord = 200

    move_once(well, port, ref_x_coord, ref_y_coord)


        
