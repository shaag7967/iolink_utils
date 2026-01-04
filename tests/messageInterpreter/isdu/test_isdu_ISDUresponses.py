import pytest

from iolink_utils.messageInterpreter.isdu.ISDUresponses import (
    createISDUResponse,
    ISDUResponse_WriteResp_M,
    ISDUResponse_WriteResp_P,
    ISDUResponse_ReadResp_M,
    ISDUResponse_ReadResp_P,
)
from iolink_utils.exceptions import InvalidISDUService, UnknownISDUError
from iolink_utils.octetDecoder.octetDecoder import IService
from iolink_utils.definitions.iServiceNibble import IServiceNibble


def test_ISDUResponse_createISDUResponse():
    _map_serviceValueToClass = {
        0b0100: ISDUResponse_WriteResp_M,
        0b0101: ISDUResponse_WriteResp_P,
        0b1100: ISDUResponse_ReadResp_M,
        0b1101: ISDUResponse_ReadResp_P
    }
    for serviceValue in _map_serviceValueToClass:
        res = createISDUResponse(IService(service=serviceValue))
        assert type(res) is _map_serviceValueToClass[serviceValue]
        assert res.__class__.__name__.endswith(res.name())
        assert res._SERVICE_NIBBLE == IServiceNibble(serviceValue)


def test_ISDUResponse_createISDUResponse_InvalidISDUService():
    service = IService()
    service.service = IServiceNibble.NoService
    service.length = 4

    with pytest.raises(InvalidISDUService):
        createISDUResponse(service)


def test_ISDUResponse_WriteResp_M():
    service = IService(service=IServiceNibble.D_WriteResp_M, length=4)
    res = ISDUResponse_WriteResp_M()
    res.appendOctets(bytearray([int(service), 0x81, 0x77, 178]))
    assert res.isComplete
    d = res.data()
    assert d['valid'] == True
    assert d['error'] == 'VENDOR_SPECIFIC(0x81, 0x77)'

    # invalid error code
    service = IService(service=IServiceNibble.D_WriteResp_M, length=4)
    res = ISDUResponse_WriteResp_M()
    with pytest.raises(UnknownISDUError):
        res.appendOctets(bytearray([int(service), 0xFF, 0xFF, 68]))

    # extended length
    service = IService(service=IServiceNibble.D_WriteResp_M, length=1)
    res = ISDUResponse_WriteResp_M()
    res.appendOctets(bytearray([int(service), 5, 0x81, 0x88, 77]))
    assert res.isComplete
    d = res.data()
    assert d['valid'] == False
    assert d['error'] == 'UNDEFINED(0x0, 0x0)'

    # invalid crc
    service = IService(service=IServiceNibble.D_WriteResp_M, length=1)
    res = ISDUResponse_WriteResp_M()
    res.appendOctets(bytearray([int(service), 5, 0x81, 0x99, 111]))
    assert res.isComplete
    d = res.data()
    assert d['valid'] == False
    assert d['error'] == 'UNDEFINED(0x0, 0x0)'


def test_ISDUResponse_ReadResp_M():
    service = IService(service=IServiceNibble.D_ReadResp_M, length=4)
    res = ISDUResponse_ReadResp_M()
    res.appendOctets(bytearray([int(service), 0x81, 0x77, 50]))
    assert res.isComplete
    d = res.data()
    assert d['valid'] == True
    assert d['error'] == 'VENDOR_SPECIFIC(0x81, 0x77)'

    # invalid error code
    service = IService(service=IServiceNibble.D_ReadResp_M, length=4)
    res = ISDUResponse_ReadResp_M()
    with pytest.raises(UnknownISDUError):
        res.appendOctets(bytearray([int(service), 0xFF, 0xFF, 196]))

    # extended length
    service = IService(service=IServiceNibble.D_ReadResp_M, length=1)
    res = ISDUResponse_ReadResp_M()
    res.appendOctets(bytearray([int(service), 5, 0x81, 0x88, 205]))
    assert res.isComplete
    d = res.data()
    assert d['valid'] == False
    assert d['error'] == 'UNDEFINED(0x0, 0x0)'

    # invalid crc
    service = IService(service=IServiceNibble.D_ReadResp_M, length=1)
    res = ISDUResponse_ReadResp_M()
    res.appendOctets(bytearray([int(service), 5, 0x81, 0x99, 111]))
    assert res.isComplete
    d = res.data()
    assert d['valid'] == False
    assert d['error'] == 'UNDEFINED(0x0, 0x0)'


def test_ISDUResponse_WriteResp_P():
    service = IService(service=IServiceNibble.D_WriteResp_P, length=2)
    res = ISDUResponse_WriteResp_P()
    res.appendOctets(bytearray([int(service), 82]))
    assert res.isComplete
    d = res.data()
    assert d['valid'] == True

    # extended length
    service = IService(service=IServiceNibble.D_WriteResp_P, length=1)
    res = ISDUResponse_WriteResp_P()
    res.appendOctets(bytearray([int(service), 2, 81]))
    assert res.isComplete
    d = res.data()
    assert d['valid'] == False

    # invalid crc
    service = IService(service=IServiceNibble.D_WriteResp_P, length=1)
    res = ISDUResponse_WriteResp_P()
    res.appendOctets(bytearray([int(service), 2, 111]))
    assert res.isComplete
    d = res.data()
    assert d['valid'] == False


def test_ISDUResponse_ReadResp_P():
    service = IService(service=IServiceNibble.D_ReadResp_P, length=4)
    res = ISDUResponse_ReadResp_P()
    res.appendOctets(bytearray([int(service), 0xAA, 0xBB, 197]))
    assert res.isComplete
    d = res.data()
    assert d['valid'] == True
    assert d['data'] == bytearray([0xAA, 0xBB])

    # extended length
    service = IService(service=IServiceNibble.D_ReadResp_P, length=1)
    res = ISDUResponse_ReadResp_P()
    res.appendOctets(bytearray([int(service), 5, 0xAA, 0xBB, 197]))
    assert res.isComplete
    d = res.data()
    assert d['valid'] == True
    assert d['data'] == bytearray([0xAA, 0xBB])

    # invalid crc
    service = IService(service=IServiceNibble.D_ReadResp_P, length=1)
    res = ISDUResponse_ReadResp_P()
    res.appendOctets(bytearray([int(service), 5, 0xAA, 0xBB, 111]))
    assert res.isComplete
    d = res.data()
    assert d['valid'] == False
    assert d['data'] == bytearray([0xAA, 0xBB])
