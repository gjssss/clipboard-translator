# Clip Translator
## Getting Start

*Command to use python virtual environment*

* First, Open terminal in code folder and setup python virtual environment

  ```bash
  python -m venv venv
  ```

* Second, install requirements

  ```bash
  pip install -r requirements.txt
  ```

* Finally, Run the `baidu.py`

  ```bash
  venv\Scripts\python.exe baidu.py
  ```

  or click the `start.bat` file

## Usage

***Please set you config first!***

Make sure the your computer and mobile phone are under the **same LAN**, It means they are under the **same WIFI**.

Open the address which is shown on terminal (such as 192.168.0.101), in your phone browser and enjoy it!

You can select text and use <kbd>Ctrl</kbd><kbd>c</kbd> twice in a shot time. The translated text while shown on your phone!

## Config

In the first time, you should open `http://localhost:5000/admin` in your browser and set your AppID and Secret.

The config file `config.json` is at the path of `%LOCALAPPDATA%/ClipTranslator/config.json`, you can use

```bash
echo %LOCALAPPDATA%/ClipTranslator/config.json
```

to find the path

You need to restart program to apply your config. (💀It is a bug, I will fix it later💀)

## Getting AppID

You can follow the document <a href="https://api.fanyi.baidu.com/doc/13">百度翻译开放平台</a> setup your app for free

You can get the `AppID` and `Secret` at the bottom of the page <a href="https://api.fanyi.baidu.com/api/trans/product/desktop">百度翻译管理控制台</a>
