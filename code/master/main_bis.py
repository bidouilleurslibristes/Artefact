"""Main de test."""

from hardware.debug import Device as DebugDevice
from hardware.real import Device as RealDevice

from enigma import SimonEnigma, SwagEnigma


def main(real=False):
    """main de test."""
    if real:
        device = RealDevice()
    else:
        device = DebugDevice()

    se = SwagEnigma(device)  # SimonEnigma(device, 4, 3)

    if not real:
        device.webserver.button_trigger = se.update_from_devices
        device.webserver._thread.join()


if __name__ == "__main__":
    print("===============================================")
    print("====== launching simulated device =============")
    main(real=False)
