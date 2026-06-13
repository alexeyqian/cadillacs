import pygame

class HitSpark:
    image = None
    image_load_failed = False
    image_path = "assets/effects/hit_spark.png"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        self.timer = 12
        self.duration = self.timer
        self.active = True

    @classmethod
    def get_image(cls):
        if cls.image_load_failed:
            return None
        if cls.image is None:
            try:
                cls.image = pygame.image.load(cls.image_path).convert_alpha()
            except pygame.error:
                cls.image_load_failed = True
                return None
        return cls.image
        
    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.active = False
            
    def draw(self, screen, camera_x):
        screen_x = self.x - camera_x
        image = self.get_image()
        if image:
            life_ratio = max(0.0, self.timer / self.duration)
            scale = 0.65 + (1.0 - life_ratio) * 0.45
            alpha = int(255 * life_ratio)
            size = max(1, int(image.get_width() * scale))
            spark_image = pygame.transform.smoothscale(image, (size, size))
            spark_image.set_alpha(alpha)
            screen.blit(
                spark_image,
                (
                    int(screen_x - size / 2),
                    int(self.y - size / 2),
                )
            )
            return

        radius = self.timer * 2
        
        pygame.draw.circle(
            screen,
            (255, 255, 120),
            (int(screen_x), int(self.y)),
            radius,
            2
        )

        pygame.draw.line(
            screen,
            (255, 255, 255),
            (screen_x - radius, self.y),
            (screen_x + radius, self.y),
            2
        )

        pygame.draw.line(
            screen,
            (255, 255, 255),
            (screen_x, self.y - radius),
            (screen_x, self.y + radius),
            2
        )
