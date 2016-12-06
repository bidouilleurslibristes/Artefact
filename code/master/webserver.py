from flask import Flask, jsonify, render_template, request
import threading

app = Flask(__name__)
_thread = None
state = None
app.config['TEMPLATES_AUTO_RELOAD'] = True


COLORS = [
    [80, 80, 80],
    [150, 1, 1],
    [1, 150, 2],
    [2, 2, 150],
    [230, 230, 30],
    [150, 00, 170],
    [00, 170, 150],
    [200, 150, 00],
    [230, 230, 230]
]


def format_colors(colors):
    color_indexes = list(map(state.color_to_index, colors))
    rgb_tuples_colors = list(map(lambda c: COLORS[c], color_indexes))
    rgb_colors = ["rgb({},{},{})".format(r, g, b) for r, g, b in rgb_tuples_colors]
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
    for button_colors in state.led_buttons:
        led_buttons.append(format_colors(button_colors))

    context = {
        "led_strips_colors": strips,
        "button_colors": led_buttons,
        "swag": state.swag_button_light,
    }
    return jsonify(context)


@app.route('/update_state', methods=["POST"])
def update_state():
    panel_id, button_id = request.form["button"].split("--")
    print("pushed : {} in panel {}".format(button_id, panel_id))
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
