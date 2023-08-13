#!/usr/bin/env python
import subprocess
import time
import serial
from Applications import *

# Set the initial window ID and name
prev_window_id = None
prev_window_name = None
prev_command = None
command =""


def send_data_processes(command):
    try:
        print(command)
        ser = serial.Serial("/dev/ttyACM0", 9600)
        ser.write(command.encode()) #send the data to arduino
    except FileNotFoundError:
        print("No Device Found\nExiting ...")
        exit()
    except serial.serialutil.SerialException as e:
        print(f"Error: {e}")


    # Infinite loop to check the focused window
while True:
    # Run the xdotool command to get the active window ID
    result = subprocess.run(['xdotool', 'getactivewindow'], capture_output=True, text=True)

    # Extract the window ID from the command output
    window_id = result.stdout.strip()

    # Run the xdotool command to get the window name for the active window
    result = subprocess.run(['xdotool', 'getwindowname', window_id], capture_output=True, text=True)

    # Extract the window name from the command output
    window_name = result.stdout.strip()

    # Check if the window focus has changed
    if window_id != prev_window_id:
        
        #loop through the various data lists
        for audio_player, video_player, browser, text_editor, document_app in zip(audio_players, video_players, browser_apps, text_ediitors, document_file_apps):
            #audio player check
            if (audio_player in window_name.lower()):
                command = "Audio Player"

            #video player check
            elif (video_player in window_name.lower()):
                command = "Video Player"

            #browser check
            elif (browser in window_name.lower()):
                command = "Browser"

            #text editor/coding apps
            elif (text_editor in window_name.lower()):
                command = "Text/Code Editor"
                
            #Document editors/viewers check
            elif (document_app in window_name.lower()):
                command = "Document Editor/Viewer"
            
            
        if (prev_command != command):
            send_data_processes(command)
        # Write the window open and time in a text file
            with open("opened_apps.txt", 'a') as file:
                file.write(f"Program: {command}\nTime: {time.ctime()}\n")

        prev_command = command # update the previous data

        # Update the previous window ID and name
        prev_window_id = window_id

    # Wait for some time before checking again
    time.sleep(1)
