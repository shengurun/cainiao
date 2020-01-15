from uuid import uuid4
from typing import List

from .errors import NoMobileOrPhone, TradeOrderListError, \
    ItemsNoneError, ItemsLimitError, TradeOrderInfoError, ItemSetError


class Item(object):
    """
    商品信息
    """
    def __init__(self, count: int = 1, name: str = 'product'):
        if name is None or name == '' or count is None or count <= 0:
            raise ItemSetError

        self.count = count
        self.name = name


class PackageInfo(object):
    """
    电子面单的 packageInfo

    参数：
    volume：   体积，单位 ml，可以为空
    weight：   重量，单位 g，可以为空
    items：    商品信息，不能为空，不填则会自动生成一个 item
    """
    def __init__(
        self,
        volume: int = None, weight: int = None,
        items: List[Item] = [Item()]
    ):
        if items is None or items == []:
            raise ItemsNoneError

        if len(items) > 100:
            raise ItemsLimitError

        self.id = str(uuid4())
        self.volume = volume
        self.weight = weight
        self.items = items


class Sender(object):
    """
    发件人信息

    """
    def __init__(
        self,
        cpCode: str = ...,
        province: str = ...,
        city: str = ...,
        district: str = ...,
        detail: str = ...,
        name: str = ...,
        town: str = None,
        phone: str = None,
        mobile: str = None,
    ):
        if phone is None and mobile is None:
            raise NoMobileOrPhone

        self.cpCode = cpCode
        self.province = province
        self.city = city
        self.district = district
        self.detail = detail
        self.name = name
        self.town = town
        self.phone = phone
        self.mobile = mobile


class Recipient(object):
    """
    收件人信息

    """
    def __init__(
        self,
        province: str = ...,
        city: str = ...,
        district: str = ...,
        detail: str = ...,
        name: str = ...,
        town: str = None,
        phone: str = None,
        mobile: str = None,
        tradeOrderList: List[str] = ...,
        orderChannelsType: str = ...,
        templateUrl: str = ...,
        packageInfo: PackageInfo = ...,
        userId: str = ...,
        objectId: str = None,
        logisticsServices: str = None
    ):
        if phone is None and mobile is None:
            raise NoMobileOrPhone
        if len(tradeOrderList) == 0 or len(tradeOrderList) > 100:
            raise TradeOrderListError

        self.province = province
        self.city = city
        self.district = district
        self.detail = detail
        self.name = name
        self.town = town
        self.phone = phone
        self.mobile = mobile
        self.tradeOrderList = tradeOrderList
        self.orderChannelsType = orderChannelsType
        self.templateUrl = templateUrl
        self.packageInfo = packageInfo
        self.userId = userId
        self.objectId = \
            objectId if objectId is not None else str(uuid4()).replace('-', '')
        self.logisticsServices = logisticsServices


class WayBillGetForm(object):
    """
    TMS_WAYBILL_GET 所需要的信息
    """
    def __init__(
        self,
        sender: Sender = ...,
        recipients: List[Recipient] = ...,
    ):
        if len(recipients) == 0 and len(recipients) > 10:
            raise TradeOrderInfoError

        self.sender = sender
        self.recipients = recipients

    @property
    def content(self):
        data = {
            "cpCode": self.sender.cpCode,
            "tradeOrderInfoDtos": [
                {
                    "logisticsServices": recipient.logisticsServices,
                    "orderInfo": {
                        "orderChannelsType": recipient.orderChannelsType,
                        "tradeOrderList": [
                            item for item in recipient.tradeOrderList
                        ]
                    },
                    "recipient": {
                        "address": {
                            "province": recipient.province,
                            "town": recipient.town,
                            "city": recipient.city,
                            "district": recipient.district,
                            "detail": recipient.detail
                        },
                        "phone": recipient.phone,
                        "mobile": recipient.mobile,
                        "name": recipient.name
                    },
                    "packageInfo": {
                        "volume": recipient.packageInfo.volume,
                        "weight": recipient.packageInfo.weight,
                        "id": recipient.packageInfo.id,
                        "items": [
                            {
                                "count": item.count,
                                "name": item.name
                            } for item in recipient.packageInfo.items
                        ]
                    },
                    "userId": recipient.userId,
                    "objectId": recipient.objectId,
                    "templateUrl": recipient.templateUrl
                } for recipient in self.recipients
            ],
            "needEncrypt": False,
            "resourceCode": None,
            "sender": {
                "address": {
                    "province": self.sender.province,
                    "town": self.sender.town,
                    "city": self.sender.city,
                    "district": self.sender.district,
                    "detail": self.sender.detail
                },
                "phone": self.sender.phone,
                "mobile": self.sender.mobile,
                "name": self.sender.name
            },
            "dmsSorting": False,
            "storeCode": None
        }
        return data
