# config model
import json
import os

# config path: %LOCALAPPDATA%\\ClipTranslate
CONFIG_DIR = os.path.join(os.getenv("LOCALAPPDATA"), "ClipTranslator")
CONFIG = os.path.join(CONFIG_DIR, "config.json")


def GetConfig() -> dict:

    # If config dir did not exists
    if os.path.exists(CONFIG_DIR) == False:
        os.makedirs(CONFIG_DIR)
        raise Exception("第一次使用请访问'/admin'填入百度翻译id")

    # If config file did not exists
    if os.path.exists(CONFIG) == False:
        os.open(CONFIG, os.O_CREAT)
        raise ValueError("配置文件错误")

    # read file content
    with open(CONFIG, 'r') as fc:
        content = json.load(fc)

    # validate config file
    if content.get("AppID") == None or content.get("secret") == None:
        raise ValueError("配置文件错误")

    return content


def ModifyConfig(content: dict):
    with open(CONFIG, 'w') as fc:
        json.dump(content, fc)
