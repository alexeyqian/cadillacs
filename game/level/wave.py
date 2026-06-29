from dataclasses import dataclass
import random
from typing import Optional

from game.factories.enemy_factory import EnemyFactory
from game.settings import LANE_BOTTOM, LANE_TOP, SCREEN_WIDTH


@dataclass
class SpawnInstruction:
    enemy_type: str
    side: str = "right"
    delay_min: int = 60
    delay_max: int = 120
    y_min: int = 700
    y_max: int = 800
    enter_offset: int = -50  # how far offscreen the enemy starts
    min_player_distance: int = 100
    capability_overrides: Optional[dict] = None


@dataclass
class PendingSpawn:
    enemy_type: str
    x: int
    y: int
    delay: int
    capability_overrides: Optional[dict] = None


class Wave:
    def __init__(self, trigger_x, spawn_instructions, max_active=4):
        self.trigger_x = trigger_x
        self.started = False
        self.completed = False
        self.max_active = max_active
        self.spawn_instructions = spawn_instructions
        self.pending_spawns = []
        self.spawn_timer = 0

    def start(self, camera_x=0, lane_top=LANE_TOP, lane_bottom=LANE_BOTTOM, player_x=None):
        self.started = True
        self.spawn_timer = 0
        self.pending_spawns = []

        viewport_left = camera_x
        viewport_right = camera_x + SCREEN_WIDTH

        spawn_inset = 100  # pixels inside the viewport edge
        for instruction in self.spawn_instructions:
            if instruction.side == "left":
                spawn_x = viewport_left + spawn_inset
                if player_x is not None:
                    spawn_x = min(spawn_x, player_x - instruction.min_player_distance)
            else:
                spawn_x = viewport_right - spawn_inset
                if player_x is not None:
                    spawn_x = max(spawn_x, player_x + instruction.min_player_distance)

            y_min = instruction.y_min if instruction.y_min is not None else lane_top + 40
            y_max = instruction.y_max if instruction.y_max is not None else lane_bottom - 40
            y_min = max(lane_top, y_min)
            y_max = min(lane_bottom, y_max)
            if y_min > y_max:
                y_min = y_max

            self.pending_spawns.append(PendingSpawn(
                enemy_type=instruction.enemy_type,
                x=spawn_x,
                y=random.randint(y_min, y_max),
                delay=random.randint(instruction.delay_min, instruction.delay_max),
                capability_overrides=instruction.capability_overrides,
            ))

        if self.pending_spawns:
            self.spawn_timer = self.pending_spawns[0].delay

    def tick(self, active_enemy_count=0):
        """Tick one frame. Returns a list of newly spawned enemies (0 or 1)."""
        if not self.pending_spawns:
            return []
        if active_enemy_count >= self.max_active:
            return []
        if self.spawn_timer > 0:
            self.spawn_timer -= 1
            return []

        pending = self.pending_spawns.pop(0)
        enemy = EnemyFactory.create_enemy(
            pending.enemy_type,
            pending.x,
            pending.y,
            capability_overrides=pending.capability_overrides,
        )
        self.spawn_timer = self.pending_spawns[0].delay if self.pending_spawns else 0
        return [enemy]

    def is_spawning_done(self):
        return not self.pending_spawns


class BossWave(Wave):
    def __init__(self, trigger_x):
        super().__init__(
            trigger_x=trigger_x,
            spawn_instructions=[
                SpawnInstruction(
                    enemy_type="boss",
                    side="right",
                    delay_min=120,
                    delay_max=180,
                    enter_offset=-100,
                )
            ],
            max_active=1,
        )
