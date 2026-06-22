import pytest

from snaplex.services import ClipboardError, InMemoryClipboardService, QtClipboardService


class FakeDesktopClipboard:
    def __init__(self, text: str = "") -> None:
        self._text = text

    def text(self) -> str:
        return self._text

    def setText(self, text: str) -> None:
        self._text = text


class FailingDesktopClipboard:
    def text(self) -> str:
        raise RuntimeError("read failed")

    def setText(self, text: str) -> None:
        raise RuntimeError("write failed")


def test_in_memory_clipboard_reads_and_writes_text() -> None:
    clipboard = InMemoryClipboardService("hello")

    assert clipboard.get_text() == "hello"

    clipboard.set_text("hola")

    assert clipboard.get_text() == "hola"


def test_in_memory_clipboard_can_be_empty() -> None:
    clipboard = InMemoryClipboardService()

    assert clipboard.get_text() == ""


def test_qt_clipboard_adapter_reads_and_writes_text_from_injected_clipboard() -> None:
    desktop_clipboard = FakeDesktopClipboard("hello")
    clipboard = QtClipboardService(desktop_clipboard)

    assert clipboard.get_text() == "hello"

    clipboard.set_text("hola")

    assert clipboard.get_text() == "hola"


def test_qt_clipboard_adapter_maps_read_errors() -> None:
    clipboard = QtClipboardService(FailingDesktopClipboard())

    with pytest.raises(ClipboardError, match="read clipboard"):
        clipboard.get_text()


def test_qt_clipboard_adapter_maps_write_errors() -> None:
    clipboard = QtClipboardService(FailingDesktopClipboard())

    with pytest.raises(ClipboardError, match="write clipboard"):
        clipboard.set_text("hola")
