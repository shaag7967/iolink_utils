import pytest

from iolink_utils.definitions.communicationChannel import CommChannel
from iolink_utils.messageInterpreter.messageInterpreter import MessageInterpreter
from iolink_utils.messageInterpreter.isdu.ISDU import ISDU
from iolink_utils.messageInterpreter.page.transactionPage import TransactionPage
from iolink_utils.messageInterpreter.process.transactionProcess import TransactionProcess
from iolink_utils.messageInterpreter.diagnosis.transactionDiagnosis import TransactionDiagEventMemory


@pytest.fixture
def interpreter():
    return MessageInterpreter()


def mock_message(mocker, channel, return_value=None):
    msg = mocker.Mock()
    msg.channel.return_value = channel
    msg.dispatch.return_value = return_value
    return msg


def test_messageInterpreter_initialActiveChannel(interpreter):
    assert interpreter._activeChannel == CommChannel.Process


def test_messageInterpreter_updatesActiveChannel(interpreter, mocker):
    message = mock_message(mocker, CommChannel.Page)
    interpreter.processMessage(message)
    assert interpreter._activeChannel == CommChannel.Page

    message = mock_message(mocker, CommChannel.ISDU)
    interpreter.processMessage(message)
    assert interpreter._activeChannel == CommChannel.ISDU

    message = mock_message(mocker, CommChannel.Diagnosis)
    interpreter.processMessage(message)
    assert interpreter._activeChannel == CommChannel.Diagnosis

    message = mock_message(mocker, CommChannel.Process)
    interpreter.processMessage(message)
    assert interpreter._activeChannel == CommChannel.Process


def test_messageInterpreter_correctHandlerCalledOnMessage(interpreter, mocker):
    # CommChannel.ISDU
    result = mocker.Mock(spec=ISDU)
    message = mock_message(mocker, CommChannel.ISDU, result)

    returned = interpreter.processMessage(message)
    message.dispatch.assert_called_once_with(interpreter._channelHandler[CommChannel.ISDU])
    assert returned is result

    # CommChannel.Page
    result = mocker.Mock(spec=TransactionPage)
    message = mock_message(mocker, CommChannel.Page, result)

    returned = interpreter.processMessage(message)
    message.dispatch.assert_called_once_with(interpreter._channelHandler[CommChannel.Page])
    assert returned is result

    # CommChannel.Diagnosis
    result = mocker.Mock(spec=TransactionDiagEventMemory)
    message = mock_message(mocker, CommChannel.Diagnosis, result)

    returned = interpreter.processMessage(message)
    message.dispatch.assert_called_once_with(interpreter._channelHandler[CommChannel.Diagnosis])
    assert returned is result

    # CommChannel.Process
    result = mocker.Mock(spec=TransactionProcess)
    message = mock_message(mocker, CommChannel.Process, result)

    returned = interpreter.processMessage(message)
    message.dispatch.assert_called_once_with(interpreter._channelHandler[CommChannel.Process])
    assert returned is result


def test_messageInterpreter_activeChannelNotChangedIfNone(interpreter, mocker):
    interpreter._activeChannel = CommChannel.Diagnosis
    message = mock_message(mocker, None)

    interpreter.processMessage(message)

    assert interpreter._activeChannel == CommChannel.Diagnosis


def test_messageInterpreter_processMessageUsesPreviousChannelWhenNone(interpreter, mocker):
    interpreter._activeChannel = CommChannel.Page
    message = mock_message(mocker, None)

    interpreter.processMessage(message)

    handler = interpreter._channelHandler[CommChannel.Page]
    message.dispatch.assert_called_once_with(handler)


def test_messageInterpreter_reset(interpreter, mocker):
    interpreter._activeChannel = CommChannel.ISDU
    for handler in interpreter._channelHandler.values():
        mocker.patch.object(handler, "reset")

    interpreter.reset()

    assert interpreter._activeChannel == CommChannel.Process
    for handler in interpreter._channelHandler.values():
        handler.reset.assert_called_once()
