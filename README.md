# Cainiao

适用于[菜鸟电子面单](https://www.cainiao.com/markets/cnwww/cnwaybill)服务的非官方Python SDK。

## Install

```shell
pip install cainiao
```

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

## CloudPrint

1. 第一种使用方法

    ```python
    import asyncio

    from cainiao import CloudPrintClient, CloudPrint
    from cainiao.templates import Content, Document, TaskForm

    content = Content(**{
        "data": {"nick": "Hello"},
        "templateURL": "http://cloudprint.cainiao.com/template/standard/278250/1",
    })

    document = Document(**{
        "documentID": "1",
        "contents": [content for _ in range(5)]
    })

    task = TaskForm(printer="Microsoft Print to PDF", documents=[document])


    async def main():
        async with CloudPrintClient(ws_url='ws://127.0.0.1:13528') as ws:
            cloudprint = CloudPrint(ws=ws)
            print(await cloudprint.get_printers())
            print(await cloudprint.print(task=task.content))


    asyncio.run(main())
    ```

1. 第二种使用方法

    ```python
    # -- snip --

    async def main():
        # 注意使用区别，session.close() 才是关闭 aiohttp.ClientSession()
        session, ws = await CloudPrintClient(ws_url='ws://127.0.0.1:13528').connect()
        cloudprint = CloudPrint(ws=ws)
        print(await cloudprint.get_printers())
        print(await cloudprint.print(task=task.content))
        await session.close()


    asyncio.run(main())
    ```
