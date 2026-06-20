from game.components.character_health import CharacterHealth


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


def test_character_health_reports_dead_state():
    health = CharacterHealth(max_hp=20)

    assert health.take_damage(10) is None
    assert health.hp == 10
    assert health.is_dead() is False
    assert health.take_damage(10) is None
    assert health.is_dead() is True
