
from sitl_env import EnvSitl
import asyncio


class   GymSitl():

    def __init__(self):
        self.env_sitl = EnvSitl()

    async def reset(self):

        await self.env_sitl.async_mission()

        print("reset done")


ins = GymSitl()

asyncio.run(ins.reset()) 

print("end")