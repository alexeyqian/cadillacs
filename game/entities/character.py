from game.entities.game_object import GameObject


class Character(GameObject):
    def __init__(
        self,
        x=0,
        y=0,
        width=0,
        height=0,
        state=None,
        facing_right=True,
        speed=0,
        sprite_scale=1,
    ):
        super().__init__(x, y, width, height)
        self.display_name = ""
        self.state = state
        self.facing_right = facing_right
        self.speed = speed
        self.sprite_scale = sprite_scale

        self.health = None
        self.movement = None
        self.combat_controller = None
        self.lifecycle_controller = None
        self.geometry = None
        self.animation_controller = None
        self.renderer = None
        self.air = None

    def draw(self, screen, camera_x):
        if not self.visible:
            return
        self._require_component("renderer").draw(self, screen, camera_x)

    def get_frame_rect(self):
        return self._require_component("geometry").get_frame_rect(self)

    def get_collision_rect(self):
        return self._require_component("geometry").get_collision_rect(self)

    def get_hurt_rect(self):
        return self._require_component("geometry").get_hurt_rect(self)

    def get_attack_rect(self):
        return self._require_component("geometry").get_attack_rect(self)

    def apply_world_bounds(self, world_width=None, lane_top=None, lane_bottom=None):
        self._require_component("movement").apply_world_bounds(
            self,
            world_width,
            lane_top,
            lane_bottom,
        )

    def _require_component(self, name):
        component = getattr(self, name, None)
        if component is None:
            raise AttributeError(
                f"{self.__class__.__name__} requires a {name} component"
            )
        return component
