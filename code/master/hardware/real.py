"""Real hardware interface.

These is used to control the physical hardware.
"""

from hardware.abstract import AbstractDevice


from state import State, ARDUINOS_CONNECTED_TO_PANELS, ARDUINO_LED_STRIPS_ID
from network import MasterNetwork

import time
from hardware.button import Button


class Device(AbstractDevice):
    """Interface to a device."""

    def __init__(self):
        """Initialisation."""
        super(Device, self).__init__()

        self.network = MasterNetwork()
        self.network.start()

    def send_state(self):
        """Send the state to the hardware."""
        self.state = self.enigma.get_state()
        messages = self.notify_slaves()
        for message in messages:
            self.network.messages_to_slaves.append(message)

    def wait_for_event(self):
        time.sleep(0.1)
        while self.network.arduino_messages:
            panel_id, msg = self.network.arduino_messages.popleft()
            if not msg.startswith("button"):
                continue

            _, button_id, status = msg.strip().split("-")
            self.enigma.button_triggered(Button(panel_id, button_id, status))

    def notify_slaves(self):
        """Put the current state to the slaves in the message_to_slaves inbox."""
        messages_to_slaves = []
        messages_to_slaves.extend(self.build_led_strip_strings())
        messages_to_slaves.extend(self.build_swag_buttons_strings())
        messages_to_slaves.extend(self.build_led_buttons_strings())
        return messages_to_slaves

    def build_led_strip_strings(self):
        """Build the messages to set the led strips colors."""
        commande = "1"
        animation = "A"

        tmp = []
        for index, colors in enumerate(self.state.led_stripes):
            colors_formatted = [self.state.color_to_index(c) for c in colors]
            string_color = "".join(map(str, colors_formatted))
            res = "{}{}{}{}".format(commande, animation, index, string_color)
            tmp.append((str(ARDUINO_LED_STRIPS_ID), res))
        return tmp

    def build_led_buttons_strings(self):
        """Build the messages to set the buttons colors."""
        tmp = []
        commande = "2"
        for panel_id, arduino_id in enumerate(ARDUINOS_CONNECTED_TO_PANELS):
            colors = [butt.state for butt in self.state.normal_button_states()[panel_id]]
            colors_formatted = [self.state.color_to_index(c) for c in colors]
            string_color = "".join(map(str, colors_formatted))
            res = "{}{}".format(commande, string_color)
            tmp.append((str(arduino_id), res))
        return tmp

    def build_swag_buttons_strings(self):
        """Build the message to set the swag buttons colors."""
        tmp = []
        commande = "3"
        for index, arduino_id in enumerate(ARDUINOS_CONNECTED_TO_PANELS):
            on_off = [str(int(butt.state == "blanc")) for butt in self.state.swag_button_states()]
            res = "{}{}".format(commande, on_off)
            tmp.append((str(arduino_id), res))
        return tmp
