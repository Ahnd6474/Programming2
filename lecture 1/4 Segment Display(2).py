# 세그먼트 상수
H1, L1, R1, H2, L2, R2, H3 = range(7)

# 숫자별 세그먼트 점등 정보
turned = [
    [True, True, True, False, True, True, True],  # 0
    [False, False, True, False, False, True, False],  # 1
    [True, False, True, True, True, False, True],  # 2
    [True, False, True, True, False, True, True],  # 3
    [False, True, True, True, False, True, False],  # 4
    [True, True, False, True, False, True, True],  # 5
    [True, True, False, True, True, True, True],  # 6
    [True, False, True, False, False, True, False],  # 7
    [True, True, True, True, True, True, True],  # 8
    [True, True, True, True, False, True, True],  # 9
]


def create_digit_canvas(scaling: int) -> list[list[str]]:
    """
    한 자릿수를 그릴 빈 캔버스(2차원 문자 격자)를 생성해서 리턴합니다.

    격자 크기:
      - 행: 2*scaling + 3
      - 열: scaling + 2
      - 모든 칸은 공백 문자(' ')로 초기화합니다.

    #>>> create_digit_canvas(1)
    [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    #>>> c2 = create_digit_canvas(2)
    #>>> len(c2), len(c2[0])
    (7, 4)
    """
    # TODO: 2차원 리스트 생성 및 반환
    l = [[' ' for i in range(scaling + 2)] for _ in range(2 * scaling + 3)]
    return l

def render_digit_on_canvas(digit: int, scaling: int) -> list[list[str]]:
    canva = create_digit_canvas(scaling)
    s = scaling

    if not (0 <= digit <= 9):
        raise ValueError("digit must be 0..9")
    if s < 1:
        raise ValueError("scaling must be >= 1")

    # 세그먼트별로 켜져 있으면 좌표 공식으로 그린다.
    for i, on in enumerate(turned[digit]):
        if not on:
            continue

        # 가로 세그먼트: i ∈ {0,3,6}
        if i in (H1, H2, H3):
            row = (i // 3) * (s + 1)       # 0, s+1, 2s+2
            for c in range(1, s + 1):      # 열 1..s
                canva[row][c] = '-'

        # 세로 세그먼트: i ∈ {1,2,4,5}
        else:
            col = 0 if i in (L1, L2) else s + 1
            if i in (L1, R1):              # 위쪽 구간
                r0, r1 = 1, s
            else:                          # 아래쪽 구간
                r0, r1 = s + 2, 2 * s + 1
            for r in range(r0, r1 + 1):
                canva[r][col] = '|'

    return canva
def test_print(canvas):
    for row in canvas:
        print(*row, sep='')


if __name__ == "__main__":
    digit = int(input())
    scaling = int(input())
    canvas = render_digit_on_canvas(digit, scaling)
    test_print(canvas)
