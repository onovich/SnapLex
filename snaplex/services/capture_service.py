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

    @classmethod
    def from_points(
        cls,
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
    ) -> "ScreenRegion":
        left = min(start_x, end_x)
        top = min(start_y, end_y)
        width = abs(end_x - start_x)
        height = abs(end_y - start_y)
        return cls(left=left, top=top, width=width, height=height)

    @property
    def right(self) -> int:
        return self.left + self.width

    @property
    def bottom(self) -> int:
        return self.top + self.height

    @property
    def area(self) -> int:
        return self.width * self.height


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
    def __init__(
        self, image_data: bytes = b"snaplex-fake-image", image_format: str = "png"
    ) -> None:
        self._image_data = image_data
        self._image_format = image_format
        self._fail = False
        self.regions: list[ScreenRegion] = []

    def fail_next(self) -> None:
        self._fail = True

    def capture_region(self, region: ScreenRegion) -> CapturedImage:
        self.regions.append(region)
        if self._fail:
            self._fail = False
            raise CaptureError("Fake capture service was configured to fail.")

        return CapturedImage(region=region, data=self._image_data, image_format=self._image_format)
