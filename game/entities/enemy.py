from game.settings import *
from game.entities.enemy_config import get_enemy_config
from game.entities.enemy_state import EnemyState
from game.entities.enemy_health import EnemyHealth
from game.entities.enemy_geometry import EnemyGeometry
from game.entities.enemy_animation_controller import EnemyAnimationController
from game.entities.enemy_renderer import EnemyRenderer
from game.entities.enemy_movement import EnemyMovement
from game.entities.enemy_flanking import EnemyFlanking
from game.entities.enemy_lifecycle_state import EnemyLifecycleState
from game.entities.enemy_coordination import EnemyCoordination
from game.entities.enemy_combat_controller import EnemyCombatController
from game.entities.enemy_reaction_controller import EnemyReactionController
from game.entities.enemy_lifecycle_controller import EnemyLifecycleController
from game.entities.enemy_state_resolver import EnemyStateResolver
from game.entities.enemy_loot_controller import EnemyLootController
from game.entities.hit_reaction import normalize_hit_reaction

# State resolver: decides what state the enemy wants
# Movement: changes x/y/facing
# Combat: handles attack hit detection
# Lifecycle: advances temporary states
# Enemy is a small coordinator. Components own movement, combat,
# reactions, lifecycle, state decisions, loot, animation, and rendering.

