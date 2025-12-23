import pytest

from iolink_utils.exceptions import EnumConversionError
from iolink_utils.definitions.bitRate import BitRate


def test_bitrateFromIntValue():
    bitrate = BitRate(0)
    assert bitrate.name == 'Undefined'
    assert bitrate.value == 0

    bitrate = BitRate(4800)
    assert bitrate.name == 'COM1'
    assert bitrate.value == 4800

    bitrate = BitRate(38400)
    assert bitrate.name == 'COM2'
    assert bitrate.value == 38400

    bitrate = BitRate(230400)
    assert bitrate.name == 'COM3'
    assert bitrate.value == 230400

def test_bitrateFromStringValue():
    bitrate = BitRate('0')
    assert bitrate.name == 'Undefined'
    assert bitrate.value == 0

    bitrate = BitRate('4800')
    assert bitrate.name == 'COM1'
    assert bitrate.value == 4800

    bitrate = BitRate('38400')
    assert bitrate.name == 'COM2'
    assert bitrate.value == 38400

    bitrate = BitRate('230400')
    assert bitrate.name == 'COM3'
    assert bitrate.value == 230400

def test_bitrateFromName():
    bitrate = BitRate('Undefined')
    assert bitrate.name == 'Undefined'
    assert bitrate.value == 0

    bitrate = BitRate('COM1')
    assert bitrate.name == 'COM1'
    assert bitrate.value == 4800

    bitrate = BitRate('COM2')
    assert bitrate.name == 'COM2'
    assert bitrate.value == 38400

    bitrate = BitRate('COM3')
    assert bitrate.name == 'COM3'
    assert bitrate.value == 230400

def test_bitrateErrors():
    with pytest.raises(EnumConversionError):
        BitRate('COM7')
    with pytest.raises(EnumConversionError):
        BitRate('234')
    with pytest.raises(EnumConversionError):
        BitRate(111)
