
import os
import subprocess
import argparse
import asyncio
from time import sleep
from custom_pymavlink import Custom_mav  


class Sitl:

    def __init__(self) -> None:
        self.container_ip = "172.17.0.2"
        self.mp_ip = "172.21.32.1"
        self.process_done = False 
        self.sitl = None
        self.py_connect = None
        self._change_os_dir()
        self.myMav = Custom_mav(ip_sitl=self.container_ip)

    def  _change_os_dir(self):
        with_pymavlink = os.path.dirname(__file__)
        cocpit_environment = os.path.dirname(with_pymavlink)
        Tools = os.path.dirname(cocpit_environment)
        autotest = os.path.join(Tools,"autotest")
        os.chdir(autotest)


    def run(self):
        try:
            self.sitl = subprocess.Popen(["sim_vehicle.py","-v","ArduCopter","--out",f"{self.mp_ip}:14550","--out",f"{self.container_ip}:14551"],stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE, text=True)
        except subprocess.CalledProcessError as e:
            print(f"command failed with return code:{e.returncode}")

        while True:   
            new_line = self.sitl.stdout.readline()
            self.progress(new_line)

            if "Flight" in new_line:
                self.progress("call to pymavlink")
                self.myMav.connect()
                break
        self.myMav.arm_copter()

    def set_rc(self,rc_channels):
        self.myMav.send_rc_command(rc_channel_values=rc_channels)
        pass

    def get_gps_and_attitude(self):
        gps = self.myMav.get_gps()
        attitude = self.myMav.get_attitude()
        return gps , attitude
            
    def progress(self,arg):
        print(f"SITL: {arg}")
