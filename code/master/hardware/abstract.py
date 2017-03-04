from state import State


class AbstractDevice:
    """Interface to a device."""

    def __init__(self):
        """Initialisation."""
        self.state = State()
        print("device init")
        self.SWAG_BUTTON_ID = 8
        self.BUTTON_DOWN_CODE = "DOWN"
        self.enigma = None

    def send_state(self):
        """Send the state to the hardware."""
        raise NotImplementedError

    def set_enigma(self, enigma):
        self.enigma = enigma
        self.send_state()

    def set_one_led_in_panel(self, panel_id, led_id, color):
        self.state.buttons[panel_id][led_id].state = color

    def solve_enigma(self):
        """ Game loop for an enigma """
        while not self.enigma.is_solved():
            self.wait_for_event()

    def wait_for_event(self):
        """ waiting for game event """
        raise NotImplementedError
