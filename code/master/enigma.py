import random
import time


class Enigma():
    """Enigma abstract class."""

    def __init__(self, device):
        """Initialisation."""
        self.device = device
        self.is_solved = False

    def update_from_devices(self, device_id, button_id, device):
        """Update the device game after receiving a button push."""
        raise NotImplementedError


class SimpleEnigma(Enigma):
    """A simple enigma."""

    def __init__(self, device):
        """Init."""
        super(SimpleEnigma, self).__init__(device)

        self.device.set_all_swag_buttons(True)
        for i in range(8):
            self.device.set_all_led_strip("orange")
        self.device.send_state()

    def update_from_devices(self, device_id, button_id, device):
        """update the game without using the arguments."""
        if self.is_solved:
            self.device.set_all_swag_buttons(True)
            self.device.set_all_led_strip("blanc")
        else:
            self.device.set_all_swag_buttons(False)
            self.device.set_all_led_strip("noir")
        self.device.send_state()
        self.is_solved != self.is_solved


class SwagEnigma(Enigma):
    """A swag enigma..."""

    def __init__(self, device):
        """Initialize a swag enigma."""
        super(SwagEnigma, self).__init__(device)

        self.different_strip_number = random.randint(0, 7)

        self.device.set_all_led_strip("vert")
        self.device.set_all_swag_buttons(False)
        self.device.set_swag_button(self.different_strip_number, True)
        self.device.set_all_leds_in_strip(self.different_strip_number, "rouge")

        self.device.send_state()

    def update_from_devices(self, device_id, button_id, button_device):
        """Update the device game after receiving a button push."""                
        right_device = (int(device_id) == int(self.different_strip_number))
        right_button = (int(button_id) == int(device.SWAG_BUTTON_ID))
        button_state_ok = (button_device in device.BUTTON_DOWN)

        if right_button and right_device and button_state_ok:
            self.device.set_all_leds_in_strip(self.different_strip_number, "vert")
            self.device.set_all_swag_buttons(True)
            self.is_solved = True
            self.device.send_state()


class SimonEnigma(Enigma):
    def __init__(self, state, color_number, sequence_size):
        super(SimonEnigma, self).__init__(state)
        self.solved = False
        self.loose = False
        self.current = 0
        self.colors = ["rouge", "vert", "bleu", "jaune"]
        self.color_number = color_number
        self.sequence_size = sequence_size
        # init buttons
        for panel_id in range(8):
            for color_index, color in enumerate(self.colors):
                self.device.set_one_led_in_panel(panel_id, color_index, color)

        self.init_sequence()
        self.show_sequence()

    def show_sequence(self):
        for i in range(self.sequence_size):
            # Mettre tous les bandeaux à noir
            self.device.set_all_led_strips("noir")
            # Mettre le bon bandeau à la bonne couleur
            self.device.set_all_leds_in_strip(self.sequencePositions[i], self.sequenceColors[i])
            # Force l'affichage sur les leds
            self.device.send_state()
            time.sleep(1)
            # Remet au noir
            self.device.set_all_led_strips("noir")
            self.device.send_state()
            time.sleep(1)

    def init_sequence(self):
        self.sequenceColors = []
        self.sequencePositions = []

        for i in range(self.sequence_size):
            self.sequenceColors.append(random.choice(self.colors[:self.color_number]))
            self.sequencePositions.append(random.randint(0, 7))

    def update_from_devices(self, device_id, button_id, button_state):
        ## ATTENTION : utiliser MAP_ARDUINO_PANEL quelque part pour utiliser le matériel réel
        device_id = int(device_id)
        button_id = int(button_id)
        print("device_id: {} -- button_id: {} -- button_state: {}".format(device_id, button_id, button_state))
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
        self.device.set_all_led_strips("rouge")
        self.device.send_state()
        time.sleep(2)

    def win(self):
        print("WIN")
        self.solved = True
        self.device.set_all_led_strips  ("vert")
        self.device.send_state()
        time.sleep(2)

    def reinit(self):
        self.current = 0
        self.loose = False
        self.solved = False
        self.show_sequence()
