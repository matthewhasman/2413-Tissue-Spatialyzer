import sys
import os
import subprocess
from pynput import keyboard
from zaber import arrow_keys

# Display instructions:
script_name = "info"
current_directory = os.path.dirname(__file__)
script_path = os.path.join(current_directory, f"{script_name}.py")
command = ["python3", script_path]
subprocess.run(command, check=True)

while True:
    # Waiting for user input
    script_name = input().strip()
    if (script_name == "C"):
        sys.exit()

    # Get the directory of the current script
    current_directory = os.path.dirname(__file__)

    # Construct the full path to the script file
    script_path = os.path.join(current_directory, f"{script_name}.py")
    
    # Write python or python3
    command = ["python3", script_path]
    try:
        subprocess.run(command, check=True)
    except:
        print("Script cannot be found")