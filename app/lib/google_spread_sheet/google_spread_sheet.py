from gspread import Client
from gspread.auth import authorize
from gspread.spreadsheet import Spreadsheet
from google.oauth2 import service_account


def getGoogleSpreadSheet(spread_sheet_id: str, credential_file_path: str) -> Spreadsheet:
    """スプレッドシートを扱うためのオブジェクトを取得する

    Args:
        spread_sheet_id(str): 操作したいスプレッドシートの ID
        credential_file_path(str): 事前に取得した Google サービスアカウントのクレデンシャルキーファイルのパス
    """
    client = __get_gspread_client(credential_file_path=credential_file_path)
    spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{spread_sheet_id}"
    return client.open_by_url(spreadsheet_url)


def __get_gspread_client(credential_file_path: str) -> Client:
    """Google スプレッドシートのクライアントを取得する

    スコープはスプレッドシートを扱うためのもので決めうちにする

    Args:
        credential_file_path(str): 事前に取得した Google サービスアカウントのクレデンシャルキーファイルのパス
    """
    scopes = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_file(credential_file_path, scopes=scopes)

    return authorize(credentials)