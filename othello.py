from collections import defaultdict


BLACK_PIECE = 1
WHITE_PIECE = 2


class Cell:

    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col
        self.piece = None

    def get_id(self) -> int:
        return self.id

    def is_empty(self) -> bool:
        return self.piece == None

    def get_piece(self) -> 'piece type':
        return self.piece

    def set_piece(self, piece) -> None:
        self.piece = piece

    def get_row(self) -> int:
        return self.row

    def get_col(self) -> int:
        return self.col

    def get_west(self) -> '(row, col)':
        return (self.row, self.col - 1)

    def get_east(self) -> '(row, col)':
        return (self.row, self.col + 1)

    def get_north(self) -> '(row, col)':
        return (self.row - 1, self.col)

    def get_south(self) -> '(row, col)':
        return (self.row + 1, self.col)

    def get_northwest(self) -> '(row, col)':
        return (self.row - 1, self.col - 1)

    def get_northeast(self) -> '(row, col)':
        return (self.row - 1, self.col + 1)

    def get_southwest(self) -> '(row, col)':
        return (self.row + 1, self.col - 1)

    def get_southeast(self) -> '(row, col)':
        return (self.row + 1, self.col + 1)

    def to_str(self) -> None:
        return 'r: {}, c: {}'.format(self.row, self.col)


