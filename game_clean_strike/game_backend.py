

class GameRunner:

    def __init__(self):
        self.game_loader = GameLoader()
        self.game = self.game_loader.load_game()
        self.in_loader = InputLoader(InputWays.LOAD_FROM_COMMAND_LINE)
        self.is_running = True

    def play(self):
        while(self.is_running):
            outcome = self.in_loader.ask_for_input(self.current_player)
            if outcome is None:
                self.is_running = False
                break
            self.is_running = self.game.play(outcome)

    
