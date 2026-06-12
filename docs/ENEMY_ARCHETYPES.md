# Enemy Archetypes

Enemies are built from two pieces:

- `EnemyConfig` in `game/entities/enemy_config.py` stores data such as name, HP, speed, damage, score, animation configs, and archetype.
- An archetype class stores behavior. Current archetypes are:
  - `BasicMeleeEnemy`
  - `FastSmallEnemy`
  - `WeaponEnemy`
  - `HeavyEnemy`
  - `RangedEnemy`

To add a normal enemy variant, add one row to `ENEMY_CONFIGS`:

```python
"driver": EnemyConfig(
    enemy_id="driver",
    display_name="Driver",
    archetype="basic_melee",
    max_hp=65,
    speed=ENEMY_SPEED * 1.08,
    attack_damage=10,
    score_points=125,
)
```

Then use the key in a wave:

```python
"enemy_types": ["ferris", "driver", "blade"]
```

Only create a new archetype class when the enemy needs new behavior, not just different stats.
