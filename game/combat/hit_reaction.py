from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class HitReaction:
    # Hit stun answers: how long is the target unable to act?
    stun_frames: Optional[int] = None
    # Knockback answers: how quickly does the target slide away from the attacker?
    knockback_velocity: float = 10


def normalize_hit_reaction(
    reaction=None,
    hit_stun_duration=None,
    knockback_velocity=None,
    default_knockback_velocity=10,
):
    # New code should pass HitReaction directly. The extra parameters keep old
    # call sites and small tests working while the combat API is migrating.
    if isinstance(reaction, HitReaction):
        return reaction

    if knockback_velocity is not None:
        reaction = knockback_velocity

    if isinstance(reaction, (int, float)):
        return HitReaction(
            stun_frames=hit_stun_duration,
            knockback_velocity=reaction,
        )

    return HitReaction(
        stun_frames=hit_stun_duration,
        knockback_velocity=default_knockback_velocity,
    )
