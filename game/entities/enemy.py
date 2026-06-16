from dataclasses import replace

from game.settings import *
from game.entities.enemy_config import get_enemy_config
from game.entities.enemy_state import EnemyState
from game.entities.enemy_lifecycle import EnemyLifecycleMixin
from game.entities.enemy_reactions import EnemyReactionMixin
from game.entities.enemy_health import EnemyHealth
from game.entities.enemy_hitboxes import EnemyHitboxes
from game.entities.enemy_animation_controller import EnemyAnimationController
from game.entities.enemy_renderer import EnemyRenderer
from game.entities.enemy_movement import EnemyMovement
from game.entities.enemy_combat_controller import EnemyCombatController
from game.entities.enemy_reaction_controller import EnemyReactionController
from game.entities.enemy_lifecycle_controller import EnemyLifecycleController
from game.entities.enemy_state_resolver import EnemyStateResolver
from game.entities.enemy_loot_controller import EnemyLootController
from game.entities.attack_controller import AttackController

# State resolver: decides what state the enemy wants
# Movement: changes x/y/facing
# Combat: handles attack hit detection
# Lifecycle: advances temporary states
# Enemy is a small coordinator. Components own movement, combat,
# reactions, lifecycle, state decisions, loot, animation, and rendering.

class Enemy(EnemyReactionMixin, EnemyLifecycleMixin):
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
        self.x = x
        self.y = y
        self.spawn_x = x # enemy remembers where it spawned
        self.enemy_type = enemy_type

        # new design
        # give every enemy attack a clean timer 
        # so the next chunk can use windup / active / recovery 
        # instead of relying only on animation frame position.
        self.attack_timer = 0
        self.attack_controller = AttackController()
        self.attack_decision_timer = 0
        self.attack_delay = ENEMY_ATTACK_DELAY
        self.attack_clash_recovery_duration = ENEMY_ATTACK_CLASH_RECOVERY_DURATION
        self.attack_clash_cooldown_duration = ENEMY_ATTACK_CLASH_COOLDOWN_DURATION

        self.state = self.IDLE
        self.facing_right = False
        self.hitboxes = EnemyHitboxes()
        self.loot_generated = False
        self.death_remaining = 30
        self.death_countdown_started = False

        self.patrol_direction = 1
        self.attack_already_hit = False
        self.attack_cooldown = 0
        # todo: add enemy coordination layer in future
        # attack slot reservation system
        # expected behavior:
        # Enemy reserves a melee attack slot when attack starts
        # Enemy releases slot when attack ends, flinches, dies, or clashes
        # Attack limit becomes more reliable and easier to reason about
        self.has_attack_slot = False
        #  if an enemy is in range but cannot attack because another melee enemy owns the slot, 
        # it should reposition toward an open side instead of just pressing into the player. 
        # This makes groups look more intentional.
        self.flank_target_side = None
        self.flank_target_y_offset = 0
        self.flank_offset_x = ENEMY_FLANK_OFFSET_X
        self.flank_offset_y = ENEMY_FLANK_OFFSET_Y
        # avoid make enemies jitter between left/right if counts are close. 
        # give each flank decision a short commitment timer.
        self.flank_decision_remaining = 0
        self.flank_decision_duration = ENEMY_FLANK_DECISION_DURATION

        # This keeps the clash fair on both sides: the player cannot instantly re-punch,
        # and the enemy cannot instantly resume pressure either.
        self.action_lock_remaining = 0
        # hit reaction # enemy gets briefly white when hit by player
        self.knockback_velocity = 0
        self.hit_stun_remaining = 0
        self.hit_stun_duration = 15
        # grab/throw
        self.thrown_velocity_x = 0
        self.thrown_remaining = 0
        self.thrown_hit_targets = set()
        #knockdown/getup
        self.knockdown_remaining = 0
        self.getup_remaining = 0

        self.apply_enemy_config(get_enemy_config(self.enemy_type))

        self.movement = EnemyMovement()
        self.combat = EnemyCombatController()
        self.reactions = EnemyReactionController()
        self.lifecycle = EnemyLifecycleController()
        self.state_resolver = EnemyStateResolver()
        self.loot_controller = EnemyLootController()
        self.animation_controller = EnemyAnimationController(self, animation_data, anim_fps)
        self.renderer = EnemyRenderer()

    def apply_enemy_config(self, config):
        self.enemy_id = config.enemy_id
        self.display_name = config.display_name
        self.archetype = config.archetype
        self.melee_attack_slot_limit = getattr(config, "melee_attack_slot_limit", None)
        self.collision_box_w = int(config.collision_box_w)
        self.collision_box_h = int(config.collision_box_h)
        self.health = EnemyHealth(config.max_hp)
        self.speed = config.speed
        self.patrol_distance = config.patrol_distance
        self.detect_range = config.detect_range

        self.attack_range = config.attack_range
        self.attack_lane_range = config.attack_lane_range
        self.attack_lane_reach = config.attack_lane_reach

        self.attack_data = config.attack
        self.attack_damage = config.attack.damage
        self.attack_delay = config.attack.delay
        self.attack_cooldown_duration = config.attack.cooldown
        self.attack_clash_recovery_duration = config.attack.clash_recovery_duration
        self.attack_clash_cooldown_duration = config.attack.clash_cooldown_duration

        self.hit_stun_duration = config.hit_stun_duration
        self.flinch_damage_threshold = config.flinch_damage_threshold
        self.attack_flinch_damage_threshold = (
            config.attack_flinch_damage_threshold
            if config.attack_flinch_damage_threshold is not None
            else config.flinch_damage_threshold
        )
        self.thrown_damage = config.thrown_damage
        self.score_points = config.score_points
        self.sprite_scale = config.sprite_scale

    def get_current_frame_data(self):
        return self.animation_controller.get_current_frame_data()

    def update_animation(self):
        self.animation_controller.update(self)

    def update(self, level, player, enemies):
        if self.update_special_states():
            return

        self.update_timers()

        if self.update_hit_state():
            return

        self.apply_knockback()

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

    def start_attack(self):
        self.combat.start_attack(self)

    def start_clash_recovery(self):
        self.combat.start_clash_recovery(self)

    def update_attack(self, level, player):
        self.combat.update_attack(self, level, player)

    def create_loot(self):
        return self.loot_controller.create_loot(self)

    def draw(self, screen, camera_x):
        self.renderer.draw(self, screen, camera_x)

    def apply_world_bounds(self, world_width=None, lane_top=None, lane_bottom=None):
        self.movement.apply_world_bounds(self, world_width, lane_top, lane_bottom)

    # returns the whole visible sprite frame in world space:
    def get_frame_rect(self):
        return self.hitboxes.get_frame_rect(self)

    def get_logical_rect(self):
        return self.get_frame_rect()

    def get_collision_rect(self):
        return self.hitboxes.get_collision_rect(self)

    def get_hurt_rect(self):
        return self.hitboxes.get_hurt_rect(self)


    def get_attack_rect(self):
        return self.hitboxes.get_attack_rect(self)
    
    def is_attack_active(self):
        return self.combat.is_attack_active(self)

    def get_attack_total_duration(self):
        return self.attack_windup + self.attack_active + self.attack_recovery

    @property
    def attack_windup(self):
        return self.attack_data.windup

    @attack_windup.setter
    def attack_windup(self, value):
        self.attack_data = replace(
            self.attack_data,
            phase=replace(self.attack_data.phase, windup=value)
        )

    @property
    def attack_active(self):
        return self.attack_data.active

    @attack_active.setter
    def attack_active(self, value):
        self.attack_data = replace(
            self.attack_data,
            phase=replace(self.attack_data.phase, active=value)
        )

    @property
    def attack_recovery(self):
        return self.attack_data.recovery

    @attack_recovery.setter
    def attack_recovery(self, value):
        self.attack_data = replace(
            self.attack_data,
            phase=replace(self.attack_data.phase, recovery=value)
        )
    
    def get_attack_phase_name(self):
        if self.state != self.ATTACK:
            return ""
        return self.attack_controller.get_phase_name()

    def get_attack_timing_label(self):
        if self.state != self.ATTACK:
            return ""
        return self.attack_controller.get_timing_label()

    # Later we can upgrade it into an “attack reservation” system
    def uses_melee_attack_slot(self):
        return self.archetype not in ["ranged", "boss"]

    def can_bypass_attack_slot_limit(self):
        return self.archetype in ["boss", "ranged"]
    
    def get_side_of_player(self, player):
        if self.x < player.x:
            return "left"
        return "right"
    
    def set_flank_target(self, player, enemies):
        if self.flank_decision_remaining > 0 and self.flank_target_side:
            return

        left_count = 0
        right_count = 0

        for enemy in enemies:
            if enemy is self:
                continue
            if enemy.state in [enemy.DEAD, enemy.GRABBED, enemy.THROWN, enemy.KNOCKDOWN]:
                continue

            if enemy.x < player.x:
                left_count += 1
            else:
                right_count += 1

        if left_count <= right_count:
            self.flank_target_side = "left"
        else:
            self.flank_target_side = "right"
            
        same_side_count = left_count if self.flank_target_side == "left" else right_count
        if same_side_count % 2 == 0:
            self.flank_target_y_offset = -self.flank_offset_y
        else:
            self.flank_target_y_offset = self.flank_offset_y

        self.flank_decision_remaining = self.flank_decision_duration

    def clear_flank_target(self):
        self.flank_target_side = None
        self.flank_target_y_offset = 0
        self.flank_decision_remaining = 0

    def get_flank_target_position(self, player):
        target_y = player.y + self.flank_target_y_offset
        if self.flank_target_side == "left":
            return player.x - self.flank_offset_x, target_y

        return player.x + self.flank_offset_x, target_y
