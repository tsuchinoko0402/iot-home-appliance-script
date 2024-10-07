import dataclasses
import time
import base64
import hashlib
import hmac
from typing import Any
import uuid

@dataclasses.dataclass(frozen=True)
class SwitchBotApiHeader:
    """Switch Bot API v1.1 を叩く際に付ける HTTP リクエストヘッダー

    API を利用する際に必要な認証情報については API の公式ドキュメントを参照
    https://github.com/OpenWonderLabs/SwitchBotAPI?tab=readme-ov-file#authentication
    """
    authorization: str
    secret: str
    contentType: str = 'application/json'
    charset: str = 'utf-8'
    t: int = int(round(time.time() * 1000))
    sign: bytes = b''
    nonce: str = str(uuid.uuid4())

    def __post_init__(self):
        string_to_sign = f"{self.authorization}{self.t}{self.nonce}"
        string_to_sign = bytes(string_to_sign, "utf-8")
        secret_byte = bytes(self.secret, "utf-8")
        object.__setattr__(self, "sign", base64.b64encode(hmac.new(secret_byte, msg=string_to_sign, digestmod=hashlib.sha256).digest()))


def create_api_header(token: str, secret: str) -> dict[str, str]:
    """Switch Bot API v1.1 を叩くのに必要な HTTP リクエストヘッダーを辞書として返却する。
    辞書に変換する際、フィールド名は API ドキュメントで指定されたヘッダー名に変換して返却する。

    トークンとシークレットの取得方法は Switch Bot サポートのページを参照
    https://support.switch-bot.com/hc/ja/articles/12822710195351-%E3%83%88%E3%83%BC%E3%82%AF%E3%83%B3%E3%81%AE%E5%8F%96%E5%BE%97%E6%96%B9%E6%B3%95

    :param token: Switch Bot API の認証に必要なトークン
    :param secret: Switch Bot API の認証に必要なシークレット
    """
    header = SwitchBotApiHeader(authorization=token, secret=secret)
    return dataclasses.asdict(header, dict_factory=__header_dict_factory)


def __header_dict_factory(items: list[tuple[str, Any]]) -> dict[str, Any]:
    """`SwitchBotApiHeader`用の `dict_factory`"""
    adict = {}
    for key, value in items:
        if key == "authorization":
            adict["Authorization"] = value
        elif key == "contentType":
            adict["Content-Type"] = value
        elif key == "charset":
            adict[key] = value
        elif key == "t":
            adict["t"] = str(value)
        elif key == "sign":
            adict[key] = str(value, "utf-8")
        elif key == "nonce":
            adict[key] = value

    return adict
