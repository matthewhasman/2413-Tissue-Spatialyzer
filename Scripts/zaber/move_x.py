from zaber_motion import Units
from zaber_motion.ascii import Connection
from pynput import keyboard
from pynput.keyboard import Key
import time

print("press key")
def on_press(key):
    try:
        if key == keyboard.Key.left:
            print("You pressed left arrow")
            print("Continuing execution...")
            time.sleep(1)
        elif key == keyboard.Key.right:
            print("You pressed right arrow")
            print("Continuing execution...")
            time.sleep(1)
    except AttributeError:
        pass

# Collect events until released
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()