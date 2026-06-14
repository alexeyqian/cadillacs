class PlayerEvents:
    def __init__(self):
        self.events = []

    def emit(self, event_type, payload=None):
        self.events.append({
            "type": event_type,
            "payload": payload,
        })

    def drain(self, event_type=None):
        drained = []
        remaining = []

        for event in self.events:
            if event_type is None or event["type"] == event_type:
                drained.append(event)
            else:
                remaining.append(event)

        self.events = remaining
        return drained