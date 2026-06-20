from game.combat.hit_reaction import HitReaction
from game.controllers.player_reaction_controller import PlayerReactionController


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

    def cancel_attack(self):
        self.cancelled = True


class FakeMovement:
    def __init__(self):
        self.cancelled_run_attack = False
        self.cancelled_combo_nudge = False

    def cancel_run_attack_momentum(self):
        self.cancelled_run_attack = True

    def cancel_combo_finisher_nudge(self):
        self.cancelled_combo_nudge = True


class FakeGrab:
    def __init__(self):
        self.grabbed_enemy = object()


class FakeLifecycle:
    def __init__(self):
        self.lost_life = False
        self.entered_dead_state = False

    def lose_life(self):
        self.lost_life = True

    def enter_dead_state(self, owner):
        self.entered_dead_state = True
        owner.state = owner.DEAD


class FakeHitReactions:
    def __init__(self):
        self.reaction = None

    def start_hit_stun(self, reaction):
        self.reaction = reaction


class FakeStateMachine:
    def change_to(self, owner, state):
        owner.state = state


class FakeOwner:
    IDLE = "IDLE"
    HIT = "HIT"
    DEAD = "DEAD"

    def __init__(self, hp=100):
        self.state = self.IDLE
        self.health = FakeHealth(hp)
        self.combat_controller = FakeCombat()
        self.movement = FakeMovement()
        self.grab_controller = FakeGrab()
        self.lifecycle_controller = FakeLifecycle()
        self.hit_reaction_controller = FakeHitReactions()
        self.state_machine = FakeStateMachine()


def test_player_reaction_controller_applies_damage_and_hit_stun():
    owner = FakeOwner(hp=100)
    reaction = HitReaction(stun_frames=8)

    PlayerReactionController().take_damage(owner, 12, reaction)

    assert owner.health.damage_taken == 12
    assert owner.state == owner.HIT
    assert owner.hit_reaction_controller.reaction is reaction
    assert owner.combat_controller.cancelled is True
    assert owner.movement.cancelled_run_attack is True
    assert owner.movement.cancelled_combo_nudge is True
    assert owner.grab_controller.grabbed_enemy is None


def test_player_reaction_controller_enters_dead_state_on_depleted_health():
    owner = FakeOwner(hp=10)

    PlayerReactionController().take_damage(owner, 12)

    assert owner.lifecycle_controller.lost_life is True
    assert owner.lifecycle_controller.entered_dead_state is True
    assert owner.state == owner.DEAD
    assert owner.hit_reaction_controller.reaction is None
