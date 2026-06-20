from game.components.character_health import CharacterHealth
from game.entities.enemy_health import EnemyHealth
from game.entities.player_health import PlayerHealth


def test_character_health_applies_damage_and_clamps_to_zero():
    health = CharacterHealth(max_hp=30)

    result = health.take_damage(40)

    assert result is None
    assert health.hp == 0


def test_character_health_can_restore_full_hp():
    health = CharacterHealth(max_hp=30)
    health.take_damage(10)

    health.hp = health.max_hp

    assert health.hp == 30


def test_enemy_health_uses_shared_depletion_logic():
    health = EnemyHealth(max_hp=20)

    assert health.take_damage(10) is None
    assert health.hp == 10
    assert health.is_dead() is False
    assert health.take_damage(10) is None
    assert health.is_dead() is True


def test_player_health_keeps_lives_and_respawn_rules_on_depletion():
    health = PlayerHealth(max_hp=20, lives=2)

    result = health.take_damage(25)
    health.lose_life()

    assert result is None
    assert health.hp == 0
    assert health.lives == 1
    assert health.respawn_remaining == 90


def test_player_health_advance_timers_updates_respawn():
    health = PlayerHealth(max_hp=50, lives=1)
    health.respawn_remaining = 2

    health.advance_timers()

    assert health.respawn_remaining == 1
    assert health.is_respawn_ready() is False

    health.advance_timers()

    assert health.respawn_remaining == 0
    assert health.is_respawn_ready() is True
