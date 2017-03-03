"""Modelisation for the game."""
from hardware.button import Button

COLORS = {
    "noir": 0,
    "rouge": 1,
    "vert": 2,
    "bleu": 3,
    "jaune": 4,
    "mauve": 5,
    "turquoise": 6,
    "orange": 7,
    "blanc": 8,
}

ARDUINOS_CONNECTED_TO_PANELS = [
    15, 11, 1, 13, 4, 5, 6, 7  # index : panel ID and value : arduino ID
]
ARDUINO_LED_STRIPS_ID = 8  # we use only one arduino for the led strips.

SWAG_BUTTON_ID = 8
BUTTON_DOWN = ["DOWN", False]
BUTTON_UP = ["UP", True]


class State():
    """Class to store the game state.

    The state is modified by the different enigmas.

    The state is also is charge to build the messages to the slaves.
    this is why it needs the "message_to_slaves" box.
    """

    def __init__(self):
        """Empty state."""
        self.init_led_strips()
        self.init_buttons()

        self.swag_button_id = 8

    def init_buttons(self):
        self.buttons = []
        for panel_id in range(8):
            tmp = []
            for button_id in range(9):
                tmp.append(Button(panel_id, button_id))
            self.buttons.append(tmp)

    def init_led_strips(self):
        self.led_stripes = [
            ["noir" for i in range(32)],  # arduino 8
            ["noir" for i in range(32)],  # arduino 9
            ["noir" for i in range(32)],
            ["noir" for i in range(32)],
            ["noir" for i in range(32)],
            ["noir" for i in range(32)],
            ["noir" for i in range(32)],
            ["noir" for i in range(32)],  # arduino 15
        ]

    def swag_button_states(self):
        return [panel[self.swag_button_id] for panel in self.buttons]

    def notify_slaves(self):
        """Put the current state to the slaves in the message_to_slaves inbox."""
        self.message_to_slaves = []
        self.notify_led_strip()
        self.notify_swag_buttons()
        self.notify_led_buttons()
        return self.message_to_slaves


    def color_to_index(self, color):
        """Format the colors in the format that arduino can understand."""
        return COLORS[color]

    def __repr__(self):
        res = ""
        res += "Led strips: \n"
        for strip in self.led_stripes:
            res += "  * ".join(strip) + "\n"

        res += "\n\n"
        res += "Swag Buttons : \n"
        for light in self.swag_button_light:
            res += "{} - ".format(light)

        return res

    def set_one_led_in_strip(self, strip_id, led_id, color):
        """Cache the color of a given led in a given panel to a given color."""
        self.led_stripes[strip_id][led_id] = color

    def set_all_leds_in_strip(self, strip_id, color):
        self.led_stripes[strip_id] = [color for _ in self.state.led_stripes[strip_id]]

    def set_swag_button(self, panel_id, value):
        """Cache the swag button led state to a given value."""
        self.buttons[panel_id][self.SWAG_BUTTON_ID].state = value
    def set_all_led_strips(self, color):
        """Set all led strips to a given color."""
        for strip_id in range(8):
            self.set_all_leds_in_strip(strip_id, color)

    def set_all_swag_buttons(self, status):
        """Set all swag buttons to the same status (True or False)."""
        for panel_id in range(8):
            self.set_swag_button(panel_id, status)

