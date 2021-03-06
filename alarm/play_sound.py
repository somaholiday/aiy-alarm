#!/usr/bin/env python3
#
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

"""Plays a sound repeatedly."""

import os
import tempfile
import time
import traceback

from aiy.voice.audio import play_wav

TEST_SOUND_PATH = '/usr/share/sounds/alsa/Front_Center.wav'

def ask(prompt):
    answer = input('%s (y/n) ' % prompt).lower()
    while answer not in ('y', 'n'):
        answer = input('Please enter y or n: ')
    return answer == 'y'

def error(message):
    print(message.strip())

def play_sound():
    print('Playing a test sound...')
    play_wav(TEST_SOUND_PATH)

    if ask('Again?'):
        return True

    return False

def main():
    while play_sound():
        pass

    print('Exiting')

if __name__ == '__main__':
    try:
        main()
    except:
        traceback.print_exc()
