"""Hardware debug interface.

These is used to simulate the hardware (in a browser for instance).
"""

from copy import deepcopy

from hardware.abstract import AbstractDevice

import webserver


class Device(AbstractDevice):
    """Interface to a device."""

    def __init__(self):
        """Initialisation."""
        super(Device, self).__init__()

        print("device init")
        self.webserver = webserver
        self.webserver.run_threaded()
        self.send_state()

    def send_state(self):
        """Send the state to the hardware."""
        self.webserver.state = deepcopy(self.state)
