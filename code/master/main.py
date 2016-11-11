import logging
import time
from collections import deque
from network import MasterNetwork

logger = logging.getLogger('root')
FORMAT = (
    '[%(asctime)s :: %(levelname)s '
    '%(filename)s:%(lineno)s - %(funcName)10s() ]'
    ' :: %(message)s'
)
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.INFO)


messages_to_slaves = deque
network = MasterNetwork(messages_to_slaves)
network.start()


def main():
    print("messages from arduino : ", network.arduino_messages)
    print("messages from slaves : ", network.status_messages)


if __name__ == '__main__':
    while 1:
        main()
        time.sleep(1)
