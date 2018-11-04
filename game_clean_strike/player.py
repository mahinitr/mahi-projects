
class Player:

    def __init__(self):
        self.points = 0
        self.continuous_loses = 0
        self.continuous_fouls = 0

    def get_points(self):
        return self.points

    def change_player_state(self, impact_obj):
        new_points = impact_obj.impact(self.points)
        if new_points <= self.points:
            self.continuous_loses = self.continuous_loses + 1
        if new_points < self.points:
            self.continuous_fouls = self.continuous_fouls + 1
        if new_points > self.points:
            self.continuous_loses = 0
            self.continuous_fouls = 0

        self.points = new_points

        if self.continuous_loses == 3:
            self.points = self.points - 1
            self.continuous_loses = 0

        if self.continuous_fouls == 3:
            self.continuous_fouls = 0
            self.points = self.points - 1

        if self.points < 0:
            self.points = 0
