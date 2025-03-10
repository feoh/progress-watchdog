# Progress Watchdog

![Cartoon Bulldog - CC
https://openverse.org/image/aedd8c62-ff3c-4365-9af1-147c1973440f?q=cartoon+bulldog&p=3](CartoonBulldog.png)

Progress Watchdog: A program to help avoid analysis paralysis and time dilation due to tunnel vision.

## External Resources

- Hat tip to [the author](https://pixabay.com/sound-effects/buzzer-or-wrong-answer-20582/) 
for the buzzer sound effect I use.

- I used [ChatGPT](https://chatgpt.com/) to help me prototype this tool. AI
haters please send your complaints, religious treatises, and assertions about
the implications this has on my character to /dev/null. I've heard them all
before and frankly I don't give a rat's posterior.

## Current Status

### What works, what doesn't.
Mac works great (tested on Sequoia.latest) - Windows works pretty well, though
the mechanism to detect hotkey presses needs more testing. Linux isn't working
yet. Natch :)

### Installation via uv

Right now you can check the project out from github and run `uv run
progress-watchdog'

If you want to run the program without installing, you can use uv for that as
well:

```
╭─cpatti at rocinante in ~ 25-03-09 - 21:06:30
╰─○ uv tool run progress-watchdog                                                    <region:us-east-1>
usage: progress-watchdog [-h] --buzzer BUZZER [--timeout TIMEOUT]
progress-watchdog: error: the following arguments are required: --buzzer
╭─cpatti at rocinante in ~ 25-03-09 - 21:06:36
╰─○ uv tool run progress-watchdog --help                                             <region:us-east-1>
usage: progress-watchdog [-h] --buzzer BUZZER [--timeout TIMEOUT]

options:
  -h, --help         show this help message and exit
  --buzzer BUZZER    Filename for the alert sound to play when no progress is detected
  --timeout TIMEOUT  Number of seconds to wait before alerting that no progress was detected.
╭─cpatti at rocinante in ~ 25-03-09 - 21:06:54
╰─○                                                                                  <region:us-east-1>

```

You'll also need to provide an MP3 file that the program will play to shock
you out of your tunnel vision :)

I used [this one](https://pixabay.com/sound-effects/buzzer-or-wrong-answer-20582/) but you can choose any you like!

## TODO

- Implement some cleaner way to exit than Ctrl-c with an exception :)
- Make configurables into args or a configuration file or something.
- Make the "I made Progress!" key chord not insert characters into the buffer.
