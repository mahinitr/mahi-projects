class Piece:

    def __init__(self):
        self.color = None

N = 8
DIR_MOVE_MAP = {
    "TOP" : (-1,0),
    "BOT" : ( 1,0),
    "LEF" : (0,-1),
    "RIG" : (0, 1),
    "TR"  : (-1,1),
    "BL"  : (1,-1),
    "TL"  : (-1,-1),
    "BR"  : (1,1) 
}


def generate_possible_moves(steps, curr_i, curr_j):
    moves = []
    for next_step in steps:
        new_i = next_step[0] + curr_i
        new_j = next_step[1] + curr_j
        if 0 <= new_i and new_i < N and 0 <= new_j and new_j < N:
            moves.append((new_i, new_j))
    return moves

def load_steps(allowed_dirs, max_no_steps):
    steps = []
    for each in allowed_dirs:
        step = DIR_MOVE_MAP[each]
        for i in range(1, max_no_steps):
            steps.append((i * step[0], i * step[1]))
    return steps

class Queen:

    def __init__(self, color):
        self.max_no_steps = N
        self.allowed_dirs = ["TOP", "BOT", "LEF", "RIG", "TR", "BL", "TL", "BR"]
        self.steps = load_steps(self.allowed_dirs, self.max_no_steps)

    def get_possible_moves(self, curr_i, curr_j):
        return generate_possible_moves(self.steps, curr_i, curr_j)

class King:
    def __init__(self, color):
        self.max_no_steps = 2
        self.allowed_dirs = ["TOP", "BOT", "LEF", "RIG", "TR", "BL", "TL", "BR"]
        self.steps = load_steps(self.allowed_dirs, self.max_no_steps)

    def get_possible_moves(self, curr_i, curr_j):
        return generate_possible_moves(self.steps, curr_i, curr_j)

class Rook:
    def __init__(self, color):
        self.max_no_steps = N
        self.allowed_dirs = ["TOP", "BOT", "LEF", "RIG"]
        self.steps = load_steps(self.allowed_dirs, self.max_no_steps)

    def get_possible_moves(self, curr_i, curr_j):
        return generate_possible_moves(self.steps, curr_i, curr_j)

class Bishop:
    def __init__(self, color):
        self.max_no_steps = N
        self.allowed_dirs = ["TR", "BL", "TL", "BR"]
        self.steps = load_steps(self.allowed_dirs, self.max_no_steps)

    def get_possible_moves(self, curr_i, curr_j):
        return generate_possible_moves(self.steps, curr_i, curr_j)

class Horse:

    def __init__(self, color):
        self.max_no_steps = N
        self.steps = [(-1,-2), (-2,-1), (-2,1), (-1,2), (1,-2), (2,-1), (1,2), (2,1)]

    def get_possible_moves(self, curr_i, curr_j):
        return generate_possible_moves(self.steps, curr_i, curr_j)

class Pawn:

    def __init__(self, color):
        self.max_no_steps = N
        if color == "W":
            self.steps = [(1,0), (2,0), (1,-1), (1,1)]
        else:
            self.steps = [(-1,0), (-2,0), (-1,-1), (-1,1)]

    def get_possible_moves(self, curr_i, curr_j):
        return generate_possible_moves(self.steps, curr_i, curr_j)

if __name__ == "__main__":
    king = Horse("W")
    king.get_possible_moves(1,1)
