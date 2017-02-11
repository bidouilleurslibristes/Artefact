BUTTON_PRESSED = "DOWN"

class Button():
    def __init__(self, panel_id, button_id, status=None):
        self.panel = int(panel_id)
        self.button = int(button_id)
        self.status = status

    def __hash__(self):
        return int(self.panel*9 + self.button)

    def __eq__(self, other):
        return (self.panel == other.panel) and (self.button == other.button)

    def __neq__(self, other):
        return not(self == other)

    def __repr__(self):
        return "Button object - panel: {} button: {} status: {}".format(self.panel, self.button, self.status)
        