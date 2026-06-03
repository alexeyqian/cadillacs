import pygame

class Weapon:
    def __init__(self, x, y, weapon_type="knife"):
        self.x = x
        self.y = y
        self.weapon_type = weapon_type

        self.width = 40
        self.height = 12

        self.damage = 20
        self.picked_up = False
        self.is_range = False
        if weapon_type == "knife":
            self.damage = 25
        elif weapon_type == "bat": # baseball bat
            self.damage = 40
        elif weapon_type == "pistol":
            self.damage = 30
            self.is_range = True
            self.ammo = 20
        else:
            self.damage = 20

    def draw(self, screen, camera_x):
        if self.picked_up:
            return

        screen_x = self.x - camera_x
        if self.weapon_type == "knife":
            color = (220,220,220)
        elif self.weapon_type == "bat":
            color = (160,90,40)
        else:
            color = (255,255,0)

        pygame.draw.rect(screen, color,
            (screen_x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x,self.y,self.width, self.height)


