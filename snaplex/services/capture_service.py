"""Screen capture service contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class CaptureError(RuntimeError):
    """Raised when screen capture cannot complete."""


@dataclass(frozen=True)
class ScreenRegion:
    left: int
    top: int
    width: int
    height: int

    def __post_init__(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError("ScreenRegion width and height must be positive.")


@dataclass(frozen=True)
class CapturedImage:
    region: ScreenRegion
    data: bytes
    image_format: str = "png"


class CaptureService(Protocol):
    def capture_region(self, region: ScreenRegion) -> CapturedImage:
        """Capture an image from a screen region."""
        ...


class FakeCaptureService:
    def __init__(self, image_data: bytes = b"snaplex-fake-image", image_format: str = "png") -> None:
        self._image_data = image_data
        self._image_format = image_format

    def capture_region(self, region: ScreenRegion) -> CapturedImage:
        return CapturedImage(region=region, data=self._image_data, image_format=self._image_format)
