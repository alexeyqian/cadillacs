from game.entities.enemy_config import get_enemy_config
from game.entities.enemy_state import EnemyState
from game.entities.enemy_boxes import EnemyBoxMixin
from game.entities.enemy_ai import EnemyAIMixin
from game.entities.enemy_combat import EnemyCombatMixin
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
from game.entities.enemy_action_controller import EnemyActionController
from game.entities.enemy_update_controller import EnemyUpdateController
from game.entities.enemy_loot_controller import EnemyLootController

# State resolver: decides what state the enemy wants
# Action executor: runs behavior for the current state
# Movement: changes x/y/facing
# Combat: handles attack hit detection
# Lifecycle: advances temporary states
# Enemy is a small coordinator. Components own movement, combat,
# reactions, lifecycle, state decisions, loot, animation, and rendering.

class Enemy(EnemyBoxMixin, EnemyAIMixin, EnemyCombatMixin,
            EnemyReactionMixin, EnemyLifecycleMixin):
    IDLE = EnemyState.IDLE
    WALK = EnemyState.WALK
    PATROL = EnemyState.PATROL
    CHASE = EnemyState.CHASE
    ATTACK = EnemyState.ATTACK
    HIT = EnemyState.HIT
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
        self.apply_enemy_config(get_enemy_config(self.enemy_type))

        self.state = self.IDLE
        self.facing_right = False
        self.hitboxes = EnemyHitboxes()
        self.loot_generated = False
        self.death_timer = 30
        self.death_timer_started = False

        self.patrol_direction = 1
        self.attack_has_hit = False
        self.attack_cooldown = 0
        # hit reaction # enemy gets briefly white when hit by player
        self.knockback_velocity = 0
        self.hit_timer = 0
        self.hit_stun_duration = 15
        # grab/throw
        self.thrown_velocity_x = 0
        self.thrown_timer = 0
        self.thrown_hit_targets = set()
        #knockdown/getup
        self.knockdown_timer = 0
        self.getup_timer = 0

        self.movement = EnemyMovement()
        self.combat = EnemyCombatController()
        self.reactions = EnemyReactionController()
        self.lifecycle = EnemyLifecycleController()
        self.state_resolver = EnemyStateResolver()
        self.action_controller = EnemyActionController()
        self.update_controller = EnemyUpdateController()
        self.loot_controller = EnemyLootController()
        self.animation_controller = EnemyAnimationController(self, animation_data, anim_fps)
        self.renderer = EnemyRenderer()

    def apply_enemy_config(self, config):
        self.enemy_id = config.enemy_id
        self.display_name = config.display_name
        self.collision_box_w = int(config.collision_box_w)
        self.collision_box_h = int(config.collision_box_h)
        self.health = EnemyHealth(config.max_hp)
        self.speed = config.speed
        self.patrol_distance = config.patrol_distance
        self.detect_range = config.detect_range
        self.attack_range = config.attack_range
        self.attack_lane_range = config.attack_lane_range
        self.attack_damage = config.attack_damage
        self.attack_cooldown_duration = config.attack_cooldown_duration
        self.hit_stun_duration = config.hit_stun_duration
        self.hit_interrupt_damage_threshold = config.hit_interrupt_damage_threshold
        self.thrown_damage = config.thrown_damage
        self.score_points = config.score_points
        self.sprite_scale = config.sprite_scale

    def get_current_frame_data(self):
        return self.animation_controller.get_current_frame_data()

    def update_animation(self):
        self.animation_controller.update(self)

    def update(self, player, enemies):
        self.update_controller.update(self, player, enemies)

    def create_loot(self):
        return self.loot_controller.create_loot(self)

    def draw(self, screen, camera_x):
        self.renderer.draw(self, screen, camera_x)

    # returns the whole visible sprite frame in world space:
    def get_frame_rect(self):
        return self.hitboxes.get_frame_rect(self)

    def get_logical_rect(self):
        return self.get_frame_rect()


    def get_hurt_rect(self):
        return self.hitboxes.get_hurt_rect(self)


    def get_attack_rect(self):
        return self.hitboxes.get_attack_rect(self)
