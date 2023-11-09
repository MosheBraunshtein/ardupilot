#!/usr/bin/env python3

import subprocess
from time import sleep



process = subprocess.Popen(['ls'])

print("sleeping")
sleep(3)

process.terminate()


process = subprocess.Popen(['ls'])

print("sleeping")
sleep(3)

