import dataclasses
from enum import Enum

class DeviceType(Enum):
    """SwitchBot のデバイスタイプを表す列挙型
    """
    # モーションセンサー
    MOTION_SENSOR = "Motion Sensor"
    # ハブミニ
    HUB_MINI = "Hub Mini"
    # 温湿度計
    MATER = "Meter"
    # カーテン3
    CURTAIN = "Curtain3"


class RemoteType(Enum):
    """リモコンのタイプを表す列挙型
    """
    # ライト
    LIGHT = "Light"
    # 扇風機
    FAN = "DIY Fan"
    # エアコン
    AIR_CONDITIONER = "Air Conditioner"
    # その他
    OTHERS = "Others"


@dataclasses.dataclass
class BaseDevice:
    """SwitchBot で扱うデバイス・リモコンの基底クラス
    """
    deviceId: str
    deviceName: str
    hubDeviceId: str


@dataclasses.dataclass
class Device(BaseDevice):
    """SwitchBot のデバイスを表すクラス
    """
    deviceType: DeviceType
    enableCloudService: bool

@dataclasses.dataclass
class InfraredRemote:
    """SwitchBot に登録した赤外線リモコンを表すクラス
    """
    remoteType: RemoteType