class OthelloBoard:

    def __init__(self, row_count: int, col_count: int, top_left: int, high_count_wins: bool,
                first_turn: 'piece type') -> None:
        self.row_count = row_count
        self.col_count = col_count
        self.board = self._init_board(top_left)
        self.high_count_wins = high_count_wins
        self.possible_valid_moves = self._calculate_possible_valid_moves(first_turn)
        self.piece_count = self._get_piece_count()

    def _init_board(self, top_left) -> [[int]]:
        board = [[Cell(row, col) for col in range(self.col_count)] for row in range(self.row_count)]

        r = int(self.row_count / 2 - 1)
        c = int(self.col_count / 2 - 1)
        if top_left == WHITE_PIECE:
            board[r][c].set_piece(WHITE_PIECE)
            board[r][c + 1].set_piece(BLACK_PIECE)
            board[r + 1][c].set_piece(BLACK_PIECE)
            board[r + 1][c + 1].set_piece(WHITE_PIECE)
        else:
            board[r][c].set_piece(BLACK_PIECE)
            board[r][c + 1].set_piece(WHITE_PIECE)
            board[r + 1][c].set_piece(WHITE_PIECE)
            board[r + 1][c + 1].set_piece(BLACK_PIECE)

        return board

    def print_board(self) -> None:
        print(' ', end = ' ')
        for c in range(self.col_count):
            print(str(c + 1), end = ' ')
        print()
        for r in range(self.row_count):
            print('{}'.format(r + 1), end = ' ')
            for c in range(self.col_count):
                cell = self.board[r][c]
                cell_str = None
                if cell.get_piece() == BLACK_PIECE:
                    cell_str = 'B'
                elif cell.get_piece() == WHITE_PIECE:
                    cell_str = 'W'
                else:
                    cell_str = '.'
                print(cell_str, end = ' ')
            print()

    def get_cell(self, pos: '(row, col)') -> Cell:
        row = pos[0]
        col = pos[1]
        if row >= 0 and row < self.row_count:
            if col >= 0 and col < self.col_count:
                return self.board[row][col]
        return None

    def get_opponent_piece_type(self, piece_type) -> 'piece type':
        if piece_type == BLACK_PIECE:
            return WHITE_PIECE
        else:
            return BLACK_PIECE

    def place_piece(self, piece_type, row, col) -> bool:
        key = self._flatten_row_col(row, col)
        if key in self.possible_valid_moves:
            self.board[row][col].set_piece(piece_type)

            for marked_cell in self.possible_valid_moves[key][1]:
                marked_cell.set_piece(piece_type)

            self.piece_count = self._get_piece_count()
            self.skip_player_move(piece_type)
            return True
        return False

    def skip_player_move(self, piece_type: 'piece type') -> None:
        opponent_piece = self.get_opponent_piece_type(piece_type)
        self.possible_valid_moves = self._calculate_possible_valid_moves(opponent_piece)
        # OthelloBoard._print_possible_moves(self.possible_valid_moves)

    def get_possible_valid_moves_num(self, piece_type = None) -> int:
        if piece_type == None:
            return len(self.possible_valid_moves.keys())
        else:
            return len(self._calculate_possible_valid_moves(piece_type).keys())

    def check_win(self) -> 'BLACK_PIECE, WHITE_PIECE or None':
        b_count = self.piece_count[0]
        w_count = self.piece_count[1]

        if self.high_count_wins:
            if b_count > w_count:
                return BLACK_PIECE
            elif b_count < w_count:
                return WHITE_PIECE
            else:
                return None
        else:
            if b_count < w_count:
                return BLACK_PIECE
            elif b_count > w_count:
                return WHITE_PIECE
            else:
                return None

    def get_piece_count(self, piece_type: 'piece type') -> int:
        if piece_type == BLACK_PIECE:
            return self.piece_count[0]
        else:
            return self.piece_count[1]

    def _get_piece_count(self) -> '(black_piece_count, white_piece_count)':
        b_count = 0
        w_count = 0
        for r in range(self.row_count):
            for c in range(self.col_count):
                cell = self.board[r][c]
                if cell.get_piece() == BLACK_PIECE:
                    b_count += 1
                elif cell.get_piece() == WHITE_PIECE:
                    w_count += 1

        return b_count, w_count

    # For debug purposes
    def _print_possible_moves(possible_valid_moves) -> None:
        print('possible valid moves: ')
        for key in possible_valid_moves.keys():
            valid_cell, marked_cells = possible_valid_moves[key]
            print(valid_cell.to_str())

            for marked_cell in marked_cells:
                print('    {}'.format(marked_cell.to_str()))

    def _get_flattened_cell_pos(self, cell: Cell) -> int:
        return self._flatten_row_col(cell.get_row(), cell.get_col())

    def _flatten_row_col(self, row: int, col: int) -> int:
        return row * self.col_count + col

    def _calculate_possible_valid_moves(self, piece) -> dict:
        possible_valid_moves = defaultdict(list)

        for r in range(self.row_count):
            for c in range(self.col_count):
                cell = self.board[r][c]
                if cell.get_piece() != piece:
                    continue

                valid_cells = []
                valid_cells.append(self._get_possible_valid_moves(cell, lambda c: c.get_east()))
                valid_cells.append(self._get_possible_valid_moves(cell, lambda c: c.get_west()))
                valid_cells.append(self._get_possible_valid_moves(cell, lambda c: c.get_north()))
                valid_cells.append(self._get_possible_valid_moves(cell, lambda c: c.get_south()))
                valid_cells.append(self._get_possible_valid_moves(cell, lambda c: c.get_northeast()))
                valid_cells.append(self._get_possible_valid_moves(cell, lambda c: c.get_northwest()))
                valid_cells.append(self._get_possible_valid_moves(cell, lambda c: c.get_southeast()))
                valid_cells.append(self._get_possible_valid_moves(cell, lambda c: c.get_southwest()))

                for element in valid_cells:
                    if element != None:
                        valid_cell, marked_cells = element
                        key = self._get_flattened_cell_pos(valid_cell)
                        if key in possible_valid_moves:
                            for marked_cell in marked_cells:
                                possible_valid_moves[key][1].append(marked_cell)
                        else:
                            possible_valid_moves[key] = (valid_cell, marked_cells)

        return possible_valid_moves

    def _get_possible_valid_moves(self, cell, dir_function) -> '(valid cell, marked cells)':
        stack = []
        west = self.get_cell(dir_function(cell))
        piece_type = cell.get_piece()
        while west != None:
            if west.is_empty():
                stack.append(west)
                break
            if west.get_piece() == piece_type:
                break

            if west.get_piece() != piece_type:
                stack.append(west)
            west = self.get_cell(dir_function(west))

        if len(stack) > 1:
            top = stack.pop()
            if top.is_empty():
                return top, stack
