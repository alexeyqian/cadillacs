from game.combat.damage_request import DamageRequest
from game.combat.hit_reaction import HitReaction
from game.entities.enemy import Enemy
from game.entities.player import Player


class FakePlayerReactions:
    def __init__(self):
        self.calls = []

    def take_damage(self, owner, damage, reaction=None):
        self.calls.append((owner, damage, reaction))


class FakeReactions:
    def __init__(self):
        self.calls = []

    def take_damage(self, owner, damage, attacker_x, reaction=None):
        self.calls.append((owner, damage, attacker_x, reaction))


def test_player_accepts_damage_request():
    player = Player.__new__(Player)
    player.reaction_controller = FakePlayerReactions()
    reaction = HitReaction(stun_frames=8, knockback_velocity=4)

    player.take_damage(DamageRequest(12, reaction=reaction))

    assert player.reaction_controller.calls == [(player, 12, reaction)]


def test_enemy_accepts_damage_request():
    enemy = Enemy.__new__(Enemy)
    enemy.x = 300
    enemy.reaction_controller = FakeReactions()
    reaction = HitReaction(stun_frames=10, knockback_velocity=6)

    enemy.take_damage(DamageRequest(15, attacker_x=120, reaction=reaction))

    assert enemy.reaction_controller.calls == [(enemy, 15, 120, reaction)]
