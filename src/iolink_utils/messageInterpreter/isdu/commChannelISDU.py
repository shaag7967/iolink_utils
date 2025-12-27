from enum import IntEnum
from typing import Optional
from datetime import datetime as dt

from iolink_utils.octetStreamDecoder.octetStreamDecoderMessages import DeviceMessage, MasterMessage
from iolink_utils.octetDecoder.octetDecoder import IService
from iolink_utils.definitions.transmissionDirection import TransmissionDirection
from iolink_utils.messageInterpreter.isdu.ISDU import IServiceNibble, FlowControl, ISDU
from iolink_utils.messageInterpreter.isdu.ISDUrequests import createISDURequest
from iolink_utils.messageInterpreter.isdu.ISDUresponses import createISDUResponse


class CommChannelISDU:
    class State(IntEnum):
        Idle = 0,
        Request = 1,
        RequestFinished = 2,
        WaitForResponse = 3,
        Response = 4,
        ResponseFinished = 5

    def __init__(self) -> None:
        self._state: CommChannelISDU.State = CommChannelISDU.State.Idle
        self._direction: TransmissionDirection = TransmissionDirection.Read
        self._flowControl: FlowControl = FlowControl()
        self._isduRequest: Optional[ISDU] = None
        self._isduResponse: Optional[ISDU] = None
        self._responseStartTime: Optional[dt] = None

    def reset(self) -> None:
        self._state = CommChannelISDU.State.Idle

    def handleMasterMessage(self, message: MasterMessage):
        self._direction = TransmissionDirection(message.mc.read)
        self._flowControl = FlowControl(message.mc.address)

        if self._state == CommChannelISDU.State.Idle:
            if self._flowControl.state == FlowControl.State.Start and self._direction == TransmissionDirection.Write:
                self._isduRequest = createISDURequest(IService(message.od[0]))

                self._isduRequest.setTime(message.startTime, message.endTime)
                self._isduRequest.appendOctets(self._flowControl, message.od)

                if self._isduRequest.isComplete:
                    self._state = CommChannelISDU.State.RequestFinished
                else:
                    self._state = CommChannelISDU.State.Request

        elif self._state == CommChannelISDU.State.Request:
            if self._flowControl.state == FlowControl.State.Count:
                self._isduRequest.setEndTime(message.endTime)
                self._isduRequest.appendOctets(self._flowControl, message.od)

                if self._isduRequest.isComplete:
                    self._state = CommChannelISDU.State.RequestFinished

            elif self._flowControl.state == FlowControl.State.Abort:
                self._state = CommChannelISDU.State.Idle

        elif self._state == CommChannelISDU.State.WaitForResponse:
            if self._flowControl.state == FlowControl.State.Start and self._direction == TransmissionDirection.Read:
                self._responseStartTime = message.startTime

    def handleDeviceMessage(self, message: DeviceMessage):
        if self._state == CommChannelISDU.State.RequestFinished:
            self._isduRequest.setEndTime(message.endTime)

            self._state = CommChannelISDU.State.WaitForResponse
            return self._isduRequest

        elif self._state == CommChannelISDU.State.WaitForResponse:
            if self._flowControl.state == FlowControl.State.Start:
                if len(message.od) > 0 and IService(message.od[0]).service != IServiceNibble.NoService:
                    self._isduResponse = createISDUResponse(IService(message.od[0]))

                    self._isduResponse.setTime(self._responseStartTime, message.endTime)
                    self._isduResponse.appendOctets(self._flowControl, message.od)

                    if self._isduResponse.isComplete:
                        self._state = CommChannelISDU.State.Idle
                        return self._isduResponse
                    else:
                        self._state = CommChannelISDU.State.Response

        elif self._state == CommChannelISDU.State.Response:
            if self._flowControl.state == FlowControl.State.Count:
                self._isduResponse.setEndTime(message.endTime)
                self._isduResponse.appendOctets(self._flowControl, message.od)

                if self._isduResponse.isComplete:
                    self._state = CommChannelISDU.State.Idle
                    return self._isduResponse

            elif self._flowControl.state == FlowControl.State.Abort:
                self._state = CommChannelISDU.State.Idle
