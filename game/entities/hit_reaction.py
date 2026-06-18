from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class HitReaction:
    # Hit stun answers: how long is the target unable to act?
    stun_frames: Optional[int] = None
    # Knockback answers: how quickly does the target slide away from the attacker?
    knockback_velocity: float = 10
