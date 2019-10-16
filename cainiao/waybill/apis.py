import json
from hashlib import md5
import base64

import requests


class BaseWaybill(object):
    """电子面单基类
    目前仅支持`json`类型的数据传输。
    """
    def __init__(
        self, msg_type='', information={},
        appkey='', appsecret='', token='', url=''
    ):
        self.headers = {
            'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
        }
        self.msg_type = msg_type
        self.information = information
        self.appkey = appkey
        self.appsecret = appsecret
        self.token = token
        self.url = url

    @property
    def content(self):
        content = json.dumps(self.information, ensure_ascii=False)
        return content

    @property
    def data_digest(self):
        data = md5()
        data.update((self.content + self.appsecret).encode('utf-8'))
        data_digest = base64.b64encode(data.digest())
        return data_digest.decode()

    @property
    def data(self):
        return {
            'msg_type': self.msg_type,
            'logistic_provider_id': self.token,
            'data_digest': self.data_digest,
            'logistics_interface': self.content,
        }

    @property
    def response(self):
        response = requests.post(
            self.url, headers=self.headers, data=self.data
        ).content.decode('utf-8')
        return response


class TMSWayBillSubscriptionQuery(BaseWaybill):
    """获取商家订阅信息（发货地，CP开通状态，账户的使用情况）
    参数：
    cpCode: `None`则获取所有信息，指定字段则会查找对应字段的快递信息。
    """
    def __init__(self, cpCode=None, *args, **kwargs):
        super(TMSWayBillSubscriptionQuery, self).__init__(
            self, *args, **kwargs)
        self.msg_type = 'TMS_WAYBILL_SUBSCRIPTION_QUERY'
        self.cpCode = cpCode

    @property
    def content(self):
        self.information['cpCode'] = self.cpCode
        content = json.dumps(self.information, ensure_ascii=False)
        return content


class CloudPrintStandardTemplates(TMSWayBillSubscriptionQuery):
    """获取快递商的基础云打印模板
    参数：
    cpCode: `None`则获取所有快递基础模板，指定字段则会查找对应字段的快递基础模板。
    """
    def __init__(self, *args, **kwargs):
        TMSWayBillSubscriptionQuery.__init__(self, *args, **kwargs)
        self.msg_type = 'CLOUDPRINT_STANDARD_TEMPLATES'


class TMSWayBillGet(BaseWaybill):
    """获取电子面单

    """
    def __init__(self, *args, **kwargs):
        super(TMSWayBillGet, self).__init__(self, *args, **kwargs)
        self.msg_type = 'TMS_WAYBILL_GET'
