import dataclasses
from enum import Enum, StrEnum, auto

# デバイスに関する情報の型を定義する
# 詳細は SwitchBot API のドキュメントを参照
# https://github.com/OpenWonderLabs/SwitchBotAPI?tab=readme-ov-file#devices

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


class CurtainOpenDirection(StrEnum):
    """SwitchBot カーテンの開く方向を示す列挙型
    """
    LEFT = auto()
    RIGHT = auto()


@dataclasses.dataclass
class BaseDevice:
    """SwitchBot で扱うデバイス・リモコンの基底クラス

    Attributes:
        deviceId(str): デバイス ID
        deviceName(str): デバイス名
        hubDeviceId(str): ハブデバイス ID
    """
    deviceId: str
    deviceName: str
    hubDeviceId: str


@dataclasses.dataclass
class Device(BaseDevice):
    """SwitchBot のデバイスを表すクラス

    Attributes:
        deviceType(DeviceType): デバイスのタイプを表す
        enableCloudService(bool): クラウドサービスと連携可能か
    """
    deviceType: DeviceType
    enableCloudService: bool


@dataclasses.dataclass
class CurtainDevice(Device):
    """SwitchBot のカーテンを表すクラス

    ベースのデバイス情報に加えて属性が追加されている

    Attributes:
        deviceType(DeviceType): CURTAIN 固定
        curtainDevicesIds(list[str]): カーテンデバイスの ID リスト
        calibrate(bool): デバイスの開位置と閉位置が適切に調整されているかどうか
        group(bool): グループ化されているかどうか
        master(bool): マスターかどうか
        openDirection(CurtainOpenDirection): カーテンが開く方向
    """
    deviceType = DeviceType.CURTAIN
    curtainDevicesIds: list[str]
    calibrate: bool
    group: bool
    master: bool
    openDirection: CurtainOpenDirection


@dataclasses.dataclass
class InfraredRemote:
    """SwitchBot に登録した赤外線リモコンを表すクラス

    Attributes:
        remoteType(RemoteType): リモコンタイプ
    """
    remoteType: RemoteType
