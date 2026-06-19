class InputBuffer:
    def __init__(self, default_frames=6):
        self.default_frames = default_frames
        self._buffered_actions = {}

    def press(self, action, frames=None):
        if frames is None:
            frames = self.default_frames
        self._buffered_actions[action] = max(1, int(frames))

    def update(self):
        expired = []
        for action, frames in self._buffered_actions.items():
            remaining = frames - 1
            if remaining <= 0:
                expired.append(action)
            else:
                self._buffered_actions[action] = remaining

        for action in expired:
            del self._buffered_actions[action]

    def has(self, action):
        return action in self._buffered_actions

    def consume(self, action):
        if action not in self._buffered_actions:
            return False
        del self._buffered_actions[action]
        return True

    def clear(self, action=None):
        if action is None:
            self._buffered_actions.clear()
            return
        self._buffered_actions.pop(action, None)
