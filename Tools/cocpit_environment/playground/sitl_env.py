import asyncio




class EnvSitl:

    def __init__(self) -> None:
        pass

    async def async_mission(self):
        print("in async")
        await asyncio.sleep(5)
        print("async mission completed")


