
from outcomes import BLACK, RED

class Board:

    def __init__(self, black_coins=0, red_coins=0):
        self.black_coins = black_coins
        self.red_coins = red_coins

    def get_black_coints(self):
        return self.black_coins

    def get_red_coints(self):
        return self.red_coins

    def is_empty(self):
        return (self.black_coins == 0 and self.red_coins == 0)

    def change_board_state(self, coin_type, impact_obj):
        if coin_type == BLACK:
            self.black_coins = impact_obj.impact(self.black_coins)
        elif coin_type == RED:
            self.red_coins = impact_obj.impact(self.red_coins)
