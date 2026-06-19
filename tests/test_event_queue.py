from game.core.events import GameEventQueue


def test_event_queue_drains_matching_events_and_keeps_others():
    events = GameEventQueue()
    events.emit("spawn_projectile", "projectile")
    events.emit("play_sound", "hit")

    drained = events.drain("spawn_projectile")

    assert drained == [{"type": "spawn_projectile", "payload": "projectile"}]
    assert events.drain() == [{"type": "play_sound", "payload": "hit"}]
