from typing import Union, Optional
from iolink_utils.octetDecoder.octetStreamDecoderMessages import DeviceMessage, MasterMessage
from iolink_utils.octetDecoder.octetDecoder import (CycleTimeOctet, MSequenceCapability, RevisionId,
                                                    ProcessDataIn, ProcessDataOut)

from iolink_utils.utils.cycleTime import CycleTime

from iolink_utils.definitions.communicationChannel import CommChannel
from iolink_utils.definitions.transmissionDirection import TransmissionDirection
from iolink_utils.definitions.directParameterPage import DirectParameterPage1Index
from iolink_utils.definitions.masterCommand import MasterCommand
from iolink_utils.definitions.systemCommand import SystemCommand


class CommChannelProcess:
    def processMasterMessage(self, message: MasterMessage):
        pass

    def processDeviceMessage(self, message: DeviceMessage):
        pass


class CommChannelPage:
    def __init__(self):
        self.direction: TransmissionDirection = TransmissionDirection.Read
        self.pageIndex: int = 0
        self.octet: int = 0

    def processMasterMessage(self, message: MasterMessage):
        self.direction = TransmissionDirection(message.mc.read)
        self.pageIndex = message.mc.address
        self.octet = message.od[0] if self.direction == TransmissionDirection.Write else 0

    def processDeviceMessage(self, message: DeviceMessage):
        if self.direction == TransmissionDirection.Read:
            self.octet = message.od[0]

        if self.pageIndex == DirectParameterPage1Index.MasterCommand:
            print(f"MasterCommand: {MasterCommand(self.octet).name}")
        elif self.pageIndex == DirectParameterPage1Index.MasterCycleTime:
            cycleTimeOctet = CycleTimeOctet.from_buffer_copy(bytes([self.octet]), 0)
            print(f"MasterCycleTime: {cycleTimeOctet} / {CycleTime.decodeToTimeInMs(cycleTimeOctet)}ms")
        elif self.pageIndex == DirectParameterPage1Index.MinCycleTime:
            cycleTimeOctet = CycleTimeOctet.from_buffer_copy(bytes([self.octet]), 0)
            print(f"MinCycleTime: {cycleTimeOctet} / {CycleTime.decodeToTimeInMs(cycleTimeOctet)}ms")
        elif self.pageIndex == DirectParameterPage1Index.MSequenceCapability:
            capaOctet = MSequenceCapability.from_buffer_copy(bytes([self.octet]), 0)
            print(f"MSequenceCapability: {capaOctet}")
        elif self.pageIndex == DirectParameterPage1Index.RevisionID:
            revOctet = RevisionId.from_buffer_copy(bytes([self.octet]), 0)
            print(f"RevisionId: {revOctet}")
        elif self.pageIndex == DirectParameterPage1Index.ProcessDataIn:
            pdOctet = ProcessDataIn.from_buffer_copy(bytes([self.octet]), 0)
            print(f"ProcessDataIn: {pdOctet}")
        elif self.pageIndex == DirectParameterPage1Index.ProcessDataOut:
            pdOctet = ProcessDataOut.from_buffer_copy(bytes([self.octet]), 0)
            print(f"ProcessDataOut: {pdOctet}")
        elif self.pageIndex == DirectParameterPage1Index.VendorID_MSB:
            print(f"VendorID_MSB: {bytes([self.octet]).hex()}")
        elif self.pageIndex == DirectParameterPage1Index.VendorID_LSB:
            print(f"VendorID_LSB: {bytes([self.octet]).hex()}")
        elif self.pageIndex == DirectParameterPage1Index.DeviceID_MSB:
            print(f"DeviceID_MSB: {bytes([self.octet]).hex()}")
        elif self.pageIndex == DirectParameterPage1Index.DeviceID:
            print(f"DeviceID: {bytes([self.octet]).hex()}")
        elif self.pageIndex == DirectParameterPage1Index.DeviceID_LSB:
            print(f"DeviceID_LSB: {bytes([self.octet]).hex()}")
        elif self.pageIndex == DirectParameterPage1Index.FunctionID_MSB:
            print(f"FunctionID_MSB: {bytes([self.octet]).hex()}")
        elif self.pageIndex == DirectParameterPage1Index.FunctionID_LSB:
            print(f"FunctionID_LSB: {bytes([self.octet]).hex()}")
        elif self.pageIndex == DirectParameterPage1Index.Reserved:
            pass
        elif self.pageIndex == DirectParameterPage1Index.SystemCommand:
            print(f"SystemCommand: {SystemCommand(self.octet).name}")


class CommChannelDiagnosis:
    def processMasterMessage(self, message: MasterMessage):
        pass

    def processDeviceMessage(self, message: DeviceMessage):
        pass


class CommChannelISDU:
    def processMasterMessage(self, message: MasterMessage):
        pass

    def processDeviceMessage(self, message: DeviceMessage):
        pass


class CommChannelTransactionResult:
    pass


class MessageInterpreter:
    def __init__(self):
        self.channels = {
            CommChannel.Process: CommChannelProcess(),
            CommChannel.Page: CommChannelPage(),
            CommChannel.Diagnosis: CommChannelDiagnosis(),
            CommChannel.ISDU: CommChannelISDU()
        }
        self.activeChannel: Optional[CommChannel] = CommChannel.Process

    def processMessage(self, message: Union[MasterMessage, DeviceMessage]) -> Union[None, CommChannelTransactionResult]:
        if isinstance(message, MasterMessage):
            self.activeChannel = CommChannel(message.mc.channel)
            self.channels[self.activeChannel].processMasterMessage(message)
        elif isinstance(message, DeviceMessage):
            self.channels[self.activeChannel].processDeviceMessage(message)

        return None
