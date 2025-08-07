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

# Global variable to track the timer for inactivity alerts
alert_timer: threading.Timer | None = None

# Global variable to hold the current configuration
configs: Configurables | None = None

# Variable to track currently pressed keys
pressed_keys = set()

def on_press(key):
    """Tracks key presses and detects if the key combo is activated."""
    # Change this if you want a different "I made progress" key!
    watchdog_key_combo = {keyboard.Key.ctrl_l, keyboard.Key.alt_l, keyboard.KeyCode(char="]")}
    global pressed_keys, alert_timer, configs
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
    global alert_timer, configs
    if alert_timer:
        alert_timer.cancel()
    # Schedule a new timer that will trigger after the configured timeout
    alert_timer = threading.Timer(configs.watchdog_timeout, watchdog_play_sound, args=[configs])
    alert_timer.start()
    print("Watchdog: Key combination detected! Timer reset.")

def watchdog_play_sound(configs: Configurables):
    """Plays a notification sound based on the operating system."""
    if platform.system() == "Darwin":  # macOS
        os.system(f"afplay {configs.watchdog_alert_sound}")  # macOS built
    else:
        playsound(configs.watchdog_alert_sound)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--buzzer", help="Filename for the alert sound to play when no progress is detected")
    parser.add_argument("--timeout", help="Number of seconds to wait before alerting that no progress was detected.")
    args = parser.parse_args()

    global configs
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
    print("================================================\n\n")
    print("Current Settings:")
    print(f"No Progress Timeout(Seconds): {configs.watchdog_timeout}")
    print("Made Progress Key Combo: Ctrl+Alt+]")
    print(f"No Progress Alert Klaxxon: {configs.watchdog_alert_sound}")

    # Set up key listener
    watchdog_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    watchdog_listener.start()

    # Start the initial inactivity timer
    watchdog_reset_timer()

    # Keep the main thread alive
    watchdog_listener.join()

if __name__ == "__main__":
    main()
