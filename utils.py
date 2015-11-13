def get_user_input_as_int(min: int, max: int) -> int:
    user_input = _get_user_input_as_int()
    if user_input != None:
        if user_input >= min and user_input <= max:
            return user_input


def get_user_input(required: 'tuple of chars') -> str:
    user_input = input().strip()
    if user_input in required:
        return user_input


def get_player_move() -> '(row, col)':
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
