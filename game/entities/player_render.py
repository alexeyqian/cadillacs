import pygame


class PlayerRenderer:
    #World:   [--------------------PLAYER----]
    #                          x=800
    #Screen window starts at camera_x=600:
    #	      [    window    ]
    #	       600          1200
    #Player appears at pixel 200 inside the window → screen_x = 200
    def draw(self, owner, screen, camera_x):
        # camera_x is how far the camera has scrolled.
        # Subtracting it converts the player's world position->screen position
        # player's screen x position after camera offset
        # bottom-center screen x:
        # add depth
        # Now moving up/down looks more like a beat'em-up character walking in depth.
        # shadow_rect = pygame.Rect(screen_x,self.y + self.height - 10,self.width,12)
        #pygame.draw.ellipse(screen,(50, 50, 50),shadow_rect)
        # end of depth
        screen_x = owner.x - camera_x

        image = owner.animation_controller.get_image()
        scale = owner.sprite_scale
        image = pygame.transform.scale(
            image,
            (image.get_width() * scale, image.get_height() * scale)
        )

        if not owner.facing_right:
            image = pygame.transform.flip(image, True, False)

        frame = owner.get_current_player_frame()
        offset_x, offset_y = frame.offset
        offset_x *= scale
        offset_y *= scale

        if owner.facing_right:
            sprite_world_x = owner.x + offset_x
        else:
            sprite_world_x = owner.x - image.get_width() - offset_x

        sprite_y = owner.y + offset_y
        screen.blit(image, (sprite_world_x - camera_x, sprite_y))

        self.draw_weapon_debug(owner, screen, screen_x)
        self.draw_health_bar(owner, screen, screen_x)

    def draw_weapon_debug(self, owner, screen, screen_x):
        if not owner.weapon:
            return

        weapon_len = 20
        if not owner.weapon.is_ranged:
            weapon_len += owner.weapon.hitbox_w_bonus

        weapon_x = screen_x + owner.width
        if not owner.facing_right:
            weapon_x = screen_x - weapon_len

        pygame.draw.rect(
            screen,
            (255, 255, 0),
            (weapon_x, owner.y + 30, weapon_len, 5)
        )

    def draw_health_bar(self, owner, screen, screen_x):
        hb_w = owner.width
        hb_h = 8
        hb_x = int(screen_x - hb_w / 2)
        hb_y = owner.get_top() - 16

        pygame.draw.rect(screen, (100, 100, 100), (hb_x, hb_y, hb_w, hb_h))

        try:
            fill_ratio = max(0.0, min(1.0, float(owner.hp) / float(owner.max_hp)))
        except Exception:
            fill_ratio = 0

        hp_w = int(hb_w * fill_ratio)
        pygame.draw.rect(screen, (0, 255, 0), (hb_x, hb_y, hp_w, hb_h))