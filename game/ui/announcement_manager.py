class AnnouncementManager:
    def __init__(self):
        self.active = False
        self.title = ""
        self.subtitle = ""
        self.timer = 0

    def show(self, title, subtitle="", duration=180):
        self.active = True
        self.title = str(title)
        self.subtitle = str(subtitle)
        self.timer = duration

    def update(self):
        if not self.active:
            return
        self.timer -= 1
        if self.timer <= 0:
            self.active = False
