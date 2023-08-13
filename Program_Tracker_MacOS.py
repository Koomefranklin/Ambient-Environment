import subprocess
import time

# Set the initial window ID and name
prev_window_id = None
prev_window_name = None
prev_app = None
app = ""

video_players = ["vlc", "quicktime player", "mplayerx", "mpv", "iina", "plex"]
audio_players = ["itunes", "spotify", "vox", "audirvana", "decibel", "musique"]
browser_apps = ["safari", "chrome", "firefox", "opera", "brave"]
text_editors = ["textedit", "sublime text", "visual studio code", "atom", "bbedit"]
document_file_apps = ["microsoft word", "google docs", "libreoffice writer", "openoffice writer", "adobe acrobat", "preview", "numbers", "google sheets", "microsoft excel", "libreoffice calc", "openoffice calc", "google slides", "microsoft powerpoint", "libreoffice impress", "openoffice impress", "pages"]

# Infinite loop to check the focused window
while True:
    # Run the AppleScript command to get the active window ID
    result = subprocess.run(['osascript', '-e', 'tell application "System Events" to get id of window 1 of (process 1 where frontmost is true)'], capture_output=True, text=True)

    # Extract the window ID from the command output
    window_id = result.stdout.strip()

    # Run the AppleScript command to get the window name for the active window
    result = subprocess.run(['osascript', '-e', 'tell application "System Events" to get name of window 1 of (process 1 where frontmost is true)'], capture_output=True, text=True)

    # Extract the window name from the command output
    window_name = result.stdout.strip()

    # Check if the window focus has changed
    if window_id != prev_window_id:

        # Loop through the various data lists
        for audio_player, video_player, browser, text_editor, document_app in zip(audio_players, video_players, browser_apps, text_editors, document_file_apps):
            # Audio player check
            if (audio_player in window_name.lower()):
                # Check if the data is a video player too
                if audio_player in video_players:
                    print("App also a video player")
                app = "Audio Player"

            # Video player check
            elif (video_player in window_name.lower()):
                app = "Video Player"

            # Browser check
            elif (browser in window_name.lower()):
                app = "Browser"

            # Text editor/coding apps
            elif (text_editor in window_name.lower()):
                app = f"Text/Code Editor {text_editor}"

            # Document editors/viewers check
            elif (document_app in window_name.lower()):
                app = "Document Editor/Viewer"

        # Try statement to avoid error if none of the test apps are opened
        try:
            if prev_app != app:
                print(f"{app} opened")
                with open("opened_apps.txt", 'a') as file:
                    file.write(f"Program: {app}\nTime: {time.ctime()}\n")
            prev_app = app
        # NameError exception if 'data' is empty to skip and continue loop
        except NameError:
            pass

        # Update the previous window ID and name
        with open("opened_apps.txt", 'a') as file:
                    file.write(f"Program: {app}\nTime: {time.ctime()}\n")

        prev_window_id = window_id

    # Wait for some time before checking again
    time.sleep(1)
