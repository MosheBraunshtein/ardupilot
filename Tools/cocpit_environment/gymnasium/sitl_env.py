#!/usr/bin/env python3

import os
import subprocess
import asyncio
from time import sleep
from mavsdk import System
from mavsdk.action import ActionError
from mavsdk.offboard import (Attitude, OffboardError)



class SitlConnection:

    def __init__(self):
        self.ip = "172.18.128.1"
        self.drone = System(mavsdk_server_address=self.ip, port=50051)
        self.DroneReady = False
        self.sitl_process = None


    async def run(self):
        '''
        run sitl process
        '''
        self._change_dir()

        self._start_sitl()

        # wait for sitl to be ready 
        while not self.DroneReady:
            newline = self.sitl_process.stdout.readline()
            print("sitl-process: " + newline)
            if "Flight" in newline:
                self.sitl_process.stdin.write("mode STABILIZE\n")
                self.sitl_process.stdin.flush()
                self.DroneReady = True 

        # wait for drone to be connected to mavsdk user and takeoff
         
        await self.takeoff()
        print("sitl process: drone ready for command")

        

    async def send_attitude_command(self, roll, pitch, yaw, throttle):
        await self.drone.offboard.set_attitude(Attitude(roll, pitch, yaw, throttle))

    
    async def get_sensor_data(self):
        async for gps in self.drone.telemetry.raw_gps():
            # down, forward, right = imu.angular_velocity_frd
            # print(f"imu: {down, forward, right}")
            # return down, forward, right 
            alt = gps.absolute_altitude_m
            lat = gps.latitude_deg
            deg = gps.latitude_deg
            print(f"imu: {alt, lat, deg}")
            return (alt, lat, deg)


    def terminate_simulator(self):
        if self.sitl_process is not None:
            self.sitl_process.terminate()
        print("sitl process: terminated successfully")

    def _change_dir(self):
        try:
            gymnasium = os.path.dirname(__file__)
            cocpit_environment = os.path.dirname(gymnasium)
            Tools = os.path.dirname(cocpit_environment)
            autotest = os.path.join(Tools, "autotest")
            os.chdir(autotest)
        except FileNotFoundError:
            print("Directory not found.")
        except Exception as e:
            print(f"An error occurred with _change_dir(): {e}")

    def _start_sitl(self):
        try:
            self.sitl_process = subprocess.Popen(
                [
                    "sim_vehicle.py",
                    "-v",
                    "ArduCopter",
                    "--out",
                    f"{self.ip}:14540",
                    "--out",
                    f"{self.ip}:14550"
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True
            )
        except subprocess.CalledProcessError as e:
            print(f"_start_sitl() failed: {e.returncode}")
        else:
            print("sitl process: SITL started successfully")



    async def wait_for_drone_mavsdk(self):
            
        await self.drone.connect(system_address="udp://:14540")

        await self.print_connection_message()
        await self.print_health_message()

        # asyncio.ensure_future(self.get_sensor_data())

        await self.arming_drone()


    async def takeoff(self):
        await self.wait_for_drone_mavsdk()
        await self.drone.offboard.set_attitude(Attitude(0.0, 0.0, 0.0, 0.7)) 
        sleep(10)
        print("sitl-process: copter in air") 
        



    async def print_health_message(self):
        async for health in self.drone.telemetry.health():
            if health.is_global_position_ok and health.is_home_position_ok:
                print("custom MAVlink: -- Global position estimate OK")
                break

    async def print_connection_message(self):
        async for connection in self.drone.core.connection_state():
            if connection.is_connected:
                print(f"custom MAVlink: -- Connected to drone!")
                break

    async def arming_drone(self):
            print("custom MAVlink: sleeping for arming - 15 seconds...")
            await asyncio.sleep(15)
            try:
                print("custom MAVlink: -- arming")
                await self.drone.action.arm()
            except ActionError as error:
                print(f"custom MAVlink: arming failed \ error: {error}")



