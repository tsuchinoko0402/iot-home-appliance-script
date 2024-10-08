import time
from app.lib.switchbot.api_setting import create_api_header
import uuid
import pytest


def test_create_api_header_正しくヘッダーが設定されること():
    """'Authorization' 以外はランダムに決まるか固定値が返されるだけなので、
    ここでは、渡した token が 'Authorization' の値として返ってくることのみテストする
     """
    token = "test_token"
    secret = "dummy_secret"
    result = create_api_header(token=token, secret=secret)
    expect = token
    assert result["Authorization"] == expect
