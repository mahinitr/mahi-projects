
from outcome_factory import get_input_message

class InputWays:
    LOAD_FROM_FILE = 1
    LOAD_FROM_COMMAND_LINE = 2

class InputLoader:

    def __init__(self, load_from=InputWays.LOAD_FROM_FILE, input_outcomes=[]):
        self.load_from = load_from
        self.input_outcomes = input_outcomes
        self.next_input = 0
        self.total_inputs = len(self.input_outcomes)

    def ask_for_input(self, player):
        try:
            input_no = None
            if self.load_from == InputWays.LOAD_FROM_FILE:
                if self.next_input < self.total_inputs:
                    input_no = self.input_outcomes[self.next_input]
                    self.next_input =  self.next_input + 1
            else:
                msg = "Player " + str(player) + ":"
                msg = msg + "Please choose an outcome from the list below.\n"
                msg = msg + get_input_message()
                input_no = int(raw_input(msg))
            return input_no
        except Exception as e:
            print "Error: Oops! something happened while asking for input"
            return None


if __name__ == "__main__":
    # just small of piece of code to test this module alone
    print "taking the input from command line..."
    loader = InputLoader(2)
    print loader.ask_for_input(1)
    print loader.ask_for_input(2)
    print loader.ask_for_input(1)

    print "taking the input from file..."
    loader = InputLoader(1, "tests/test_cases/test_case_1.txt")
    print loader.ask_for_input(1)
    print loader.ask_for_input(2)
    print loader.ask_for_input(1)
    print loader.ask_for_input(2)
