import pytest
from typing import List

from iolink_utils.messageInterpreter.isdu.commChannelISDU import CommChannelISDU
from iolink_utils.messageInterpreter.isdu.ISDUrequests import (
    ISDURequest_Read8bitIdxSub,
    ISDURequest_Read16bitIdxSub,
    ISDURequest_Write8bitIdx
)
from iolink_utils.messageInterpreter.isdu.ISDUresponses import (
    ISDUResponse_ReadResp_P,
    ISDUResponse_WriteResp_P
)
from iolink_utils.octetStreamDecoder.octetStreamDecoderMessages import MasterMessage, DeviceMessage
from iolink_utils.octetDecoder.octetDecoder import MC, CKT, CKS


def test_commChannelDiagnosis_reset():
    channel = CommChannelISDU()

    channel._state = CommChannelISDU.State.Response
    channel.reset()

    assert channel._state == CommChannelISDU.State.Idle


def createMasterMessage(mc: int, ckt: int, pdOutSize: int, od: List[int]):
    masterMsg = MasterMessage()
    masterMsg.mc = MC(mc)
    masterMsg.ckt = CKT(ckt)
    masterMsg.pdOut = bytearray(pdOutSize)
    masterMsg.od = bytearray(od)
    masterMsg.isValid = True
    return masterMsg


def createDeviceMessage(od: List[int], pdInSize: int, cks: int):
    deviceMsg = DeviceMessage()
    deviceMsg.od = bytearray(od)
    deviceMsg.pdIn = bytearray(pdInSize)
    deviceMsg.cks = CKS(cks)
    deviceMsg.isValid = True
    return deviceMsg


def test_commChannelDiagnosis_read():
    messages = [
        (createMasterMessage(0x70, 0x83, 7, [0xA4, 0x03]),
         createDeviceMessage([], 10, 0x2D), None),
        (createMasterMessage(0x61, 0x86, 7, [0x01, 0xA6]),
         createDeviceMessage([], 10, 0x2D), ISDURequest_Read8bitIdxSub),
        (createMasterMessage(0xF0, 0x85, 7, []),
         createDeviceMessage([0xD3, 0x00], 10, 0x39), None),
        (createMasterMessage(0xE1, 0x80, 7, []),
         createDeviceMessage([0xD3, 0x00], 10, 0x39), ISDUResponse_ReadResp_P)
    ]

    channel = CommChannelISDU()

    for masterMessage, deviceMessage, resultType in messages:
        assert channel.handleMasterMessage(masterMessage) is None
        transaction = channel.handleDeviceMessage(deviceMessage)

        if transaction or resultType:
            assert type(transaction) == resultType
            assert transaction.isComplete
            assert transaction.isValid


