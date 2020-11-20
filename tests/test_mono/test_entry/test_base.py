from datetime import datetime

from dlparse.mono.asset.base import MasterEntryBase


def test_parse_datetime():
    assert MasterEntryBase.parse_datetime("2020/07/28 05:59:59") == datetime(2020, 7, 28, 5, 59, 59)
    assert MasterEntryBase.parse_datetime("2020/07/28 06:00:00") == datetime(2020, 7, 28, 6)
