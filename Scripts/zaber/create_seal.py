from zaber_motion import Units
from zaber_motion.ascii import Connection
from PyQt6.QtWidgets import *
from Fluigent.SDK import *
import time
import sys

def create_seal(port="COM1"):
    """Moves to the given well based off of A1 reference x and y coordinates by connection to the Zaber stage with the input port.

    Args:
        well (string): Desired well to move to.
        port (string): Port that Zaber stage is connected to.
        ref_x_coord (int): X coordinate of the A1 well.
        ref_y_coord (int): Y coordinate of the A1 well.
    """
    try:
        with Connection.open_serial_port(port) as connection:
            connection.enable_alerts()

            device_list = connection.detect_devices()
            print("Found {} devices".format(len(device_list)))

            device = device_list[0]

            z_axis = device.get_axis(4)

            z_axis.home(wait_until_idle=False)

            #Set this distance to be the max distance where the wheel could be
            z_axis.move_relative(100, Units.LENGTH_MILLIMETRES)

            sealed = False
            fgt_set_pressure(0, -400)
            for i in range(0, 10 + 1):
                z_axis.move_relative(1, Units.LENGTH_MILLIMETRES)
                time.sleep(.01)
                if fgt_get_pressure(0) < -100:
                    sealed = True
                    break

            return sealed
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
        return False
   

# If script is called from terminal check for optional arguments and set default values
if __name__ == "__main__":
    if len(sys.argv) > 1:
        port = sys.argv[1]
    else:
        port = "COM1"

    create_seal(port)