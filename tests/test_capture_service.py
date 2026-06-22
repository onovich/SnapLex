import pytest

from snaplex.services import CaptureError, FakeCaptureService, ScreenRegion


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
