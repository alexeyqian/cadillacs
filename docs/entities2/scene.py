from game.entities2.game_object import GameObject

class Scene:
    """Provides object registration, lookup, and the shared event bus."""

    def event_bus(self):
        pass

    def find_by_id(self, entity_id: str) -> GameObject:
        pass

    def find_by_tag(self, tag: str) -> list[GameObject]:
        pass

    def spawn(self, obj: GameObject) -> None:
        pass

    def destroy(self, obj: GameObject) -> None:
        """Schedules object for end-of-frame removal."""
        pass