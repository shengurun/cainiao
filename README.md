# Cainiao SDK

适用于[菜鸟电子面单](https://www.cainiao.com/markets/cnwww/cnwaybill)服务的非官方Python SDK。

## 安装

`pip install cainiao`

## 例子

* 获取电子面单信息

```python
import json
from cainiao.waybill.apis import CAINIAO_PARAMETERS, TMSWayBillGet

CAINIAO_PARAMETERS['CAINIAO_APPKEY'] = 'xxxxxx'
CAINIAO_PARAMETERS['CAINIAO_APPSECRET'] = 'xxxxxxxxxx'
CAINIAO_PARAMETERS['CAINIAO_TOKEN'] = 'xxxxxxxxxxxxxxxxxxxxxxx'
CAINIAO_PARAMETERS['CAINIAO_URL'] = 'http://link.cainiao.com/gateway/link.do'

if __name__ == '__main__':
    case = TMSWayBillGet(parameters=CAINIAO_PARAMETERS)
    with open('response.json', 'w', encoding='utf-8') as f:
        f.write(case.response)
```

* 打印电子面单

```python
from cainiao.printer.apis import generate_client, get_printers

if __name__ == '__main__':
    ws = generate_client()
    response = get_printers(ws)
    with open('printers.json', 'w', encoding='utf-8') as f:
        f.write(response)
```
