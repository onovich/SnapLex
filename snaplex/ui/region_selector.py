"""Screen region selection helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from snaplex.services import ScreenRegion


@dataclass(frozen=True)
class RegionSelectionState:
    start_x: int | None = None
    start_y: int | None = None
    current_x: int | None = None
    current_y: int | None = None
    region: ScreenRegion | None = None
    cancelled: bool = False
    error_message: str = ""
    status_text: str = "Ready to select a screen region."


class RegionSelectionPresenter:
    def __init__(self) -> None:
        self._state = RegionSelectionState()

    @property
    def state(self) -> RegionSelectionState:
        return self._state

    def begin(self, x: int, y: int) -> RegionSelectionState:
        self._state = RegionSelectionState(
            start_x=x,
            start_y=y,
            current_x=x,
            current_y=y,
            status_text="Drag to select a screen region.",
        )
        return self._state

    def update(self, x: int, y: int) -> RegionSelectionState:
        self._state = RegionSelectionState(
            start_x=self._state.start_x,
            start_y=self._state.start_y,
            current_x=x,
            current_y=y,
            status_text="Release to translate the selected region.",
        )
        return self._state

    def confirm(self, x: int, y: int) -> RegionSelectionState:
        if self._state.start_x is None or self._state.start_y is None:
            self._state = RegionSelectionState(
                error_message="Start selecting a region first.",
                status_text="Selection not started.",
            )
            return self._state

        try:
            region = ScreenRegion.from_points(self._state.start_x, self._state.start_y, x, y)
        except ValueError:
            self._state = RegionSelectionState(
                error_message="Select a non-empty screen region.",
                status_text="Selection needs an area.",
            )
            return self._state

        self._state = RegionSelectionState(
            region=region,
            status_text="Region selected.",
        )
        return self._state

    def cancel(self) -> RegionSelectionState:
        self._state = RegionSelectionState(
            cancelled=True,
            status_text="Screen selection cancelled.",
        )
        return self._state


class RegionSelector(Protocol):
    def select_region(self) -> ScreenRegion | None:
        """Return a selected screen region, or None when cancelled."""
        ...


class FixedRegionSelector:
    def __init__(self, region: ScreenRegion) -> None:
        self._region = region

    def select_region(self) -> ScreenRegion | None:
        return self._region


class CancelledRegionSelector:
    def select_region(self) -> ScreenRegion | None:
        return None


class QtRegionSelector:
    def select_region(self) -> ScreenRegion | None:
        try:
            from PySide6.QtCore import QEventLoop, QPoint, QRect, QSize, Qt
            from PySide6.QtWidgets import QApplication, QRubberBand, QWidget
        except ModuleNotFoundError:
            return None

        app = QApplication.instance()
        if app is None:
            return None

        presenter = RegionSelectionPresenter()
        loop = QEventLoop()

        class SelectionOverlay(QWidget):
            def __init__(self) -> None:
                super().__init__()
                self.selected_region: ScreenRegion | None = None
                self._rubber_band = QRubberBand(QRubberBand.Shape.Rectangle, self)
                self._rubber_band.setStyleSheet(
                    "QRubberBand { border: 2px solid #1f6feb; background: rgba(31, 111, 235, 36); }"
                )

            def mousePressEvent(self, event: Any) -> None:
                point = event.position().toPoint()
                presenter.begin(point.x(), point.y())
                self._rubber_band.setGeometry(QRect(point, QSize()))
                self._rubber_band.show()

            def mouseMoveEvent(self, event: Any) -> None:
                point = event.position().toPoint()
                presenter.update(point.x(), point.y())
                state = presenter.state
                if state.start_x is None or state.start_y is None:
                    return
                start = QPoint(state.start_x, state.start_y)
                self._rubber_band.setGeometry(QRect(start, point).normalized())

            def mouseReleaseEvent(self, event: Any) -> None:
                point = event.position().toPoint()
                state = presenter.confirm(point.x(), point.y())
                self.selected_region = state.region
                self.close()
                loop.quit()

            def keyPressEvent(self, event: Any) -> None:
                if event.key() == Qt.Key.Key_Escape:
                    presenter.cancel()
                    self.selected_region = None
                    self.close()
                    loop.quit()

        overlay = SelectionOverlay()
        overlay.setWindowTitle("SnapLex Region Selection")
        overlay.setAccessibleName("Screen region selector")
        overlay.setToolTip("Drag to select a screen region. Press Esc to cancel.")
        overlay.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
        overlay.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        overlay.setWindowOpacity(0.25)
        overlay.setCursor(Qt.CursorShape.CrossCursor)
        overlay.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        overlay.showFullScreen()
        overlay.activateWindow()
        overlay.setFocus()
        loop.exec()
        return overlay.selected_region
