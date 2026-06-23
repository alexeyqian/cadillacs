from game import display
from game.settings import SCREEN_HEIGHT, SCREEN_WIDTH


class FakeDisplayInfo:
    current_w = 1470
    current_h = 956


def test_window_size_uses_internal_resolution_by_default(monkeypatch):
    monkeypatch.setattr(display, "FIT_WINDOW_TO_DISPLAY", False)

    assert display.get_window_size() == (SCREEN_WIDTH, SCREEN_HEIGHT)


def test_window_size_can_fit_to_display_when_enabled(monkeypatch):
    monkeypatch.setattr(display, "FIT_WINDOW_TO_DISPLAY", True)
    monkeypatch.setattr(display.pygame.display, "Info", lambda: FakeDisplayInfo())

    assert display.get_window_size() == (1470, 826)
