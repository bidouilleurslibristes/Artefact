from hardware.button import Button
from state import State

SWAG_BUTTON_ID = 8


class Enigma:
    def __init__(self):
        self.sub_enigmas = []
        self.buttons_mapping = {}

    def add_sub_enigma(self, sub_enigma):
        self.sub_enigmas.append(sub_enigma)
        for button in sub_enigma.buttons_of_interest():
            self.buttons_mapping[button] = sub_enigma

    def is_solved(self):
        return all((se.is_solved() for se in self.sub_enigmas))

    def button_triggered(self, button):
        if button in self.buttons_mapping:
            enigma = self.buttons_mapping[button]
            enigma.button_trigger(button)

    def get_state(self):
        st = State()

        # état initial de tous les bandeaux de leds
        st.init_led_strips()

        # état initial de tous les boutons de tous les panneaux
        st.init_buttons()

        # Valable uniquement car les status ne s'appliquent qu'à un bandeau à chaque fois
        if not self.is_solved():
            for sub in self.sub_enigmas:
                # Récupère le status du bandeau pour la sous énigme
                sub_status = sub.get_led_status()

                # Met à jour le bandeau dans l'objet status
                for i in range(32):
                    if not sub_status[i] is None:
                        st.led_stripes[sub.interest_id][i] = sub_status[i]

                for button in sub.buttons_of_interest():
                    st.buttons[button.panel][button.button].state = button.state

        return st


class SubEnigma:
    def __init__(self):
        pass

    def is_solved(self):
        raise NotImplementedError

    def get_led_status(self):
        """Renvoie un iterable de 32 couleurs, pouvant être None si l'on ne considère pas la led."""
        raise NotImplementedError

    def button_trigger(self, button):
        """
        button : un dictionnaire avec panel_id, button_id, status
        """
        raise NotImplementedError

    def buttons_of_interest(self):
        raise NotImplementedError

    # todo : init buttons
    def __repr__(self):
        return "SubEnigma ({}) : {}".format(self.name, self.led_strip_status)


class SwagEnigma(SubEnigma):
    def __init__(self, message):
        """
        interest_id : the id of the panel / strip to listen to (the red strip, and the ID of the panel to press)
        led_strip_status: iterable of 8 booleans with the leds to consider
        """
        self.name = "Swag Enigma"
        _, interest_id, led_strip_status = message.strip().split()
        led_strip_status = [c == "x" for c in led_strip_status]

        self.interest_id = int(interest_id)
        self.panel_id = interest_id
        self.led_strip_status = led_strip_status
        self.solved = False

        self.button = Button(self.panel_id, SWAG_BUTTON_ID, Button.BUTTON_UP, "blanc")

    def is_solved(self):
        return self.solved

    def get_led_status(self):
        status = []
        for led_status in self.led_strip_status:
            color = "rouge" if (not self.solved) and led_status else None
            for _ in range(4):
                status.append(color)
        return status

    def button_trigger(self, button):
        if button.status == Button.BUTTON_DOWN:
            self.solved = True

    def buttons_of_interest(self):
        return [self.button]


class ButtonEnigma(SubEnigma):

    def __init__(self, message):
        self.name = "Button"
        _, panel_id, button_statuses = message.strip().split()
        self.panel_id = panel_id
        self.buttons = []

        self.colors = {
            "r" : "rouge",
            "l" : "bleu",
            "j" : "jaune",
            "m" : "mauve",
            "o" : "orange",
            "v" : "vert",
            "t" : "turquoise",
            "b" : "blanc",
            "n" : "noir"
        }

        for index, char in enumerate(button_statuses[:-1]):
            if char != ".":
                self.buttons.append(Button(self.panel_id, index, Button.BUTTON_UP, self.colors[char]))

        if button_statuses[-1] == "T":
            self.buttons.append(Button(self.panel_id, SWAG_BUTTON_ID, Button.BUTTON_UP, "blanc"))

    def is_solved(self):
        return True

    def get_led_status(self):
        return [None] * 32

    def button_trigger(self, button):
        pass

    def buttons_of_interest(self):
        return self.buttons