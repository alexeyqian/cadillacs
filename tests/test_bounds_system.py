from game.systems.bounds_system import BoundsSystem


class FakeCharacter:
    def __init__(self):
        self.bounds_calls = []

    def apply_world_bounds(self, world_width=None, lane_top=None, lane_bottom=None):
        self.bounds_calls.append((world_width, lane_top, lane_bottom))


class FakeLevel:
    world_width = 1000
    lane_top = 300
    lane_bottom = 800


class FakeGameState:
    def __init__(self):
        self.level = FakeLevel()
        self.player = FakeCharacter()
        self.enemies = [FakeCharacter(), FakeCharacter()]


def test_apply_player_level_bounds_calls_world_bounds():
    game_state = FakeGameState()

    BoundsSystem.apply_player_level(game_state)

    assert game_state.player.bounds_calls == [(1000, 300, 800)]


def test_apply_enemy_level_bounds_calls_world_bounds_for_each_enemy():
    game_state = FakeGameState()

    BoundsSystem.apply_enemy_level(game_state)

    assert game_state.enemies[0].bounds_calls == [(1000, 300, 800)]
    assert game_state.enemies[1].bounds_calls == [(1000, 300, 800)]
