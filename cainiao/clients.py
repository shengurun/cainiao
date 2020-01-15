import asyncio

import aiohttp


class WayBillClient(object):
    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def __aenter__(self):
        return self.session

    async def __aexit__(self, *args, **kwargs):
        await asyncio.sleep(0)
        await self.session.close()

    async def connection(self):
        return self.session

    async def close(self):
        await asyncio.sleep(0)
        await self.session.close()
