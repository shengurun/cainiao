import json
from uuid import uuid4
import asyncio
from typing import Dict

import aiohttp

from .logger import logger
from .errors import CloudPrintConnectError


class CloudPrint(object):
    def __init__(
        self,
        ws=...,
    ):
        self.ws = ws

    async def request(self, content: Dict = ...):
        await self.ws.send_str(content)
        response = await self.ws.receive()
        if response.type == aiohttp.WSMsgType.ERROR:
            raise CloudPrintConnectError(e=ws.exception())
        message = json.loads(response.data)
        logger.debug(message)
        return message

    async def get_printers(self):
        """
        获取打印机列表
        """
        content = json.dumps({
            "cmd": "getPrinters",
            "requestID": str(uuid4()),
            "version": "1.0",
        }, ensure_ascii=False)
        return await self.request(content=content)

    async def print(self, requestID: str = None, task: Dict = ...):
        """
        发送打印/预览数据协议

        注：因为打印机质量乘次不齐，建议 1 个 task 使用 一个 document，可以有效避免重打问题。
        """
        content = json.dumps({
            "cmd": "print",
            "requestID": requestID if requestID is not None else str(uuid4()),
            "version": "1.0",
            "task": task
        }, ensure_ascii=False)
        return await self.request(content=content)
