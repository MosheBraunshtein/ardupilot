#!/usr/bin/env python3

import asyncio
from mavsdk import System


class Custom_mavlink:

    #class level attributes

    def __init__(self,server_ip):
        self.server_ip = server_ip
        self.drone = System(mavsdk_server_address=self.server_ip, port=50051)

    
    async def run(self):

        await self.drone.connect(system_address="udp://:14540")

        status_text_task = asyncio.ensure_future(self.print_status_text())

        print("custom mavlink: Waiting for drone to connect...")
        async for state in self.drone.core.connection_state():
            if state.is_connected:
                print(f"custom mavlink: -- Connected to drone!")
                break
    

    
        async for raw in self.drone.telemetry.raw_gps():
            print(f"custom mavlink: f{raw}")


        status_text_task.cancel()


    async def print_status_text(self):
        try:
            async for status_text in self.drone.telemetry.status_text():
                print(f"Status: {status_text.type}: {status_text.text}")
        except asyncio.CancelledError:
            return


