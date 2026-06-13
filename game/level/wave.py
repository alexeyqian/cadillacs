from dataclasses import dataclass
import random
from typing import Optional

from game.entities.enemy_factory import EnemyFactory
from game.settings import LANE_BOTTOM, LANE_TOP, SCREEN_WIDTH

@dataclass
class SpawnInstruction:
    enemy_type: str
    side: str = "right"
    delay_min: int = 60
    delay_max: int = 120
    y_min: Optional[int] = None
    y_max: Optional[int] = None
    # how far offscreen the enemy starts.
    enter_offset: int = 80

@dataclass
class PendingSpawn:
    enemy_type: str
    x: int
    y: int
    delay: int

class Wave:
    def __init__(self, trigger_x, spawn_instructions, max_active=4):
        self.trigger_x = trigger_x
        self.started = False
        self.completed = False
        self.max_active = max_active
        self.spawn_instructions = spawn_instructions
        self.pending_spawns = []
        self.spawn_timer = 0

    def spawn(self, camera_x=0, lane_top=LANE_TOP, lane_bottom=LANE_BOTTOM):
        self.started = True
        self.spawn_timer = 0
        self.pending_spawns = []

        viewport_left = camera_x
        viewport_right = camera_x + SCREEN_WIDTH

        for instruction in self.spawn_instructions:
            if instruction.side == "left":
                spawn_x = viewport_left - instruction.enter_offset
            else:
                spawn_x = viewport_right + instruction.enter_offset

            y_min = instruction.y_min
            y_max = instruction.y_max

            if y_min is None:
                y_min = lane_top + 40
            if y_max is None:
                y_max = lane_bottom - 40

            y_min = max(lane_top, y_min)
            y_max = min(lane_bottom, y_max)

            if y_min > y_max:
                y_min = y_max

            spawn_y = random.randint(y_min, y_max)
            delay = random.randint(instruction.delay_min, instruction.delay_max)

            self.pending_spawns.append(PendingSpawn(
                enemy_type=instruction.enemy_type,
                x=spawn_x,
                y=spawn_y,
                delay=delay,
            ))

        return []

    def update_spawn(self, active_enemy_count=0):
        if len(self.pending_spawns) == 0:
            return []
        if active_enemy_count >= self.max_active:
            return []

        if self.spawn_timer > 0:
            self.spawn_timer -= 1
            return []

        pending_spawn = self.pending_spawns.pop(0)
        enemy = EnemyFactory.create_enemy(
            pending_spawn.enemy_type,
            pending_spawn.x,
            pending_spawn.y
        )

        self.spawn_timer = pending_spawn.delay
        return [enemy]

class SpawnWave:
    def __init__(self, trigger_x, spawners):
        self.trigger_x = trigger_x
        self.spawners = spawners
        self.started = False
        self.completed = False

    def spawn(self, camera_x=0, lane_top=LANE_TOP, lane_bottom=LANE_BOTTOM):
        self.started = True
        viewport_left = camera_x
        viewport_right = camera_x + SCREEN_WIDTH
        spawn_y = max(lane_top, min(lane_bottom, lane_bottom - 80))
        for spawner in self.spawners:
            spawner.spawn_x = max(
                viewport_left + 120,
                min(spawner.spawn_x, viewport_right - 220)
            )
            spawner.spawn_y = spawn_y
        return []

    def update(self):
        new_enemies = []
        for spawner in self.spawners:
            enemy = spawner.update()
            if enemy:
                new_enemies.append(enemy)
        return new_enemies

    def all_spawners_finished(self):
        for spawner in self.spawners:
            if not spawner.finished():
                return False
        return True

class BossWave(Wave):
    def __init__(self, trigger_x):
        spawn_instructions = [
            SpawnInstruction(
                enemy_type="boss",
                side="right",
                delay_min=120,
                delay_max=180,
                enter_offset=160,
            )
        ]
        super().__init__(
            trigger_x=trigger_x,
            spawn_instructions=spawn_instructions,
            max_active=1,
        )