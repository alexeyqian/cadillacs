import pygame
from game.settings import (
    BAT_DAMAGE,
    FIST_DAMAGE,
    KNIFE_DAMAGE,
    PISTOL_DAMAGE,
    PLAYER_W,
)
from game.managers.asset_manager import AssetManager

KNIFE_IMAGE_FILE = "assets/weapons/knife_3x.png"

# Fist: short range, low damage
# Knife: medium range, fast damage
# Bat: long range, heavy damage
# Pistol: ranged only, no melee bonus

class Weapon:
    def __init__(self, x, y, weapon_type="knife"):
        self.x = x
        self.y = y
        self.weapon_type = weapon_type

        self.width = PLAYER_W*0.6
        self.height = 12

        self.damage = FIST_DAMAGE
        self.picked_up = False

        # cache for procedural icons
        self._knife_image = None
        self._icon_knife = None
        self._icon_bat = None
        self._icon_pistol = None

        self.is_ranged = False
        if weapon_type == "knife":
            self.width = 90
            self.height = 40
            self.damage = KNIFE_DAMAGE
        elif weapon_type == "bat":
            self.width = PLAYER_W
            self.damage = BAT_DAMAGE
        elif weapon_type == "pistol":
            self.width = PLAYER_W
            self.damage = PISTOL_DAMAGE
            self.is_ranged = True
            self.ammo = 10
        else:
            self.damage = FIST_DAMAGE

    def _load_knife_image(self):
        return AssetManager.load_image(KNIFE_IMAGE_FILE, alpha=True)

    def get_overlay_image(self, scale=1.0):
        """Return a scaled pygame Surface for the held-weapon overlay, or None."""
        if self.weapon_type == "knife":
            if self._knife_image is None:
                self._knife_image = self._load_knife_image()
            if self._knife_image is None:
                return None
            w = int(self._knife_image.get_width() * scale)
            h = int(self._knife_image.get_height() * scale)
            return pygame.transform.scale(self._knife_image, (w, h))
        return None

    def draw(self, screen, camera_x):
        if self.picked_up:
            return

        if self.weapon_type == "knife":
            if self._knife_image is None:
                self._knife_image = self._load_knife_image()

            if self._knife_image:
                icon = pygame.transform.scale(
                    self._knife_image,
                    (self.width * 2, self.height * 2)
                )
                icon_x = self.x - camera_x - icon.get_width() // 2
                icon_y = self.y - icon.get_height()
            else:
                # Fallback if the image file is missing or cannot be loaded.
                if self._icon_knife is None:
                    raise ValueError(" Cannot find icon")
                icon = pygame.transform.scale(self._icon_knife,
                    (self.width, self.height))
                icon_x = self.x - camera_x - icon.get_width() // 2
                icon_y = self.y - icon.get_height()
            screen.blit(icon, (icon_x, icon_y))
        elif self.weapon_type == "bat":
            if self._icon_bat is None:
                raise ValueError(" Cannot find icon")
            icon = pygame.transform.scale(self._icon_bat, (self.width * 2, self.height * 2))
            icon_x = self.x - camera_x - icon.get_width() // 2
            icon_y = self.y - icon.get_height()
            screen.blit(icon, (icon_x, icon_y))
        else:
            # pistol or other ranged; draw procedural pistol icon
            if self._icon_pistol is None:
                raise ValueError(" Cannot find icon")
            icon = pygame.transform.scale(self._icon_pistol, (self.width * 2, self.height * 2))
            icon_x = self.x - camera_x - icon.get_width() // 2
            icon_y = self.y - icon.get_height()
            screen.blit(icon, (icon_x, icon_y))

    def get_left(self):
        return self.x - self.width // 2

    def get_top(self):
        return self.y - self.height

    def get_rect(self):
        return pygame.Rect(self.get_left(),self.get_top(),self.width, self.height)
