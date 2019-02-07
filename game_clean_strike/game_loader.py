
CONFIG_FILE = "game_config.json"

class GameLoader:

    def __init__(self):
        self.game_config = {}
        self.load_from = None
    def load_config(self):
        try:
            with open(CONFIG_FILE) as fp:
                self.game_config = json.load(fp)
        except:
            raise Exception("Error: Failed to load game config")

    def load_game(self):
        self.load_config()
        b_coins = self.game_config["black_coins"]
        r_coins = self.game_config["red_coins"]
        no_players = self.game_config["no_of_players"]
        self.load_from = self.game_config["load_input_from"]
        game  = Game(b_coins, r_coins, no_players)
        return game

    def get_load_from(self):
        return self.load_from;
