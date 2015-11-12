DEFAULT_BOARD_SIZE = 8


class Piece:

    _BLACK_PIECE = 1
    _WHITE_PIECE = 2

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.piece = None

    def is_empty(self) -> bool:
        return self.piece == None

    def is_black(self) -> bool:
        return self.piece == Piece._BLACK_PIECE

    def is_white(self) -> bool:
        return self.piece == Piece._WHITE_PIECE

    def flip_to_black(self) -> None:
        self.piece = Piece._BLACK_PIECE

    def flip_to_white(self) -> None:
        self.piece = Piece._WHITE_PIECE


class OthelloBoard:

    def __init__(self, board_size = DEFAULT_BOARD_SIZE, white_piece_first = False) -> None:
        self.rows = board_size
        self.cols = board_size
        self.board = self._init_board(white_piece_first)

    def _init_board(self, white_piece_first) -> [[int]]:
        board = [[Piece(row, col) for col in range(self.cols)] for row in range(self.rows)]

        x = int(self.cols / 2 - 1)
        y = int(self.rows / 2 - 1)
        if white_piece_first:
            board[y][x].flip_to_black()
            board[y][x + 1].flip_to_white()
            board[y + 1][x].flip_to_white()
            board[y + 1][x + 1].flip_to_black()
        else:
            board[y][x].flip_to_white()
            board[y][x + 1].flip_to_black()
            board[y + 1][x].flip_to_black()
            board[y + 1][x + 1].flip_to_white()

        return board

    def print_board(self) -> None:
        for row in self.board:
            for piece in row:
                cell = None
                if piece.is_black():
                    cell = 'B'
                elif piece.is_white():
                    cell = 'W'
                else:
                    cell = '.'
                print(cell, end = ' ')
            print()

    def place_piece(self, piece_type, row, col):
        pass

    def possible_valid_moves(self, piece_type) -> int:
        for r in range(self.rows):
            for c in range(self.cols):
                piece = self.board[r][c]

