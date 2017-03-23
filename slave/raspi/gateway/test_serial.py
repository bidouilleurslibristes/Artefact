""""""
from collections import deque, defaultdict
from serial_device import SerialDevice, list_devices_connected
import time


messages_from_devices = deque()
messages_to_devices = defaultdict(lambda: deque(maxlen=1000))
messages_exceptions = deque()
connected_devices = set([])

serial_ids = ["2a03:0043", "2341:0043", "2341:0243", "214b:7000"]
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


def build_led_strip_strings():
    nb_led_strips = 8
    nb_leds_per_strip = 32

    res = []
    for i in range(nb_led_strips):
        res.append("1A" + str(i) + str(i) * nb_leds_per_strip)
    return res



def build_led_buttons_strings(col):
    nb_leds_per_strip = 8
    return "2" + str(col) * nb_leds_per_strip


def build_swag_button_led(on):
    return "3" + str(int(on is True))


def send_to_device(string):
    messages_to_devices[serial_device.device_id].append(string)


# import ipdb; ipdb.set_trace()

time.sleep(10)
#[send_to_device(build_led_buttons_strings(i%8)) for i in range(8)]

for mess in build_led_strip_strings():
    print("sending : {}".format(mess))
    send_to_device(mess)

print("FINI")

