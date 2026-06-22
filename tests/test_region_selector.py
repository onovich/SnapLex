from snaplex.services import ScreenRegion
from snaplex.ui.region_selector import (
    CancelledRegionSelector,
    FixedRegionSelector,
    RegionSelectionPresenter,
)


def test_region_selection_presenter_confirms_reverse_drag() -> None:
    presenter = RegionSelectionPresenter()

    presenter.begin(120, 80)
    presenter.update(40, 20)
    state = presenter.confirm(40, 20)

    assert state.region == ScreenRegion(left=40, top=20, width=80, height=60)
    assert state.cancelled is False
    assert state.error_message == ""


def test_region_selection_presenter_rejects_empty_selection() -> None:
    presenter = RegionSelectionPresenter()

    presenter.begin(10, 10)
    state = presenter.confirm(10, 30)

    assert state.region is None
    assert state.error_message == "Select a non-empty screen region."


def test_region_selection_presenter_can_cancel() -> None:
    presenter = RegionSelectionPresenter()

    presenter.begin(10, 10)
    state = presenter.cancel()

    assert state.cancelled is True
    assert state.region is None


def test_fixed_region_selector_returns_region() -> None:
    region = ScreenRegion(left=1, top=2, width=3, height=4)

    assert FixedRegionSelector(region).select_region() == region


def test_cancelled_region_selector_returns_none() -> None:
    assert CancelledRegionSelector().select_region() is None
