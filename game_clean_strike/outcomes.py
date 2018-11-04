"""
this contains the outcomes classes and impact class for updating the player points and board coins
"""

IMPACT_PLAYER = 'impact_player'
IMPACT_BOARD = 'impact_board'
COIN_TYPE = "coin_type"
BLACK = "BLACK"
RED = "RED"

class IMPACT:
    """
    class for updating the points and coins
    """
    def __init__(self, c):
        self.c = c

    def impact(self, points):
        return points + self.c

class Outcome(object):
    """
    Base class for all outcomes
    self.player_impact - Impact object for updating the player points
    self.board_impact - Impact object for updating the board coins
    """
    def __init__(self, *args, **kwargs):
        self.player_impact = None
        self.board_impact = None
        self.coin_type = None
        if IMPACT_PLAYER in kwargs:
            self.player_impact = kwargs[IMPACT_PLAYER]
        if IMPACT_BOARD in kwargs:
            self.board_impact = kwargs[IMPACT_BOARD]
        if COIN_TYPE in kwargs:
            self.coin_type = kwargs[COIN_TYPE]

    def get_player_impact(self):
        return self.player_impact

    def get_board_impact(self):
        return self.board_impact

class Strike(Outcome):

    def __init__(self, *args, **kwargs):
        kwargs[IMPACT_PLAYER] = IMPACT(1)
        kwargs[IMPACT_BOARD] = IMPACT(-1)
        kwargs[COIN_TYPE] = BLACK
        super(Strike, self).__init__(*args, **kwargs)


class MultiStrike(Outcome):

    def __init__(self, *args, **kwargs):
        kwargs[IMPACT_PLAYER] = IMPACT(2)
        kwargs[IMPACT_BOARD] = IMPACT(0)
        kwargs[COIN_TYPE] = BLACK
        super(MultiStrike, self).__init__(*args, **kwargs)


class RedStrike(Outcome):

    def __init__(self, *args, **kwargs):
        kwargs[IMPACT_PLAYER] = IMPACT(3)
        kwargs[IMPACT_BOARD] = IMPACT(-1)
        kwargs[COIN_TYPE] = RED
        super(RedStrike, self).__init__(*args, **kwargs)

class StrikerStrike(Outcome):

    def __init__(self, *args, **kwargs):
        kwargs[IMPACT_PLAYER] = IMPACT(-1)
        kwargs[IMPACT_BOARD] = IMPACT(0)
        super(StrikerStrike, self).__init__(*args, **kwargs)

class DefunctCoin(Outcome):

    def __init__(self, *args, **kwargs):
        kwargs[IMPACT_PLAYER] = IMPACT(-2)
        kwargs[IMPACT_BOARD] = IMPACT(-1)
        kwargs[COIN_TYPE] = BLACK
        super(DefunctCoin, self).__init__(*args, **kwargs)

class NoneStrike(Outcome):

    def __init__(self, *args, **kwargs):
        kwargs[IMPACT_PLAYER] = IMPACT(0)
        kwargs[IMPACT_BOARD] = IMPACT(0)
        super(NoneStrike, self).__init__(*args, **kwargs)


if __name__ == "__main__":
    # just test to this module alone
    o = Strike()
    p_impact = o.get_player_impact()
    b_impact = o.get_board_impact()
    print p_impact.impact(10)
    print b_impact.impact(20)
    o = MultiStrike()
    p_impact = o.get_player_impact()
    b_impact = o.get_board_impact()
    print p_impact.impact(10)
    print b_impact.impact(20)
    o = RedStrike()
    p_impact = o.get_player_impact()
    b_impact = o.get_board_impact()
    print p_impact.impact(10)
    print b_impact.impact(20)
    o = StrikerStrike()
    p_impact = o.get_player_impact()
    b_impact = o.get_board_impact()
    print p_impact.impact(10)
    print b_impact.impact(20)
    o = DefunctCoin()
    p_impact = o.get_player_impact()
    b_impact = o.get_board_impact()
    print p_impact.impact(10)
    print b_impact.impact(20)
    o = NoneStrike()
    p_impact = o.get_player_impact()
    b_impact = o.get_board_impact()
    print p_impact.impact(10)
    print b_impact.impact(20)
