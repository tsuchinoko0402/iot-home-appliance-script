from logging import getLogger, config
from dotenv import load_dotenv
import os
from os.path import join, dirname
import json

import requests

from lib.google_spread_sheet.google_spread_sheet import getGoogleSpreadSheet
from lib.switchbot.api_setting import create_api_header

# 環境変数設定
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

TOKEN = os.environ.get("SWITCHBOT_TOKEN")
SECRET = os.environ.get("SWITCHBOT_SECRET")
APP_HOME = os.environ.get("APP_HOME")
GSPREAD_SHEET_KEY = os.environ.get("GSPREAD_SHEET_KEY")
GOOGLE_APPLICATION_CREDENTIALS_JSON_FILE_NAME = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON_FILE_NAME")

GOOGLE_CREDENTIAL_FILE_PATH = f"{APP_HOME}/{GOOGLE_APPLICATION_CREDENTIALS_JSON_FILE_NAME}"

# ロギングの設定
with open(f"{APP_HOME}/log_config.json", "r") as f:
    log_conf = json.load(f)
config.dictConfig(log_conf)
logger = getLogger(__name__)


def main():
    logger.info("Started")

    header = create_api_header(token=TOKEN, secret=SECRET)
    logger.debug(header)

    response = requests.get("https://api.switch-bot.com/v1.1/devices", headers=header)
    devices = response.json()
    logger.debug(devices)

    gspreadsheet = getGoogleSpreadSheet(spread_sheet_id=GSPREAD_SHEET_KEY, credential_file_path=GOOGLE_CREDENTIAL_FILE_PATH)
    print(gspreadsheet.sheet1.get_all_values())

    logger.info("Finished")


if __name__ == "__main__":
    main()
