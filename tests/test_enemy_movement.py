from game.components.enemy_movement import EnemyMovement


class FakeOwner:
    DEAD = "DEAD"

    def __init__(self, x=100, y=200):
        self.x = x
        self.y = y
        self.facing_right = False
        self.state = "IDLE"


class FakeFlanking:
    def has_target(self):
        return False


class FakePlayer:
    def __init__(self, x=120, y=220):
        self.x = x
        self.y = y


def test_enemy_movement_owns_patrol_runtime_state():
    owner = FakeOwner(x=115)
    movement = EnemyMovement(
        speed=3,
        patrol_distance=10,
        detect_range=300,
        patrol_direction=1,
    )

    movement.patrol(owner, patrol_center_x=100)

    assert movement.patrol_direction == -1
    assert owner.facing_right is True


def test_enemy_movement_uses_component_speed_when_chasing():
    owner = FakeOwner(x=100, y=200)
    movement = EnemyMovement(speed=4)

    movement.move_toward_player(owner, FakePlayer())

    assert owner.x == 104
    assert owner.y == 204
