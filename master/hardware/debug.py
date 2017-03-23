"""Hardware debug interface.

These is used to simulate the hardware (in a browser for instance).
"""

from copy import deepcopy

from hardware.abstract import AbstractDevice

import webserver
import time


class Device(AbstractDevice):
    """Interface to a device."""

    def __init__(self):
        """Initialisation."""
        super(Device, self).__init__()

        self.webserver = webserver
        self.webserver.run_threaded()
        self.webserver.hardware = self

    def send_state(self):
        """Send the state to the hardware."""
        if self.enigma:
            self.webserver.state = self.enigma.get_state()

    def wait_for_event(self):
        time.sleep(0.1)
        self.send_state()
