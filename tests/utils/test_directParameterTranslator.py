from iolink_utils.utils.directParameterTranslator import translateDirectParameter, Translation
from iolink_utils.definitions.directParameterPage import DirectParameterPage1Index
from iolink_utils.definitions.masterCommand import MasterCommand
from iolink_utils.definitions.systemCommand import SystemCommand
from iolink_utils.utils.cycleTime import CycleTime
from iolink_utils.definitions.transmissionDirection import TransmissionDirection


def test_translateDirectParameter_unknownIndex():
    translation: Translation = translateDirectParameter(123, 0xAB, TransmissionDirection.Write)

    assert translation.name == "DirectParameter 123"
    assert translation.value == "0xAB"
    assert translation.error == "Index 123 unknown"


def test_translateDirectParameter_handleMasterCommand():
    translation: Translation = translateDirectParameter(
        DirectParameterPage1Index.MasterCommand.value,
        MasterCommand.DeviceOperate.value,
        TransmissionDirection.Write
    )
    assert translation.name == "MasterCommand"
    assert translation.value == "DeviceOperate"
    assert translation.error == ""


def test_translateDirectParameter_handleMasterCommand_invalid():
    # TransmissionDirection invalid
    translation: Translation = translateDirectParameter(
        DirectParameterPage1Index.MasterCommand.value,
        MasterCommand.DeviceOperate.value,
        TransmissionDirection.Read  # invalid
    )
    assert translation.name == "MasterCommand"
    assert translation.value == "DeviceOperate"
    assert translation.error == "Invalid direction (Read)"

    # MasterCommand invalid
    translation: Translation = translateDirectParameter(
        DirectParameterPage1Index.MasterCommand.value,
        1,  # invalid
        TransmissionDirection.Write
    )
    assert translation.name == "MasterCommand"
    assert translation.value == "0x01"
    assert translation.error == "Unknown MasterCommand"

    # TransmissionDirection and MasterCommand invalid
    translation: Translation = translateDirectParameter(
        DirectParameterPage1Index.MasterCommand.value,
        1,  # invalid
        TransmissionDirection.Read  # invalid
    )
    assert translation.name == "MasterCommand"
    assert translation.value == "0x01"
    assert translation.error == "Invalid direction (Read), Unknown MasterCommand"


def test_translateDirectParameter_handleMasterCycleTime():
    translation: Translation = translateDirectParameter(
        DirectParameterPage1Index.MasterCycleTime.value,
        0x00,
        TransmissionDirection.Write
    )
    assert translation.name == "MasterCycleTime"
    assert translation.value == "0.0ms"
    assert translation.error == ""

    translation: Translation = translateDirectParameter(
        DirectParameterPage1Index.MasterCycleTime.value,
        CycleTime.encodeAsCycleTimeOctet(10.0).get(),
        TransmissionDirection.Write
    )
    assert translation.name == "MasterCycleTime"
    assert translation.value == "10.0ms"
    assert translation.error == ""


def test_translateDirectParameter_handleMasterCycleTime_invalidOctet():
    translation: Translation = translateDirectParameter(
        DirectParameterPage1Index.MasterCycleTime.value,
        0xFF,  # invalid
        TransmissionDirection.Write
    )
    assert translation.name == "MasterCycleTime"
    assert translation.value == "0xFF"
    assert translation.error == "Invalid cycle time"


def test_translateDirectParameter_handleMinCycleTime():
    translation: Translation = translateDirectParameter(
        DirectParameterPage1Index.MinCycleTime.value,
        0x00,
        TransmissionDirection.Write
    )
    assert translation.name == "MinCycleTime"
    assert translation.value == "0.0ms"
    assert translation.error == ""

    translation: Translation = translateDirectParameter(
        DirectParameterPage1Index.MinCycleTime.value,
        CycleTime.encodeAsCycleTimeOctet(10.0).get(),
        TransmissionDirection.Write
    )
    assert translation.name == "MinCycleTime"
    assert translation.value == "10.0ms"
    assert translation.error == ""


def test_translateDirectParameter_handleMinCycleTime_invalidOctet():
    translation: Translation = translateDirectParameter(
        DirectParameterPage1Index.MinCycleTime.value,
        0xFF,  # invalid
        TransmissionDirection.Write
    )
    assert translation.name == "MinCycleTime"
    assert translation.value == "0xFF"
    assert translation.error == "Invalid cycle time"


