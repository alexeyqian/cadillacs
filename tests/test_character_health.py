from game.components.character_health import CharacterHealth
from game.entities.enemy_health import EnemyHealth
from game.combat.hit_reaction import HitReaction
from game.entities.player_health import PlayerHealth


def test_character_health_applies_damage_and_clamps_to_zero():
    health = CharacterHealth(max_hp=30)

    depleted = health.apply_damage(40)

    assert depleted is True
    assert health.hp == 0
    assert health.is_depleted() is True


def test_character_health_can_restore_full_hp():
    health = CharacterHealth(max_hp=30)
    health.apply_damage(10)

    health.restore_full()

    assert health.hp == 30


def test_enemy_health_uses_shared_depletion_logic():
    health = EnemyHealth(max_hp=20)

    assert health.take_damage(10) is False
    assert health.hp == 10
    assert health.take_damage(10) is True
    assert health.is_dead() is True


def test_player_health_keeps_lives_and_respawn_rules_on_depletion():
    health = PlayerHealth(max_hp=20, lives=2, hit_stun_duration=8)

    lost_life = health.take_damage(25)

    assert lost_life is True
    assert health.hp == 0
    assert health.lives == 1
    assert health.respawn_remaining == 90


def test_player_health_accepts_shared_hit_reaction_stun_frames():
    health = PlayerHealth(max_hp=50, lives=1, hit_stun_duration=8)

    health.take_damage(5, reaction=HitReaction(stun_frames=14))

    assert health.hp == 45
    assert health.hit_stun_remaining == 14


def test_player_health_keeps_legacy_hit_stun_bonus_argument():
    health = PlayerHealth(max_hp=50, lives=1, hit_stun_duration=8)

    health.take_damage(5, 3)

    assert health.hp == 45
    assert health.hit_stun_remaining == 11
