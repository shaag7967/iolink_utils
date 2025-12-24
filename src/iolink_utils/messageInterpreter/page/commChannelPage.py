from datetime import datetime as dt

from iolink_utils.exceptions import InvalidOctetValue
from iolink_utils.octetStreamDecoder.octetStreamDecoderMessages import DeviceMessage, MasterMessage
from iolink_utils.definitions.directParameterPage import DirectParameterPage1Index
from iolink_utils.definitions.masterCommand import MasterCommand
from iolink_utils.definitions.systemCommand import SystemCommand
from iolink_utils.octetDecoder.octetDecoder import (CycleTimeOctet, MSequenceCapability, RevisionId,
                                                    ProcessDataIn, ProcessDataOut)

from iolink_utils.utils.cycleTime import CycleTime
from iolink_utils.definitions.transmissionDirection import TransmissionDirection

from .transactionPage import TransactionPage


class CommChannelPage:
    def __init__(self):
        self.start_time: dt = dt(1970, 1, 1)
        self.end_time: dt = dt(1970, 1, 1)

        self.direction: TransmissionDirection = TransmissionDirection.Read
        self.pageIndex: int = 0
        self.octet: int = 0

        self._pageIndexHandler = {
            DirectParameterPage1Index.MasterCommand: self._handleMasterCommand,
            DirectParameterPage1Index.MasterCycleTime: self._handleMasterCycleTime,
            DirectParameterPage1Index.MinCycleTime: self._handleMinCycleTime,
            DirectParameterPage1Index.MSequenceCapability: self._handleMSeqCapability,
            DirectParameterPage1Index.RevisionID: self._handleRevisionId,
            DirectParameterPage1Index.ProcessDataIn: self._handlePDIn,
            DirectParameterPage1Index.ProcessDataOut: self._handlePDOut,
            DirectParameterPage1Index.VendorID_MSB: lambda: self._handleHexValue("VendorID_MSB"),
            DirectParameterPage1Index.VendorID_LSB: lambda: self._handleHexValue("VendorID_LSB"),
            DirectParameterPage1Index.DeviceID_MSB: lambda: self._handleHexValue("DeviceID_MSB"),
            DirectParameterPage1Index.DeviceID: lambda: self._handleHexValue("DeviceID"),
            DirectParameterPage1Index.DeviceID_LSB: lambda: self._handleHexValue("DeviceID_LSB"),
            DirectParameterPage1Index.FunctionID_MSB: lambda: self._handleHexValue("FunctionID_MSB"),
            DirectParameterPage1Index.FunctionID_LSB: lambda: self._handleHexValue("FunctionID_LSB"),
            DirectParameterPage1Index.SystemCommand: self._handleSystemCommand,
        }

    def _handleMasterCommand(self):
        if self.direction == TransmissionDirection.Write:
            return TransactionPage("MasterCommand", MasterCommand(self.octet).name)
        else:
            return TransactionPage("MasterCommand", f'Invalid {hex(self.octet)} (Read)')

    def _handleMasterCycleTime(self):
        cto = CycleTimeOctet.from_buffer_copy(bytes([self.octet]), 0)
        try:
            return TransactionPage("MasterCycleTime", f"{CycleTime.decodeToTimeInMs(cto)}ms")
        except InvalidOctetValue:
            return TransactionPage("MasterCycleTime", f'invalid: {hex(self.octet)}')

    def _handleMinCycleTime(self):
        cto = CycleTimeOctet.from_buffer_copy(bytes([self.octet]), 0)
        try:
            return TransactionPage("MinCycleTime", f"{CycleTime.decodeToTimeInMs(cto)}ms")
        except InvalidOctetValue:
            return TransactionPage("MinCycleTime", f'invalid: {hex(self.octet)}')

    def _handleMSeqCapability(self):
        val = MSequenceCapability.from_buffer_copy(bytes([self.octet]), 0)
        return TransactionPage(str(val), '')

    def _handleRevisionId(self):
        val = RevisionId.from_buffer_copy(bytes([self.octet]), 0)
        return TransactionPage(str(val), '')

    def _handlePDIn(self):
        val = ProcessDataIn.from_buffer_copy(bytes([self.octet]), 0)
        return TransactionPage(str(val), '')

    def _handlePDOut(self):
        val = ProcessDataOut.from_buffer_copy(bytes([self.octet]), 0)
        return TransactionPage(str(val), '')

    def _handleHexValue(self, label):
        return TransactionPage(label, bytes([self.octet]).hex())

    def _handleSystemCommand(self):
        if self.direction == TransmissionDirection.Write:
            return TransactionPage("SystemCommand", SystemCommand(self.octet).name)
        else:
            return TransactionPage("SystemCommand", f'Invalid {hex(self.octet)} (Read)')

    def handleMasterMessage(self, message: MasterMessage) -> None:
        self.start_time = message.start_time
        self.end_time = message.end_time

        self.direction = TransmissionDirection(message.mc.read)
        self.pageIndex = message.mc.address
        self.octet = message.od[0] if self.direction == TransmissionDirection.Write else 0

        return None

    def handleDeviceMessage(self, message: DeviceMessage) -> TransactionPage:
        self.end_time = message.end_time
        if self.direction == TransmissionDirection.Read:
            self.octet = message.od[0]

        handler = self._pageIndexHandler.get(self.pageIndex)
        transaction = handler() if handler else TransactionPage(
            f"DirectParameterPage1 '{self.pageIndex}' unhandled:",
            bytes([self.octet]).hex()
        )
        transaction.direction = self.direction.name
        transaction.start_time = self.start_time
        transaction.end_time = self.end_time

        return transaction
