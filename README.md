# Watchdog

Watchdog: A program to help avoid analysis paralysis and time dilation due to tunnel vision.

## External Resources

- Hat tip to [the author](https://pixabay.com/sound-effects/buzzer-or-wrong-answer-20582/) 
for the buzzer sound effect I use.

- I used [ChatGPT](https://chatgpt.com/) to help me prototype this tool. AI
- haters please send your complaints, religious treatises, and assertions about
the implications this has on my character to /dev/null. I've heard them all
before and frankly I don't give a rat's posterior.

## Current Status

Broken. Currently blows up with the following deep in its C code dependencies on
Mac:
```
╭─cpatti at rocinante in ~/src/personal/python/watchdog on main✘✘✘ 25-03-04 - 11:56:48
╰─(.venv) ⠠⠵ python watchdog.py                                                      <region:us-east-1>
Assertion failed: (range.location <= dataLength), function __CFDataValidateRange, file CFData.c, line 219.
[1]    27867 abort      python watchdog.py
```
