from collections import OrderedDict
from outcomes import Strike, MultiStrike, RedStrike, StrikerStrike, DefunctCoin, NoneStrike

OUTCOMES_MAP = OrderedDict()
OUTCOMES_MAP["Strike"] = Strike
OUTCOMES_MAP["Multi Strike"] = MultiStrike
OUTCOMES_MAP["Red Strike"] = RedStrike
OUTCOMES_MAP["Striker Strike"] = StrikerStrike
OUTCOMES_MAP["Defunct Coin"] = DefunctCoin
OUTCOMES_MAP["None"] = NoneStrike


def get_input_message():
    msg = ''
    i = 1
    for outcome in OUTCOMES_MAP.keys():
        msg = msg + str(i) + ". " + outcome + "\n"
        i = i + 1
    return msg

class OutcomeFactory:
    
    def load_outcomes(self):
        self.outcomes_to_objects_map = {}
        for outcome in OUTCOMES_MAP.keys():
            self.outcomes_to_objects_map[outcome] = OUTCOMES_MAP[outcome]()

    def get_outcome_object(self,input_no):
        if input_no <= len(OUTCOMES_MAP.keys()):
            outcome = OUTCOMES_MAP.keys()[input_no - 1]
            return self.outcomes_to_objects_map[outcome]
        return None

if __name__ == "__main__":
    # this is just test piece of code to test this module alone.
    factory = OutcomeFactory()
    factory.load_outcomes()
    o = factory.get_outcome_object(1)
    p_impact = o.get_player_impact()
    b_impact = o.get_board_impact()
    print p_impact.impact(10)
    print b_impact.impact(20)

    o = factory.get_outcome_object(3)
    p_impact = o.get_player_impact()
    b_impact = o.get_board_impact()
    print p_impact.impact(10)
    print b_impact.impact(20)
