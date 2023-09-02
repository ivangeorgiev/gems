
from unittest.mock import Mock, patch
from .events import Event, handle, HANDLERS

class FakeEvent(Event):
    pass

class Test_handle_Function:
    def test_should_call_registered_handler(self):
        handler = Mock()
        event = FakeEvent()
        with patch.dict(HANDLERS, {FakeEvent: [handler]}):
            handle(event)
        handler.assert_called_once_with(event)

    def test_should_pass_without_error_if_no_registered_handler(self):
        ev = Mock(Event)
        handle(ev)
