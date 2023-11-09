#!/usr/bin/env python3

import os
import subprocess
import argparse
from communication import Custom_mavlink
import asyncio
from time import sleep


simulator = os.path.dirname(__file__)
cocpit_environment = os.path.dirname(simulator)
Tools = os.path.dirname(cocpit_environment)
autotest = os.path.join(Tools,"autotest")
os.chdir(autotest)

print(f"sitl-process: {os.getcwd()}")

parser = argparse.ArgumentParser()
parser.add_argument("-ip",help="the ip of the local host for ")
args = parser.parse_args()




print(f"sitl-process: run sim_vehicle with --out {args.ip}:14540")

try:
    sitl = subprocess.Popen(["sim_vehicle.py","-v","ArduCopter","--out",f"{args.ip}:14540","--out",f"{args.ip}:14550"],stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE, text=True)
except subprocess.CalledProcessError as e:
    print(f"command failed with return code:{e.returncode}")


done = False 
while done is not True:   
    line = sitl.stdout.readline()
    print(f"sitl-process: {line}")
    
    # check for: 1 link down. 
    # if "link" in line and "down" in line:
    #     print("custom-mavlink: cant connect, need reboot")
    #     print(f"readline: {line}")
    #     sleep(1)
    #     line = sitl.stdout.
    #     print(f"readline: {line}")
    #     if line.empty():      
    #         sitl.terminate()
    #         sleep(5)
    #         try:
    #             sitl = subprocess.Popen(["sim_vehicle.py","-v","ArduCopter","--out",f"{args.ip}:14540"],stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    #         except subprocess.CalledProcessError as e:
    #             print(f"command failed with return code:{e.returncode}")

    # raise message 
    # if 1 link down: restart container 


    if "Flight" in line:
        print("main process: change to guided_nogps")
        sitl.stdin.write("mode GUIDED_NOGPS\n")
        sitl.stdin.flush()
        sleep(2)
        print("main process: call to custom-mavlink")
        custom_mavlink = Custom_mavlink(server_ip=args.ip)
        asyncio.run(custom_mavlink.start_send_packets())
        print("main process: end communication")
        ## when custom_mavlink end , script goes here
        done = True 

print("main process: end")



