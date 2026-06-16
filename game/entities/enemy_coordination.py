class EnemyCoordination:
    # Later we can upgrade it into an “attack reservation” system
    def uses_melee_attack_slot(self, owner):
        return owner.archetype not in ["ranged", "boss"]

    def can_bypass_attack_slot_limit(self, owner):
        return owner.archetype in ["boss", "ranged"]

    def get_side_of_player(self, owner, player):
        if owner.x < player.x:
            return "left"
        return "right"
