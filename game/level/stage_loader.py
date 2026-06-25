from game.entities.breakable_object import BreakableObject
from game.entities.explosive_barrel import ExplosiveBarrel
from game.entities.weapon import Weapon
from game.level.level import Level


def load_stage(game_state, stage_data):
    game_state.level = Level(stage_data)

    # Do not create a new Player. Keep the same player so lives, score,
    # and weapon behavior can be decided intentionally later.
    start_x, start_y = stage_data["player_start"]
    game_state.player.reset_for_stage_start(start_x, start_y)

    game_state.camera.x = 0

    game_state.enemies.clear()
    game_state.weapons.clear()
    game_state.projectiles.clear()
    game_state.enemy_projectiles.clear()
    game_state.objects.clear()
    game_state.loot_items.clear()
    game_state.hit_sparks.clear()
    game_state.floating_texts.clear()
    game_state.explosions.clear()

    game_state.weapons.extend(_create_weapons(stage_data))
    game_state.objects.extend(_create_objects(stage_data))

    game_state.stage_clear_manager.active = False
    game_state.stage_clear_manager.timer = 0
    game_state.stage_clear_manager.bonus_applied = False

    game_state.announcement_manager.active = False


def load_current_stage(game_state):
    load_stage(game_state, game_state.stage_manager.get_current_stage())


def advance_to_next_stage(game_state):
    next_stage_data = game_state.stage_manager.advance_stage()
    if next_stage_data:
        load_stage(game_state, next_stage_data)
        return True
    return False


def _create_weapons(stage_data):
    return [
        Weapon(wc["x"], wc["y"], wc["type"])
        for wc in stage_data["weapons"]
    ]


def _create_objects(stage_data):
    objects = []
    for oc in stage_data["objects"]:
        kind = oc["kind"]
        if kind == "breakable":
            objects.append(BreakableObject(oc["x"], oc["y"], loot_type=oc.get("loot_type")))
        elif kind == "barrel":
            objects.append(ExplosiveBarrel(oc["x"], oc["y"]))
    return objects
