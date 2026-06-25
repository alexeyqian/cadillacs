from dataclasses import dataclass

@dataclass
class DamageInfo:
    def __init__(self, amount, damage_type="physical", source=None):
        self.damage_type = damage_type
        self.amount = amount
        self.source = source # GameObject
        self.knockback = None