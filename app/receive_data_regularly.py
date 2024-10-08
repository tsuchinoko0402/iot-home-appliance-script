from logging import getLogger, config
from dotenv import load_dotenv
import os
from os.path import join, dirname
import json

import requests

from lib.switchbot.api_setting import create_api_header

# 環境変数設定
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN = os.environ.get("SWITCHBOT_TOKEN")
SECRET = os.environ.get("SWITCHBOT_SECRET")
GAS_URL = os.environ.get("GAS_URL")
APP_HOME = os.environ.get("APP_HOME")

# ロギングの設定
with open(f'{APP_HOME}/log_config.json', 'r') as f:
    log_conf = json.load(f)
config.dictConfig(log_conf)
logger = getLogger(__name__)


def main():
    logger.info('Started')
    
    header = create_api_header(token=TOKEN, secret=SECRET)
    logger.debug(header)

    # response = requests.get("https://api.switch-bot.com/v1.1/devices", headers=header)
    # devices = response.json()
    # logger.debug(devices)

    response = requests.get(
        f"https://api.switch-bot.com/v1.1/devices/CA3234352A7A/status",
        headers=header,
    )
    devices = response.json()
    logger.debug(devices)
    temp = devices["body"]["temperature"]
    hum = devices["body"]["humidity"]

    url = f"{GAS_URL}?t={temp}&h={hum}"
    response = requests.get(url)
    logger.debug(response)

    logger.info('Finished')


if __name__ == '__main__':
    main()

