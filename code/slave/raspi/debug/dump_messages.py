import asyncio
import sys
import time

import zmq
import zmq.asyncio


MASTER_ADDR = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
print("Listening to: " + MASTER_ADDR)

def got_stdin_data(q):
    asyncio.async(q.put(sys.stdin.readline()))


ctx = zmq.asyncio.Context()
loop = zmq.asyncio.ZMQEventLoop()
asyncio.set_event_loop(loop)


@asyncio.coroutine
def recv_and_process():
    sock = ctx.socket(zmq.SUB)
    sock.connect("tcp://{}:5556".format(MASTER_ADDR))
    sock.setsockopt(zmq.SUBSCRIBE, b"")

    while True:
        msg = yield from sock.recv_multipart()
        print(time.time(), msg)


@asyncio.coroutine
def send_status():
    sock = ctx.socket(zmq.PUB)
    sock.connect("tcp://{}:5557".format(MASTER_ADDR))

    while True:
        msg = yield from q.get()  # waits for msg to be ready
        msg = msg.strip().encode()
        to_send = [b"1", msg]
        sock.send_multipart(to_send)
        print("sent : ", to_send)


q = asyncio.Queue()
loop.add_reader(sys.stdin, got_stdin_data, q)

asyncio.async(recv_and_process())
asyncio.async(send_status())
# loop.run_until_complete(heartbeat())
loop.run_forever()
