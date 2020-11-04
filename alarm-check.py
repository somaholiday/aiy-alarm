#!/usr/bin/env python3
from datetime import datetime
import subprocess
import os

ALARM_PATH = '%s/alarm/alarm.py' % os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = '%s/config.txt' % os.path.dirname(os.path.abspath(__file__))

now = datetime.now()

current_time = now.strftime("%H:%M")

with open(CONFIG_PATH) as reader:
    target_time = reader.read()

    print(target_time, current_time)

    if current_time == target_time:
      print("SAME TIME!")
      cmd = ALARM_PATH
      subprocess.check_call(cmd, shell=True)

