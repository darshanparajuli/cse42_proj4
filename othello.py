import othello_board


def init_game() -> None:
    othello = othello_board.OthelloBoard(first_turn = othello_board.BLACK_PIECE)
    othello.print_board()
    othello.calculate_possible_valid_moves(othello_board.BLACK_PIECE)

if __name__ == '__main__':
    init_game()
