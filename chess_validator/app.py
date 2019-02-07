import sys
from chesslib.check import is_valid_move

def display(board):
    for row in board:
        print " ".join(row)
    print "\n"

def change_board_status(board, moves):
    for each in moves:
        print "=========================================================="
        print each, ": \n"
        try:
            if is_valid_move(board, each):
                piece, start, dest = each.split(" ")
                board[int(dest[0])][int(dest[1])] = piece
                board[int(start[0])][int(start[1])] = "--"
                display(board)
            else:
                print "Error: Invalid Move\n"
        except Exception as e:
            print "Error: Some error occured - " + str(e)

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print "pass input file"
        sys.exit(0)
    file_path = sys.argv[1]
    board = []
    moves = []
    with open(file_path) as fp:
        fp.readline()
        for i in range(0,8):
            line = fp.readline().strip()
            board.append(line.split(" "))
        fp.readline()
        while(1):
            line = fp.readline().strip()
            if not line:
                break
            moves.append(line)
    change_board_status(board, moves)
