#!/usr/bin/env python
import win32gui
import time
import serial
import threading
import speech_recognition as sr
from Applications import *

# Set the initial window ID and name
prev_window_handle = None
prev_window_name = None
prev_app = None
app =""

# Create a lock object
lock = threading.Lock()

# Define a function to send data to the Arduino
def send_data(app):
    try:
        ser = serial.Serial("/dev/ttyACM0", 9600)
        ser.write(app.encode()) #send the data to arduino
    except FileNotFoundError:
        print("No Device Found\nExiting ...")
        exit()
    except serial.serialutil.SerialException as e:
        print(f"Error: {e}")

# Define a function to check the focused window and send data to Arduino
def process_open_apps():
    global prev_window_id, prev_app

    while True:
        # Get the handle of the active window
        window_handle = win32gui.GetForegroundWindow()

        # Get the window text for the active window
        window_name = win32gui.GetWindowText(window_handle)

        # Check if the window focus has changed
        if window_handle != prev_window_handle:
            
            #loop through the various data lists
            for audio_player, video_player, browser, text_editor, document_app in zip(audio_players, video_players, browser_apps, text_ediitors, document_file_apps):
                #audio player check
                if (audio_player in window_name.lower()):
                    app = "Audio Player"

                #video player check
                elif (video_player in window_name.lower()):
                    app = "Video Player"

                #browser check
                elif (browser in window_name.lower()):
                    app = "Browser"

                #text editor/coding apps
                elif (text_editor in window_name.lower()):
                    app = "Text/Code Editor"
                
                #Document editors/viewers check
                elif (document_app in window_name.lower()):
                    app = "Document Editor/Viewer"
                
            if (prev_app != app):
                # Acquire the lock before sending data to the Arduino
                lock.acquire()
                send_data(app)
                lock.release()
                
                # Write the window open and time in a text file
                with open("opened_apps.txt", 'a') as file:
                    file.write(f"Program: {app}\nTime: {time.ctime()}\n")

            prev_app = app # update the previous data

            # Update the previous window ID and name
            prev_window_handle = window_handle

        # Wait for some time before checking again
        time.sleep(1)

# Define a function to process speech input and send data to Arduino
def process_speech():
    global app

    #initialize the recognizer
    r = sr.Recognizer()
    mic = sr.Microphone()
    trigger_phrase = "activate"
    shutdown_phrase = "sleep"
    # keep the recognizer on in an indefinite loop
    while True:
        # Initialize the data as none
        app = "None"
        
        #open the microphone to listen for input
        with mic as source:
            print("Waiting for Trigger Phrase...")
            r.adjust_for_ambient_noise(source)#remove noise
            audio = r.listen(source, phrase_time_limit=5)
        #try recognizing the input using google API
        try:
            print("Recognizing...")
            activator = r.recognize_google(audio, language='en-in')
            if trigger_phrase in activator.lower():
                with mic as source:
                    print("Activated\nListening...")
                    r.adjust_for_ambient_noise(source)#remove noise
                    command = r.listen(source, phrase_time_limit=5)
                query = r.recognize_google(command)
                if "movie" in query.lower():
                    app = "Video Player"
                    #subprocess.Popen("vlc")
                elif "music" in query.lower():
                    app = "Audio Player"
                    #subprocess.Popen("audacious")
                elif "study" in query.lower():
                    app = "Text Editor"
                    #subprocess.Popen("mousepad")
                print(app+" sent")
                send_data(app)

            elif shutdown_phrase in activator.lower():
                send_data(shutdown_phrase) # Send a sleep command to arduino
                exit()
        # catch any errors from the recognizer
        except sr.UnknownValueError:
            print("Could not understand speech")
        except sr.RequestError:
            print("Could not recognize your speech input")
        except Exception as e:
            print(e)

        time.sleep(5)

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
