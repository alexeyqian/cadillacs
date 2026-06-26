from game.components.enemy_reaction_state import EnemyReactionState
from game.controllers.enemy_reaction_controller import EnemyReactionController
from game.controllers.enemy_state_controller import EnemyStateController
from game.entities.enemy_state import EnemyState


def _make_owner(x=100, facing_right=False):
    class Owner:
        pass
    owner = Owner()
    owner.x = x
    owner.facing_right = facing_right
    owner.reaction_state = EnemyReactionState()
    owner.reaction_controller = EnemyReactionController()
    return owner


def test_enemy_reaction_state_ticks_action_lock_and_hit_stun():
    owner = _make_owner()
    rc = owner.reaction_controller

    rc.set_action_lock(owner, 2)
    owner.reaction_state._hit_stun_remaining = 2

    rc.tick_action_lock(owner)
    rc._tick_hit_stun(owner)

    assert owner.reaction_state._action_lock_remaining == 1
    assert owner.reaction_state._hit_stun_remaining == 1
    assert rc.has_action_lock(owner) is True
    assert owner.reaction_state._hit_stun_remaining > 0


def test_reaction_controller_applies_knockback():
    owner = _make_owner()
    owner.reaction_state._knockback_velocity = 0.4

    EnemyReactionController()._apply_knockback(owner)

    assert owner.x == 100.4
    assert owner.reaction_state._knockback_velocity == 0


def test_lifecycle_controller_applies_thrown_motion():
    class ThrownOwner:
        KNOCKDOWN = EnemyState.KNOCKDOWN
        state = EnemyState.THROWN
        x = 100
        facing_right = False
        reaction_state = EnemyReactionState()
        reaction_controller = EnemyReactionController()

    owner = ThrownOwner()
    owner.reaction_controller.start_thrown(owner, direction=1, damage=12, velocity=2, duration=1)

    EnemyStateController()._update_thrown_state(owner)

    assert owner.x == 102
    assert owner.facing_right is True
    assert owner.state == EnemyState.KNOCKDOWN
    assert owner.reaction_state.throw_damage == 12


def test_enemy_reaction_controller_manages_thrown_hit_targets():
    target = object()
    owner = _make_owner()
    rc = owner.reaction_controller
    rc.start_thrown(owner, direction=1, damage=12)

    rc.mark_thrown_hit(owner, target)

    assert rc.has_thrown_hit(owner, target) is True


def test_enemy_reaction_controller_manages_knockdown_getup_and_death():
    owner = _make_owner()
    rc = owner.reaction_controller

    rc.start_knockdown(owner, duration=1)
    rc.start_getup(owner, duration=1)
    owner.reaction_state._death_remaining = 1

    knockdown_finished = rc.tick_knockdown(owner)
    getup_finished = rc.tick_getup(owner)
    rc.tick_death(owner)

    assert knockdown_finished is True
    assert getup_finished is True
    assert rc.is_death_finished(owner) is True
