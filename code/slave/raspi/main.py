"""Main for the arduino connection."""

import time
from collections import deque, defaultdict
import logging
from serial_device import SerialDevice, list_devices_connected
from network import NetworkCommunication

messages_from_devices = deque()
messages_to_devices = defaultdict(deque)
messages_exceptions = deque()
connected_devices = set([])


logger = logging.getLogger('root')
FORMAT = (
    '[%(asctime)s :: %(levelname)s '
    '%(filename)s:%(lineno)s - %(funcName)10s() ]'
    ' :: %(message)s'
)
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.INFO)


def _main():
    nc = NetworkCommunication(messages_to_devices, messages_from_devices)
    nc.start()

    ports = list(list_devices_connected("."))
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
    print("connected devices", connected_devices)


def main():
    """Manage the devices list."""
    _main()
    while messages_exceptions:
        broken_device = messages_exceptions.pop()
        print("cassé", str(broken_device))
        print(messages_from_devices)
        connected_devices.remove(broken_device.port)
    messages_from_devices.append(
        ["slave1", "connected devices", str(connected_devices)]
    )

if __name__ == '__main__':
    while 1:
        main()
        time.sleep(1)
