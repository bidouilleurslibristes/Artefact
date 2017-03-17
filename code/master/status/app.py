""" Receive statuses from the slaves and display them in a web page.

Code for aiohttp inspired from :
 * https://github.com/steelkiwi/aiohttp_test_chat/
 * http://steelkiwi.com/blog/an-example-of-a-simple-chat-written-in-aiohttp/
 * http://aiohttp.readthedocs.io/en/stable/web.html#static-file-handling
"""

import asyncio
import json
import time
from aiohttp import web

import aiohttp_debugtoolbar
import jinja2
import aiohttp_jinja2
import zmq
import zmq.asyncio


ctx = zmq.asyncio.Context()
loop = zmq.asyncio.ZMQEventLoop()
asyncio.set_event_loop(loop)


@asyncio.coroutine
def recv_statuses(statuses):
    sock = ctx.socket(zmq.SUB)
    sock.bind("tcp://0.0.0.0:5558")
    sock.setsockopt(zmq.SUBSCRIBE, b"")

    while True:
        msg = yield from sock.recv_multipart()
        msg = [s.decode() for s in msg]
        _, device_id, status, connected = msg

        if status == "connected devices":
            connected = json.loads(connected)

        statuses[device_id] = {
            "status": status,
            "connected": connected,
            "timestamp": time.time()
        }
        print(statuses)


@aiohttp_jinja2.template('index.html')
def index(request):
    # return web.Response(text=str(statuses))
    return {"status": statuses}


def data(request):
    # statuses = {
    #     'xps13-matt': {
    #         'status': 'connected devices',
    #         'timestamp': 1489517409.8815544,
    #         'connected': {"/dev/ttyACM1": "1", "/dev/ttyACM2": "2"}
    #     },
    #     'xps13-matt2': {
    #         'status': 'connected devices',
    #         'timestamp': 1489517409.881532544,
    #         'connected': {"/dev/ttyACM1": "1", "/dev/ttyACM2": "2"}
    #     },
    # }

    return web.json_response(statuses)


@asyncio.coroutine
def init_web(loop):
    app = web.Application(loop=loop)

    if DEBUG:
        aiohttp_debugtoolbar.setup(app)

    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('.'))
    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/data', data)
    app.router.add_static('/static', 'static', name='static')

    handler = app.make_handler()
    serv_generator = loop.create_server(handler, SITE_HOST, SITE_PORT)
    return serv_generator, handler, app


DEBUG = True
statuses = {}
SITE_HOST = "0.0.0.0"
SITE_PORT = "8081"

app = web.Application(loop=loop)

asyncio.async(recv_statuses(statuses))
serv_generator, handler, app = loop.run_until_complete(init_web(loop))
serv = loop.run_until_complete(serv_generator)
loop.run_forever()



print("end")