from state import State


class AbstractDevice:
    """Interface to a device."""

    def __init__(self):
        """Initialisation."""
        self.state = State()
        print("device init")

    def send_state(self):
        """Send the state to the hardware."""
        raise NotImplementedError

    def set_led_strip(self, strip_id, led_id, color):
        """Cache the color of a given led in a given panel to a given color."""
        print("set led {} of strip {} to color {}".format(strip_id, led_id, color))
        self.state.led_stripes[strip_id][led_id] = color

    def set_swag_button(self, panel_id, value):
        """Cache the swag button led state to a given value."""
        print("set swag button of panel {} to {}".format(panel_id, value))
        self.state.swag_button_light[panel_id] = value
