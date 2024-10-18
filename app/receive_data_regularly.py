from logging import getLogger, config
from dotenv import load_dotenv
import os
from os.path import join, dirname
import json
from datetime import datetime
from zoneinfo import ZoneInfo

import requests

from lib.switchbot.api_setting import create_api_header
from lib.google_spread_sheet.google_spread_sheet import getGoogleSpreadSheet
from lib.switchbot.api_setting import create_api_header

# 環境変数設定
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

TOKEN = os.environ.get("SWITCHBOT_TOKEN")
SECRET = os.environ.get("SWITCHBOT_SECRET")
GAS_URL = os.environ.get("GAS_URL")
APP_HOME = os.environ.get("APP_HOME")
GSPREAD_SHEET_KEY = os.environ.get("GSPREAD_SHEET_KEY")
GOOGLE_APPLICATION_CREDENTIALS_JSON_FILE_NAME = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON_FILE_NAME")

GOOGLE_CREDENTIAL_FILE_PATH = f"{APP_HOME}/{GOOGLE_APPLICATION_CREDENTIALS_JSON_FILE_NAME}"

DEVICE_ID_ENTRANCE_THERMOMETER = "CA3234352A7A"
DEVICE_ID_LIVING_THERMOMETER = "D13234353F96"

SHEET_NAME_ENTRANCE = "室温（玄関）"
SHEET_NAME_LIVING = "室温（リビング）"

# ロギングの設定
with open(f"{APP_HOME}/log_config.json", "r") as f:
    log_conf = json.load(f)
config.dictConfig(log_conf)
logger = getLogger(__name__)


def __get_meter_info(device_id: str) -> tuple[str, str, str]:
    logger.info("Started")

    header = create_api_header(token=TOKEN, secret=SECRET)
    res = requests.get(
        f"https://api.switch-bot.com/v1.1/devices/{device_id}/status",
        headers=header,
    )
    info = res.json()
    logger.debug(f"info: {info}")

    now = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d %H:%M:%S")
    temp = info["body"]["temperature"]
    hum = info["body"]["humidity"]
    logger.debug(f"id: {device_id}, time: {now}, temp: {temp}, hum: {hum}")
    logger.info("Finished")  

    return (now, temp, hum)


def main():
    logger.info("Started")

    header = create_api_header(token=TOKEN, secret=SECRET)
    logger.debug(header)

    entrance_info = __get_meter_info(DEVICE_ID_ENTRANCE_THERMOMETER)

    gspreadsheet = getGoogleSpreadSheet(spread_sheet_id=GSPREAD_SHEET_KEY, credential_file_path=GOOGLE_CREDENTIAL_FILE_PATH)
    worksheet = gspreadsheet.worksheet(SHEET_NAME_ENTRANCE)
    worksheet.append_row([entrance_info[0], entrance_info[1], entrance_info[2]])
    logger.debug(worksheet.get_all_values())

    logger.info("Finished")


if __name__ == "__main__":
    main()
