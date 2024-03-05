# Enables keyboard controls for Zaber Stage.
# Use left/right arrows to control X
# Use up/down arrows to control Y
# Use w/s to control Z

from zaber_motion import Units
from zaber_motion.ascii import Connection
from pynput import keyboard
import time
import sys

def on_press(key):
  well_distance = 8.99 # Distance between microwells
  sleep_time = 0.3
  try:
        if key == keyboard.Key.left:
          try: 
            axis_x.move_relative(well_distance, Units.LENGTH_MILLIMETRES)
          except:
            print("Cannot move further in X")
          print("You pressed left arrow")
          time.sleep(sleep_time)

          
        elif key == keyboard.Key.right:
          try:
            axis_x.move_relative(-1*well_distance, Units.LENGTH_MILLIMETRES)
          except:
            print("Cannot move further in X")
          print("You pressed right arrow")
          time.sleep(sleep_time)

          
        elif key == keyboard.Key.up:
          print("You pressed up arrow")
          try:
            axis_y.move_relative(well_distance, Units.LENGTH_MILLIMETRES)
          except:
            print("Cannot move further in Y")
          time.sleep(sleep_time)

          
        elif key == keyboard.Key.down:
          print("You pressed down arrow")
          try:
            axis_y.move_relative(-1*well_distance, Units.LENGTH_MILLIMETRES)
          except:
            print("Cannot move further in Y")
          time.sleep(sleep_time)

          
        elif key.char == 'w':
          print("You pressed w")
          try:
            axis_z.move_relative(10, Units.LENGTH_MILLIMETRES)
          except:
            print("Cannot move further in Z")
          time.sleep(sleep_time)

          
        elif key.char == 's':
          print("You pressed s")
          try:
            axis_z.move_relative(-10, Units.LENGTH_MILLIMETRES)
          except:
            print("Cannot move further in Z")
          time.sleep(sleep_time)
          
  except AttributeError:
      pass

def on_release(key):
    if key == keyboard.Key.esc:
        print("Exiting...")
        sys.exit()
    

with Connection.open_serial_port("COM6") as connection:
    connection.enable_alerts()

    device_list = connection.detect_devices()
    print("Found {} devices".format(len(device_list)))

    device = device_list[0]

    axis_x = device.get_lockstep(1)
    axis_x.home()
    axis_y = device.get_axis(3)
    axis_z = device.get_axis(4)
    if not axis_y.is_homed():
      axis_y.home()
    if not axis_z.is_homed():
      axis_z.home()

    print("Controls :")
    print("-> left/right arrows to control X-Position")
    print("-> up/down arrows to control Y-Position")
    print("-> w/s characters to control Z-Position")
  
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
      listener.join()
