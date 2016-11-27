"""Code to simulate server emission."""

import zmq

ctx = zmq.Context()


def send_command():
    socket = ctx.socket(zmq.PUB)
    socket.bind("tcp://127.0.0.1:5556")
    channel = b"2"
    message = "plop"

    import ipdb; ipdb.set_trace()

    socket.send_multipart([channel, message.encode("utf8")])


if __name__ == '__main__':
    send_command()