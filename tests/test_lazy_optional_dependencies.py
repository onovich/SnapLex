import importlib
import sys


def test_app_shell_import_does_not_load_capture_or_ocr_backends() -> None:
    sys.modules.pop("mss", None)
    sys.modules.pop("mss.tools", None)
    sys.modules.pop("paddleocr", None)

    importlib.import_module("snaplex.ui.app_shell")

    assert "mss" not in sys.modules
    assert "mss.tools" not in sys.modules
    assert "paddleocr" not in sys.modules


def test_services_import_does_not_load_capture_or_ocr_backends() -> None:
    sys.modules.pop("mss", None)
    sys.modules.pop("mss.tools", None)
    sys.modules.pop("paddleocr", None)

    importlib.import_module("snaplex.services")

    assert "mss" not in sys.modules
    assert "mss.tools" not in sys.modules
    assert "paddleocr" not in sys.modules


def test_services_import_does_not_load_keyring_backend() -> None:
    sys.modules.pop("keyring", None)

    importlib.import_module("snaplex.services")

    assert "keyring" not in sys.modules
