from game.components.enemy_condition import EnemyCondition
from game.controllers.enemy_reaction_controller import EnemyReactionController
from game.controllers.enemy_lifecycle_controller import EnemyLifecycleController
from game.entities.enemy_state import EnemyState


class FakeOwner:
    def __init__(self):
        self.x = 100
        self.facing_right = False


def test_enemy_condition_ticks_action_lock_and_hit_stun():
    condition = EnemyCondition()

    condition.set_action_lock(2)
    condition.set_hit_stun(2)

    condition.tick_action_lock()
    condition.tick_hit_stun()

    assert condition._action_lock_remaining == 1
    assert condition._hit_stun_remaining == 1
    assert condition.has_action_lock() is True
    assert condition.has_hit_stun() is True


def test_reaction_controller_applies_knockback():
    owner = FakeOwner()
    owner.condition = EnemyCondition()
    owner.condition.set_knockback(0.4)

    EnemyReactionController()._apply_knockback(owner)

    assert owner.x == 100.4
    assert owner.condition._knockback_velocity == 0


def test_lifecycle_controller_applies_thrown_motion():
    class ThrownOwner:
        state = EnemyState.THROWN
        x = 100
        facing_right = False
        condition = EnemyCondition()

    owner = ThrownOwner()
    owner.condition.start_thrown(direction=1, damage=12, velocity=2, duration=1)

    EnemyLifecycleController()._update_thrown_state(owner)

    assert owner.x == 102
    assert owner.facing_right is True
    assert owner.state == EnemyState.KNOCKDOWN
    assert owner.condition.throw_damage == 12


def test_enemy_condition_manages_thrown_hit_targets():
    target = object()
    condition = EnemyCondition()
    condition.start_thrown(direction=1, damage=12)

    condition.mark_thrown_hit(target)

    assert condition.has_thrown_hit(target) is True


def test_enemy_condition_manages_knockdown_getup_and_death():
    condition = EnemyCondition()

    condition.start_knockdown(duration=1)
    condition.start_getup(duration=1)
    condition.start_death_countdown(duration=1)
    knockdown_finished = condition.tick_knockdown()
    getup_finished = condition.tick_getup()
    condition.tick_death()

    assert knockdown_finished is True
    assert getup_finished is True
    assert condition.is_death_finished() is True
