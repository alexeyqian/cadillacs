class EventBus:
    """Decoupled publish-subscribe channel shared across the scene."""

    def on(self, event: str, handler):
        pass
    def off(self, event: str, handler):
        pass
    def emit(self, event: str, payload):
        pass