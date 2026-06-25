from dataclasses import dataclass
from base import *

# ─────────────────────────────────────────────
# CollisionComponent
# Hitbox and hurtbox data; resolution done by PhysicsSystem.
# ─────────────────────────────────────────────

@dataclass
class HitboxDef:
    id: str
    rect: Rect2             # relative to owner position
    damage: float
    knockback: Vec2
    active: bool = False