# Moves stage to particular well
# Input numbers 1-12
# Input letters A-H

from zaber_motion import Units
from zaber_motion.ascii import Connection
from pynput import keyboard
import time
import sys

def main():
    pass

def info():
  print("-------------------------------------------")
  print("Controls: ")
  print(" -> Enter 1 - 12 to select Y-Coordinate")
  print(" -> Enter A - H to select X-Coordinate")
  print(" -> Enter 'exit' to close script")
  print(" -> Enter 'info' to de-display controls")
  print("-------------------------------------------")

if __name__ == "__main__":
  with Connection.open_serial_port("COM6") as connection:

      well_distance = 8.99
      connection.enable_alerts()

      device_list = connection.detect_devices()
      print("Found {} devices".format(len(device_list)))

      device = device_list[0]

      axis_x = device.get_lockstep(1)
      axis_y = device.get_axis(3)
      axis_z = device.get_axis(4)

      info()

      while True:
        # Waiting for user input
        coord = input().strip()

        if (coord == "exit"):
            sys.exit()
        
        if (coord == "info"):
          info()
          continue

        # Convert to int and char
        try:
            val = int(coord)
        except:
            val = -1
        try:
            character = ord(coord) - 64
        except:
            character = -1

        # Check if the int/char are in the desired bounds
        if (val >= 1 and val <= 12):
            axis_y.home()
            axis_y.move_relative(well_distance*(val - 1), Units.LENGTH_MILLIMETRES)
        elif (character >= 1 and character <= 8):
            axis_x.home()
            axis_x.move_relative(well_distance*(character - 1), Units.LENGTH_MILLIMETRES)
        else:
            print("invalid input")


        
