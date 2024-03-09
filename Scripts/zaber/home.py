# Sets Zaber stage to home

from zaber_motion import Units
from zaber_motion.ascii import Connection
from pynput import keyboard
import time
import sys

def main():
    pass

if __name__ == "__main__":
  try:
    with Connection.open_serial_port("COM6") as connection:

        connection.enable_alerts()

        device_list = connection.detect_devices()
        print("Found {} devices".format(len(device_list)))

        device = device_list[0]

        axis_x = device.get_lockstep(1)
        axis_x.home()
        axis_y = device.get_axis(3)
        axis_z = device.get_axis(4)
        axis_y.home()
        axis_z.home()
        
  except:
    # End script if connection cannot be established
    print("Cannot open serial port... ending script")
    sys.exit()
