import pygame


class Background:
    def __init__(
        self,
        far_file,
        mid_file,
        front_file
    ):
        self.far = pygame.image.load(far_file).convert()
        self.mid = pygame.image.load(mid_file).convert_alpha()
        self.front = pygame.image.load(front_file).convert_alpha()

    def draw_layer(
        self,
        screen,
        image,
        camera_x,
        scroll_speed
    ):
        image_width = image.get_width()

        x = -camera_x * scroll_speed

        # repeat image horizontally
        while x > 0:
            x -= image_width

        while x < screen.get_width():
            screen.blit(image, (x, 0))
            x += image_width

    def draw_back(
        self,
        screen,
        camera_x
    ):
        self.draw_layer(
            screen,
            self.far,
            camera_x,
            0.25
        )

        self.draw_layer(
            screen,
            self.mid,
            camera_x,
            0.55
        )

    def draw_front(
        self,
        screen,
        camera_x
    ):
        self.draw_layer(
            screen,
            self.front,
            camera_x,
            0.85
        )