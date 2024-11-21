from logging import getLogger, config
from dotenv import load_dotenv
import os
from os.path import join, dirname
from datetime import datetime
from zoneinfo import ZoneInfo

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
GOOGLE_APPLICATION_CREDENTIALS_JSON_FILE_NAME = os.environ.get(
    "GOOGLE_APPLICATION_CREDENTIALS_JSON_FILE_NAME"
)

GOOGLE_CREDENTIAL_FILE_PATH = (
    f"{APP_HOME}/{GOOGLE_APPLICATION_CREDENTIALS_JSON_FILE_NAME}"
)

SHEET_NAME = "SwitchBotデバイス一覧"

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
    # response = requests.get("https://api.switch-bot.com/v1.1/devices/C1163DE60941/status", headers=header)

    devices = response.json()
    logger.debug(devices)

    gspreadsheet = getGoogleSpreadSheet(
        spread_sheet_id=GSPREAD_SHEET_KEY,
        credential_file_path=GOOGLE_CREDENTIAL_FILE_PATH,
    )
    print(gspreadsheet.sheet1.get_all_values())
    ws = gspreadsheet.worksheet(SHEET_NAME)

    now = datetime.now(ZoneInfo("Asia/Tokyo"))

    ws.update_acell("B1", now.strftime("%Y/%m/%d %H:%M:%S"))
    device_list = [info for info in devices["body"]["deviceList"]]
    logger.info(device_list)
    device_info_list = [
        [
            device["deviceId"],
            device["deviceName"],
            device["hubDeviceId"],
            device["deviceType"],
        ]
        for device in [info for info in devices["body"]["deviceList"]]
    ]

    logger.info(device_info_list)
    ws.batch_clear(['A3:D'])
    for device_info in device_info_list:
        ws.append_row(device_info)

    logger.info("Finished")


if __name__ == "__main__":
    main()
