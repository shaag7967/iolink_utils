import pytest

from iolink_utils.utils.calculateProcessDataLength import calculateProcessDataLength
from iolink_utils.octetDecoder.octetDecoder import ProcessDataIn, ProcessDataOut
from iolink_utils.exceptions import InvalidLengthInProcessDataParameter


@pytest.mark.parametrize("cls", [ProcessDataIn, ProcessDataOut])
def test_calculateProcessDataLength_zero(cls):
    octet = cls()
    assert octet.byte == 0
    assert octet.length == 0
    assert calculateProcessDataLength(octet) == 0


@pytest.mark.parametrize(
    "length, expected",
    [
        (0, 0),
        (1, 1),
        (7, 1),
        (8, 1),
        (9, 2),
        (15, 2),
        (16, 2),
    ],
)
@pytest.mark.parametrize("cls", [ProcessDataIn, ProcessDataOut])
def test_calculateProcessDataLength_bitsValid(cls, length, expected):
    octet = cls(byte=0, length=length)
    assert calculateProcessDataLength(octet) == expected


@pytest.mark.parametrize("length", range(17, 32))
@pytest.mark.parametrize("cls", [ProcessDataIn, ProcessDataOut])
def test_calculateProcessDataLength_bitsInvalid(cls, length):
    octet = cls(byte=0, length=length)
    with pytest.raises(InvalidLengthInProcessDataParameter) as exc:
        calculateProcessDataLength(octet)

    msg = str(exc.value)
    assert cls.__name__ in msg
    assert "allowed 0 - 16" in msg


@pytest.mark.parametrize(
    "length, expected",
    [
        (2, 3),
        (3, 4),
        (10, 11),
        (31, 32),
    ],
)
@pytest.mark.parametrize("cls", [ProcessDataIn, ProcessDataOut])
def test_calculateProcessDataLength_octetsValid(cls, length, expected):
    octet = cls(byte=1, length=length)
    assert calculateProcessDataLength(octet) == expected


@pytest.mark.parametrize("length", [0, 1])
@pytest.mark.parametrize("cls", [ProcessDataIn, ProcessDataOut])
def test_calculateProcessDataLength_octetsInvalid(cls, length):
    octet = cls(byte=1, length=length)
    with pytest.raises(InvalidLengthInProcessDataParameter) as exc:
        calculateProcessDataLength(octet)

    msg = str(exc.value)
    assert cls.__name__ in msg
    assert "allowed 2 - 31" in msg
