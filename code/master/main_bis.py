"""Main de test."""

import sys

from hardware.debug import Device as DebugDevice
from hardware.real import Device as RealDevice

from enigma import SwagEnigma, Enigma, ButtonEnigma
import time


class Game:

    @classmethod
    def parse_enigma(cls, f):
        sub_enigmas = []
        for line in f:
            line = line.strip()
            if not line:
                e = Enigma()
                [e.add_sub_enigma(se) for se in sub_enigmas]
                return e

            if line.startswith("swag"):
                sub_enigmas.append(SwagEnigma(line))

            if line.startswith("button"):
                sub_enigmas.append(ButtonEnigma(line))

    @classmethod
    def load_from_file(self, fname):
        enigmas = []
        with open(fname) as f:
            for line in f:
                line = line.strip()
                if line.startswith("#"):
                    enigmas.append(self.parse_enigma(f))
        return enigmas


def main(real=False):
    """main de test."""
    if real:
        device = RealDevice()
    else:
        device = DebugDevice()

    # Test création d'une énigme simple
    # message = "swag 3 xxx..x.."
    # se = SwagEnigma(message)  # SimonEnigma(device, 4, 3)
    # e = Enigma()
    # e.add_sub_enigma(se)
    # device.set_enigma(e)

    enigmas = Game.load_from_file(sys.argv[1])
    for enigma in enigmas:
        if enigma:  # a virer
            device.set_enigma(enigma)
            device.solve_enigma()
            time.sleep(3)

    if not real:
        # device.webserver.shutdown_server()
        device.webserver._thread.join()


if __name__ == "__main__":
    print("===============================================")
    print("====== launching simulated device =============")
    main(real=False)
