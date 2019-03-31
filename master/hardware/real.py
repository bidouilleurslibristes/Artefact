"""Real hardware interface.

These is used to control the physical hardware.
"""

import os
import time
import logging
import errno

from hardware.abstract import AbstractDevice


from state import State, ARDUINOS_CONNECTED_TO_PANELS, ARDUINO_LED_STRIPS_ID, REBOOT_ARDUINO
from network import MasterNetwork

from hardware.button import Button


logger = logging.getLogger('root')
THRESHOLD_DOUBLE_CLICK = 1  # seconds


def symlink_force(target, link_name):
    try:
        os.symlink(target, link_name)
    except OSError as e:
        if e.errno == errno.EEXIST:
            os.remove(link_name)
            os.symlink(target, link_name)
        else:
            raise e


def change_difficulty(fname):
    """Change the game difficulty.

    We change the symlink to the "data" file and restart the service.
    """
    file_dir = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.normpath(os.path.join(file_dir, "..", "data"))
    src = os.path.join(data_dir, fname)
    dst = os.path.join(data_dir, "culture.txt")
    symlink_force(src, dst)


class Device(AbstractDevice):
    """Interface to a device."""

    def __init__(self):
        """Initialisation."""
        super(Device, self).__init__()

        self.network = MasterNetwork()
        self.network.start()
        self.last_clicks = {}

    def send_state(self):
        """Send the state to the hardware."""
        self.state = self.enigma.get_state()
        messages = self.notify_slaves()
        for message in messages:
            self.network.messages_to_slaves.append(message)

    def wait_for_event(self):
        time.sleep(0.1)
        while self.network.arduino_messages:
            arduino_id, msg = self.network.arduino_messages.popleft()
            if int(arduino_id) == REBOOT_ARDUINO:  # button to restart the game
                if "DOWN" not in msg:
                    return

                # msg : button-(easy/normal/hard)-UP

                # change difficulty
                self.enigma.on_error = True
                self.reboot = True
                self.network.arduino_messages.clear()
                difficulty = msg.split("-")[1]
                change_difficulty(difficulty + ".txt")
                return

            try:
                panel_id = ARDUINOS_CONNECTED_TO_PANELS.index(int(arduino_id))
            except Exception as e:
                logger.exception("Got message {} from unknown arduino: {}".format(msg, arduino_id))
                continue

            if not msg.startswith("button"):
                continue

            _, button_id, status = msg.strip().split("-")
            current_ts = time.time()
            last_click_ts = self.last_clicks.get((panel_id, button_id, status), 0)
            if (current_ts - last_click_ts) < THRESHOLD_DOUBLE_CLICK:
                continue
            self.last_clicks[(panel_id, button_id, status)] = current_ts

            color = self.state.buttons[panel_id][int(button_id)].state
            button_changed = Button(panel_id, button_id, status, color)
            button_exists_in_enigma = self.enigma.button_triggered(button_changed)
            self.log_game("button pushed", button_changed)
            if button_exists_in_enigma and status == Button.BUTTON_DOWN:
                self.send_button_click()

    def notify_slaves(self):
        """Put the current state to the slaves in the message_to_slaves inbox."""
        messages_to_slaves = []
        messages_to_slaves.extend(self.build_led_strip_strings())
        messages_to_slaves.extend(self.build_swag_buttons_strings())
        messages_to_slaves.extend(self.build_led_buttons_strings())
        return messages_to_slaves

    def send_fade_out(self):
        message = (str(ARDUINO_LED_STRIPS_ID), "3")
        self.network.messages_to_slaves.append(message)

    def send_button_click(self):
        message = ("sound", "validation")
        self.network.messages_to_slaves.append(message)

    def send_win_animation(self):
        message = (str(ARDUINO_LED_STRIPS_ID), "2")
        self.network.messages_to_slaves.append(message)

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
            on_off = str(int(self.state.swag_button_states()[index].state == "blanc"))
            res = "{}{}".format(commande, on_off)
            tmp.append((str(arduino_id), res))
        return tmp









