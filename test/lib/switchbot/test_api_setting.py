import time
from app.lib.switchbot.api_setting import create_api_header
import uuid
import pytest


def test_create_api_header_Authorizationヘッダーが正しく設定されること():
    """'Authorization' 以外はランダムに決まるか固定値が返されるだけなので、
    ここでは、渡した token が 'Authorization' の値として返ってくることのみテストする
     """
    token = "test_token"
    secret = "dummy_secret"
    result = create_api_header(token=token, secret=secret)
    expect = token
    assert result["Authorization"] == expect

def test_create_api_header_ヘッダーのキーが正しく設定されること():
    token = "test_token"
    secret = "dummy_secret"
    result = list(create_api_header(token=token, secret=secret).keys())
    expect = ['Authorization', 'Content-Type', 'charset', 't', 'sign', 'nonce']
    assert set(result) == set(expect)