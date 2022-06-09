from pynput import keyboard
import pyperclip
from flask import Flask, render_template
from flask_cors import CORS
import requests
from json import loads
from datetime import datetime

app = Flask(__name__)
CORS(app, supports_credentials=True)

first_keydown = None
clip = {}


def on_release(key):
    v = 0
    try:
        v = key.vk
    except:
        v = v

    if v == 67:
        global first_keydown
        if first_keydown:
            delta = datetime.now() - first_keydown
            if delta.seconds < 1 and delta.microseconds < 800000:
                first_keydown = None
                global clip
                str = pyperclip.paste()
                try:
                    r = requests.get('http://fanyi.youdao.com/translate',
                                     params={
                                         'doctype': 'json',
                                         'type': 'AUTO',
                                         'i': str
                                     })
                    clip = loads(r.text)['translateResult'][0][0]
                except:
                    print('err')
            else:
                first_keydown = datetime.now()
        else:
            first_keydown = datetime.now()


def listen_keyboard():
    listener = keyboard.Listener(on_release=on_release)
    listener.start()


@app.route('/clip/')
def getClip():
    return clip


@app.route("/")
def index():
    return render_template("youdao.html")


if __name__ == "__main__":
    listen_keyboard()
    app.run(host='0.0.0.0')
