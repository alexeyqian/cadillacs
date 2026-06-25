from game.entities2.component_base import ComponentBase

class HealthComponent(ComponentBase):
    def __init__(self, max_hp, invincibility_duration=0.1):
        self.max_hp = max_hp
        self.hp = max_hp
        # measured in seconds
        self._invincibility_duration = invincibility_duration
        self._invincibility_countdown_timer = invincibility_duration
        self.max_shield = 0 
        self.shield = 0

        self.on_damage = None
        self.on_heal = None
        self.on_death = None

    def update(self, dt: float):
        self.advance_timers(dt)

    def is_alive(self):
        return self.hp > 0
    
    def is_invincible(self):
        return self._invincibility_countdown_timer > 0

    def health_percent(self) -> float:
        return self.hp / self.max_hp

    def advance_timers(self, dt: float):
        if self._invincibility_countdown_timer > 0:
            self._invincibility_countdown_timer -= dt

    def take_damage(self, damage_info):
        """
        Apply damage. Returns the actual HP removed (after shields / i-frames).
        Emits scene events when available.
        """
        if not self.is_alive or  self.is_invincible:
            return 0

        amount = damage_info.amount
        # Shield absorbs first
        if self.shield > 0:
            absorbed = min(self.shield, amount)
            self.shield -= absorbed
            amount -= absorbed

        amount = min(amount, self.hp)
        self.hp -= amount
        # ??
        self._invincibility_countdown_timer = self.invincibility_duration
        
        if self.on_damage:
            self.on_damage(damage_info, amount)

        scene = getattr(self, "owner", None) and self.owner.scene
        if scene: # if current component's owner has a parent scene
            scene.event_bus.emit("damage:taken", {
                "target": self.owner, "amount": amount, "source": damage_info.source
            })

        if not self.is_alive:
            if self.on_death:
                self.on_death(damage_info)
            if scene:
                scene.event_bus.emit("object:died", {
                    "object": self.owner, "killed_by": damage_info.source
                })

        return amount

    def heal(self, amount: int):
        actual = min(amount, self.max_hp - self.hp)
        self.hp += actual
        if self.on_heal:
            self.on_heal(actual, self.hp)