# See "Example sequence of an ISDU transmission"
def test_commChannelDiagnosis_exampleFigureJ1():
    messages = [
        # Idle_1 / 0
        (createMasterMessage(0b11110001, 0b10000000, 1, []),
         createDeviceMessage([0b00000000], 1, 0b00000000), None),
        # ISDURequest_2, transmission / 1
        (createMasterMessage(0b01110000, 0b10000000, 1, [0b10110101]),
         createDeviceMessage([], 1, 0b00000000), None),
        # ISDURequest_2, transmission / 2
        (createMasterMessage(0b01100001, 0b10000000, 1, [0xAA]),
         createDeviceMessage([], 1, 0b00000000), None),
        # ISDURequest_2, transmission / 3
        (createMasterMessage(0b01100010, 0b10000000, 1, [0xBB]),
         createDeviceMessage([], 1, 0b00000000), None),
        # ISDURequest_2, transmission / 4
        (createMasterMessage(0b01100011, 0b10000000, 1, [0xCC]),
         createDeviceMessage([], 1, 0b00000000), None),
        # ISDURequest_2, transmission / 5
        (createMasterMessage(0b01100100, 0b10000000, 1, [104]),
         createDeviceMessage([], 1, 0b00000000), ISDURequest_Read16bitIdxSub),
        # ISDUWait_3, start ISDU Timer / 6
        (createMasterMessage(0b11110000, 0b10000000, 1, []),
         createDeviceMessage([0b00000001], 1, 0b00000000), None),
        # ISDUWait_3, start ISDU Timer / 7
        (createMasterMessage(0b11110000, 0b10000000, 1, []),
         createDeviceMessage([0b00000001], 1, 0b00000000), None),
        # ISDUWait_3, start ISDU Timer / 8
        (createMasterMessage(0b11110000, 0b10000000, 1, []),
         createDeviceMessage([0b00000001], 1, 0b00000000), None),
        # ISDUWait_3, start ISDU Timer / 9
        (createMasterMessage(0b11110000, 0b10000000, 1, []),
         createDeviceMessage([0b00000001], 1, 0b00000000), None),
        # ISDUWait_3, start ISDU Timer / 10
        (createMasterMessage(0b11110000, 0b10000000, 1, []),
         createDeviceMessage([0b00000001], 1, 0b00000000), None),
        # ISDUResponse_4, reception, Stop ISDU Timer / 11
        (createMasterMessage(0b11110000, 0b10000000, 1, []),
         createDeviceMessage([0b11010001], 1, 0b00000000), None),
        # ISDUResponse_4, reception / 12
        (createMasterMessage(0b11100001, 0b10000000, 1, []),
         createDeviceMessage([0b00010011], 1, 0b00000000), None),
        # ISDUResponse_4, reception / 13
        (createMasterMessage(0b11100010, 0b10000000, 1, []),
         createDeviceMessage([0xD1], 1, 0b00000000), None),
        # ISDUResponse_4, reception / 14
        (createMasterMessage(0b11100011, 0b10000000, 1, []),
         createDeviceMessage([0xD2], 1, 0b00000000), None),
        # ISDUResponse_4, reception / 15
        (createMasterMessage(0b11100100, 0b10000000, 1, []),
         createDeviceMessage([0xD3], 1, 0b00000000), None),
        # ISDUResponse_4, reception / 16
        (createMasterMessage(0b11100101, 0b10000000, 1, []),
         createDeviceMessage([0xD4], 1, 0b00000000), None),
        # ISDUResponse_4, reception / 17
        (createMasterMessage(0b11100110, 0b10000000, 1, []),
         createDeviceMessage([0xD5], 1, 0b00000000), None),
        # ISDUResponse_4, reception / 18
        (createMasterMessage(0b11100111, 0b10000000, 1, []),
         createDeviceMessage([0xD6], 1, 0b00000000), None),
        # ISDUResponse_4, reception / 19
        (createMasterMessage(0b11101000, 0b10000000, 1, []),
         createDeviceMessage([0xD7], 1, 0b00000000), None),
        # ISDUResponse_4, no response, retry in next cycle / 20
        (createMasterMessage(0b11101001, 0b10000000, 1, []),
         None, None),
        # ISDUResponse_4, no response, retry in next cycle / 21
        (createMasterMessage(0b11101001, 0b10000000, 1, []),
         None, None),
        # ISDUResponse_4, reception / 22
        (createMasterMessage(0b11101001, 0b10000000, 1, []),
         createDeviceMessage([0xD8], 1, 0b00000000), None),
        # ISDUResponse_4, reception / 34
        (createMasterMessage(0b11101010, 0b10000000, 1, []),
         createDeviceMessage([0xD9], 1, 0b00000000), None),
        # ISDUResponse_4, reception, start eventhandler / 35
        (createMasterMessage(0b11101011, 0b10000000, 1, []),
         createDeviceMessage([0xDA], 1, 0b10000000), None),
        # event reception skipped ...
        # ISDUResponse_4, reception / 42
        (createMasterMessage(0b11101100, 0b10000000, 1, []),
         createDeviceMessage([0xDB], 1, 0b00000000), None),
        # ISDUResponse_4, reception / 43
        (createMasterMessage(0b11101101, 0b10000000, 1, []),
         createDeviceMessage([0xDC], 1, 0b00000000), None),
        # ISDUResponse_4, reception / 44
        (createMasterMessage(0b11101110, 0b10000000, 1, []),
         createDeviceMessage([0xDD], 1, 0b00000000), None),
        # ISDUResponse_4, reception / 45
        (createMasterMessage(0b11101111, 0b10000000, 1, []),
         createDeviceMessage([0xDE], 1, 0b00000000), None),
        # ISDUResponse_4, reception / 46
        (createMasterMessage(0b11100000, 0b10000000, 1, []),
         createDeviceMessage([0xDF], 1, 0b00000000), None),
        # ISDUResponse_4, reception / 47
        (createMasterMessage(0b11100001, 0b10000000, 1, []),
         createDeviceMessage([0xE0], 1, 0b00000000), None),
        # ISDUResponse_4, reception / 48
        (createMasterMessage(0b11100010, 0b10000000, 1, []),
         createDeviceMessage([242], 1, 0b00000000), ISDUResponse_ReadResp_P),
        # Idle_1 / 49
        (createMasterMessage(0b11110001, 0b10000000, 1, []),
         createDeviceMessage([0b00000000], 1, 0b00000000), None),
        # Idle_1 / 50
        (createMasterMessage(0b11110001, 0b10000000, 1, []),
         createDeviceMessage([0b00000000], 1, 0b00000000), None),
        # Idle_1 / 51
        (createMasterMessage(0b11110001, 0b10000000, 1, []),
         createDeviceMessage([0b00000000], 1, 0b00000000), None),
        # Idle_1 / 52
        (createMasterMessage(0b11110001, 0b10000000, 1, []),
         createDeviceMessage([0b00000000], 1, 0b00000000), None),
        # # Write Parameter, transmission / 53
        # (createMasterMessage(0b00110000, 0b10000000, 1, [0x00]),
        #  createDeviceMessage([], 1, 0b00000000), None),
        # # Read Parameter, reception / 54
        # (createMasterMessage(0b10110000, 0b10000000, 1, []),
        #  createDeviceMessage([0x00], 1, 0b00000000), None),
        # Idle_1 / 55
        (createMasterMessage(0b11110001, 0b10000000, 1, []),
         createDeviceMessage([0b00000000], 1, 0b00000000), None),
        # ISDURequest_2, transmission / 58
        (createMasterMessage(0b01110000, 0b10000000, 1, [0b00011011]),
         createDeviceMessage([], 1, 0b00000000), None),
        # ISDURequest_2, transmission / 59
        (createMasterMessage(0b01100001, 0b10000000, 1, [0xAA]),
         createDeviceMessage([], 1, 0b00000000), None),
        # ISDURequest_2, transmission / 60
        (createMasterMessage(0b01100010, 0b10000000, 1, [0x01]),
         createDeviceMessage([], 1, 0b00000000), None),
        # ISDURequest_2, transmission / 61
        (createMasterMessage(0b01100011, 0b10000000, 1, [0x02]),
         createDeviceMessage([], 1, 0b00000000), None),
        # ISDURequest_2, transmission / 62
        (createMasterMessage(0b01100100, 0b10000000, 1, [0x03]),
         createDeviceMessage([], 1, 0b00000000), None),
        # ISDURequest_2, transmission / 63
        (createMasterMessage(0b01100101, 0b10000000, 1, [0x04]),
         createDeviceMessage([], 1, 0b00000000), None),
        # ISDURequest_2, transmission / 64
        (createMasterMessage(0b01100110, 0b10000000, 1, [0x05]),
         createDeviceMessage([], 1, 0b00000000), None),
        # ISDURequest_2, transmission / 65
        (createMasterMessage(0b01100111, 0b10000000, 1, [0x06]),
         createDeviceMessage([], 1, 0b00000000), None),
        # ISDURequest_2, transmission / 66
        (createMasterMessage(0b01101000, 0b10000000, 1, [0x07]),
         createDeviceMessage([], 1, 0b00000000), None),
        # ISDURequest_2, transmission / 67
        (createMasterMessage(0b01101001, 0b10000000, 1, [0x08]),
         createDeviceMessage([], 1, 0b00000000), None),
        # ISDURequest_2, transmission / 68
        (createMasterMessage(0b01101010, 0b10000000, 1, [185]),
         createDeviceMessage([], 1, 0b00000000), ISDURequest_Write8bitIdx),
        # ISDUWait_3, start ISDU Timer / 69
        (createMasterMessage(0b11110000, 0b10000000, 1, []),
         createDeviceMessage([0b00000001], 1, 0b00000000), None),
        # ISDUResponse_4, reception, Stop ISDU Timer / 70
        (createMasterMessage(0b11110000, 0b10000000, 1, []),
         createDeviceMessage([0b01010010], 1, 0b00000000), None),
        # ISDUResponse_4, reception / 71
        (createMasterMessage(0b11100001, 0b10000000, 1, []),
         createDeviceMessage([82], 1, 0b00000000), ISDUResponse_WriteResp_P),
        # Idle_1 / 72
        (createMasterMessage(0b11110001, 0b10000000, 1, []),
         createDeviceMessage([0b00000000], 1, 0b00000000), None),
        # Idle_1 / 73
        (createMasterMessage(0b11110001, 0b10000000, 1, []),
         createDeviceMessage([0b00000000], 1, 0b00000000), None),
        # ISDURequest_2, transmission / 74
        (createMasterMessage(0b01110000, 0b10000000, 1, [0b10110101]),
         createDeviceMessage([], 1, 0b00000000), None),
        # ISDURequest_2, transmission / 75
        (createMasterMessage(0b01100001, 0b10000000, 1, [0xAA]),
         createDeviceMessage([], 1, 0b00000000), None),
        # ISDURequest_2, transmission / 76
        (createMasterMessage(0b01100010, 0b10000000, 1, [0xBB]),
         createDeviceMessage([], 1, 0b00000000), None),
        # ISDURequest_2, transmission / 77
        (createMasterMessage(0b01100011, 0b10000000, 1, [0xCC]),
         createDeviceMessage([], 1, 0b00000000), None),
        # ISDURequest_2, transmission / 78
        (createMasterMessage(0b01100100, 0b10000000, 1, [104]),
         createDeviceMessage([], 1, 0b00000000), ISDURequest_Read16bitIdxSub),
        # ISDUWait_3, start ISDU Timer / 79
        (createMasterMessage(0b11110000, 0b10000000, 1, []),
         createDeviceMessage([0b00000001], 1, 0b00000000), None),
        # ISDUResponse_4, reception, Stop ISDU Timer / 84
        (createMasterMessage(0b11110000, 0b10000000, 1, []),
         createDeviceMessage([0b11010001], 1, 0b00000000), None),
        # ISDUResponse_4, reception / 85
        (createMasterMessage(0b11100001, 0b10000000, 1, []),
         createDeviceMessage([0b00011110], 1, 0b00000000), None),
        # ISDUResponse_4, reception / 86
        (createMasterMessage(0b11100010, 0b10000000, 1, []),
         createDeviceMessage([0x01], 1, 0b00000000), None),
        # ISDUResponse_4, ABORT / 87
        (createMasterMessage(0b11111111, 0b10000000, 1, []),
         createDeviceMessage([0x00], 1, 0b00000000), None),
        # Idle_1 / 88
        (createMasterMessage(0b11110001, 0b10000000, 1, []),
         createDeviceMessage([0b00000000], 1, 0b00000000), None),
        # Idle_1 / 89
        (createMasterMessage(0b11110001, 0b10000000, 1, []),
         createDeviceMessage([0b00000000], 1, 0b00000000), None),
    ]

    channel = CommChannelISDU()

    for masterMessage, deviceMessage, resultType in messages:
        transaction = None

        if masterMessage:
            assert channel.handleMasterMessage(masterMessage) is None
        if deviceMessage:
            transaction = channel.handleDeviceMessage(deviceMessage)

        if transaction or resultType:
            assert type(transaction) == resultType
            assert transaction.isComplete
            assert transaction.isValid
