from game.effects.floating_text import FloatingText


class LifeRewardSystem:
    @staticmethod
    def update(game_state):
        score_manager = game_state.score_manager
        player = game_state.player
        while score_manager.should_award_extra_life():
            player.lifecycle_controller.gain_life()
            game_state.floating_texts.append(
                FloatingText(player.x, player.y - 40, "+1 LIFE", (0, 255, 255)))
            score_manager.advance_extra_life_threshold()
