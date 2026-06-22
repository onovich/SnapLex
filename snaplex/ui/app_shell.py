"""Minimal desktop shell for SnapLex."""

from __future__ import annotations


def is_pyside_available() -> bool:
    try:
        import PySide6.QtWidgets  # noqa: F401
    except ModuleNotFoundError:
        return False

    return True


def launch_gui() -> int:
    try:
        from PySide6.QtCore import Qt
        from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget
    except ModuleNotFoundError:
        print(
            "PySide6 is not installed. Run `python -m pip install -e .[gui]` "
            "to start the desktop shell, or `python -m snaplex --no-gui` "
            "for a bootstrap check."
        )
        return 0

    app = QApplication.instance() or QApplication([])

    window = QMainWindow()
    window.setWindowTitle("SnapLex")
    window.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)

    central = QWidget()
    layout = QVBoxLayout(central)
    layout.addWidget(QLabel("SnapLex"))
    layout.addWidget(QLabel("Ready"))

    window.setCentralWidget(central)
    window.resize(320, 160)
    window.show()

    return app.exec()