class Enemy:
    IDLE = EnemyState.IDLE
    WALK = EnemyState.WALK
    PATROL = EnemyState.PATROL
    CHASE = EnemyState.CHASE
    ATTACK = EnemyState.ATTACK
    HIT = EnemyState.HIT
    RECOIL = EnemyState.RECOIL
    DEAD = EnemyState.DEAD
    GRABBED = EnemyState.GRABBED
    THROWN = EnemyState.THROWN
    KNOCKDOWN = EnemyState.KNOCKDOWN
    GETUP = EnemyState.GETUP

    # attack_range: should i attack
    #  attack_rect = did i hit
    # detect_range: within detect_range, enemy chases player
    # outside this range, enemy ignores player
    def __init__(self, x, y, enemy_type, 
                animation_data, anim_fps, sprite_scale=4):
        # Identity / position
        self.x = x
        self.y = y
        self.spawn_x = x # enemy remembers where it spawned
        self.enemy_type = enemy_type

        # Core state
        self.state = self.IDLE
        self.facing_right = False

        self.lifecycle_state = EnemyLifecycleState()

        # Movement
        self.patrol_direction = 1

        self.hit_stun_duration = 15

        # Rendering / collision / loot
        self.geometry = EnemyGeometry()
        self.loot_generated = False

        # Components
        self.combat = EnemyCombatController()

        self.apply_enemy_config(get_enemy_config(self.enemy_type))

        self.movement = EnemyMovement()
        self.flanking = EnemyFlanking()
        self.reactions = EnemyReactionController()
        self.lifecycle = EnemyLifecycleController()
        self.state_resolver = EnemyStateResolver()
        self.loot_controller = EnemyLootController()
        self.coordination = EnemyCoordination()
        self.animation_controller = EnemyAnimationController(self, animation_data, anim_fps)
        self.renderer = EnemyRenderer()

    def apply_enemy_config(self, config):
        self.enemy_id = config.enemy_id
        self.display_name = config.display_name
        self.archetype = config.archetype

        self.collision_box_w = int(config.collision_box_w)
        self.collision_box_h = int(config.collision_box_h)
        self.hurt_box_w = int(config.hurt_box_w)
        self.hurt_box_h = int(config.hurt_box_h)
        self.hurt_box_offset_x = int(config.hurt_box_offset_x)
        self.hurt_box_offset_y = int(config.hurt_box_offset_y)
        
        self.health = EnemyHealth(config.max_hp)
        self.speed = config.speed
        self.patrol_distance = config.patrol_distance
        self.detect_range = config.detect_range

        self.attack_range = config.attack_range
        self.attack_lane_range = config.attack_lane_range
        self.attack_lane_reach = config.attack_lane_reach

        self.combat.attack_data = config.attack
        self.attack_damage = config.attack.damage
        self.attack_delay = config.attack.delay
        self.attack_cooldown_duration = config.attack.cooldown

        self.hit_stun_duration = config.hit_stun_duration
        self.flinch_damage_threshold = config.flinch_damage_threshold
        self.attack_flinch_damage_threshold = (
            config.attack_flinch_damage_threshold
            if config.attack_flinch_damage_threshold is not None
            else config.flinch_damage_threshold
        )
        self.anti_stunlock_hit_limit = config.anti_stunlock_hit_limit
        self.anti_stunlock_hit_window = config.anti_stunlock_hit_window
        self.stun_resistance_duration = config.stun_resistance_duration
        self.resisted_hit_stun_duration = config.resisted_hit_stun_duration
        self.breakout_recoil_duration = config.breakout_recoil_duration
        self.breakout_velocity = config.breakout_velocity
        self.recovery_punish_delay_multiplier = config.recovery_punish_delay_multiplier
        self.thrown_damage = config.thrown_damage

        self.melee_attack_slot_limit = getattr(config, "melee_attack_slot_limit", None)
        self.score_points = config.score_points
        self.sprite_scale = config.sprite_scale

    def update(self, level, player, enemies):
        if self.lifecycle.update_special_states(self):
            return

        self.lifecycle.update_timers(self)

        if self.lifecycle.update_hit_state(self):
            return

        self.reactions.apply_knockback(self)

        dx, dy, distance_x, distance_y = self.get_player_distance(player)

        if distance_x <= self.detect_range:
            self.face_player(player)

        self.choose_state(level, player, distance_x, distance_y, enemies)
        if self.state == self.ATTACK:
            self.update_animation()
            self.execute_state(level, player, enemies, dx, dy)
        else:
            self.execute_state(level, player, enemies, dx, dy)
            self.update_animation()

    # Lifecycle / reactions
    def is_ready_to_remove(self):
        return self.lifecycle.is_ready_to_remove(self)

    def take_damage(
        self,
        damage,
        attacker_x,
        reaction=None,
        hit_stun_duration=None,
        knockback_velocity=None,
    ):
        reaction = normalize_hit_reaction(
            reaction,
            hit_stun_duration,
            knockback_velocity,
        )
        self.reactions.take_damage(
            self,
            damage,
            attacker_x,
            reaction,
        )

    def grabbed_by_player(self):
        self.reactions.grabbed_by_player(self)

    def thrown_by_player(self, direction):
        self.reactions.thrown_by_player(self, direction)

    def take_grab_knee_damage(self, damage):
        self.reactions.take_grab_knee_damage(self, damage)

    # Movement / state decisions
    def get_player_distance(self, player):
        return self.movement.get_player_distance(self, player)

    def face_player(self, player):
        self.movement.face_player(self, player)

    def choose_state(self, level, player, distance_x, distance_y, enemies):
        self.state_resolver.choose_state(
            self, level, player, distance_x, distance_y, enemies
        )

    def execute_state(self, level, player, enemies, dx, dy):
        if self.state == self.PATROL:
            self.movement.update_patrol(self)
        elif self.state == self.CHASE:
            self.movement.update_chasing(self, player, dx, dy)
            self.movement.separate_from_other_enemies(self, enemies)
        elif self.state == self.ATTACK:
            self.update_attack(level, player)

    def apply_world_bounds(self, world_width=None, lane_top=None, lane_bottom=None):
        self.movement.apply_world_bounds(self, world_width, lane_top, lane_bottom)

    # Combat
    def start_attack(self):
        self.combat.start_attack(self)

    def start_clash_recovery(self):
        self.combat.start_clash_recovery(self)

    def update_attack(self, level, player):
        self.combat.update_attack(self, level, player)

    def is_attack_active(self):
        return self.combat.is_attack_active(self)

    def get_attack_total_duration(self):
        if hasattr(self, "attack_data"):
            return self.attack_data.total_duration
        return self.combat.get_attack_data(self).total_duration

    def get_attack_phase_name(self):
        if self.state != self.ATTACK:
            return ""
        return self.combat.attack_manager.get_phase_name()

    def get_attack_timing_label(self):
        if self.state != self.ATTACK:
            return ""
        return self.combat.attack_manager.get_timing_label()

    # Rendering / animation / geometry
    def draw(self, screen, camera_x):
        self.renderer.draw(self, screen, camera_x)

    def get_current_frame_data(self):
        return self.animation_controller.get_current_frame_data()

    def update_animation(self):
        self.animation_controller.update(self)

    # returns the whole visible sprite frame in world space:
    def get_frame_rect(self):
        return self.geometry.get_frame_rect(self)

    def get_collision_rect(self):
        return self.geometry.get_collision_rect(self)

    def get_hurt_rect(self):
        return self.geometry.get_hurt_rect(self)

    def get_attack_rect(self):
        return self.geometry.get_attack_rect(self)

    # Loot
    def create_loot(self):
        return self.loot_controller.create_loot(self)
