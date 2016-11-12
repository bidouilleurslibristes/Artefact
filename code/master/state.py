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
    def __init__(self):
        self.led_stripes = [
            ["noir" for i in range(32)],
            ["noir" for i in range(32)],
            ["noir" for i in range(32)],
            ["noir" for i in range(32)],
            ["noir" for i in range(32)],
            ["noir" for i in range(32)],
            ["noir" for i in range(32)],
            ["noir" for i in range(32)],
        ]

        self.led_buttons = [
            ["noir" for i in range(8)],
            ["noir" for i in range(8)],
            ["noir" for i in range(8)],
            ["noir" for i in range(8)],
            ["noir" for i in range(8)],
            ["noir" for i in range(8)],
            ["noir" for i in range(8)],
            ["noir" for i in range(8)],
        ]

        self.pushed_buttons = [
            [False for _ in range(8)],
            [False for _ in range(8)],
            [False for _ in range(8)],
            [False for _ in range(8)],
            [False for _ in range(8)],
            [False for _ in range(8)],
            [False for _ in range(8)],
            [False for _ in range(8)],
        ]

        self.swag_button_pushed = [
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
        ]

        self.swag_button_light = [
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
        ]

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
        """Send the current state to the slaves to inform the arduino."""
        pass

    def __repr__(self):
        import ipdb; ipdb.set_trace()
        res = ""
        res += "Led strips"
        for strip in self.led_stripes:
            res += "  * \n".join(strip)

        res += "\n\n"
        res += "Swag Buttons"
        for light in self.swag_button_light:
            res += "  * \n".join(light)

        return res