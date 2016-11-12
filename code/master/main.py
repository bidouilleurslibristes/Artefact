import logging
import time
from collections import deque
from network import MasterNetwork
from enigma import SwagEnigma
from state import State

logger = logging.getLogger('root')
FORMAT = (
    '[%(asctime)s :: %(levelname)s '
    '%(filename)s:%(lineno)s - %(funcName)10s() ]'
    ' :: %(message)s'
)
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.INFO)


messages_to_slaves = deque()
arduino_messages = deque()
status_messages = deque()

network = MasterNetwork(messages_to_slaves, arduino_messages, status_messages)
network.start()

s = State(messages_to_slaves)
se = SwagEnigma(s)


def main():
    print("messages from arduino : ", arduino_messages)
    print("messages from slaves : ", status_messages)

    while arduino_messages:
        arduino_id, message = arduino_messages.pop()
        if "button" in message:
            _, button_id, status = message.split("-")
            se.update_from_devices(arduino_id, button_id, status)
        else:
            logger.error("WTF: {}".format(message))

    status_messages.clear()

if __name__ == '__main__':
    while 1:
        main()
        time.sleep(0.1)
