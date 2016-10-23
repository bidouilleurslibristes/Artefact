import asyncio
import zmq
import zmq.asyncio

# python 3.4.4 => 3.4.5
asyncio.ensure_future = asyncio.async

ctx = zmq.asyncio.Context()
loop = zmq.asyncio.ZMQEventLoop()
asyncio.set_event_loop(loop)

protocol = "tcp"
port = "5556"
adress = "127.0.0.1"
url = "{}://{}:{}".format(protocol, adress, port)

@asyncio.coroutine
def recv_and_process():
    while True:
        sock = ctx.socket(zmq.SUB)
        sock.connect(url)
        sock.setsockopt(zmq.SUBSCRIBE, b"")
        msg = yield from sock.recv_multipart() # waits for msg to be ready
        print(msg)

@asyncio.coroutine
def heartbeat():
    print("heartbeat")
    while True:
        yield from asyncio.sleep(2)
        print("alive")


asyncio.async(recv_and_process())
loop.run_until_complete(heartbeat())
loop.run_forever()