# Hitbox Size Notes

Recommended box types:

- `collision_box`: body/feet box used for movement and lane blocking
- `hurt_box`: area that can receive damage
- `attack_box`: active damaging area during attacks
- `grab_box`: short-range grab detection area

Example:

```python
collision_box = Rect(x + 20, y + 125, 40, 28)
hurt_box = Rect(x + 12, y + 20, 56, 130)
attack_box = Rect(x + 65, y + 55, 45, 35)
```
