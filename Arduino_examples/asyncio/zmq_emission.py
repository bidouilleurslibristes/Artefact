import asyncio
import json

import zmq
import zmq.asyncio

ctx = zmq.asyncio.Context()


@asyncio.coroutine
def receive_status():
    sock = ctx.socket(zmq.SUB)
    sock.bind("tcp://127.0.0.1:5557")
    sock.setsockopt(zmq.SUBSCRIBE, b"")

    while True:
        msg = yield from sock.recv_multipart()
        print("updated status : {}".format(msg))


@asyncio.coroutine
def send_command():
    socket = ctx.socket(zmq.PUB)
    socket.bind("tcp://127.0.0.1:5556")
    i = 0
    channel = b"1"
    while True:
        yield from asyncio.sleep(2)
        message = {"data": i}
        socket.send_multipart([channel, json.dumps(message).encode("utf8")])
        print("sending : ", json.dumps(message))
        i += 1


loop = zmq.asyncio.ZMQEventLoop()
asyncio.set_event_loop(loop)

asyncio.async(send_command())
loop.run_until_complete(receive_status())
loop.run_forever()
