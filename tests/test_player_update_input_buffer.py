from game.controllers.player_action_controller import PlayerActionController
from game.controllers.player_action_context import PlayerActionContext
from game.controllers.player_combat_controller import PlayerCombatController
from game.components.player_intent import PlayerIntent
from game.data.player_config import DEFAULT_PLAYER_ATTACKS
from game.entities.player import Player
from game.entities.player_state_machine import PlayerStateMachine
from game.input.input_buffer import InputBuffer
from game.input.player_input_state import PlayerInputState


class FakeInput:
    def __init__(self, attack=False, jump=False):
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.run = False
        self.jump = jump
        self.attack = attack
        self.fire = False


class FakeMovement:
    def __init__(self):
        self.is_running = False
        self.is_jumping = False
        self.moving = False
        self.last_run_attack_distance = 0

    def advance_timers(self):
        pass

    def update_movement(self, owner, player_input):
        self.moving = False

    def update_jump_physics(self, owner, player_input):
        pass

    def start_jump(self, owner, player_input):
        if owner.combat_controller.is_attacking:
            return
        owner.state_machine.change_to(owner, owner.JUMP_TAKEOFF)

    def can_start_run_attack(self):
        return False

    def start_run_attack_momentum(self, owner):
        pass

    def start_combo_finisher_nudge(self, owner):
        pass

    def cancel_run_attack_momentum(self):
        pass

    def cancel_combo_finisher_nudge(self):
        pass


class FakeGrab:
    grabbed_enemy = None

    def advance_timers(self, owner):
        pass

    def update_grabbed_enemy_position(self, owner):
        pass


class FakeWeaponSlot:
    weapon = None

    def fire(self, owner):
        pass


class FakeLifecycle:
    def update_dead_state(self, owner):
        pass


class FakeReactionController:
    def is_in_hit_stun(self):
        return False

    def update_hit_state(self, owner):
        pass


class FakeStateController:
    def resolve(self, owner, moving):
        if not owner.combat_controller.is_attacking and owner.state not in [owner.JUMP_TAKEOFF, owner.JUMP]:
            owner.state_machine.change_to(owner, owner.IDLE)


class FakeAnimationController:
    def update(self, owner):
        pass


def make_player_like():
    player = Player.__new__(Player)
    player.x = 300
    player.y = 500
    player.state = Player.IDLE
    player.state_machine = PlayerStateMachine(player)
    player.intent = PlayerIntent()
    player.input_buffer = InputBuffer()
    player.input_state = PlayerInputState()
    player.movement = FakeMovement()
    player.air = None
    player.combat_controller = PlayerCombatController()
    player.combat_controller.attacks = DEFAULT_PLAYER_ATTACKS
    player.combat_controller.weapon_attacks = {}
    player.action_controller = PlayerActionController()
    player.grab_controller = FakeGrab()
    player.weapon_slot = FakeWeaponSlot()
    player.lifecycle_controller = FakeLifecycle()
    player.reaction_controller = FakeReactionController()
    player.state_resolver = FakeStateController()
    player.animation_controller = FakeAnimationController()
    return player


def update_player_frame(player, player_input):
    context = PlayerActionContext(player_input)
    lifecycle_blocked = player.state == player.DEAD
    player.update_lifecycle_state()
    player.update_reactions()
    if lifecycle_blocked or player.reaction_controller.is_in_hit_stun():
        player.update_animation()
        return

    player.advance_timers()
    player.request_actions(context)
    player.update_movement(context)
    player.update_attack(context)
    player.update_animation()


def test_player_update_uses_buffered_attack_after_recovery():
    player = make_player_like()

    update_player_frame(player, FakeInput(attack=True))
    assert player.combat_controller.current_attack_name == player.ATTACK

    update_player_frame(player, FakeInput())
    update_player_frame(player, FakeInput(attack=True))
    assert player.input_buffer.has("attack") is True

    player.combat_controller.attack_manager.has_connected = True
    while player.combat_controller.current_attack_name == player.ATTACK:
        update_player_frame(player, FakeInput())

    assert player.combat_controller.current_attack_name == player.ATTACK2
    assert player.input_buffer.has("attack") is False


def test_player_update_jump_buffer_does_not_bypass_attack_lock():
    player = make_player_like()

    update_player_frame(player, FakeInput(attack=True))
    update_player_frame(player, FakeInput(jump=True))

    assert player.input_buffer.has("jump") is True
    assert player.state == player.ATTACK
