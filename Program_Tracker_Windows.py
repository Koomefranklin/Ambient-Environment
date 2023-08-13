import win32gui
import time

# Set the initial window handle and name
prev_window_handle = None
prev_window_name = None
prev_app = None

video_players = ["vlc", "windows media player", "quicktime", "media player classic", "realplayer", "mplayer", "mpv", "kmplayer", "potplayer", "gstreamer"]
audio_players = ["winamp", "foobar2000", "windows media player", "itunes", "spotify", "lollipop", "musicolet", "aimp", "vlc", "audacious", "groove"]
browser_apps = ["chrome", "firefox", "safari", "edge", "opera", "brave", "vivaldi", "tor", "internet explorer", "uc browser"]
text_ediitors = ["notepad", "atom", "sublime text", "visual studio code", "gedit", "nano", "emacs", "vim", "notepad++", "jupyter notebook"]
document_file_apps = ["microsoft word", "google docs", "libreoffice writer", "openoffice writer", "adobe acrobat", "foxit reader", \
                      "sumatra pdf", "google sheets", "microsoft excel", "libreoffice calc", "openoffice calc", "google slides", "microsoft powerpoint", "libreoffice impress", "openoffice impress", "abiword"]


# Infinite loop to check the focused window
while True:
    # Get the handle of the active window
    window_handle = win32gui.GetForegroundWindow()

    # Get the window text for the active window
    window_name = win32gui.GetWindowText(window_handle)

    # Check if the window focus has changed
    if window_handle != prev_window_handle:
        
        if prev_window_handle is not None:
            print(f"Window '{prev_window_name}' closed")
        
        #loop through the various data lists
        for audio_player, video_player, browser, text_editor, document_app in zip(audio_players, video_players, browser_apps, text_ediitors, document_file_apps):
            #audio player check
            if (audio_player in window_name.lower()):
                #check if the data is a video player too
                if audio_player in video_players:
                    print("data also a video player")
                app = f"Audio Player {audio_player}"

            #video player check
            elif (video_player in window_name.lower()):
                app = f"Video Player {video_player}"

            #browser check
            elif (browser in window_name.lower()):
                app = f"Browser {browser}"

            #text editor/coding apps
            elif (text_editor in window_name.lower()):
                app = f"Text/Code Editor {text_editor}"
            
            #Document editors/viewers check
            elif (document_app in window_name.lower()):
                app = f"Document Editor/Viewer {document_app}"
        
        #try satement to avoid error if none of the test apps are opened
        try:
            if (prev_app != app):
            # Output a message with the new window name
                with open("opened_apps.txt", 'a') as file:
                    file.write(f"Program: {app}\nTime: {time.ctime()}\n")
            prev_app = app
        #nameerror exception if 'data' is empty to skip and continue loop
        except NameError:
            pass
        
        prev_window_handle = window_handle

    time.sleep(1)
