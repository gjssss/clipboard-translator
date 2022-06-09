from flask import Flask, render_template, request
from datetime import datetime
from pynput import keyboard
from hashlib import md5
from socket import socket, AF_INET, SOCK_DGRAM
from wsgiref.simple_server import make_server

import config as appConfig
import pyperclip
import requests
import json

# flask application instance
app = Flask(__name__)

ConfigInfo = None
first_keydown = None
clip = 'translate'
lastTranslateClip = ''
lastTranslate = {}
salt = '1435660288'


# after release key
def on_release(key):
    # when `ctrl + c` released, key.vk == 67.
    # but some key, such as `a`, dont has vk property.
    v = 0
    try:
        v = key.vk
    except:
        v = v

    if v == 67:

        # calculate the delta time for ensuring user has released `ctrl c` twice in a short time!
        global first_keydown
        if first_keydown:
            delta = datetime.now() - first_keydown

            if delta.seconds < 1 and delta.microseconds < 800000:  # 0.8s

                # clear last keydown time
                first_keydown = None

                #clip is used to save the clipboard content
                global clip
                clip = pyperclip.paste()
                print(clip)
            else:

                # else reflash last keydown time
                first_keydown = datetime.now()
        else:

            # else reflash last keydown time
            first_keydown = datetime.now()


# listening thread
def listen_keyboard():
    listener = keyboard.Listener(on_release=on_release)
    listener.start()


def getSign(content):
    raw = ConfigInfo['AppID'] + content + salt + ConfigInfo['secret']
    return md5(raw.encode(encoding='UTF-8')).hexdigest()


# URL: 'localhost' return a website
@app.route("/")
def index():
    return render_template("baidu.html", Config=ConfigInfo)


# URL: 'localhost/clip' return `translated info`
# To proxy baidu translate api
@app.route('/translate/')
def translateClip():
    global lastTranslate
    global lastTranslateClip

    # if clip content is same with last content which is translated
    if lastTranslateClip == clip:
        return lastTranslate
    try:
        data = {
            'q': clip,
            'from': "auto",
            'to': "zh",
            'appid': ConfigInfo['AppID'],
            'salt': salt,
            'sign': getSign(clip)
        }
        result = requests.get(
            'https://fanyi-api.baidu.com/api/trans/vip/translate', params=data, timeout=5)
        result = json.loads(result.text)

        # flush buffer
        lastTranslate = result
        lastTranslateClip = clip
    except:
        result = {}
    return result


# URL: 'localhost' return a website
@app.route("/admin/", methods=['GET', 'POST'])
def admin():
    global ConfigInfo
    input = request.form.to_dict()
    if input != {}:
        appConfig.ModifyConfig(input)
        ConfigInfo = input
    return render_template("admin.html", Config=ConfigInfo)


# In main thread
if __name__ == "__main__":

    try:
        ConfigInfo = appConfig.GetConfig()
    except ValueError as e:
        print(e.args)
    except Exception as e:
        print(e.args)
        exit(-1)

    # starting listening thread
    listen_keyboard()

    # get ip address
    with socket(AF_INET, SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        print('手机浏览器输入 http://' + s.getsockname()[0] + ':5000 来连接翻译')

    # starting flask application, listening HTTP request
    # app.run(host='0.0.0.0')
    server = make_server('0.0.0.0', 5000, app)
    server.serve_forever()
