#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import subprocess
import time
import threading
import os

from aiy.board import Board, Led
from aiy.leds import Leds, Color, Pattern
from aiy.voice.audio import play_wav

SOUND_DIR = '%s/sounds' % os.path.dirname(os.path.abspath(__file__))
def sound_path(sound_file):
    return '%s/%s' % (SOUND_DIR, sound_file)

ALARM_SOUND_PATH = sound_path('core_66.wav')
GOOD_MORNING_SOUND_PATH = sound_path('good_morning.wav')
SLEEP_TIME = 1.75
TIMEOUT_LIMIT = 10 * 60

VOLUME_CMD = 'amixer sset Master playback %d%%'
def set_volume(percent):
    cmd = VOLUME_CMD % percent
    # print(cmd)
    subprocess.check_call(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

MAX_BRIGHTNESS = 255
MAX_VOLUME = 70

def map(value, low1, high1, low2, high2):
    return low2 + (high2 - low2) * (value - low1) / (high1 - low1)

def alarm(done, leds):
    print("alarm thread")
    intensity = 0
    start = time.monotonic()
    duration = 0

    while not done.is_set():
        if (intensity < 1):
            intensity += (5./70.)
            if (intensity > 1):
                intensity = 1

            set_volume(intensity * MAX_VOLUME)
            leds.pattern = Pattern.breathe(map(intensity, 0., 1., 1000., 100.))
            leds.update(Leds.rgb_pattern((0, 0, intensity * MAX_BRIGHTNESS)))

        duration = time.monotonic() - start
        print('Alarm [Press button to stop] %.02fs, intensity: %.02f' % (duration, intensity))

        play_wav(ALARM_SOUND_PATH)
        time.sleep(SLEEP_TIME)

def main():
    with Board() as board:
        with Leds() as leds:
            # init volume and brightness
            set_volume(0)
            leds.pattern = Pattern.breathe(750)
            leds.update(Leds.rgb_pattern(Color.BLACK))

            done = threading.Event()
            board.button.when_pressed = done.set

            alarm_thread = threading.Thread(target=alarm, args=(done,leds), daemon=True)
            alarm_thread.start()

            if done.wait(timeout=TIMEOUT_LIMIT):
                set_volume(MAX_VOLUME)
                leds.update(Leds.rgb_on(Color.GREEN))
                print('GOOD MORNING!')
                play_wav(GOOD_MORNING_SOUND_PATH)
            else:
                print('Timed out.')

if __name__ == '__main__':
    main()
