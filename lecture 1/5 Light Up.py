def count_adjacent_lamps(board, start_x, start_y):
    """(x, y)의 상하좌우 인접 칸 중 램프('L') 개수 반환"""
    lamps = 0
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        x, y = start_x + dx, start_y + dy
        if is_on_board(board, x, y) and is_lamp(board[y][x]):
            lamps += 1
    return lamps


def is_black(cell):
    """검은 칸(X) 또는 숫자 칸 여부"""
    return cell == 'X' or is_numbered(cell)


def is_lamp(cell):
    return cell == 'L'


def is_numbered(cell):
    return cell.isdigit()


def is_white(cell):
    return cell == '.'


def is_on_board(board, x, y):
    size = len(board)
    return 0 <= x < size and 0 <= y < size


def is_illuminated(board, start_x, start_y):
    """같은 행/열에서 검은 칸에 막히기 전 램프가 있으면 비춰짐"""
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        x, y = start_x, start_y
        while True:
            x, y = x + dx, y + dy
            if not is_on_board(board, x, y):
                break
            cell = board[y][x]
            if is_black(cell):
                break
            if is_lamp(cell):
                return True
    return False


def board_is_happy(board):
    """
    숫자 칸 인접 램프 수가 숫자를 초과하지 않고,
    서로를 비추는 램프 쌍이 없으면 happy
    """
    size = len(board)
    for y in range(size):
        for x in range(size):
            cell = board[y][x]
            if is_numbered(cell) and count_adjacent_lamps(board, x, y) > int(cell):
                return False
            if is_lamp(cell) and is_illuminated(board, x, y):
                return False
    return True


def board_is_solved(board):
    """
    모든 숫자 칸의 인접 램프 수가 정확히 일치하고,
    모든 흰 칸이 비춰지면 solved
    """
    size = len(board)
    for y in range(size):
        for x in range(size):
            cell = board[y][x]
            if is_numbered(cell) and count_adjacent_lamps(board, x, y) != int(cell):
                return False
            if is_white(cell) and not is_illuminated(board, x, y):
                return False
    return True


def get_board_state(board):
    if board_is_happy(board):
        return 'solved' if board_is_solved(board) else 'happy'
    return 'unhappy'


# --- 입력 및 실행 ---
board = []
line = input()
while line:
    board.append(line)
    line = input()

print(get_board_state(board))
