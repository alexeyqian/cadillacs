from game.input.input_buffer import InputBuffer


def test_input_buffer_keeps_attack_until_duration_expires():
    buffer = InputBuffer()

    buffer.press_attack(2)

    assert buffer.has_attack() is True
    buffer.update()
    assert buffer.has_attack() is True
    buffer.update()
    assert buffer.has_attack() is False


def test_input_buffer_consume_attack_clears_it():
    buffer = InputBuffer()
    buffer.press_attack(6)

    buffer.consume_attack()

    assert buffer.has_attack() is False


def test_input_buffer_jump_and_attack_are_independent():
    buffer = InputBuffer()
    buffer.press_jump(6)
    buffer.press_attack(12)

    buffer.consume_jump()

    assert buffer.has_jump() is False
    assert buffer.has_attack() is True
