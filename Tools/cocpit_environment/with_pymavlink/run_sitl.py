
import os
import subprocess
import argparse
import asyncio
from time import sleep
import custom_pymavlink 







with_pymavlink = os.path.dirname(__file__)
cocpit_environment = os.path.dirname(with_pymavlink)
Tools = os.path.dirname(cocpit_environment)
autotest = os.path.join(Tools,"autotest")
os.chdir(autotest)

ip = "172.21.32.1"
try:
    sitl = subprocess.Popen(["sim_vehicle.py","-v","ArduCopter","--out",f"{ip}:14550","--out",f"172.17.0.2:14551"],stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE, text=True)
except subprocess.CalledProcessError as e:
    print(f"command failed with return code:{e.returncode}")



done = False 
while done is not True:   
    line = sitl.stdout.readline()
    print(f"sitl-process: {line}")

    if "Flight" in line:

        print("main process: call to pymavlink")
        custom_pymavlink.connect()
        print("main process: end communication")
        ## when custom_mavlink end , script goes here
        done = True 

print("main process: end")

