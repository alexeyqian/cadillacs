import pygame

class Enemy:
    CHASE = "CHASE"
    ATTACK = "ATTACK"
    HIT = "HIT"
    DEAD = "DEAD"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 80
        self.speed = 2
        self.hp = 100
        self.state = self.CHASE

        # attack players / combat
        self.attack_timer = 0 # ?
        self.attack_cooldown = 0
        self.attack_damage = 10
        self.attack_range = 70

        # hit reaction
        self.knockback_velocity = 0
        # enemy gets briefly white when hit by player
        self.hit_timer = 0

    def update(self, player, enemies):
        if self.state == self.DEAD:
            return
        
        # attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # hit state
        # enemy pauses briefly when hit by player, but can still be knocked back
        if self.hit_timer > 0:
            self.hit_timer -= 1
            self.apply_knockback()
            if self.hit_timer == 0:
                self.state = self.CHASE
            return
        # apply any remaining knockback
        self.apply_knockback()

        # distance to player
        dx = player.x - self.x
        dy = player.y - self.y
        distance_x = abs(dx)

        # state selection
        # attack if close enough
        if distance_x <= self.attack_range:
            self.state = self.ATTACK
        else:
            self.state = self.CHASE

        # execute state
        if self.state == self.CHASE:
            self.update_chase(dx, dy)
            self.separate_from_other_enemies(enemies)
        elif self.state == self.ATTACK:
            self.update_attack(player)

        # 1 attack per second at 60 FPS
        if self.state == self.ATTACK:
            if self.attack_cooldown == 0:
                player.take_damage(20)
                self.attack_cooldown = 60

    def update_chase(self, dx, dy):
        if dx <= 60:
            return # stop near player

        # horizontal movement
        if dx > 0:
            self.x += self.speed
        elif dx < 0:
            self.x -= self.speed
        # vertical movement
        if abs(dy) > 10: # allow some vertical leniency
            if dy > 0:
                self.y += self.speed
            else:
                self.y -= self.speed

        # Keep enemy inside lane
        self.y = max(250, self.y)
        self.y = min(450, self.y)

    def separate_from_other_enemies(self, enemies):
        for other in enemies:
            if other is self:
                continue
            if other.state == self.DEAD:
                continue
            dx = other.x - self.x
            if abs(dx) < 40:
                if dx > 0:
                    self.x -= 1
                else:
                    self.x += 1
    
    def update_attack(self, player):
        if self.attack_cooldown > 0:
            return
        player.take_damage(self.attack_damage)
        self.attack_cooldown = 60

    def draw(self, screen, camera_x):
        screen_x = self.x - camera_x
        # shadow
        pygame.draw.ellipse(
            screen, (50, 50, 50),
            (
                screen_x,
                self.y + self.height - 10,
                self.width,
                12
            )
        )
        # body color
        body_color = (220, 40, 220)
        if self.state == self.DEAD:
            body_color = (80, 80, 80)
        elif self.state == self.HIT:
            body_color = (255, 255, 255)
        elif self.state == self.ATTACK:
            body_color = (220, 40, 220)
        elif self.state == "CHASE":
            body_color = (40, 40, 220)

        #if self.hit_timer > 0:
        #    body_color = (255, 255, 255)

        pygame.draw.rect(
            screen, body_color,
            (
                screen_x,
                self.y,
                self.width,
                self.height
            )
        )
        
        # health bar background
        pygame.draw.rect(
            screen, (120, 120, 120),
            (
                screen_x,
                self.y - 12,
                50,
                6
            )
        )
        # health bar
        hp_width = int(50 * (self.hp / 100))
        pygame.draw.rect(
            screen, (255, 0, 0),
            (
                screen_x,
                self.y - 12,
                hp_width,
                6
            )
        )

    def take_damage(self, damage, attacker_x):
        if self.state == self.DEAD:
            return

        self.hp -= damage
        self.hit_timer = 15
        self.state = self.HIT

        # knockback direction based on attacker's position
        if attacker_x < self.x:
            self.knockback_velocity = 10
        else:
            self.knockback_velocity = -10

        if self.hp <= 0:
            self.hp = 0
            self.state = self.DEAD

    def apply_knockback(self):
        if self.knockback_velocity == 0:
            return
        self.x += self.knockback_velocity
        # friction slows down knockback over time
        self.knockback_velocity *= 0.8
        if abs(self.knockback_velocity) < 0.5:
            self.knockback_velocity = 0
