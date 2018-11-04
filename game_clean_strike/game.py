import json
import sys
from board import Board
from player import Player
from input_handler import InputLoader
from outcome_factory import OutcomeFactory

CONFIG_FILE = "game_config.json"

class Game:

    def __init__(self):
        self.game_config = {}
        self.board = None
        self.outcome_factory = None
        self.players = []
        self.load_config()
        self.current_player = 1
        self.is_running = True
        self.winner = None
        self.is_game_draw = False

    def load_config(self):
        try:
            with open(CONFIG_FILE) as fp:
                self.game_config = json.load(fp)
        except:
            raise Exception("Error: Failed to load game config")

    def init_game(self, input_outcomes=[]):
        b_coins = self.game_config["black_coins"]
        r_coins = self.game_config["red_coins"]
        no_players = self.game_config["no_of_players"]
        load_from = self.game_config["load_input_from"]
        self.in_loader = InputLoader(load_from, input_outcomes)
        self.board = Board(b_coins, r_coins)
        for i in range(0, no_players):
            self.players.append(Player())
        self.outcome_factory = OutcomeFactory()
        self.outcome_factory.load_outcomes()
        return True

    def update_current_player(self):
        self.current_player = self.current_player + 1
        if self.current_player > len(self.players):
            self.current_player = 1

    def get_result(self):
        result = "Result: %s. Final Scores: %s %s"
        if self.winner == 1:
            winner_name = "Winner - P1"
        elif self.winner == 2:
            winner_name = "Winner - P2"
        else:
            winner_name = "Draw"
        return result % (
            winner_name,
            self.players[0].get_points(),
            self.players[1].get_points())

    def is_there_any_winner(self):
        p1_points = self.players[0].get_points()
        p2_points = self.players[1].get_points()
        min_points = p1_points
        max_points = p1_points
        max_player = 1
        if p2_points > max_points:
            max_points = p2_points
            max_player = 2
        else:
            min_points = p2_points

        diff = max_points - min_points
        winner = None
        if max_points >= 5 and diff >= 3:
            winner = max_player
        return winner

    def check_game_status(self):
        winner = self.is_there_any_winner()
        if winner:
            self.winner = winner
            self.is_running = False
            return
        if self.board.is_empty():
            self.is_running = False
            self.is_game_draw = False

    def play(self):
        while(self.is_running):
            outcome = self.in_loader.ask_for_input(self.current_player)
            if outcome is None:
                self.is_running = False
                break
            outcome_obj = self.outcome_factory.get_outcome_object(outcome)
            player_impact = outcome_obj.get_player_impact()
            board_impact = outcome_obj.get_board_impact()
            player_obj = self.players[self.current_player - 1]
            player_obj.change_player_state(player_impact)
            coin_type = outcome_obj.coin_type
            if coin_type:
                self.board.change_board_state(coin_type, board_impact)
            #print str(self.current_player), "input - ", outcome
            #print player_obj.points, self.board.black_coins, self.board.red_coins
            #print "\n"
            self.check_game_status()
            self.update_current_player()

if __name__ == "__main__":
    input_outcomes = [1,1,2,4,3,1]
    game = Game()
    game.init_game(input_outcomes)
    game.play()
    result = game.get_result()
    print result

