"""Modelisation for the game"""

led_stripes = [
    "".join([str(i % 8) for i in range(32)]),
    "".join([str((i + 1) % 8) for i in range(32)]),
    "".join([str((i + 2) % 8) for i in range(32)]),
    "".join([str((i + 3) % 8) for i in range(32)]),
    "".join([str((i + 4) % 8) for i in range(32)]),
    "".join([str((i + 5) % 8) for i in range(32)]),
    "".join([str((i + 6) % 8) for i in range(32)]),
    "".join([str((i + 7) % 8) for i in range(32)]),
]

led_buttons = [
    "".join([str(i % 8) for i in range(8)]),
    "".join([str((i + 1) % 8) for i in range(8)]),
    "".join([str((i + 2) % 8) for i in range(8)]),
    "".join([str((i + 3) % 8) for i in range(8)]),
    "".join([str((i + 4) % 8) for i in range(8)]),
    "".join([str((i + 5) % 8) for i in range(8)]),
    "".join([str((i + 6) % 8) for i in range(8)]),
    "".join([str((i + 7) % 8) for i in range(8)]),
]

pushed_buttons = [
    [False for _ in range(8)],
    [False for _ in range(8)],
    [False for _ in range(8)],
    [False for _ in range(8)],
    [False for _ in range(8)],
    [False for _ in range(8)],
    [False for _ in range(8)],
    [False for _ in range(8)],
]

swag_button_pushed = [
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
]

swag_button_ligth = [
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
]