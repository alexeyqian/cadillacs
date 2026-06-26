from game.entities.character import Character
from game.data.enemy_config import get_enemy_config
from game.entities.enemy_state import EnemyState
from game.components.character_health import CharacterHealth
from game.components.character_geometry import CharacterGeometry
from game.controllers.enemy_animation_controller import EnemyAnimationController
from game.components.enemy_renderer import EnemyRenderer
from game.components.enemy_movement import EnemyMovement
from game.components.enemy_reaction_state import EnemyReactionState
from game.components.enemy_intent import EnemyIntent
from game.components.enemy_combat_state import EnemyCombatState
from game.components.enemy_ai_state import EnemyAIState
from game.controllers.enemy_combat_controller import EnemyCombatController
from game.controllers.enemy_reaction_controller import EnemyReactionController
from game.controllers.enemy_state_controller import EnemyStateController
from game.controllers.enemy_ai_controller import EnemyAIController, EnemyAIConfig
from game.controllers.enemy_loot_controller import EnemyLootController
from game.combat.damage_request import DamageRequest

class Enemy(Character, EnemyState):
    def __init__(self, x, y, enemy_type,
                animation_data, anim_fps=None, sprite_scale=1):
        super().__init__(x=x, y=y, state=self.IDLE,
                        facing_right=False, sprite_scale=sprite_scale)

        self.enemy_type = enemy_type
        self.pending_projectile = None

        self._build_components()
        self._build_controllers()
        self._apply_config(get_enemy_config(self.enemy_type))
        self._build_presentation_components(animation_data, anim_fps)

    # --- Init helpers ---

    def _build_components(self):
        self.geometry = CharacterGeometry()
        self.reaction_state = EnemyReactionState()
        self.combat_state = EnemyCombatState()
        self.ai_state = EnemyAIState()
        self.intent = EnemyIntent()
        self.movement = EnemyMovement()
        self.air = None  # set to EnemyAirState when can_jump=True

    def _build_controllers(self):
        self.combat_controller = EnemyCombatController()
        self.reaction_controller = EnemyReactionController()
        self.state_controller = EnemyStateController()
        self.ai_controller = EnemyAIController()
        self.loot_controller = EnemyLootController()

    def _apply_config(self, config):
        self._apply_identity_config(config)
        self._apply_body_config(config)
        self._apply_movement_config(config)
        self._apply_combat_config(config)
        self._apply_ai_config(config)
        self._apply_reward_config(config)

    def _build_presentation_components(self, animation_data, anim_fps=None):
        self.animation_controller = EnemyAnimationController(self, animation_data, anim_fps)
        self.renderer = EnemyRenderer()

    def _apply_identity_config(self, config):
        self.enemy_id = config.enemy_id
        self.display_name = config.display_name
        self.archetype = config.archetype

    def _apply_body_config(self, config):
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

    def _apply_movement_config(self, config):
        self.movement.configure(
            speed=config.speed,
            patrol_distance=config.patrol_distance,
            detect_range=config.detect_range,
            can_run=config.can_run,
            run_speed=config.run_speed,
            can_jump=config.can_jump,
            can_run_attack=config.can_run_attack,
            can_jump_attack=config.can_jump_attack,
        )
        self.movement.patrol_center_x = self.x
        if config.can_jump:
            self.air = self.movement.air_state

    def _apply_combat_config(self, config):
        self.combat_state.configure(config.attack, config.run_attack, config.jump_attack)
        self.reaction_controller.flinch_damage_threshold = config.flinch_damage_threshold
        self.reaction_controller.knockdown_damage_threshold = config.knockdown_damage_threshold

    def _apply_ai_config(self, config):
        self.ai_controller.config = EnemyAIConfig(
            attack_range=config.attack_range,
            attack_lane_range=config.attack_lane_range,
            melee_attack_slot_limit=config.melee_attack_slot_limit,
        )

    def _apply_reward_config(self, config):
        self.score_points = config.score_points

    def apply_capability_overrides(self, overrides):
        if "can_run" in overrides:
            self.movement.can_run = overrides["can_run"]
        if "can_jump" in overrides:
            self.movement.can_jump = overrides["can_jump"]
            if overrides["can_jump"]:
                self.air = self.movement.air_state
        if "can_run_attack" in overrides:
            self.movement.can_run_attack = overrides["can_run_attack"]
        if "can_jump_attack" in overrides:
            self.movement.can_jump_attack = overrides["can_jump_attack"]

    # --- Cross-controller coordination ---

    def _clear_combat_commitment(self):
        self.combat_controller.cancel_attack(self)
        self.ai_controller.reset_decision_timer(self)
        self.combat_state.owns_attack_slot = False

    def _begin_attack(self, state, attack_name, attack_data):
        self.state = state
        self.ai_controller.reset_decision_timer(self)
        self.combat_state.attack_manager.start(attack_name, attack_data)
        self.animation_controller.play(state)
        self.animation_controller.reset_current_animation()

    # --- Per-frame update ---

    def update_state(self):
        self.state_controller.update(self)

    def advance_timers(self):
        self.combat_controller.advance_timers(self)
        self.movement.advance_timers()

    def update_ai(self, context):
        self.ai_controller.update(self, context)

    def update_movement(self, context):
        if self.state in (self.ATTACK, self.RUN_ATTACK, self.JUMP_ATTACK):
            return
        if self.intent.wants_attack_player() or self.intent.wants_run_attack() or self.intent.wants_jump_attack():
            return

        self.movement.tick_air_cooldown()

        if self.intent.wants_jump():
            self.movement.start_jump()
        elif self.movement.is_jumping:
            self.movement.update_jump()
            if not self.movement.is_jumping:
                self.state = self.IDLE
        elif self.intent.wants_patrol():
            self.movement.patrol(self)
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
        if self.intent.wants_run_attack() and self.state != self.RUN_ATTACK:
            self.combat_controller.start_run_attack(self)
            self.intent.clear()
        elif self.intent.wants_jump_attack() and self.state != self.JUMP_ATTACK:
            self.combat_controller.start_jump_attack(self)
            self.intent.clear()
        elif self.intent.wants_attack_player() and self.state != self.ATTACK:
            self.combat_controller.start_attack(self)
            self.intent.clear()

        if self.state == self.RUN_ATTACK:
            self.combat_controller.update_run_attack(self, context.level, context.player)
        elif self.state == self.JUMP_ATTACK:
            self.combat_controller.update_jump_attack(self, context.level, context.player)
        elif self.state == self.ATTACK:
            self.combat_controller.update_attack(self, context.level, context.player)

    def update_reactions(self):
        self.reaction_controller.update_reactions(self)

    def update_animation(self):
        self.animation_controller.update(self)

    # --- Public API ---

    def is_ready_to_remove(self):
        return self.state_controller.is_ready_to_remove(self)

    def take_damage(self, damage, attacker_x=None, reaction=None):
        if isinstance(damage, DamageRequest):
            request = damage
            damage = request.damage
            attacker_x = request.attacker_x if request.attacker_x is not None else attacker_x
            reaction = request.reaction
        if attacker_x is None:
            attacker_x = self.x
        self.reaction_controller.take_damage(self, damage, attacker_x, reaction=reaction)

    def grabbed_by_player(self):
        self.reaction_controller.grabbed_by_player(self)

    def thrown_by_player(self, direction, damage):
        self.reaction_controller.thrown_by_player(self, direction, damage)

    def take_grab_knee_damage(self, damage):
        self.reaction_controller.take_grab_knee_damage(self, damage)

    def create_loot(self):
        return self.loot_controller.create_loot(self)
