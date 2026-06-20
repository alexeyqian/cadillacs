from game.components.enemy_condition import EnemyCondition


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

    assert condition.action_lock_remaining == 1
    assert condition.hit_stun_remaining == 1
    assert condition.has_action_lock() is True
    assert condition.has_hit_stun() is True


def test_enemy_condition_applies_and_clears_knockback():
    owner = FakeOwner()
    condition = EnemyCondition()
    condition.set_knockback(0.4)

    condition.apply_knockback(owner)

    assert owner.x == 100.4
    assert condition.knockback_velocity == 0


def test_enemy_condition_manages_thrown_motion_and_targets():
    owner = FakeOwner()
    target = object()
    condition = EnemyCondition()

    condition.start_thrown(direction=1, damage=12, velocity=2, duration=1)
    finished = condition.tick_thrown(owner)
    condition.mark_thrown_hit(target)

    assert owner.x == 102
    assert owner.facing_right is True
    assert finished is True
    assert condition.throw_damage == 12
    assert condition.has_thrown_hit(target) is True


def test_enemy_condition_manages_knockdown_getup_and_death():
    condition = EnemyCondition()

    condition.start_knockdown(duration=1)
    condition.start_getup(duration=1)
    condition.start_death_countdown(duration=1)
    condition.begin_death_countdown()
    knockdown_finished = condition.tick_knockdown()
    getup_finished = condition.tick_getup()
    condition.tick_death()

    assert knockdown_finished is True
    assert getup_finished is True
    assert condition.death_countdown_started is True
    assert condition.is_death_finished() is True
