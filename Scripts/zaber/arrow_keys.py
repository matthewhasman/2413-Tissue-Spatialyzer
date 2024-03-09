# Enables keyboard controls for Zaber Stage.
# Use left/right arrows to control X
# Use up/down arrows to control Y
# Use w/s to control Z

from zaber_motion import Units
from zaber_motion.ascii import Connection
from pynput import keyboard
import time
import sys

def main():
    pass

def on_press(key):
  well_distance = 8.99 # Distance between microwells
  sleep_time = 0.3 #
  try:
        if key == keyboard.Key.left:
          try:
            axis_x.move_relative(well_distance, Units.LENGTH_MILLIMETRES)
            print("You pressed left arrow")
          except:
            print("X Out of Range")
          time.sleep(sleep_time)

        elif key == keyboard.Key.right:
          try:
            axis_x.move_relative(-1*well_distance, Units.LENGTH_MILLIMETRES)
            print("You pressed right arrow")
          except:
            print("X out of range")
          time.sleep(sleep_time)

        elif key == keyboard.Key.up:
          try:
            axis_y.move_relative(well_distance, Units.LENGTH_MILLIMETRES)
            print("You pressed up arrow")
          except:
            print("Y out of range")
          time.sleep(sleep_time)

        elif key == keyboard.Key.down:
          try:
            axis_y.move_relative(-1*well_distance, Units.LENGTH_MILLIMETRES)
            print("You pressed down arrow")
          except:
            print("Y out of range")
          time.sleep(sleep_time)
          
        elif key.char == 'w':
          try:
            axis_z.move_relative(1, Units.LENGTH_MILLIMETRES)
            print("You pressed w")
          except:
            print("Z out of range")
          time.sleep(sleep_time)

        elif key.char == 's':
          try:
            axis_z.move_relative(-1, Units.LENGTH_MILLIMETRES)
            print("You pressed s")
          except:
            print("Z out of range")
          time.sleep(sleep_time)
  except AttributeError:
      pass

def on_release(key):
    if key == keyboard.Key.esc:
        print("Exiting...")
        sys.exit()

if __name__ == "__main__":
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

      print("-------------------------------------------")
      print("Controls: ")
      print(" -> Control X: Left/Right arrow keys ")
      print(" -> Control Y: Up/Down arrow keys ")
      print(" -> Control Z: W/S arrow keys ")

      with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()