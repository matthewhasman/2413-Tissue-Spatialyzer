from zaber_motion import Units
from zaber_motion.ascii import Connection
from pynput import keyboard
import time
import sys
from zaber import arrow_keys

import os
import subprocess

print("Run a script to get started: ")

while True:
    # Waiting for user input
    script_name = input().strip()
    print(script_name)

    # Get the directory of the current script
    current_directory = os.path.dirname(__file__)

    # Construct the full path to the script file
    script_path = os.path.join(current_directory, f"{script_name}.py")
    
    command = ["python", script_path]
    subprocess.run(command, check=True)