# Cainiao

适用于[菜鸟电子面单](https://www.cainiao.com/markets/cnwww/cnwaybill)服务的非官方Python SDK。

## WayBill

1. 第一种使用方法

```python
import asyncio

from cainiao import WayBillClient, WayBill
from cainiao.templates import WayBillGetForm, Sender, PackageInfo, Recipient


sender = Sender(**{
    "cpCode": "YTO",
    "name": "XXX",
    "province": "XX省",
    "city": "XX市",
    "district": "XX区",
    "detail": "XX街道",
    "mobile": "1XXXXXXXXXX",
})

recipient = Recipient(**{
    "name": "XXX",
    "province": "XX省",
    "city": "XX市",
    "district": "XX区",
    "detail": "XX街道",
    "mobile": "1XXXXXXXXXX",
    "tradeOrderList": [str(item) for item in range(10)],
    "orderChannelsType": "OTHERS",
    "templateUrl": ("http://cloudprint.cainiao.com"
                    "/template/standard/111/12003"),
    "packageInfo": PackageInfo(),
    "userId": "520",
})

waybill_get_form = WayBillGetForm(sender=sender, recipients=[recipient])


async def main():
    async with WayBillClient() as session:
        waybill = WayBill(
            url='http://link.cainiao.com/gateway/link.do',
            token='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
            appsecret='yyyyyyyyyyyyyyyyyyyyy',
            session=session
        )
        print(await waybill.tms_waybill_get(data=waybill_get_form))
        print(await waybill.subscription_query())
        print(await waybill.cloudprint_standard_templates())
        print(await waybill.cloudprint_isv_templates())
        print(await waybill.cloudprint_seller_custom_areas())
        print(await waybill.cloudpirnt_seller_custom_area_detail(mappingId=1))

asyncio.run(main())
```

1. 第二种使用方法

```python
# -- snip --

async def main():
    session = await WayBillClient().connection()
    waybill = WayBill(
        url='http://link.cainiao.com/gateway/link.do',
        token='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        appsecret='yyyyyyyyyyyyyyyyyyyyy',
        session=session
    )
    print(await waybill.tms_waybill_get(data=waybill_get_form))
    print(await waybill.subscription_query())
    print(await waybill.cloudprint_standard_templates())
    print(await waybill.cloudprint_isv_templates())
    print(await waybill.cloudprint_seller_custom_areas())
    print(await waybill.cloudpirnt_seller_custom_area_detail(mappingId=1))
    await session.close()

asyncio.run(main())
```
