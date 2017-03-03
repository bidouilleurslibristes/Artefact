

class Button():

    BUTTON_DOWN = "DOWN"
    BUTTON_UP = "UP"
    DEFAULT_STATE = "noir"

    def __init__(self, panel_id, button_id, status=BUTTON_UP, state=DEFAULT_STATE):
        """
         panel_id : id du panneau
         button : id du bouton
         status : appuyé ou éteind
         state : état (couleur / effet lumineux)
        """
        self.panel = int(panel_id)
        self.button = int(button_id)
        self.status = status
        self.state = state

    def __hash__(self):
        return int(self.panel * 9 + self.button)

    def __eq__(self, other):
        return (self.panel == other.panel) and (self.button == other.button)

    def __neq__(self, other):
        return not(self == other)

    def __repr__(self):
        return "Button object - panel: {} button: {} status: {}".format(self.panel, self.button, self.status)
