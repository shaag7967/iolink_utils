from typing import Union, Optional, List, Dict
from datetime import datetime as dt

from iolink_utils.octetDecoder.octetStreamDecoderMessages import DeviceMessage, MasterMessage
from iolink_utils.definitions.directParameterPage import DirectParameterPage1Index
from iolink_utils.definitions.masterCommand import MasterCommand
from iolink_utils.definitions.systemCommand import SystemCommand
from iolink_utils.octetDecoder.octetDecoder import (CycleTimeOctet, MSequenceCapability, RevisionId,
                                                    ProcessDataIn, ProcessDataOut)

from iolink_utils.utils.cycleTime import CycleTime
from iolink_utils.definitions.transmissionDirection import TransmissionDirection


class TransactionPage:
    def __init__(self, name: str, value: str):
        self.start_time: dt = dt(1970, 1, 1)
        self.end_time: dt = dt(1970, 1, 1)

        self.name: str = name
        self.value: str = value

    def data(self) -> Dict:
        return {
            'page': ' '.join(filter(None, [self.name, self.value]))
        }

    def __str__(self):
        return f"Page: {' '.join(filter(None, [self.name, self.value]))} ({self.start_time} {self.end_time})"


class CommChannelPage:
    def __init__(self):
        self.start_time: dt = dt(1970, 1, 1)
        self.end_time: dt = dt(1970, 1, 1)

        self.direction: TransmissionDirection = TransmissionDirection.Read
        self.pageIndex: int = 0
        self.octet: int = 0

    def processMasterMessage(self, message: MasterMessage):
        self.start_time = message.start_time
        self.end_time = message.end_time

        self.direction = TransmissionDirection(message.mc.read)
        self.pageIndex = message.mc.address
        self.octet = message.od[0] if self.direction == TransmissionDirection.Write else 0

        return []

    def processDeviceMessage(self, message: DeviceMessage) -> List[TransactionPage]:
        self.end_time = message.end_time
        if self.direction == TransmissionDirection.Read:
            self.octet = message.od[0]

        transaction = None

        if self.pageIndex == DirectParameterPage1Index.MasterCommand:
            if self.direction == TransmissionDirection.Write:
                transaction = TransactionPage("MasterCommand", MasterCommand(self.octet).name)
        elif self.pageIndex == DirectParameterPage1Index.MasterCycleTime:
            cycleTimeOctet = CycleTimeOctet.from_buffer_copy(bytes([self.octet]), 0)
            transaction = TransactionPage("MasterCycleTime", f"{CycleTime.decodeToTimeInMs(cycleTimeOctet)}ms")
        elif self.pageIndex == DirectParameterPage1Index.MinCycleTime:
            cycleTimeOctet = CycleTimeOctet.from_buffer_copy(bytes([self.octet]), 0)
            transaction = TransactionPage("MinCycleTime", f"{CycleTime.decodeToTimeInMs(cycleTimeOctet)}ms")
        elif self.pageIndex == DirectParameterPage1Index.MSequenceCapability:
            capaOctet = MSequenceCapability.from_buffer_copy(bytes([self.octet]), 0)
            transaction = TransactionPage("", str(capaOctet))
        elif self.pageIndex == DirectParameterPage1Index.RevisionID:
            revOctet = RevisionId.from_buffer_copy(bytes([self.octet]), 0)
            transaction = TransactionPage("", str(revOctet))
        elif self.pageIndex == DirectParameterPage1Index.ProcessDataIn:
            pdOctet = ProcessDataIn.from_buffer_copy(bytes([self.octet]), 0)
            transaction = TransactionPage("", str(pdOctet))
        elif self.pageIndex == DirectParameterPage1Index.ProcessDataOut:
            pdOctet = ProcessDataOut.from_buffer_copy(bytes([self.octet]), 0)
            transaction = TransactionPage("", str(pdOctet))
        elif self.pageIndex == DirectParameterPage1Index.VendorID_MSB:
            transaction = TransactionPage("VendorID_MSB", bytes([self.octet]).hex())
        elif self.pageIndex == DirectParameterPage1Index.VendorID_LSB:
            transaction = TransactionPage("VendorID_LSB", bytes([self.octet]).hex())
        elif self.pageIndex == DirectParameterPage1Index.DeviceID_MSB:
            transaction = TransactionPage("DeviceID_MSB", bytes([self.octet]).hex())
        elif self.pageIndex == DirectParameterPage1Index.DeviceID:
            transaction = TransactionPage("DeviceID", bytes([self.octet]).hex())
        elif self.pageIndex == DirectParameterPage1Index.DeviceID_LSB:
            transaction = TransactionPage("DeviceID_LSB", bytes([self.octet]).hex())
        elif self.pageIndex == DirectParameterPage1Index.FunctionID_MSB:
            transaction = TransactionPage("FunctionID_MSB", bytes([self.octet]).hex())
        elif self.pageIndex == DirectParameterPage1Index.FunctionID_LSB:
            transaction = TransactionPage("FunctionID_LSB", bytes([self.octet]).hex())
        elif self.pageIndex == DirectParameterPage1Index.Reserved:
            pass
        elif self.pageIndex == DirectParameterPage1Index.SystemCommand:
            if self.direction == TransmissionDirection.Write:
                transaction = TransactionPage("SystemCommand", SystemCommand(self.octet).name)

        if transaction is not None:
            transaction.start_time = self.start_time
            transaction.end_time = self.end_time
            return [transaction]
        else:
            return []

