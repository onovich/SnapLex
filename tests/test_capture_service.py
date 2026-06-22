from types import SimpleNamespace

import pytest

from snaplex.services import CaptureError, FakeCaptureService, MssCaptureService, ScreenRegion
from snaplex.services.capture_service import _load_mss_dependencies


def test_screen_region_exposes_edges_and_area() -> None:
    region = ScreenRegion(left=10, top=20, width=30, height=40)

    assert region.right == 40
    assert region.bottom == 60
    assert region.area == 1200


def test_screen_region_can_be_built_from_drag_points() -> None:
    region = ScreenRegion.from_points(start_x=80, start_y=90, end_x=20, end_y=30)

    assert region == ScreenRegion(left=20, top=30, width=60, height=60)


def test_screen_region_rejects_zero_sized_drag() -> None:
    with pytest.raises(ValueError, match="width and height"):
        ScreenRegion.from_points(start_x=10, start_y=10, end_x=10, end_y=20)


def test_fake_capture_records_regions_and_returns_image() -> None:
    service = FakeCaptureService(image_data=b"fixture", image_format="jpeg")
    region = ScreenRegion(left=1, top=2, width=3, height=4)

    image = service.capture_region(region)

    assert service.regions == [region]
    assert image.region == region
    assert image.data == b"fixture"
    assert image.image_format == "jpeg"


def test_fake_capture_can_fail_once() -> None:
    service = FakeCaptureService()
    region = ScreenRegion(left=1, top=2, width=3, height=4)
    service.fail_next()

    with pytest.raises(CaptureError):
        service.capture_region(region)

    assert service.capture_region(region).region == region
    assert service.regions == [region, region]


def test_mss_capture_adapter_uses_region_and_encoder() -> None:
    region = ScreenRegion(left=10, top=20, width=30, height=40)
    grabbed_monitors: list[dict[str, int]] = []
    encoded: list[tuple[bytes, tuple[int, int]]] = []

    class FakeMss:
        def __enter__(self):
            return self

        def __exit__(self, *args) -> None:
            return None

        def grab(self, monitor: dict[str, int]):
            grabbed_monitors.append(monitor)
            return SimpleNamespace(rgb=b"rgb", size=(30, 40))

    def encode_png(rgb: bytes, size: tuple[int, int]) -> bytes:
        encoded.append((rgb, size))
        return b"png"

    service = MssCaptureService(mss_factory=FakeMss, png_encoder=encode_png)

    image = service.capture_region(region)

    assert grabbed_monitors == [{"left": 10, "top": 20, "width": 30, "height": 40}]
    assert encoded == [(b"rgb", (30, 40))]
    assert image.region == region
    assert image.data == b"png"
    assert image.image_format == "png"


def test_mss_capture_adapter_maps_grab_failures() -> None:
    class FailingMss:
        def __enter__(self):
            return self

        def __exit__(self, *args) -> None:
            return None

        def grab(self, monitor: dict[str, int]):
            raise RuntimeError("screen denied")

    service = MssCaptureService(mss_factory=FailingMss, png_encoder=lambda rgb, size: b"unused")

    with pytest.raises(CaptureError, match="Failed to capture"):
        service.capture_region(ScreenRegion(left=10, top=20, width=30, height=40))


def test_mss_dependency_loader_maps_missing_dependency() -> None:
    def missing_import(module_name: str):
        raise ModuleNotFoundError(module_name)

    with pytest.raises(CaptureError, match="mss is required"):
        _load_mss_dependencies(import_module=missing_import)
