from game.combat.hit_reaction import HitReaction
from game.controllers.player_reaction_controller import PlayerReactionController
from game.components.player_reaction_state import PlayerReactionState


class FakeHealth:
    def __init__(self, hp=100):
        self.hp = hp
        self.damage_taken = 0

    def take_damage(self, damage):
        self.damage_taken += damage
        self.hp = max(0, self.hp - damage)

    def is_dead(self):
        return self.hp <= 0


class FakeCombat:
    def __init__(self):
        self.cancelled = False

    def cancel_attack(self, owner):
        self.cancelled = True


class FakeAttackMovement:
    def __init__(self):
        self.cancelled_run_attack = False
        self.cancelled_combo_nudge = False

    def cancel_run_attack_momentum(self):
        self.cancelled_run_attack = True

    def cancel_combo_finisher_nudge(self):
        self.cancelled_combo_nudge = True


class FakeMovement:
    def __init__(self):
        self.attack_movement = FakeAttackMovement()


class FakeGrabState:
    def __init__(self):
        self.grabbed_enemy = object()


class FakeLifecycle:
    def __init__(self):
        self.lost_life = False
        self.entered_dead_state = False

    def lose_life(self, owner):
        self.lost_life = True

    def enter_dead_state(self, owner):
        self.entered_dead_state = True
        owner.state = owner.DEAD


class FakeStateMachine:
    def change_to(self, owner, state):
        owner.state = state


class FakeOwner:
    IDLE = "IDLE"
    HIT = "HIT"
    DEAD = "DEAD"

    def __init__(self, hp=100, default_stun_frames=10):
        self.state = self.IDLE
        self.health = FakeHealth(hp)
        self.combat_controller = FakeCombat()
        self.movement = FakeMovement()
        self.grab_state = FakeGrabState()
        self.lifecycle_controller = FakeLifecycle()
        self.state_machine = FakeStateMachine()
        self.reaction_state = PlayerReactionState(default_stun_frames)

    def _cancel_combat_commitment(self):
        self.combat_controller.cancel_attack(self)
        self.movement.attack_movement.cancel_run_attack_momentum()
        self.movement.attack_movement.cancel_combo_finisher_nudge()
        self.grab_state.grabbed_enemy = None

    def _on_death(self):
        self.lifecycle_controller.lose_life(self)
        self.lifecycle_controller.enter_dead_state(self)


def test_player_reaction_controller_applies_damage_and_hit_stun():
    owner = FakeOwner(hp=100, default_stun_frames=10)
    reaction = HitReaction(stun_frames=8)
    controller = PlayerReactionController()

    controller.take_damage(owner, 12, reaction)

    assert owner.health.damage_taken == 12
    assert owner.state == owner.HIT
    assert controller.is_in_hit_stun(owner)
    assert owner.reaction_state._hit_stun_remaining == 8
    assert owner.combat_controller.cancelled is True
    assert owner.movement.attack_movement.cancelled_run_attack is True
    assert owner.movement.attack_movement.cancelled_combo_nudge is True
    assert owner.grab_state.grabbed_enemy is None


def test_player_reaction_controller_enters_dead_state_on_depleted_health():
    owner = FakeOwner(hp=10, default_stun_frames=10)
    controller = PlayerReactionController()

    controller.take_damage(owner, 12)

    assert owner.lifecycle_controller.lost_life is True
    assert owner.lifecycle_controller.entered_dead_state is True
    assert owner.state == owner.DEAD
    assert not controller.is_in_hit_stun(owner)
