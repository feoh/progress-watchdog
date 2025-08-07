# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "playsound",
#     "pynput",
# ]
# ///
import time
import platform
import os
from importlib.resources import files, as_file
from playsound import playsound
from pynput import keyboard
import argparse
import logging


logging.basicConfig(level=logging.INFO)

# Note: watchdog_key_combo is defined below in on_press for now :\
class Configurables():
    watchdog_timeout = 60 * 15  # Time in seconds before the notification sound plays
    watchdog_alert_sound: str = "" 

# Shared variable to track the last key press time
watchdog_last_activity = time.time()

# Variable to track currently pressed keys
pressed_keys = set()

def on_press(key):
    """Tracks key presses and detects if the key combo is activated."""
    # Change this if you want a different "I made progress" key!
    watchdog_key_combo = {keyboard.Key.ctrl_l, keyboard.Key.alt_l, keyboard.KeyCode(char="]")}
    global watchdog_last_activity, pressed_keys
    pressed_keys.add(key)
    logger = logging.getLogger(__name__)
    logger.debug(f"Key pressed: {key}")  # Debugging log


    if watchdog_key_combo.issubset(pressed_keys):
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

def watchdog_play_sound(configs: Configurables):
    """Plays a notification sound based on the operating system."""
    if platform.system() == "Darwin":  # macOS
        os.system(f"afplay {configs.watchdog_alert_sound}")  # macOS built
    else:
        playsound(configs.watchdog_alert_sound)
 

def check_inactivity_timeout(configs: Configurables):
    """Checks for inactivity and plays an alert if timeout is exceeded."""
    global watchdog_last_activity
    if time.time() - watchdog_last_activity >= configs.watchdog_timeout:
        print("Watchdog: Inactivity timeout exceeded! Playing notification sound...")
        watchdog_play_sound(configs)
        watchdog_last_activity = time.time()  # Reset timer after alert

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--buzzer", help="Filename for the alert sound to play when no progress is detected")
    parser.add_argument("--timeout", help="Number of seconds to wait before alerting that no progress was detected.")
    args = parser.parse_args()

    configs = Configurables()
    if args.buzzer:
        configs.watchdog_alert_sound = args.buzzer
    else:
        source = files("progress_watchdog.sounds").joinpath("buzzer-or-wrong-answer-20582.mp3")
        with as_file(source) as sound_path:
            configs.watchdog_alert_sound = str(sound_path)
        print(f"{configs.watchdog_alert_sound=}")

    if args.timeout:
        configs.watchdog_timeout = int(args.timeout)

    print("Welcome to progress watchdog! Starting!")
    print("=======================================\n\n")
    print("Current Settings:")
    print(f"No Progress Timeout(Seconds): {configs.watchdog_timeout}")
    print("Made Progress Key Combo: Ctrl+Alt+]")
    print(f"No Progress Alert Klaxxon: {configs.watchdog_alert_sound}")
    
    # Set up key listener
    watchdog_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    watchdog_listener.start()

    # Main loop that checks for inactivity timeout periodically
    try:
        while True:
            time.sleep(1)  # Check every second
            check_inactivity_timeout(configs)
    except KeyboardInterrupt:
        print("\nShutting down progress watchdog...")
    finally:
        watchdog_listener.stop()

