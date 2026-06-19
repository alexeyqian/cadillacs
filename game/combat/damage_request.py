from dataclasses import dataclass
from typing import Optional

from game.combat.hit_reaction import HitReaction


@dataclass(frozen=True)
class DamageRequest:
    damage: int
    attacker_x: Optional[float] = None
    reaction: Optional[HitReaction] = None

    @classmethod
    def from_attack_data(cls, attack_data, attacker_x=None):
        return cls(
            damage=attack_data.damage,
            attacker_x=attacker_x,
            reaction=HitReaction(
                stun_frames=attack_data.hit_stun_duration,
                knockback_velocity=attack_data.knockback_velocity,
            ),
        )
