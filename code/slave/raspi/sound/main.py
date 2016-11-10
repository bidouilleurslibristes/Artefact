#! /usr/bin/env python

"""Main for the sound player."""

import logging
import pygame.mixer
import pygame.time
import zmq

logger = logging.getLogger('root')
FORMAT = (
    '[%(asctime)s :: %(levelname)s '
    '%(filename)s:%(lineno)s - %(funcName)10s() ]'
    ' :: %(message)s'
)
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.INFO)

server_adress_in = "tcp://127.0.0.1:5556"

ctx = zmq.Context()
poller = zmq.Poller()
sock_in = ctx.socket(zmq.SUB)
sock_in.connect(server_adress_in)

topic = "slave.sound".encode()
sock_in.setsockopt(zmq.SUBSCRIBE, topic)
poller.register(sock_in, zmq.POLLIN)


mixer = pygame.mixer
time = pygame.time


def play_music(file_path):
    """Play file using pygame.

    This is ugly, we will put it in it's own class and thread...
    """
    mixer.init(44100, -16, 2, 512)  # raises exception on fail
    mixer.music.load(file_path)

    print('Playing Sound...')
    mixer.music.play()

    while mixer.music.get_busy():
        print('  ...still going...')
        time.wait(1000)
    print('...Finished')


def main():
    while True:
        sockets = dict(poller.poll(10))
        if not sockets:
            continue
        msg = sock_in.recv_multipart()  # we only have one listening socket
        logger.info("received {} from master".format(msg))
        message_string = msg[1].decode()

        if "start" in message_string:
            play_music("./sample.mp3")
        if "stop" in message_string:
            print("stop music")

if __name__ == "__main__":
    main()
