from state import State


class AbstractDevice:
    """Interface to a device."""

    def __init__(self):
        """Initialisation."""
        self.state = State()
        print("device init")
        self.SWAG_BUTTON_ID = 8
        self.BUTTON_DOWN_CODE = "DOWN"

    def send_state(self):
        """Send the state to the hardware."""
        raise NotImplementedError

    def set_one_led_in_strip(self, strip_id, led_id, color):
        """Cache the color of a given led in a given panel to a given color."""
        self.state.led_stripes[strip_id][led_id] = color

    def set_all_leds_in_strip(self, strip_id, color):
        self.state.led_stripes[strip_id] = [color for _ in self.state.led_stripes[strip_id]]

    def set_swag_button(self, panel_id, value):
        """Cache the swag button led state to a given value."""
        self.state.swag_button_light[panel_id] = value

    def set_button_trigger(self, callback_update_button):
        """Trigger the state update after a change in button."""
        raise NotImplementedError

    def set_one_led_in_panel(self, panel_id, led_id, color):
        self.state.led_buttons[panel_id][led_id] = color

    def set_all_led_strips(self, color):
        """Set all led strips to a given color."""
        self.state.led_stripes = [
            [color for i in range(32)],
            [color for i in range(32)],
            [color for i in range(32)],
            [color for i in range(32)],
            [color for i in range(32)],
            [color for i in range(32)],
            [color for i in range(32)],
            [color for i in range(32)],
        ]

    def set_all_swag_buttons(self, status):
        """Set all swag buttons to the same status (True or False)."""
        self.state.swag_button_light = \
            [status for _ in range(len(self.state.swag_button_light))]
