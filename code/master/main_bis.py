"""Main de test."""

import sys

from hardware.debug import Device as DebugDevice
from hardware.real import Device as RealDevice

from enigma import SwagEnigma, Enigma, ButtonEnigma
from copy import deepcopy
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

    enigmas = Game.load_from_file(sys.argv[1])
    game_loop(device, enigmas)

    if not real:
        # device.webserver.shutdown_server()
        device.webserver._thread.join()

def game_loop (device, enigmas):
    for enigma in enigmas:
        dup = deepcopy(enigma)
        device.set_enigma(dup)
        while not device.solve_enigma():
            device.enigma.set_wrong()
            time.sleep(3)
            dup = deepcopy(enigma)
            device.set_enigma(dup)
        time.sleep(3)


if __name__ == "__main__":
    print("===============================================")
    print("====== launching simulated device =============")
    main(real=False)
