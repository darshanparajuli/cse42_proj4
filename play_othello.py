import othello


def _get_input_in_range(min: int, max: int) -> int:
    user_input = _get_user_input_as_int()
    if user_input != None:
        if user_input >= min and user_input <= max:
            return user_input


def _get_matching_user_input(required: 'tuple of chars') -> str:
    user_input = input().strip()
    if user_input in required:
        return user_input


def _get_player_move() -> '(row, col)':
    user_input = input().split()
    if type(user_input) == list and len(user_input) == 2:
        try:
            return int(user_input[0]), int(user_input[1])
        except ValueError:
            return None


def _get_user_input_as_int() -> int:
    user_input = input().strip()
    try:
        return int(user_input)
    except ValueError:
        return None


def init_game() -> 'Othello game board, first player piece type':
    print('FULL')
    options = othello.OthelloBoardOptions()
    options.set_row_count(_get_input_in_range(4, 16))
    options.set_col_count(_get_input_in_range(4, 16))

    first_turn = _get_matching_user_input(('W', 'B'))
    top_left = _get_matching_user_input(('W', 'B'))
    win_condition = _get_matching_user_input(('<', '>'))

    first_turn = othello.BLACK_PIECE if first_turn == 'B' else othello.WHITE_PIECE

    options.set_first_turn(first_turn)
    options.set_top_left_piece(othello.BLACK_PIECE if top_left == 'B' else othello.WHITE_PIECE)
    options.set_high_count_wins(win_condition == '>')

    game = othello.OthelloBoard(options)

    return game, first_turn


def play_game(game: 'Othello game board', first_turn: 'piece type') -> None:
    players = {othello.BLACK_PIECE: 'B', othello.WHITE_PIECE: 'W'}
    current_player = first_turn

    while True:
        b_count = game.get_piece_count(othello.BLACK_PIECE)
        w_count = game.get_piece_count(othello.WHITE_PIECE)
        print('B: {}  W: {}'.format(b_count, w_count))
        game.print_board()

        opponent = game.get_opponent_piece_type(current_player)
        if game.get_possible_valid_moves_num() == 0:
            if game.get_possible_valid_moves_num(opponent) == 0:
                break
            else:
                game.skip_player_move(current_player)
                current_player = opponent
                continue

        print('TURN: {}'.format(players[current_player]))

        while True:
            # player_move = None
            # if current_player == othello.BLACK_PIECE:
            row, col = game.get_ai_move(current_player)
            row += 1
            col += 1
            print('{} {}'.format(row, col))
            player_move = row, col
            # else:
            # player_move = _get_player_move()

            if player_move != None:
                row, col = player_move
                if game.place_piece(current_player, row - 1, col - 1):
                    current_player = opponent
                    print('VALID')
                    break;
            print('INVALID')

    winner = game.check_win()
    winning_player = 'NONE'
    if winner == othello.BLACK_PIECE:
        winning_player = 'B'
    else:
        winning_player = 'W'
    print('WINNER: {}'.format(winning_player))


def main() -> None:
    game, first_player = init_game()
    play_game(game, first_player)


if __name__ == '__main__':
    main()
