"""Modelisation for the game"""


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


class State():
    """Plop."""
    def __init__(self, message_to_slaves):
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
        self.led_stripes[number] = [color for i in range(32)]

    def notify_slaves(self):
        """Put the current state to the slaves in the message_to_slaves inbox."""
        self.notify_led_strip()
        self.notify_led_buttons()
        self.notify_swag_buttons()

    def notify_led_strip(self):
        commande = "1"
        animation = "A"
        for index, arduino_id in enumerate(range(8, 16)):
            colors = self.led_stripes[index]
            colors_formatted = [COLORS[c] for c in colors]
            string_color = "".join(map(str, colors_formatted))
            res = "{}{}{}".format(commande, animation, string_color)
            self.message_to_slaves.append((str(arduino_id), res))

    def notify_led_buttons(self):
        commande = "2"
        for index, arduino_id in enumerate(range(0, 8)):
            colors = self.led_buttons[index]
            colors_formatted = [COLORS[c] for c in colors]
            string_color = "".join(map(str, colors_formatted))
            res = "{}{}".format(commande, string_color)
            #self.message_to_slaves.append(("led button", str(arduino_id), res))
            self.message_to_slaves.append(("0", res))

    def notify_swag_buttons(self):
        commande = "3"
        for index, arduino_id in enumerate(range(0, 8)):
            on_off = self.swag_button_light[index]
            on_off_formatted = int(on_off)
            res = "{}{}".format(commande, on_off_formatted)
            self.message_to_slaves.append((str(arduino_id), res))

    def __repr__(self):
        res = ""
        res += "Led strips"
        for strip in self.led_stripes:
            res += "  * \n".join(strip)

        res += "\n\n"
        res += "Swag Buttons"
        for light in self.swag_button_light:
            res += "  * \n".join(light)

        return res
