import othello_board


def init_game() -> None:
    othello = othello_board.OthelloBoard(white_piece_first = False)
    othello.print_board()


if __name__ == '__main__':
    init_game()
