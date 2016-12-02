"""Enigme."""


import signal
import threading
import time
import random

SWAG_BUTTON_ID = 8
BUTTON_DOWN = "DOWN"
BUTTON_UP = "UP"


MAP_ARDUINO_PANEL = {
    "15": "0",
    "11": "1",
    "13": "3",
    "1": "2",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7"
}


class Enigma():
    """Enigma class."""

    def __init__(self, state):
        """Initialisation."""
        self.state = state
        self.is_solved = False

    def update_from_devices(self, device_id, button_id, button_state):
        """Update the state game after receiving a button push."""
        raise NotImplementedError


class SimpleEnigma(Enigma):
    """A simple enigma."""
    def __init__(self, state):
        """Init."""
        super(SimpleEnigma, self).__init__(state)

        self.state.set_all_swag_buttons(True)
        for i in range(8):
            self.state.set_all_led_strip("orange")
        self.state.notify_slaves()

    def update_from_devices(self, device_id, button_id, button_state):
        """update the game without using the arguments."""
        if self.is_solved:
            self.state.set_all_swag_buttons(True)
            self.state.set_all_led_strip("blanc")
        else:
            self.state.set_all_swag_buttons(False)
            self.state.set_all_led_strip("noir")
        self.state.notify_slaves()
        self.is_solved != self.is_solved


class Waiting(Enigma):
    def __init__(self, state):
        super(Waiting, self).__init__(state)

        self.anim = threading.Thread(target=self.affiche)
        self.anim.start()

    def affiche(self):
        i = 0
        button_on_index = 0
        led_on_index = 0
        nb_iteration_to_change = 10
        while True:
            self.state.set_all_led_strip("noir")
            self.state.set_all_swag_buttons(False)

            led_on_index = (i % (8 * nb_iteration_to_change)) // nb_iteration_to_change
            button_on_index = (i % (8 * nb_iteration_to_change)) // nb_iteration_to_change

            self.state.swag_button_light[button_on_index] = True
            for colors in self.state.led_stripes:
                colors[led_on_index] = "blanc"
            self.state.notify_slaves()
            i += 1
            time.sleep(1)

    def update_from_device(self, device_id, button_id, button_state):
        pass


class SwagEnigma(Enigma):
    """A swag enigma..."""

    def __init__(self, state):
        """Initialize a swag enigma."""
        super(SwagEnigma, self).__init__(state)

        self.different_strip_number = random.randint(0, 7)
        for i in range(8):
            if self.state.led_stripes[i][31] == "noir":
                self.state.set_all_led_strip("vert")

        self.state.set_all_swag_buttons(False)
        self.state.swag_button_light[self.different_strip_number] = True
        self.state.set_led_strip("rouge", self.different_strip_number)
        self.state.notify_slaves()

    def update_from_devices(self, device_id, button_id, button_state):
        """Update the state game after receiving a button push."""
        right_device = int(device_id) == int(self.different_strip_number)
        right_button = int(button_id) == int(SWAG_BUTTON_ID)
        button_ok = button_state == BUTTON_DOWN
        if right_button and right_device and button_ok:
            self.state.set_led_strip("vert", self.different_strip_number)
            self.state.set_all_swag_buttons(True)
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


class SimonEnigma(Enigma):

    #penser à eteindre les boutons lors de la sequence

    def __init__(self, state, color_number, sequence_size):
        super(SimonEnigma, self).__init__(state)
        self.solved = False
        self.loose = False
        self.current = 0
        self.colors = ["rouge", "vert", "bleu", "jaune"]
        self.color_number = color_number
        self.sequence_size = sequence_size
        # init buttons
        for i in range(8):
            for j in range(len(self.colors)):
                self.state.led_buttons[i][j] = self.colors[j]

        self.init_sequence()
        self.show_sequence()

    def show_sequence(self):
        for i in range(self.sequence_size):
            # Mettre tous les bandeaux à noir
            self.state.set_all_led_strip("noir")
            # Mettre le bon bandeau à la bonne couleur
            self.state.set_led_strip(self.sequenceColors[i], self.sequencePositions[i])
            # Force l'affichage sur les leds
            self.state.notify_slaves()
            time.sleep(1)
            # Remet au noir
            self.state.set_all_led_strip("noir")
            self.state.notify_slaves()
            time.sleep(1)

    def init_sequence(self):
        self.sequenceColors = []
        self.sequencePositions = []

        for i in range(self.sequence_size):
            self.sequenceColors.append(random.choice(self.colors[:self.color_number]))
            self.sequencePositions.append(random.randint(0, 7))

    def update_from_devices(self, device_id, button_id, button_state):
        device_id = int(MAP_ARDUINO_PANEL[device_id])
        button_id = int(button_id)
        if button_state == "UP":
            return
        if device_id != self.sequencePositions[self.current]:
            self.error()
            return

        color = self.colors[button_id]
        if color != self.sequenceColors[self.current]:
            self.error()
            return

        self.current += 1
        if self.sequence_size == self.current:
            self.win()

    def error(self):
        self.loose = True
        print("ON ERROR")
        self.state.set_all_led_strip("rouge")
        self.state.notify_slaves()
        time.sleep(2)

    def win(self):
        print("WIN")
        self.solved = True
        self.state.set_all_led_strip("vert")
        self.state.notify_slaves()
        time.sleep(2)

    def reinit(self):
        self.current = 0
        self.loose = False
        self.solved = False
        self.show_sequence()
