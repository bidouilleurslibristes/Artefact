"""Main de test."""

import sys
import os
import time
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

try:
    os.mkdir("./game_log")
except FileExistsError:
    pass


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
        nb_logs_in_dir = len(os.listdir("./game_log"))
        game_log_file = "./game_log/{}.log".format(nb_logs_in_dir)
        with open(game_log_file, "w") as f:
            device.log_file = f
            game_loop(device, enigmas, f)

    if not real:
        # device.webserver.shutdown_server()
        device.webserver._thread.join()

def game_loop(device, enigmas, log_file):
    log_file.write("{}\t{}\n".format(time.time(), "new game"))
    print("gamelog : new game")

    for enigma in enigmas:
        dup = deepcopy(enigma)
        log_file.write("{}\t{}\n".format(time.time(), "new enigma"))
        print("gamelog : new enigma")

        device.set_enigma(dup)
        while not device.solve_enigma():
            # On reboot
            if device.reboot:
                device.reboot = False
                log_file.write("{}\t{}\n".format(time.time(), "reboot"))
                print("gamelog : new enigma")
                return
            log_file.flush()
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
