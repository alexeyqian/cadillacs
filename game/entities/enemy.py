from game.entities.character import Character
from game.data.enemy_config import get_enemy_config
from game.entities.enemy_state import EnemyState
from game.components.character_health import CharacterHealth
from game.components.character_geometry import CharacterGeometry
from game.controllers.enemy_animation_controller import EnemyAnimationController
from game.components.enemy_renderer import EnemyRenderer
from game.components.enemy_movement import EnemyMovement
from game.components.enemy_flanking import EnemyFlanking
from game.components.enemy_life_cycle import EnemyLifeCycle
from game.controllers.enemy_combat_controller import EnemyCombatController
from game.controllers.enemy_reaction_controller import EnemyReactionController
from game.controllers.enemy_lifecycle_controller import EnemyLifecycleController
from game.controllers.enemy_state_controller import EnemyStateController
from game.controllers.enemy_loot_controller import EnemyLootController
from game.combat.damage_request import DamageRequest

class Enemy(Character, EnemyState):
    def __init__(self, x, y, enemy_type, 
                animation_data, anim_fps, sprite_scale=4):
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
        self.life_cycle = EnemyLifeCycle()
        self.geometry = CharacterGeometry()
        self.movement = EnemyMovement(spawn_x=self.x)
        self.flanking = EnemyFlanking()

    def build_controllers(self):
        self.combat_controller = EnemyCombatController()
        self.reaction_controller = EnemyReactionController()
        self.lifecycle_controller = EnemyLifecycleController()
        self.state_controller = EnemyStateController()
        self.loot_controller = EnemyLootController()

    def configure_from_enemy_config(self, config):
        self.apply_identity_config(config)
        self.apply_body_config(config)
        self.apply_movement_config(config)
        self.apply_combat_config(config)
        self.apply_reward_config(config)

    def build_presentation_components(self, animation_data, anim_fps):
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
        )

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
        return self.lifecycle_controller.update_special_states(self)

    def advance_timers(self):
        self.lifecycle_controller.update_timers(self)

    def update_ai(self, level, player, enemies):
        dx, dy, distance_x, distance_y = self.movement.get_player_distance(self, player)

        if distance_x <= self.movement.detect_range:
            self._face_player(player)

        self.state_controller.choose_state(
            self, level, player, distance_x, distance_y, enemies
        )
        return dx, dy

    def update_movement(self, level, player, enemies):
        dx, dy, distance_x, distance_y = self.movement.get_player_distance(self, player)
        if self.state == self.ATTACK:
            return
        self.state_controller.execute_movement_state(self, level, player, enemies, dx, dy)

    def update_attack(self, level, player):
        if self.state != self.ATTACK:
            return
        self.combat_controller.update_attack(self, level, player)

    def update_reactions(self):
        if self.lifecycle_controller.update_hit_state(self):
            return True
        self.reaction_controller.apply_knockback(self)
        return False

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

    def _face_player(self, player):
        self.movement.face_player(self, player)

    # Combat
    def start_attack(self):
        self.combat_controller.start_attack(self)

    # Loot
    def create_loot(self):
        return self.loot_controller.create_loot(self)
