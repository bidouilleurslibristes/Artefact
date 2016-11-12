"""Enigme."""


import signal
import time
import random

SWAG_BUTTON_ID = 8
BUTTON_DOWN = "DOWN"
BUTTON_UP = "UP"


class Enigma():
    """Enigma class."""

    def __init__(self, state):
        """Initialisation."""
        self.state = state
        self.is_solved = False

    def update_from_devices(self, device_id, button_id, button_state):
        """Update the state game after receiving a button push."""
        raise NotImplementedError


class SwagEnigma(Enigma):
    """A swag enigma..."""

    def __init__(self, state):
        """Initialize a swag enigma."""
        super(SwagEnigma, self).__init__(state)

        self.different_strip_number = random.randint(0, 7)
        for i in range(8):
            if self.state.led_stripes[i][31] == "noir":
                self.state.set_all_led_strip("vert")

        self.state.set_led_strip("rouge", self.different_strip_number)

    def update_from_devices(self, device_id, button_id, button_state):
        """Update the state game after receiving a button push."""
        right_device = int(device_id) == int(self.different_strip_number)
        right_button = int(button_id) == int(SWAG_BUTTON_ID)
        button_ok = button_state == BUTTON_DOWN
        if right_button and right_device and button_ok:
            self.state.set_led_strip("vert", self.different_strip_number)
            self.is_solved = True
            self.state.notify_slaves()


class TimeEnigma(Enigma):
    """Temporal enigma like guitat hero."""

    def __init__(self, state, sequence_size):
        """Constructor."""
        # Enigma init
        ens = []
        for i in range(8):
            if self.state.led_stripes[i][31] == "vert" or self.state.led_stripes[i][31] == "noir":
                ens.append(i)
        self.different_strip_number = random.choice(ens)
        self.is_solved = False

        self.sequence = []
        available_colors = ["rouge", "vert", "bleu"]
        for i in range(sequence_size):
            self.sequence.append(random.choice(available_colors))

        self.sequence_idx = 0

        # Led strip init
        for i in range(31):
            self.state.led_stripes[self.different_strip_number][i] = "noir"
        self.state.led_stripes[self.different_strip_number][31] = "orange"

        idx = 0
        for color in self.sequence:
            self.state.led_stripes[self.different_strip_number][idx] = self.sequence[idx]
            idx += 1

        # Interface buttons init
        idx = 0
        for color in available_colors:
            self.state.led_buttons[self.different_strip_number][idx] = available_colors[idx]
            idx += 1

        # Trigger alarm
        signal.signal(signal.SIGALRM, self.callback)
        signal.alarm(1)

    def update_from_devices(self, device_id, button_id, button_state):
        """Update the state game after receiving a button push."""
        if not device_id == self.different_strip_number:
            return
        if not button_state == "DOWN":
            return

        button_color = self.state.led_buttons[device_id][button_id]
        if self.sequence[len(self.sequence) - 1] == button_color:
            # removing the last item of the sequence
            self.sequence.pop()

        if len(self.sequence) == 0:
            self.is_solved = True

    def callback(self, signum, stack):
        """Called by the alarm."""
        self.sequence_idx += 1
        # si la sequence atteind la fin du bandeau
        if self.sequence_idx + len(self.sequence) == 31:
            # on met tout à rouge et on arrete
            for i in range(32):
                self.state.led_stripes[self.different_strip_number][i] = "rouge"
            return
        # On decalle toutes les leds
        for i in reversed(range(len(self.sequence))):
            self.state.led_stripes[self.different_strip_number][self.sequence_idx + i] = \
                self.state.led_stripes[self.different_strip_number][self.sequence_idx + i - 1]
        # on met le dernier à noir
        self.state.led_stripes[self.different_strip_number][self.sequence_idx] = "noir"
        signal.alarm(1)
