from piece import King, Queen, Horse, Bishop, Pawn, Rook

piece = {
    "K" : King,
    "Q" : Queen,
    "H" : Horse,
    "B" : Bishop,
    "P" : Pawn,
    "R" : Rook
}


def get_object(p, color):
    return piece[p](color)


if __name__ == "__main__":
    obj = get_object("P","W")
    print obj.get_possible_moves(3,3)
