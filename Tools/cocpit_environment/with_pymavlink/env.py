
import os
import subprocess
import argparse
import asyncio
from time import sleep
from custom_pymavlink import Custom_mav  
from reference_flight import trajectory
import random
import psutil


class Sitl:

    def __init__(self) -> None:
        self.container_ip = "172.17.0.2"
        self.mp_ip = "127.0.0.1"#"172.18.128.1"#"10.0.0.3"
        self.process_done = False 
        self.sitl = None
        self.py_connect = None
        self._change_os_dir()
        self.myMav = Custom_mav(ip_sitl=self.container_ip)
        self.reference_trajectory = None

    def  _change_os_dir(self):
        with_pymavlink = os.path.dirname(__file__)
        cocpit_environment = os.path.dirname(with_pymavlink)
        Tools = os.path.dirname(cocpit_environment)
        autotest = os.path.join(Tools,"autotest")
        os.chdir(autotest)


    def run(self):
        try:
            self.sitl = subprocess.Popen(["sim_vehicle.py","-v","ArduCopter","--out",f"{self.mp_ip}:14550","--out",f"{self.container_ip}:14551"],stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE, text=True)
            #  self.sitl = subprocess.Popen(["sim_vehicle.py","-v","ArduCopter","--out",f"{self.container_ip}:14551"],stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE, text=True)
        except subprocess.CalledProcessError as e:
            print(f"command failed with return code:{e.returncode}")

        while True:   
            new_line = self.sitl.stdout.readline()
            self.progress(new_line)

            if "Flight" in new_line:
                self.progress("call to pymavlink")
                self.myMav.connect()
                break
        self.changeModeToGuided()

        self.myMav.arm_copter()

        initial_lat, inital_long, initial_alt, heading = self.myMav.takeoff_to100()

        self.changeModeToStabilize()

        return initial_lat, inital_long, initial_alt, heading


    def set_rc(self,rc_channels):
        self.myMav.send_rc_command(rc_channel_values=rc_channels)

    def get_gps_and_attitude(self):
        gps = self.myMav.get_gps()
        attitude = self.myMav.get_attitude()
        return gps , attitude
            
    def changeModeToGuided(self):
        self.sitl.stdin.write("mode GUIDED\n")
        self.sitl.stdin.flush()
    
    def changeModeToStabilize(self):
        self.sitl.stdin.write("mode STABILIZE\n")
        self.sitl.stdin.flush()

    def close(self):
        self.myMav.close()
        self.sitl.stdin.write(f"output remove {self.mp_ip}:14550 {self.container_ip}:14551 \n")
        self.sitl.stdin.flush()
        self.kill_all_process()
        self.progress("terminate sitl process")

    def kill_all_process(self):
        process_list = ["run_in_terminal","arducopter"]
        parent = psutil.Process(self.sitl.pid)
        for child in parent.children(recursive=True):
            child.terminate()
        parent.terminate()
        for process_name in process_list:
            self.kill_process_by_name(process_name)

    def kill_process_by_name(self,process_name):
        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'] == process_name:
                try:
                    # Attempt to terminate the process
                    process_obj = psutil.Process(process.info['pid'])
                    process_obj.terminate()
                    # print(f"Process {process_name} terminated successfully.")
                except Exception as e:
                    print(f"Error terminating process {process_name}: {e}")

    def progress(self,arg):
        print(f"SITL: {arg}")

