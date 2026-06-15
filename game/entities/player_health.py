class PlayerHealth:
    def __init__(self, max_hp, lives, hit_stun_duration):
        self.max_hp = max_hp
        self.hp = max_hp
        self.lives = lives
        self.hit_stun_duration = hit_stun_duration
        self.hit_timer = 0
        self.respawn_timer = 0

    # A counter-hit should feel like “you got caught during your attack,” not just ordinary damage.
    def take_damage(self, damage, hit_stun_bonus=0):
        self.hp -= damage
        self.hit_timer = self.hit_stun_duration + hit_stun_bonus

        if self.hp <= 0:
            self.hp = 0
            return self.lose_life()

        return False

    def lose_life(self):
        self.lives -= 1
        self.respawn_timer = 90
        return True

    def update_hit_timer(self):
        if self.hit_timer <= 0:
            return False

        self.hit_timer -= 1
        return self.hit_timer > 0

    def update_respawn_timer(self):
        if self.lives <= 0:
            return False

        if self.respawn_timer > 0:
            self.respawn_timer -= 1

        return self.respawn_timer <= 0

    def reset_for_respawn(self):
        self.hp = self.max_hp
        self.hit_timer = 0
        self.respawn_timer = 0