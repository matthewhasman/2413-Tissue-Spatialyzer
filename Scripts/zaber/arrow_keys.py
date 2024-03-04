from zaber_motion import Units
from zaber_motion.ascii import Connection
from pynput import keyboard
import time

def on_press(key):
  well_distance = 8.99 # Distance between microwells
  try:
        if key == keyboard.Key.left:
          axis_x.move_relative(well_distance, Units.LENGTH_MILLIMETRES)
          print("You pressed left arrow")
          time.sleep(0.1)
        elif key == keyboard.Key.right:
          axis_x.move_relative(-1*well_distance, Units.LENGTH_MILLIMETRES)
          print("You pressed right arrow")
          time.sleep(0.1)
        elif key == keyboard.Key.up:
          print("You pressed up arrow")
          axis_y.move_relative(well_distance, Units.LENGTH_MILLIMETRES)
          time.sleep(0.1)
        elif key == keyboard.Key.down:
          print("You pressed down arrow")
          axis_y.move_relative(-1*well_distance, Units.LENGTH_MILLIMETRES)
          time.sleep(0.1)
        elif key == keyboard.Key.W:
          print("You pressed w")
          axis_z.move_relative(1, Units.LENGTH_MILLIMETRES)
          time.sleep(0.1)
          zPos += 1
        elif key == keyboard.Key.S:
          print("You pressed s")
          axis_z.move_relative(-1, Units.LENGTH_MILLIMETRES)
          # zPos -= 1
          time.sleep(0.1)
  except AttributeError:
      pass
    

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

    print("Press arrow keys to control:")
  
    with keyboard.Listener(on_press=on_press) as listener:
      listener.join()
