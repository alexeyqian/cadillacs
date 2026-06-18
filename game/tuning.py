"""Global game tuning helpers.

This module provides one place to control broad game feel.

The important rule is:

    Store readable base values, then apply tuning scalers once.

For example, an enemy can define a base attack as 20 windup frames,
8 active frames, and 25 recovery frames. The current timing preset can
then make that attack slower, normal, or faster without changing the
enemy-specific base numbers.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class TimingPreset:
    """A high-level game-feel preset.

    animation:
        Multiplies animation FPS. Larger values play sprite animations faster.

    combat:
        Multiplies gameplay timing windows measured in frames. Smaller values
        make attacks, cooldowns, hit-stun, and recovery finish faster.

    movement:
        Multiplies walking/chasing/running movement speeds.

    projectile:
        Multiplies projectile travel speeds.
    """

    animation: float = 1.0
    combat: float = 1.0
    movement: float = 1.0
    projectile: float = 1.0


TIMING_PRESETS = {
    "slow": TimingPreset(
        animation=0.90,
        combat=1.15,
        movement=0.90,
        projectile=0.90,
    ),
    "normal": TimingPreset(
        animation=1.00,
        combat=1.00,
        movement=1.00,
        projectile=1.00,
    ),
    "fast": TimingPreset(
        animation=1.15,
        combat=0.90,
        movement=1.10,
        projectile=1.10,
    ),
    "turbo": TimingPreset(
        animation=1.30,
        combat=0.75,
        movement=1.20,
        projectile=1.20,
    ),
}

# Change this value to quickly test the whole game's feel.
# Keep "normal" as the default baseline for regular development.
CURRENT_TIMING_PRESET = "normal"


def get_timing_preset(name=None):
    """Return the active timing preset.

    Unknown preset names fall back to "normal" so a typo does not crash the
    game during development.
    """

    preset_name = name or CURRENT_TIMING_PRESET
    return TIMING_PRESETS.get(preset_name, TIMING_PRESETS["normal"])


def scale_frames(base_frames, scale=None, minimum=1):
    """Scale a gameplay duration measured in game frames.

    Use this for windup, recovery, cooldowns, hit-stun, knockdown timers,
    spawn delays, invulnerability timers, and similar values.
    """

    if scale is None:
        scale = get_timing_preset().combat
    return max(minimum, int(round(base_frames * scale)))


def scale_active_frames(base_frames, scale=None, minimum=3):
    """Scale active hit frames while preserving a useful minimum.

    Active windows should usually not shrink to 1 frame. Very small active
    windows are easy to miss and can make attacks feel broken.
    """

    return scale_frames(base_frames, scale=scale, minimum=minimum)


def scale_timing(windup, active, recovery, scale=None, minimum_active=3):
    """Scale a standard attack timing block.

    Returns a dictionary so callers can keep code explicit:

        timing = scale_timing(20, 8, 25)
        attack = PlayerAttackData(
            windup=timing["windup"],
            active=timing["active"],
            recovery=timing["recovery"],
            ...
        )
    """

    if scale is None:
        scale = get_timing_preset().combat

    scaled_windup = scale_frames(windup, scale=scale)
    scaled_active = scale_active_frames(
        active,
        scale=scale,
        minimum=minimum_active,
    )
    scaled_recovery = scale_frames(recovery, scale=scale)

    return {
        "windup": scaled_windup,
        "active": scaled_active,
        "recovery": scaled_recovery,
        "total": scaled_windup + scaled_active + scaled_recovery,
    }


def scale_animation_fps(base_fps, scale=None, minimum=1.0):
    """Scale sprite animation FPS.

    Larger animation scale means faster sprite playback.
    """

    if scale is None:
        scale = get_timing_preset().animation
    return max(minimum, base_fps * scale)


def scale_animation_fps_map(base_fps_map, scale=None, minimum=1.0):
    """Scale every value in an animation FPS dictionary."""

    return {
        name: scale_animation_fps(fps, scale=scale, minimum=minimum)
        for name, fps in base_fps_map.items()
    }


def scale_speed(base_speed, scale=None, minimum=0.0):
    """Scale movement speed."""

    if scale is None:
        scale = get_timing_preset().movement
    return max(minimum, base_speed * scale)


def scale_projectile_speed(base_speed, scale=None, minimum=0.0):
    """Scale projectile speed separately from character movement."""

    if scale is None:
        scale = get_timing_preset().projectile
    return max(minimum, base_speed * scale)
