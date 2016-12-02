from flask import Flask, jsonify
import threading

app = Flask(__name__)
_thread = None
state = None


@app.route('/')
def index():
    return str(state)


def run_flask():
    app.user_reloader = False
    app.run(port=8080)


def run_threaded():
    global _thread
    _thread = threading.Thread(target=run_flask)
    _thread.start()


if __name__ == '__main__':
    run_threaded()
