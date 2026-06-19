from game.components.enemy_life_cycle import EnemyLifeCycle


class FakeOwner:
    def __init__(self):
        self.x = 100
        self.facing_right = False


def test_enemy_life_cycle_ticks_action_lock_and_hit_stun():
    life_cycle = EnemyLifeCycle()

    life_cycle.set_action_lock(2)
    life_cycle.set_hit_stun(2)

    life_cycle.tick_action_lock()
    life_cycle.tick_hit_stun()

    assert life_cycle.action_lock_remaining == 1
    assert life_cycle.hit_stun_remaining == 1
    assert life_cycle.has_action_lock() is True
    assert life_cycle.has_hit_stun() is True


def test_enemy_life_cycle_applies_and_clears_knockback():
    owner = FakeOwner()
    life_cycle = EnemyLifeCycle()
    life_cycle.set_knockback(0.4)

    life_cycle.apply_knockback(owner)

    assert owner.x == 100.4
    assert life_cycle.knockback_velocity == 0


def test_enemy_life_cycle_manages_thrown_motion_and_targets():
    owner = FakeOwner()
    target = object()
    life_cycle = EnemyLifeCycle()

    life_cycle.start_thrown(direction=1, damage=12, velocity=2, duration=1)
    finished = life_cycle.tick_thrown(owner)
    life_cycle.mark_thrown_hit(target)

    assert owner.x == 102
    assert owner.facing_right is True
    assert finished is True
    assert life_cycle.throw_damage == 12
    assert life_cycle.has_thrown_hit(target) is True


def test_enemy_life_cycle_manages_knockdown_getup_and_death():
    life_cycle = EnemyLifeCycle()

    life_cycle.start_knockdown(duration=1)
    life_cycle.start_getup(duration=1)
    life_cycle.start_death_countdown(duration=1)
    life_cycle.begin_death_countdown()
    knockdown_finished = life_cycle.tick_knockdown()
    getup_finished = life_cycle.tick_getup()
    life_cycle.tick_death()

    assert knockdown_finished is True
    assert getup_finished is True
    assert life_cycle.death_countdown_started is True
    assert life_cycle.is_death_finished() is True
