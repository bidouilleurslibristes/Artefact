from hardware.button import Button, BUTTON_PRESSED


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
            print("BRAVOOOOOOOO")
            enigma = self.buttons_mapping[button]
            enigma.button_trigger(button)
        else :
            print("NUUULLLLLLLLLL mauvais button", button)


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


    def is_solved(self):
        return self.solved

    def get_led_status(self):
        status = []
        for led_status in self.led_strip_status:
            color = "red" if led_status else None
            for _ in range(4):
                status.append(color)
        return status

    def button_trigger(self, button):
        if button.status == BUTTON_PRESSED:
            self.solved = True

    def buttons_of_interest(self):
        return [Button(self.panel_id, self.panel_id)]