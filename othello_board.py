DEFAULT_BOARD_SIZE = 8
BLACK_PIECE = 1
WHITE_PIECE = 2


class Cell:

    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col
        self.piece = None

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

    def print(self) -> None:
        print('r: {}, c: {}'.format(self.row, self.col))


class OthelloBoard:

    def __init__(self, board_size = DEFAULT_BOARD_SIZE, first_turn = BLACK_PIECE) -> None:
        self.row_count = board_size
        self.col_count = board_size
        self.board = self._init_board(first_turn)
        self.possible_valid_moves = []

    def _init_board(self, first_turn) -> [[int]]:
        board = [[Cell(row, col) for col in range(self.col_count)] for row in range(self.row_count)]

        x = int(self.col_count / 2 - 1)
        y = int(self.row_count / 2 - 1)
        if first_turn == WHITE_PIECE:
            board[y][x].set_piece(BLACK_PIECE)
            board[y][x + 1].set_piece(WHITE_PIECE)
            board[y + 1][x].set_piece(WHITE_PIECE)
            board[y + 1][x + 1].set_piece(BLACK_PIECE)
        else:
            board[y][x].set_piece(WHITE_PIECE)
            board[y][x + 1].set_piece(BLACK_PIECE)
            board[y + 1][x].set_piece(BLACK_PIECE)
            board[y + 1][x + 1].set_piece(WHITE_PIECE)

        return board

    def print_board(self) -> None:
        for r in range(self.row_count):
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

    def place_piece(self, piece_type, row, col):
        pass

    def _print_possible_moves(self) -> None:
        print('possible valid moves: ')
        for cell in self.possible_valid_moves:
            cell.print()

    def calculate_possible_valid_moves(self, piece) -> None:
        self.possible_valid_moves = []

        for r in range(self.row_count):
            for c in range(self.col_count):
                cell = self.board[r][c]
                if cell.get_piece() != piece:
                    continue

                valid_cells = []
                valid_cells.append(self._calculate_possible_valid_moves(cell, lambda c: c.get_east()))
                valid_cells.append(self._calculate_possible_valid_moves(cell, lambda c: c.get_west()))
                valid_cells.append(self._calculate_possible_valid_moves(cell, lambda c: c.get_north()))
                valid_cells.append(self._calculate_possible_valid_moves(cell, lambda c: c.get_south()))
                valid_cells.append(self._calculate_possible_valid_moves(cell, lambda c: c.get_northeast()))
                valid_cells.append(self._calculate_possible_valid_moves(cell, lambda c: c.get_northwest()))
                valid_cells.append(self._calculate_possible_valid_moves(cell, lambda c: c.get_southeast()))
                valid_cells.append(self._calculate_possible_valid_moves(cell, lambda c: c.get_southwest()))
                for valid_cell in valid_cells:
                    if valid_cell != None:
                        self.possible_valid_moves.append(valid_cell)

        self._print_possible_moves()

    def _calculate_possible_valid_moves(self, cell, dir_function) -> Cell:
        stack = []
        west = self.get_cell(dir_function(cell))
        while west != None:
            if west.is_empty():
                stack.append(west)
                break
            elif west.get_piece() != cell.get_piece():
                stack.append(west)

            west = self.get_cell(dir_function(west))

        if len(stack) > 1:
            top = stack[-1]
            if top.is_empty():
                return top
