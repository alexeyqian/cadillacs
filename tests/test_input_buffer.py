from game.input.player_input_tracker import PlayerInputTracker


def test_input_buffer_keeps_attack_until_duration_expires():
    buffer = PlayerInputTracker()

    buffer.press_attack()
    assert buffer.has_attack() is True

    for _ in range(PlayerInputTracker.ATTACK_BUFFER_FRAMES):
        buffer.advance_timers()

    assert buffer.has_attack() is False


def test_input_buffer_consume_attack_clears_it():
    buffer = PlayerInputTracker()
    buffer.press_attack()

    buffer.consume_attack()

    assert buffer.has_attack() is False


def test_input_buffer_jump_and_attack_are_independent():
    buffer = PlayerInputTracker()
    buffer.press_jump()
    buffer.press_attack()

    buffer.consume_jump()

    assert buffer.has_jump() is False
    assert buffer.has_attack() is True
