import json
import hashlib
import base64
from typing import Dict, Any
import json
from json.decoder import JSONDecodeError
from collections import OrderedDict

import xmltodict

from .errors import RequestFailedError
from .logger import logger
from .templates import WayBillGetForm


class WayBill(object):
    def __init__(
        self,
        url: str = ...,
        token: str = ...,
        appsecret: str = ...,
        charset: str = 'utf-8',
        session=...,
    ):
        self.url = url
        self.token = token
        self.appsecret = appsecret
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
        self.charset = charset
        self.session = session

    def public_request_parameters(
        self, msg_type: str = ..., content: str = ...
    ) -> Dict[str, str]:
        data_digest = base64.b64encode(hashlib.md5(
            (content + self.appsecret).encode(self.charset)
        ).digest()).decode()
        return {
            'msg_type': msg_type,
            'logistic_provider_id': self.token,
            'data_digest': data_digest,
            'logistics_interface': content,
        }

    async def request(self, data=...) -> OrderedDict:
        response = await self.session.post(
            self.url, data=data, headers=self.headers
        )
        if response.status == 200:
            text = await response.text(self.charset)
            try:
                text = json.loads(text, object_pairs_hook=OrderedDict)
                logger.debug('json to dict: {}'.format(text))
                return text
            except JSONDecodeError:
                text = xmltodict.parse(await response.text(self.charset))
                logger.debug('xml to dict: {}'.format(text))
                return text
            except Exception as e:
                raise e
        else:
            raise RequestFailedError

    async def subscription_query(self, cpCode: str = None):
        """
        获取发货地，CP开通状态，账户的使用情况

        参数：
        cpCode：    物流公司code，非必需参数
        """
        content = json.dumps({'cpCode': cpCode}, ensure_ascii=False)
        data = self.public_request_parameters(
            msg_type='TMS_WAYBILL_SUBSCRIPTION_QUERY',
            content=content
        )
        return await self.request(data=data)

    async def cloudprint_standard_templates(self, cpCode: str = None):
        """
        获取云打印标准面单

        参数：
        cpCode：    物流公司code，非必需参数
        """
        content = json.dumps({'cpCode': cpCode}, ensure_ascii=False)
        data = self.public_request_parameters(
            msg_type='CLOUDPRINT_STANDARD_TEMPLATES',
            content=content
        )
        return await self.request(data=data)

    async def cloudprint_isv_templates(self, templateType: int = 4):
        """
        获取云打印ISV模板

        参数：
        template_type：    获取模板类型，4 - 自定义模板，6 - isv预设自定义区
        """
        content = json.dumps(
            {'templateType': templateType}, ensure_ascii=False)
        data = self.public_request_parameters(
            msg_type='CLOUDPRINT_ISV_TEMPLATES',
            content=content
        )
        return await self.request(data=data)

    async def cloudprint_seller_custom_areas(self, object_id: Any = None):
        """
        获取商家自定义区列表

        参数：
        object_id：    暂未定义，作为日后的保留字
        """
        content = json.dumps({'object_id': object_id}, ensure_ascii=False)
        data = self.public_request_parameters(
            msg_type='CLOUDPRINT_SELLER_CUSTOM_AREAS',
            content=content
        )
        return await self.request(data=data)

    async def cloudpirnt_seller_custom_area_detail(self, mappingId: int = ...):
        """
        商家自定义区详情

        参数：
        mappingId：    自定义区 mapppingId，该值从CLOUDPRINT_SELLER_CUSTOM_AREAS接口取到
        """
        content = json.dumps({'mappingId': mappingId}, ensure_ascii=False)
        data = self.public_request_parameters(
            msg_type='CLOUDPRINT_SELLER_CUSTOM_AREA_DETAIL',
            content=content
        )
        return await self.request(data=data)

    async def tms_waybill_get(self, data: WayBillGetForm = ...):
        """
        电子面单云打印取号接口

        参数：
        data：    WayBillForm 类，电子面单需要的数据
        """
        content = json.dumps(data.content, ensure_ascii=False)
        logger.debug("tms_waybill_get request content: {}".format(content))
        data = self.public_request_parameters(
            msg_type='TMS_WAYBILL_GET',
            content=content
        )
        return await self.request(data=data)
