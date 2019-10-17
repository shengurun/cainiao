import ssl
from uuid import uuid4
import json

from websocket import create_connection


def generate_client(protocol='ws', host='localhost'):
    """创建WS客户端（用于“短连接”）
    短链接需要在使用后，执行关闭。代码如下：
    ```
        ws = generate_client()

        ...

        ws.close()
    ```

    protocol: 使用的协议，`wss`为使用ssl的链接，必须使用本机，`ws`则可以指定不同IP
    host: 安装菜鸟云打印客户端的PC的IP
    """
    if protocol == 'wss':
        ws = create_connection(
            'wss://localhost:13529',
            sslopt={"cert_reqs": ssl.CERT_NONE}
        )
    else:
        ws = create_connection('ws://{host}:13528'.format(host=host))
    return ws


def get_printers(ws, request_id=str(uuid4())):
    """获取所有打印机
    request_id: 一个可以确定唯一性的随机数，保证每次请求不一
    """
    request = json.dumps({
        'cmd': 'getPrinters',
        'requestID': request_id,
        'version': '1.0'
    }, ensure_ascii=False)

    ws.send(request)
    response = ws.recv()

    return response


def print_order(ws, request_id=str(uuid4()), task=''):
    """开启电子面单打印任务
    request_id: 一个可以确定唯一性的随机数，保证每次请求不一。
                也可以使用相同的request_id + task组合，创建重新打印的任务。
    task:       打印任务的内容，需按照文档要求编写。
    """
    request = json.dumps({
        'cmd': 'print',
        'requestID': request_id,
        'version': '1.0',
        'task': task
    }, ensure_ascii=False)

    ws.send(request)
    response = ws.recv()

    return response
