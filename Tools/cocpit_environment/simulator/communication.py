#!/usr/bin/env python3

import asyncio
from mavsdk import System
from mavsdk.offboard import (Attitude, OffboardError)
from mavsdk.action import ActionError
from mavsdk.action_server import FlightMode
from time import sleep
import random

class Custom_mavlink:

    #class level attributes

    def __init__(self,server_ip):
        self.drone = System(mavsdk_server_address=server_ip, port=50051)
        # self.is_armed = None
        # self.is_gps_caliborated = False



    
    async def start_send_packets(self):

        await self.drone.connect(system_address="udp://:14540")
        print("custom mavlink: drone connected")

        await self.print_connection_message()
        await self.print_health_message()

        # await self.subscribe_to_arm_message()

        asyncio.ensure_future(self.print_status_message())

        asyncio.ensure_future(self.print_sensor_data())

        await self.offboard_flight()



    async def offboard_flight(self):

        await self.arming()

        print("custom mavlink: -- Setting initial setpoint")
        await self.drone.offboard.set_attitude(Attitude(0.0, 0.0, 0.0, 0.0))
        
        print("custom mavlink: -- Go up at 60% thrust")
        await self.drone.offboard.set_attitude(Attitude(0.0, 0.0, 0.0, 0.6))
        await asyncio.sleep(10)
        print("custom mavlink: -- second Go up at 80% thrust")
        await self.drone.offboard.set_attitude(Attitude(0.0, 0.0, 0.0, 0.8))
        await asyncio.sleep(10)

        while True:
            print("custom mavlink: -- Pitch 30 at 30% thrust")
            await self.drone.offboard.set_attitude(Attitude(0, -30.0, 0.0, 0.3))
            await asyncio.sleep(1)

        print("custom mavlink: -- Stopping offboard")
        try:
            await self.drone.offboard.stop()
        except OffboardError as error:
            print(f"custom mavlink: Stopping offboard mode failed with error code: \
            {error._result.result}")



    async def arming(self):
        print("custom mavlink: sleeping for arming - 15 seconds...")
        await asyncio.sleep(15)
        try:
            print("custom mavlink: -- arming")
            await self.drone.action.arm()
        except ActionError as error:
            print(f"custom mavlink: arming failed \ error: {error}")

    async def start_mode_offboard(self):
        try:
            await self.drone.offboard.start()
        except OffboardError as error:
            print(f"custom mavlink: Starting offboard mode failed with error code: \
                error: {error}")

    async def print_status_message(self):
        async for status_text in self.drone.telemetry.status_text():
            print(f"custom mavlink: Status: {status_text.type}: {status_text.text}")
            if status_text.text == "Disarming motors":
                self.is_armed = False
            if status_text.text == "Arming motors":
                self.is_armed = True 
            if status_text.text == "EKF3 IMU0 is using GPS":
                self.is_gps_caliborated = True
            


    async def print_health_message(self):
        async for health in self.drone.telemetry.health():
            if health.is_global_position_ok and health.is_home_position_ok:
                print("custom mavlink: -- Global position estimate OK")
                break

    async def print_connection_message(self):
        async for connection in self.drone.core.connection_state():
            if connection.is_connected:
                print(f"custom mavlink: -- Connected to drone!")
                break

    async def print_sensor_data(self):
        async for raw in self.drone.telemetry.imu():
            print(f"custom mavlink: imu data {raw.angular_velocity_frd}")
            await asyncio.sleep(1)

    async def subscribe_to_arm_message(self):
        async for message in self.drone.action_server.arm_disarm():
            print(f"arm message: {message}")
            await asyncio.sleep(1)


    async def manual_control_flight(self):
        print("custom mavlink: in manual_control_flight")       

        await self.arming()

        try:
            print("manual control 0 0 0.5 0 ")
            await self.drone.manual_control.set_manual_control_input(float(0), float(0), float(0.5), float(0))         
        except Exception as e:
            print(e)

        # set the manual control input after arming
        while True:
            # if not self.is_armed:
            #     print("re-armed")
            #     await self.arming()
            await self.drone.manual_control.set_manual_control_input(float(0), float(0), float(1), float(0))
            print("manual control 0 0 1 0")
            await asyncio.sleep(0.1)

