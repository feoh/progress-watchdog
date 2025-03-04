import keyboard
import time
import threading
from playsound import playsound

# CONFIGURABLE SETTINGS
WATCHDOG_KEY_COMBO = "ctrl+alt+k"  # Change this to the desired key combination
WATCHDOG_TIMEOUT = 10  # Time in seconds before the notification sound plays
WATCHDOG_ALERT_SOUND = "./buzzer-or-wrong-answer-20582.mp3"  # Provide a valid sound file path

# Shared variable to track the last key press time
watchdog_last_activity = time.time()

def watchdog_key_listener():
    """Listens for the configured key combination and resets the timer when detected."""
    global watchdog_last_activity
    keyboard.add_hotkey(WATCHDOG_KEY_COMBO, watchdog_reset_timer)
    keyboard.wait()  # Keeps the program running

def watchdog_reset_timer():
    """Resets the inactivity timer when the key combination is detected."""
    global watchdog_last_activity
    watchdog_last_activity = time.time()
    print("Watchdog: Key combination detected! Timer reset.")

def watchdog_alert_checker():
    """Continuously checks for inactivity and plays an alert if timeout is exceeded."""
    while True:
        time.sleep(1)  # Check every second
        if time.time() - watchdog_last_activity >= WATCHDOG_TIMEOUT:
            print("Watchdog: Inactivity timeout exceeded! Playing notification sound...")
            playsound(WATCHDOG_ALERT_SOUND)
            watchdog_last_activity = time.time()  # Reset timer after alert

# Run both listener and checker in separate threads
watchdog_listener_thread = threading.Thread(target=watchdog_key_listener, daemon=True)
watchdog_alert_thread = threading.Thread(target=watchdog_alert_checker, daemon=True)

watchdog_listener_thread.start()
watchdog_alert_thread.start()

# Keep the main thread alive
while True:
    time.sleep(10)

