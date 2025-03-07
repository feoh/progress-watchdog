# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "playsound",
#     "pynput",
# ]
# ///
import time
import threading
import platform
import os
from playsound import playsound
from pynput import keyboard
import logging


logging.basicConfig(level=logging.INFO)

# CONFIGURABLE SETTINGS
WATCHDOG_KEY_COMBO = {keyboard.Key.ctrl_l, keyboard.Key.alt_l, keyboard.KeyCode(char="]")}
WATCHDOG_TIMEOUT = 60 * 15  # Time in seconds before the notification sound plays
WATCHDOG_ALERT_SOUND = "buzzer-or-wrong-answer-20582.mp3"  # Provide a valid sound file path

# Shared variable to track the last key press time
watchdog_last_activity = time.time()

# Variable to track currently pressed keys
pressed_keys = set()

def on_press(key):
    """Tracks key presses and detects if the key combo is activated."""
    global watchdog_last_activity, pressed_keys
    pressed_keys.add(key)
    logger = logging.getLogger(__name__)
    logger.debug(f"Key pressed: {key}")  # Debugging log


    if WATCHDOG_KEY_COMBO.issubset(pressed_keys):
        watchdog_reset_timer()

def on_release(key):
    """Removes keys from the pressed set when released."""
    if key in pressed_keys:
        pressed_keys.remove(key)

    logger = logging.getLogger(__name__)
    logger.debug(f"Key released: {key}")  # Debugging log

def watchdog_reset_timer():
    """Resets the inactivity timer when the key combination is detected."""
    global watchdog_last_activity
    watchdog_last_activity = time.time()
    print("Watchdog: Key combination detected! Timer reset.")

def watchdog_play_sound():
    """Plays a notification sound based on the operating system."""
    if platform.system() == "Darwin":  # macOS
        os.system(f"afplay {WATCHDOG_ALERT_SOUND}")  # macOS built-in player
    else:
        playsound(WATCHDOG_ALERT_SOUND)

def watchdog_alert_checker():
    """Continuously checks for inactivity and plays an alert if timeout is exceeded."""
    global watchdog_last_activity  # Fix: Explicitly declare global variable
    while True:
        time.sleep(1)  # Check every second
        if time.time() - watchdog_last_activity >= WATCHDOG_TIMEOUT:
            print("Watchdog: Inactivity timeout exceeded! Playing notification sound...")
            watchdog_play_sound()
            watchdog_last_activity = time.time()  # Reset timer after alert

def main():
    # Set up key listener
    watchdog_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    watchdog_listener.start()

    # Run alert checker in a separate thread
    watchdog_alert_thread = threading.Thread(target=watchdog_alert_checker, daemon=True)
    watchdog_alert_thread.start()

    # Keep the main thread alive
    watchdog_listener.join()

