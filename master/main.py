"""Main de test."""

import sys
import logging

from hardware.debug import Device as DebugDevice
from hardware.real import Device as RealDevice

from enigma import *
from copy import deepcopy
import time


logger = logging.getLogger('root')
FORMAT = (
    '[%(asctime)s :: %(levelname)s '
    '%(filename)s:%(lineno)s - %(funcName)10s() ]'
    ' :: %(message)s'
)

logging.basicConfig(format=FORMAT)
#setup_logging(handler)
logger.setLevel(logging.CRITICAL)


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

            if line.startswith("swagLittle"):
                sub_enigmas.append(SwagLittleEnigma(line))

            elif line.startswith("swag"):
                sub_enigmas.append(SwagEnigma(line))

            elif line.startswith("button"):
                sub_enigmas.append(ButtonEnigma(line))

            elif line.startswith("little"):
                sub_enigmas.append(LittleEnigma(line))

            elif line.startswith("dark"):
                sub_enigmas.append(DarkEnigma(line))

            elif line.startswith("sequence"):
                sub_enigmas.append(SequenceEnigma(line))


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
        print("====== launching real device =============")
        device = RealDevice()
    else:
        print("====== launching simulated device =============")
        device = DebugDevice()

    enigmas = Game.load_from_file(sys.argv[1])
    while True:
        game_loop(device, enigmas)

    if not real:
        # device.webserver.shutdown_server()
        device.webserver._thread.join()

def game_loop (device, enigmas):
    print("Start game loop")

    for enigma in enigmas:
        dup = deepcopy(enigma)
        device.set_enigma(dup)
        while not device.solve_enigma():
            # On reboot
            if device.reboot:
                device.reboot = False
                return

            # On error set colors
            device.send_state()
            time.sleep(3)

            # Reinit the current enigma
            dup = deepcopy(enigma)
            device.set_enigma(dup)
    device.send_win_animation()
    time.sleep(30)

if __name__ == "__main__":
    print("===============================================")
    main(real=True)
