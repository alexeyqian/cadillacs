from dataclasses import dataclass, field

@dataclass
class Vec2:
    x: float = 0.0
    y: float = 0.0
    
    def __add__(self, other: Vec2) -> Vec2:
        return Vec2(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: float) -> Vec2:
        return Vec2(self.x * scalar, self.y * scalar)

    def __repr__(self) -> str:
        return f"Vec2({self.x:.2f}, {self.y:.2f})"

@dataclass
class Rect2:
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0
    height: float = 0.0