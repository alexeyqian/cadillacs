from game.input.input_buffer import InputBuffer


def test_input_buffer_keeps_action_until_duration_expires():
    buffer = InputBuffer(default_frames=2)

    buffer.press("attack")

    assert buffer.has("attack") is True
    buffer.update()
    assert buffer.has("attack") is True
    buffer.update()
    assert buffer.has("attack") is False


def test_input_buffer_consumes_action_once():
    buffer = InputBuffer()
    buffer.press("jump")

    assert buffer.consume("jump") is True
    assert buffer.consume("jump") is False


def test_input_buffer_can_clear_one_or_all_actions():
    buffer = InputBuffer()
    buffer.press("attack")
    buffer.press("jump")

    buffer.clear("attack")

    assert buffer.has("attack") is False
    assert buffer.has("jump") is True

    buffer.clear()

    assert buffer.has("jump") is False
