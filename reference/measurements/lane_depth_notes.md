# Lane Depth Notes

For a 960 x 540 internal resolution:

```python
PLAYER_H = 160
LANE_BOTTOM = SCREEN_HEIGHT - PLAYER_H
LANE_TOP = LANE_BOTTOM - PLAYER_H
```

Recommended walkable Y range:

```text
LANE_TOP    ≈ 220
LANE_BOTTOM ≈ 380
LANE_DEPTH  ≈ 160
```

Use feet-position sorting for draw order:

```python
sprites.sort(key=lambda obj: obj.feet_y)
```
