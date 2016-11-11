#! /usr/bin/env python

"""Main for the arduino connection."""

import time
import socket
from collections import deque, defaultdict
import logging
import sys
from serial_device import SerialDevice, list_devices_connected
from network import NetworkCommunication

messages_from_devices = deque()
messages_to_devices = defaultdict(deque)
messages_exceptions = deque()
connected_devices = set([])

HOSTNAME = socket.gethostname()

logger = logging.getLogger('root')
FORMAT = (
    '[%(asctime)s :: %(levelname)s '
    '%(filename)s:%(lineno)s - %(funcName)10s() ]'
    ' :: %(message)s'
)
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.INFO)

master_adress = sys.argv[1]
nc = NetworkCommunication(
    master_adress,
    messages_to_devices,
    messages_from_devices
)
nc.start()


def _main():
    serial_ids = ["2a03:0043", "2341:0043"]
    ports = list(list_devices_connected(serial_ids))
    for port in ports:
        if port in connected_devices:
            continue

        serial_device = SerialDevice(
            port,
            messages_from_devices,
            messages_to_devices,
            messages_exceptions
        )
        serial_device.start()
        connected_devices.add(port)


def main():
    """Manage the devices list."""
    _main()

    while messages_exceptions:
        broken_device = messages_exceptions.pop()
        print("cassé", str(broken_device))
        print(messages_from_devices)
        connected_devices.remove(broken_device.port)

    messages_from_devices.append(
        [HOSTNAME, "connected devices", str(connected_devices)]
    )

if __name__ == '__main__':
    while 1:
        main()
        time.sleep(1)
