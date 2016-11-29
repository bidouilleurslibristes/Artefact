import logging
import time
from collections import deque
from network import MasterNetwork
from enigma import SimonEnigma, SwagEnigma, SimpleEnigma, Waiting
from state import State

from raven.handlers.logging import SentryHandler
from raven.conf import setup_logging


logger = logging.getLogger('root')
FORMAT = (
    '[%(asctime)s :: %(levelname)s '
    '%(filename)s:%(lineno)s - %(funcName)10s() ]'
    ' :: %(message)s'
)

handler = SentryHandler(
    'https://5351cd7e946648c2a537ed641f5b4663:56cb93aa44df4e0a92e4fec93fc9ccd8@sentry.io/103075',
    level=logging.ERROR
)

logging.basicConfig(format=FORMAT)
#setup_logging(handler)
logger.setLevel(logging.CRITICAL)

messages_to_slaves = deque()
arduino_messages = deque()
status_messages = deque()

network = MasterNetwork(messages_to_slaves, arduino_messages, status_messages)
network.start()

s = State(messages_to_slaves)

difficulty = 3
se = SimonEnigma(s, 4, difficulty)
#se = SimpleEnigma(s)
ses = [se]
#w = Waiting(s)


def main():
    global difficulty

    while arduino_messages:
        arduino_id, message = arduino_messages.pop()
        if "button" in message:
            try:
                _, button_id, status = message.split("-")
            except ValueError as e:
                logger.error("Unknown message: {}".format(e))
                logger.exception(e)
            else:
                ses[0].update_from_devices(arduino_id, button_id, status)
        else:
            logger.error("Unkown message: {}".format(message))

    status_messages.clear()

    if ses[0].loose:
        ses[0].sequence_size = 3
        ses[0].reinit()

    if ses[0].solved:
        difficulty += 1
        ses[0] = SimonEnigma(s, 4, difficulty)


if __name__ == '__main__':
    while 1:
        main()
        time.sleep(0.05)
