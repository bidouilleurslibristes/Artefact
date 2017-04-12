import json
import threading

from flask import Flask, jsonify, render_template, request

from hardware.button import Button

app = Flask(__name__)
_thread = None
state = None
app.config['TEMPLATES_AUTO_RELOAD'] = True
hardware = None

SWAG_BUTTON_ID = 8

BLACK = [80, 80, 80]
WHITE = [230, 230, 230]

COLORS = [
    BLACK,
    [150, 1, 1],
    [1, 150, 2],
    [2, 2, 150],
    [230, 230, 30],
    [150, 00, 170],
    [00, 170, 150],
    [200, 150, 00],
    WHITE,
]


def shutdown_server():
    pass


def format_color(r, g, b):
    return "rgb({},{},{})".format(r, g, b)


def format_colors(colors):
    color_indexes = list(map(state.color_to_index, colors))
    rgb_tuples_colors = list(map(lambda c: COLORS[c], color_indexes))
    rgb_colors = [format_color(r, g, b) for r, g, b in rgb_tuples_colors]
    return rgb_colors


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data')
def send_data():
    strips = []
    for strip_colors in state.led_stripes:
        strips.append(format_colors(strip_colors))

    led_buttons = []
    for panel in state.normal_button_states():
        led_buttons.append(format_colors([button.state for button in panel]))

    tmp_swag = [WHITE if sb.state == "blanc" else BLACK for sb in state.swag_button_states()]
    context = {
        "led_strips_colors": strips,
        "button_colors": led_buttons,
        "swag": [format_color(r, g, b) for (r, g, b) in tmp_swag],
    }
    return jsonify(context)


@app.route('/update_state', methods=["POST"])
def update_state():
    panel_id, button_id = request.form["button"].split("--")
    pressed = json.loads(request.form["pressed"])

    pressed_text = "pressed" if pressed else "released"
    status = Button.BUTTON_DOWN if pressed else Button.BUTTON_UP
    print("{} : {} in panel {}".format(pressed_text, button_id, panel_id))

    color = None
    if "button" in button_id:
        if "swag" in button_id:
            button_id = SWAG_BUTTON_ID
        else:
            button_id = button_id[7]
            color = state.buttons[int(panel_id[6])][int(button_id)].state

    button_changed = Button(panel_id[6], button_id, status, color)
    hardware.log_game("button pushed", button_changed)
    hardware.enigma.button_triggered(button_changed)
    return "ok"


def run_flask():
    app.user_reloader = False
    app.run(port=8080)


def run_threaded():
    global _thread
    _thread = threading.Thread(target=run_flask)
    _thread.start()


if __name__ == '__main__':
    run_threaded()
