import pytest

from iolink_utils.octetDecoder._octetDecoderBase import OctetDecoderBase, ctypes
from iolink_utils.exceptions import InvalidOctetValue


def test_octetDecoder_octetDecoderBase():
    class MyOctet(OctetDecoderBase):
        _fields_ = [
            ("field_1", ctypes.c_uint8, 1),
            ("field_2", ctypes.c_uint8, 2),
            ("field_3", ctypes.c_uint8, 5)
        ]

    myOctet = MyOctet()
    assert myOctet.field_1 == 0
    assert myOctet.field_2 == 0
    assert myOctet.field_3 == 0

    myOctet = MyOctet(0b10011111)
    assert myOctet.field_1 == 0b1
    assert myOctet.field_2 == 0
    assert myOctet.field_3 == 0b11111

    assert myOctet.get() == 0b10011111
    assert int(myOctet) == 0b10011111

    myOctet.set(0b01101010)
    assert myOctet.field_1 == 0
    assert myOctet.field_2 == 0b11
    assert myOctet.field_3 == 0b01010

    assert int(myOctet) == 0b01101010


def test_octetDecoder_octetDecoderBase_invalidValue():
    class MyOctet(OctetDecoderBase):
        _fields_ = [
            ("field_1", ctypes.c_uint8, 4),
            ("field_2", ctypes.c_uint8, 4)
        ]

    with pytest.raises(InvalidOctetValue):
        MyOctet(1000)

    myOctet = MyOctet(0xFF)
    with pytest.raises(InvalidOctetValue):
        myOctet.set(2000)
