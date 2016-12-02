"""Main de test."""

from hardware.debug import Device as DebugDevice
from hardware.real import Device as RealDevice

def main_test():
    """main de test."""
    device = DebugDevice()

    strip_id = 1
    led_id = 2
    color = "turquoise"

    panel_id = 4
    swag_button_state = True

    device.set_led_strip(strip_id, led_id, color)
    device.set_swag_button(panel_id, swag_button_state)

    device.send_state()
    device.webserver._thread.join()


def main_real():
    """main de test."""
    device = RealDevice()

    strip_id = 1
    led_id = 2
    color = "turquoise"

    panel_id = 4
    swag_button_state = True

    device.set_led_strip(strip_id, led_id, color)
    device.set_swag_button(panel_id, swag_button_state)

    device.send_state()


if __name__ == "__main__":
    print("=========================")
    print("====== test =============")
    main_test()



    #print("=========================")
    #print("====== real =============")
    #main_real()