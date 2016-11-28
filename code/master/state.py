"""Modelisation for the game."""


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


class State():
    """Class to store the game state.

    The state is modified by the different enigmas.

    The state is also is charge to build the messages to the slaves.
    this is why it needs the "message_to_slaves" box.
    """

    def __init__(self, message_to_slaves):
        """Empty state."""
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

        self.led_buttons = [
            ["noir" for i in range(8)],  # arduino 0
            ["noir" for i in range(8)],  # arduino 1
            ["noir" for i in range(8)],
            ["noir" for i in range(8)],
            ["noir" for i in range(8)],
            ["noir" for i in range(8)],
            ["noir" for i in range(8)],
            ["noir" for i in range(8)],  # arduino 7
        ]

        self.pushed_buttons = [
            [False for _ in range(8)],  # arduino 0
            [False for _ in range(8)],
            [False for _ in range(8)],
            [False for _ in range(8)],
            [False for _ in range(8)],
            [False for _ in range(8)],
            [False for _ in range(8)],
            [False for _ in range(8)],  # arduino 7
        ]

        self.swag_button_pushed = [
            False,  # arduino 0
            False,
            False,
            False,
            False,
            False,
            False,
            False,  # arduino 7
        ]

        self.swag_button_light = [
            False,  # arduino 0
            False,
            False,
            False,
            False,
            False,
            False,
            False,  # arduino 7
        ]

        self.message_to_slaves = message_to_slaves

    def set_all_led_strip(self, color):
        """Set all led strips to a given color."""
        self.led_stripes = [
            [color for i in range(32)],
            [color for i in range(32)],
            [color for i in range(32)],
            [color for i in range(32)],
            [color for i in range(32)],
            [color for i in range(32)],
            [color for i in range(32)],
            [color for i in range(32)],
        ]

    def set_led_strip(self, color, number):
        """Set a led strip to a color."""
        self.led_stripes[number] = [color for i in range(32)]

    def set_all_swag_buttons(self, status):
        """Set all swag buttons to the same status (True or False)."""
        self.swag_button_light = [status for i in range(len(self.swag_button_light))]

    def notify_slaves(self):
        """Put the current state to the slaves in the message_to_slaves inbox."""
        self.notify_led_strip()
        self.notify_led_buttons()
        self.notify_swag_buttons()

    def notify_led_strip(self):
        """Build the messages to set the led strips colors."""
        commande = "1"
        animation = "A"

        for index, colors in enumerate(self.led_stripes):
            colors_formatted = [COLORS[c] for c in colors]
            string_color = "".join(map(str, colors_formatted))
            res = "{}{}{}{}".format(commande, animation, index, string_color)
            self.message_to_slaves.append((str(ARDUINO_LED_STRIPS_ID), res))

    def notify_led_buttons(self):
        """Build the messages to set the buttons colors."""
        commande = "2"
        for index, arduino_id in enumerate(ARDUINOS_CONNECTED_TO_PANELS):
            colors = self.led_buttons[index]
            colors_formatted = [COLORS[c] for c in colors]
            string_color = "".join(map(str, colors_formatted))
            res = "{}{}".format(commande, string_color)
            self.message_to_slaves.append((str(arduino_id), res))

    def notify_swag_buttons(self):
        """Build the message to set the swag buttons colors."""
        commande = "3"
        for index, arduino_id in enumerate(ARDUINOS_CONNECTED_TO_PANELS):
            on_off = self.swag_button_light[index]
            on_off_formatted = int(on_off)
            res = "{}{}".format(commande, on_off_formatted)
            self.message_to_slaves.append((str(arduino_id), res))

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
