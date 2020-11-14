#!/usr/bin/env python3
from datetime import datetime
import subprocess
import os
import json

ALARM_PATH = '%s/alarm/alarm.py' % os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = '%s/config.json' % os.path.dirname(os.path.abspath(__file__))

now = datetime.now()

current_time = now.strftime("%H:%M")

with open(CONFIG_PATH) as reader:
    config_json = reader.read()
    config = json.loads(config_json)

    target_time = config['time']
    enabled = config['enabled']

    print(target_time, current_time)

    if not enabled:
      print("Not enabled")
      exit()

    if current_time == target_time:
      print("SAME TIME!")
      cmd = ALARM_PATH
      subprocess.check_call(cmd, shell=True)

