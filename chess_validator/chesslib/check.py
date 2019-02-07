
from chesslib.factory import get_object

def is_valid_move(board, each):
    piece, start, dest = each.split(" ")
    if board[int(start[0])][int(start[1])] != piece:
        return False
    p_obj = get_object(piece[1], piece[0])
    possible_moves = p_obj.get_possible_moves(int(start[0]), int(start[1]))
    dest_move = (int(dest[0]), int(dest[1]))
    if dest_move in possible_moves:
        dest_i = int(dest[0])
        dest_j = int(dest[1])
        dest_piece = board[dest_i][dest_j]
        if piece[1] != 'P':
            if dest_piece == "--" or (not dest_piece.startswith(piece[0])):
                return True
            else:
                return False
        else:
            if dest_move[1] != int(start[1]):
                if dest_piece == "--" or dest_piece.startswith(piece[0]):
                    return False
                else:
                    return True
            else:
                if dest_piece != "--":
                    return False
                else:
                    if abs(dest_move[0] - int(start[0])) > 1:
                        if piece[0] == 'W':
                            temp_i = int(start[0]) + 1
                        else:
                            temp_i = int(start[0]) - 1
                        if board[temp_i][dest_move[1]] != "--":
                            return False
                    return True

    else:
        return False
