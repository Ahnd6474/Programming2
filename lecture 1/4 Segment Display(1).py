def create_digit_canvas(scaling: int) -> list[list[str]]:
	"""
    한 자릿수를 그릴 빈 캔버스(2차원 문자 격자)를 생성해서 리턴합니다.

    격자 크기:
      - 행: 2*scaling + 3
      - 열: scaling + 2
      - 모든 칸은 공백 문자(' ')로 초기화합니다.

    >>> create_digit_canvas(1)
    [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    >>> c2 = create_digit_canvas(2)
    >>> len(c2), len(c2[0])
    (7, 4)
	"""
	# TODO: 2차원 리스트 생성 및 반환
	l=[[' ' for i in range(scaling+2)] for _ in range(2*scaling+3)]
	return l
if __name__ == "__main__":
	scaling = int(input())
	canvas = create_digit_canvas(scaling)
	print(canvas)