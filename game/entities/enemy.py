from game.entities.character import Character
from game.data.enemy_config import get_enemy_config
from game.entities.enemy_state import EnemyState
from game.components.character_health import CharacterHealth
from game.components.character_geometry import CharacterGeometry
from game.controllers.enemy_animation_controller import EnemyAnimationController
from game.components.enemy_renderer import EnemyRenderer
from game.components.enemy_movement import EnemyMovement
from game.components.enemy_flanking import EnemyFlanking
from game.components.enemy_condition import EnemyCondition
from game.components.enemy_intent import EnemyIntent
from game.controllers.enemy_combat_controller import EnemyCombatController
from game.controllers.enemy_reaction_controller import EnemyReactionController
from game.controllers.enemy_lifecycle_controller import EnemyLifecycleController
from game.controllers.enemy_ai_controller import EnemyAIController
from game.controllers.enemy_loot_controller import EnemyLootController
from game.combat.damage_request import DamageRequest

class Enemy(Character, EnemyState):
    def __init__(self, x, y, enemy_type,
                animation_data, anim_fps=None, sprite_scale=1):
        super().__init__(
            x=x,
            y=y,
            state=self.IDLE,
            facing_right=False,
            sprite_scale=sprite_scale,
        )

        self.configure_spawn_state(x, enemy_type)
        self.build_components()
        self.build_controllers()
        self.configure_from_enemy_config(get_enemy_config(self.enemy_type))
        self.build_presentation_components(animation_data, anim_fps)

    ##### begin of init #####
    def configure_spawn_state(self, x, enemy_type):
        self.enemy_type = enemy_type
        self.pending_projectile = None

    def build_components(self):
        self.condition = EnemyCondition()
        self.intent = EnemyIntent()
        self.geometry = CharacterGeometry()
        self.movement = EnemyMovement()
        self.flanking = EnemyFlanking()
        self.air = None  # set to EnemyAirState when can_jump=True

    def build_controllers(self):
        self.combat_controller = EnemyCombatController()
        self.reaction_controller = EnemyReactionController()
        self.lifecycle_controller = EnemyLifecycleController(spawn_x=self.x)
        self.ai_controller = EnemyAIController()
        self.loot_controller = EnemyLootController()

    def configure_from_enemy_config(self, config):
        self.apply_identity_config(config)
        self.apply_body_config(config)
        self.apply_movement_config(config)
        self.apply_combat_config(config)
        self.apply_reward_config(config)

    def build_presentation_components(self, animation_data, anim_fps=None):
        self.animation_controller = EnemyAnimationController(self, animation_data, anim_fps)
        self.renderer = EnemyRenderer()

    def apply_identity_config(self, config):
        self.enemy_id = config.enemy_id
        self.display_name = config.display_name
        self.archetype = config.archetype

    def apply_body_config(self, config):
        self.geometry.configure(
            config.collision_box_w,
            config.collision_box_h,
            config.hurt_box_w,
            config.hurt_box_h,
            config.hurt_box_offset_x,
            config.hurt_box_offset_y,
        )

        self.health = CharacterHealth(config.max_hp)
        self.sprite_scale = config.sprite_scale

    def apply_movement_config(self, config):
        self.movement.configure(
            speed=config.speed,
            patrol_distance=config.patrol_distance,
            detect_range=config.detect_range,
            can_run=config.can_run,
            run_speed=config.run_speed,
            can_jump=config.can_jump,
        )
        if config.can_jump:
            self.air = self.movement.air_state

    def apply_combat_config(self, config):
        self.combat_controller.attack_data = config.attack
        self.combat_controller.attack_range = config.attack_range
        self.combat_controller.attack_lane_range = config.attack_lane_range
        self.combat_controller.melee_attack_slot_limit = config.melee_attack_slot_limit

        self.reaction_controller.flinch_damage_threshold = config.flinch_damage_threshold
        self.reaction_controller.attack_flinch_damage_threshold = (
            config.attack_flinch_damage_threshold
            if config.attack_flinch_damage_threshold is not None
            else config.flinch_damage_threshold
        )
        self.reaction_controller.knockdown_damage_threshold = config.knockdown_damage_threshold

    def apply_reward_config(self, config):
        self.score_points = config.score_points

    ##### end of init #####

    ##### begin of main loop update #####
    def update_lifecycle_state(self):
        return self.lifecycle_controller.update_lifecycle_state(self)

    def advance_timers(self):
        self.combat_controller.advance_timers()
        self.flanking.advance_timers()

    def update_ai(self, context):
        self.ai_controller.update(self, context)

    def update_movement(self, context):
        if self.state == self.ATTACK or self.intent.wants_attack_player():
            return

        if self.intent.wants_jump():
            self.movement.start_jump()
        elif self.movement.is_jumping:
            self.movement.update_jump()
            if not self.movement.is_jumping:
                self.state = self.IDLE
        elif self.intent.wants_patrol():
            self.movement.patrol(self, self.lifecycle_controller.spawn_x)
        elif self.intent.wants_run_toward_player():
            self.movement.run_toward_player(self, context.player)
            self.movement.separate_from_enemies(self, context.enemies)
        elif self.intent.wants_move_toward_player():
            self.movement.move_toward_player(self, context.player)
            self.movement.separate_from_enemies(self, context.enemies)
        elif self.intent.wants_flank():
            self.movement.move_toward_position(self, self.intent.flank_position)
            self.movement.separate_from_enemies(self, context.enemies)

    def update_attack(self, context):
        if self.intent.wants_attack_player() and self.state != self.ATTACK:
            self.start_attack()
            self.intent.clear()

        if self.state != self.ATTACK:
            return
        self.combat_controller.update_attack(self, context.level, context.player)

    def update_reactions(self):
        return self.reaction_controller.update_reactions(self)

    def update_animation(self):
        self.animation_controller.update(self)

    ##### end of main loop update #####

    def is_ready_to_remove(self):
        return self.lifecycle_controller.is_ready_to_remove(self)

    def take_damage(
        self,
        damage,
        attacker_x=None,
        reaction=None,
    ):
        if isinstance(damage, DamageRequest):
            request = damage
            damage = request.damage
            attacker_x = request.attacker_x if request.attacker_x is not None else attacker_x
            reaction = request.reaction
        if attacker_x is None:
            attacker_x = self.x

        self.reaction_controller.take_damage(
            self,
            damage,
            attacker_x,
            reaction=reaction,
        )

    def grabbed_by_player(self):
        self.reaction_controller.grabbed_by_player(self)

    def thrown_by_player(self, direction, damage):
        self.reaction_controller.thrown_by_player(self, direction, damage)

    def take_grab_knee_damage(self, damage):
        self.reaction_controller.take_grab_knee_damage(self, damage)

    # Combat
    def start_attack(self):
        self.combat_controller.start_attack(self)

    # Loot
    def create_loot(self):
        return self.loot_controller.create_loot(self)
