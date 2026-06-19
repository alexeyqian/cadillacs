import pygame
from game.settings import (
    BAT_DAMAGE,
    FIST_DAMAGE,
    KNIFE_DAMAGE,
    PISTOL_DAMAGE,
    PLAYER_W,
)
from game.managers.asset_manager import AssetManager

KNIFE_IMAGE_FILE = "game/assets/weapon/knife.png"

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
            self.width = PLAYER_W*0.5
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

    def _create_knife_icon(self):
        # create a small surface with transparent background and draw a simple knife
        w = max(48, self.width * 2)
        h = max(20, self.height * 2)
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        # blade (light gray) - a tapered polygon
        blade_color = (200, 200, 200)
        blade_pts = [
            (4, h//2 - 4),
            (w - 12, h//2 - 8),
            (w - 4, h//2),
            (w - 12, h//2 + 8),
            (4, h//2 + 4)
        ]
        pygame.draw.polygon(surf, blade_color, blade_pts)
        # handle (dark brown)
        handle_color = (90, 45, 20)
        pygame.draw.rect(surf, handle_color, (0, h//2 - 6, 10, 12))
        # rivets on handle
        pygame.draw.circle(surf, (200,200,200), (6, h//2), 2)
        pygame.draw.circle(surf, (200,200,200), (6, h//2 - 5), 2)
        return surf

    def _create_bat_icon(self):
        w = max(60, self.width * 2)
        h = max(18, self.height * 2)
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        shaft_color = (160, 90, 40)
        # draw shaft
        shaft_rect = (4, h//2 - 4, w - 8, 8)
        pygame.draw.rect(surf, shaft_color, shaft_rect)
        # rounded end (larger circle)
        end_color = (120, 70, 30)
        pygame.draw.ellipse(surf, end_color, (w - 18, h//2 - 9, 18, 18))
        # small highlight
        pygame.draw.rect(surf, (200,160,120), (w - 14, h//2 - 4, 6, 8))
        return surf

    def _create_pistol_icon(self):
        w = max(48, self.width * 2)
        h = max(24, self.height * 2)
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        # body
        body_color = (60, 60, 60)
        pygame.draw.rect(surf, body_color, (4, h//2 - 6, w - 18, 12))
        # barrel
        pygame.draw.rect(surf, (30,30,30), (w - 18, h//2 - 3, 14, 6))
        # grip (angled) as polygon
        grip_color = (40, 40, 40)
        grip_pts = [
            (10, h//2 + 6),
            (18, h//2 + 6),
            (w - 6, h//2 + 18),
            (w - 12, h//2 + 18)
        ]
        pygame.draw.polygon(surf, grip_color, grip_pts)
        # small highlight on barrel
        pygame.draw.rect(surf, (120,120,120), (w - 14, h//2 - 2, 6, 4))
        return surf

    def draw(self, screen, camera_x):
        if self.picked_up:
            return

        screen_x = self.get_left() - camera_x
        screen_y = self.get_top()

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
                    self._icon_knife = self._create_knife_icon()
                icon = pygame.transform.scale(self._icon_knife,
                    (self.width * 2, self.height * 2))
                icon_x = self.x - camera_x - icon.get_width() // 2
                icon_y = self.y - icon.get_height()
            screen.blit(icon, (icon_x, icon_y))
        elif self.weapon_type == "bat":
            if self._icon_bat is None:
                self._icon_bat = self._create_bat_icon()
            icon = pygame.transform.scale(self._icon_bat, (self.width * 2, self.height * 2))
            icon_x = self.x - camera_x - icon.get_width() // 2
            icon_y = self.y - icon.get_height()
            screen.blit(icon, (icon_x, icon_y))
        else:
            # pistol or other ranged; draw procedural pistol icon
            if self._icon_pistol is None:
                self._icon_pistol = self._create_pistol_icon()
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
