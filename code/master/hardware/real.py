"""Real hardware interface.

These is used to control the physical hardware.
"""

from hardware.abstract import AbstractDevice


from state import State
from network import MasterNetwork


class Device(AbstractDevice):
    """Interface to a device."""

    def __init__(self):
        """Initialisation."""
        super(Device, self).__init__()

        self.network = MasterNetwork()
        self.state = State()
        self.send_state()
        print("device init")

    def send_state(self):
        """Send the state to the hardware."""
        messages = self.state.notify_slaves()
        print(messages)
        for message in messages:
            self.network.messages_to_slaves.append(message)
