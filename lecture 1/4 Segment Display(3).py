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


def render_canvases_for_digits(digits: str, scaling: int) -> list[list[list[str]]]:
    """

    """
    digits=list(map(int, digits))
    return [render_digit_on_canvas(number,scaling) for number in digits]
# TODO: 문자열 타입의 숫자를 렌더링한 캔버스들의 리스트를 반환


def display_canvases(canvases: list[list[list[str]]], padding: int) -> None:
    """

    """
    canvas=[[] for _ in range(len(canvases[0]))]
    k = 0
    for canva in canvases:
        for i in range(len(canvas)):
            canvas[i] += [' ']*padding + canva[i] if k else canva[i]
        k=1
    for row in canvas:
        print(''.join(row))

# TODO: 같은 행끼리 병합해서 출력


def test_print_canvases(canvases: list[list[list[str]]]) -> None:
    """
    1자리 숫자에 대한 7-세그먼트 표현인 canvas(2차원 리스트)를
    1개 이상 포함하는 canvas의 리스트를 콘솔에 출력합니다. (세로 출력)
    """
    for canvas in canvases:
        for row in canvas:
            print(*row, sep='')
        print()


if __name__ == "__main__":
    try:
        digits = input("digits? ").strip()
        scaling = int(input("scaling? ").strip())
        padding = int(input("padding? ").strip())
    except Exception:
        print("입력 형식을 확인하세요. scaling, padding은 정수여야 합니다.")
        raise SystemExit(1)

    if not digits.isdigit():
        print("digits는 숫자만 입력하세요.")
        raise SystemExit(1)
    if scaling < 1:
        print("scaling은 1 이상의 정수여야 합니다.")
        raise SystemExit(1)
    if padding < 0:
        print("padding은 0 이상의 정수여야 합니다.")
        raise SystemExit(1)

    # --- 렌더링 & 출력 ---
    canvases = render_canvases_for_digits(digits, scaling)
    # test_print_canvases(canvases)
    display_canvases(canvases, padding)