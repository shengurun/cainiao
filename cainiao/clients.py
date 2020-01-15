import asyncio

import aiohttp
from aiohttp import ClientWebSocketResponse


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


class CloudPrintClient(object):
    def __init__(self, ws_url: str = ...):
        self.session = aiohttp.ClientSession()
        self.ws_url = ws_url

    async def __aenter__(self):
        self.ws = await self.session.ws_connect(
            url=self.ws_url,
            autoclose=False,
            autoping=False,
            verify_ssl=False
        )
        return self.ws

    async def __aexit__(self, *args, **kwargs):
        await asyncio.sleep(0)
        await self.session.close()

    async def connect(self):
        self.ws = await self.session.ws_connect(
            url=self.ws_url,
            autoclose=False,
            autoping=False,
        )
        return (self.session, self.ws)

    async def close(self):
        await asyncio.sleep(0)
        await self.session.close()
