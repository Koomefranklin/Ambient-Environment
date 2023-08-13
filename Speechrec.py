import speech_recognition as sr
import time
import serial
import pyttsx3

#initialize the recognizer
r = sr.Recognizer()
mic = sr.Microphone()
trigger_phrase = "activate"
shutdown_phrase = "sleep"

def voiceOut(command):
	# Initialize the engine
	engine = pyttsx3.init()
	engine.say(command)
	engine.runAndWait()

def send_data_speech(app):
    try:
        ser = serial.Serial("/dev/ttyACM0", 9600)
        ser.write(app.encode()) #send the data to arduino
    except FileNotFoundError:
        print("No Device Found\nExiting ...")
        exit()
    except Exception:
        print("Another Process connected\nDissconect it first")

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
            voiceOut("Activated, waiting for command.")
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

            send_data_speech(app)

        elif shutdown_phrase in activator.lower():
            voiceOut("Sleeping")
            send_data_speech(shutdown_phrase) # Send a sleep command to arduino
            exit()
    # catch any errors from the recognizer
    except sr.UnknownValueError:
        print("Could not understand speech")
    except sr.RequestError:
        print("Could not recognize your speech input")
    except Exception as e:
        print(e)

    time.sleep(1)