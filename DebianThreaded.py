#!/usr/bin/env python
import subprocess
import time
import serial
import threading
import speech_recognition as sr
from Applications import *
import pyttsx3

# Set the initial window ID and name
prev_window_id = None
prev_window_name = None
prev_command = "sleep"
command = "sleep"
# Create a lock object
lock = threading.Lock()


def voice_out(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(command)
    engine.runAndWait()


# Define a function to send data to the Arduino
def send_data(data):
    try:
        ser = serial.Serial("/dev/ttyACM0", 9600)
        ser.write(data.encode())  # send the data to arduino
    except FileNotFoundError:
        print("No Device Found\nExiting ...")
        exit()
    except serial.serialutil.SerialException as e:
        print(f"Error: {e}")


# Define a function to check the focused window and send data to Arduino
def process_open_apps():
    global prev_window_id, prev_command, command

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
            # loop through the various data lists
            for audio_player, video_player, browser, text_editor, document_app in zip(audio_players, video_players,
                                                                                      browser_apps, text_ediitors,
                                                                                      document_file_apps):
                # audio player check
                if audio_player in window_name.lower():
                    command = "audio"
                    
                # video player check
                elif video_player in window_name.lower():
                    command = "video"
                    
                # browser check
                elif browser in window_name.lower():
                    command = "browser"

                # text editor/coding apps
                elif text_editor in window_name.lower():
                    command = "code"
                    
                # Document editors/viewers check
                elif document_app in window_name.lower():
                    command = "document"
                # Browser check
                elif browser in window_name.lower():
                    command = "browser"

            if prev_command != command:
                # Acquire the lock before sending data to the Arduino
                if command == "audio":
                    voice_out("Adjusting environment for music")
                elif command == "video":
                    voice_out("Adjusting environment for watching")
                elif command == "browser":
                    voice_out("Adjusting environment for browsing")
                elif command == "code":
                    voice_out("Adjusting environment for coding")
                elif command == "document":
                    voice_out("Adjusting environment for studying")

                lock.acquire()
                send_data(command)
                lock.release()

                # Write the window open and time in a text file
                with open("opened_apps.txt", 'a') as file:
                    file.write(f"Program: {command}\nTime: {time.ctime()}\n")

            prev_command = command  # update the previous data

            # Update the previous window ID and name
            prev_window_id = window_id

        # Wait for some time before checking again
        time.sleep(1)


# Define a function to process speech input and send data to Arduino
def process_speech():
    global command
    # initialize the recognizer
    r = sr.Recognizer()
    mic = sr.Microphone()
    trigger_phrase = "activate"
    shutdown_phrase = "sleep"
    # keep the recognizer on in an indefinite loop
    while True:
        # open the microphone to listen for input
        with mic as source:
            print("Waiting for Trigger Phrase...")
            r.adjust_for_ambient_noise(source)  # remove noise
            audio = r.listen(source, phrase_time_limit=5)
        # try recognizing the input using google API
        try:
            print("Recognizing...")
            activator = r.recognize_google(audio, language='en-in')
            if trigger_phrase in activator.lower():
                voice_out("Activated, waiting for command.")
                with mic as source:
                    print("Activated\nListening...")
                    r.adjust_for_ambient_noise(source)  # remove noise
                    command = r.listen(source, phrase_time_limit=5)
                try:
                    query = r.recognize_google(command)
                except sr.exceptions.UnknownValueError:
                    voice_out("No command taken")
                except sr.exceptions.RequestError:
                    pass
                else:
                    if "lights" in query.lower() and "on" in query.lower():
                        command = "light on"
                    elif "lights" in query.lower() and "off" in query.lower():
                        command = "light off"
                    elif "speaker" in query.lower() and "on" in query.lower():
                        command = "speaker on"
                    elif "speaker" in query.lower() and "off" in query.lower():
                        command = "speaker off"
                    elif "movie" in query.lower():
                        command = "video"
                        voice_out("Adjusting environment for watching")
                    # subprocess.Popen("vlc")
                    elif "music" in query.lower():
                        command = "audio"
                        voice_out("Adjusting environment for music")
                    # subprocess.Popen("audacious")
                    elif "code" in query.lower() or "coding" in query.lower():
                        command = "code"
                        voice_out("Adjusting environment for coding")
                    elif "study" in query.lower():
                        command = "document"
                        voice_out("Adjusting environment for studying")
                    elif "browse" in query.lower():
                        command = "browser"
                        voice_out("Adjusting environment for browsing")
                
                    # subprocess.Popen("mousepad")
                    print(command + " sent")
                    send_data(command)

            elif shutdown_phrase in activator.lower():
                voice_out("Sleeping")
                send_data(shutdown_phrase)  # Send a sleep command to arduino
                exit()
        # catch any errors from the recognizer
        except (sr.exceptions.RequestError, sr.exceptions.UnknownValueError):
                    pass

        time.sleep(1)


def main():
    # Create two threads for each function
    open_apps_thread = threading.Thread(target=process_open_apps)
    speech_thread = threading.Thread(target=process_speech)

    # Start both threads
    open_apps_thread.start()
    speech_thread.start()

    # Wait for both threads to finish
    open_apps_thread.join()
    speech_thread.join()


if __name__ == '__main__':
    main()
