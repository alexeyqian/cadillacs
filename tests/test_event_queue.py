from game.core.events import GameEventQueue
from game.components.player_weapon_slot import PlayerWeaponSlot
from game.systems.projectile_system import ProjectileSystem

collect_player_projectiles = ProjectileSystem.collect_player


def test_event_queue_drains_matching_events_and_keeps_others():
    events = GameEventQueue()
    events.emit("spawn_projectile", "projectile")
    events.emit("play_sound", "hit")

    drained = events.drain("spawn_projectile")

    assert drained == [{"type": "spawn_projectile", "payload": "projectile"}]
    assert events.drain() == [{"type": "play_sound", "payload": "hit"}]


class FakeWeapon:
    is_ranged = True
    ammo = 2
    damage = 7


class FakeOwner:
    x = 100
    y = 200
    facing_right = True

    def __init__(self):
        self.events = GameEventQueue()

    def get_top(self):
        return self.y - 150


class FakeGameState:
    def __init__(self, player):
        self.player = player
        self.projectiles = []


def test_player_weapon_slot_emits_projectile_event_collected_by_projectile_system():
    owner = FakeOwner()
    weapon_slot = PlayerWeaponSlot()
    weapon_slot.weapon = FakeWeapon()
    game_state = FakeGameState(owner)

    weapon_slot.fire(owner)
    collect_player_projectiles(game_state)

    assert len(game_state.projectiles) == 1
    assert game_state.projectiles[0].damage == 7
    assert weapon_slot.weapon.ammo == 1
    assert owner.events.drain("spawn_projectile") == []