def test_translateDirectParameter_handleMSeqCapa():
    translation: Translation = translateDirectParameter(
        DirectParameterPage1Index.MSequenceCapability.value,
        0xFF,
        TransmissionDirection.Write
    )
    assert translation.name == "MSequenceCapability"
    assert translation.value == "preoperateCode=3, operateCode=7, isduSupport=1"
    assert translation.error == ""


def test_translateDirectParameter_handleRevisionId():
    translation: Translation = translateDirectParameter(
        DirectParameterPage1Index.RevisionId.value,
        0x34,
        TransmissionDirection.Read
    )
    assert translation.name == "RevisionId"
    assert translation.value == "majorRev=3, minorRev=4"
    assert translation.error == ""


def test_translateDirectParameter_handlePDIn():
    translation: Translation = translateDirectParameter(
        DirectParameterPage1Index.ProcessDataIn.value,
        0b11000010,
        TransmissionDirection.Read
    )
    assert translation.name == "ProcessDataIn"
    assert translation.value == "byte=1, sio=1, length=2"
    assert translation.error == ""


def test_translateDirectParameter_handlePDOut():
    translation: Translation = translateDirectParameter(
        DirectParameterPage1Index.ProcessDataOut.value,
        0b10000011,
        TransmissionDirection.Read
    )
    assert translation.name == "ProcessDataOut"
    assert translation.value == "byte=1, length=3"
    assert translation.error == ""


def test_translateDirectParameter_handleHexValue_VendorID_MSB():
    translation: Translation = translateDirectParameter(
        DirectParameterPage1Index.VendorId_MSB.value,
        0x12,
        TransmissionDirection.Read
    )
    assert translation.name == "VendorID_MSB"
    assert translation.value == "0x12"
    assert translation.error == ""


def test_translateDirectParameter_handleHexValue_VendorID_LSB():
    translation: Translation = translateDirectParameter(
        DirectParameterPage1Index.VendorId_LSB.value,
        0x34,
        TransmissionDirection.Read
    )
    assert translation.name == "VendorID_LSB"
    assert translation.value == "0x34"
    assert translation.error == ""


def test_translateDirectParameter_handleHexValue_DeviceID_MSB():
    translation: Translation = translateDirectParameter(
        DirectParameterPage1Index.DeviceId_MSB.value,
        0x56,
        TransmissionDirection.Read
    )
    assert translation.name == "DeviceID_MSB"
    assert translation.value == "0x56"
    assert translation.error == ""


def test_translateDirectParameter_handleHexValue_DeviceID():
    translation: Translation = translateDirectParameter(
        DirectParameterPage1Index.DeviceId.value,
        0x78,
        TransmissionDirection.Read
    )
    assert translation.name == "DeviceID"
    assert translation.value == "0x78"
    assert translation.error == ""


def test_translateDirectParameter_handleHexValue_DeviceID_LSB():
    translation: Translation = translateDirectParameter(
        DirectParameterPage1Index.DeviceId_LSB.value,
        0x9A,
        TransmissionDirection.Read
    )
    assert translation.name == "DeviceID_LSB"
    assert translation.value == "0x9A"
    assert translation.error == ""


def test_translateDirectParameter_handleHexValue_FunctionID_MSB():
    translation: Translation = translateDirectParameter(
        DirectParameterPage1Index.FunctionId_MSB.value,
        0xBC,
        TransmissionDirection.Read
    )
    assert translation.name == "FunctionID_MSB"
    assert translation.value == "0xBC"
    assert translation.error == ""


def test_translateDirectParameter_handleHexValue_FunctionID_LSB():
    translation: Translation = translateDirectParameter(
        DirectParameterPage1Index.FunctionId_LSB.value,
        0xDE,
        TransmissionDirection.Read
    )
    assert translation.name == "FunctionID_LSB"
    assert translation.value == "0xDE"
    assert translation.error == ""


def test_translateDirectParameter_handleSystemCommand():
    translation: Translation = translateDirectParameter(
        DirectParameterPage1Index.SystemCommand.value,
        SystemCommand.BackToBox.value,
        TransmissionDirection.Write
    )
    assert translation.name == "SystemCommand"
    assert translation.value == "BackToBox"
    assert translation.error == ""
