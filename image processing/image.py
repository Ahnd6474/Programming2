from PIL import Image
# -------------------------------
# Helper: mod for wrap
# -------------------------------
def _mod(a, m):
    # 파이썬 %는 음수에도 양수 나머지를 반환하므로 그대로 사용 가능
    return a % m


def remove_image_section(image: Image.Image, cut_start: int, cut_end: int, direction: str) -> Image.Image:
    """
    이미지에서 지정된 범위의 행 또는 열을 제거하고, 남은 픽셀을 이동시켜 빈 공간을 메운 새 이미지를 반환합니다.
    """


def flip_image(image: Image.Image, direction: str) -> Image.Image:
    """
    이미지를 좌우 또는 상하로 반전시켜 새로운 이미지를 반환합니다.
    """


def rotate_image(image: Image.Image, angle: int) -> Image.Image:
    """
    이미지를 주어진 각도(90도의 배수)만큼 회전시켜 새로운 이미지를 반환합니다.
    """


def translate_image(image: Image.Image, shift_x: int, shift_y: int) -> Image.Image:
    """
    이미지를 지정된 만큼 평행이동하되, 경계를 넘어간 픽셀은 반대편에서 나타나도록 래핑 처리합니다.
    """


def mosaic_simple(image: Image.Image, block_size: int) -> Image.Image:
    """
    이미지를 주어진 블록 크기로 나누어 각 블록의 좌상단 픽셀 색으로 채워 모자이크 효과를 적용합니다.
    """


def mosaic_average(image: Image.Image, block_size: int) -> Image.Image:
    """
    이미지를 주어진 블록 크기로 나누어 블록 내부 픽셀의 평균 색으로 채워 모자이크 효과를 적용합니다.
    """

    """
    테스트 코드입니다. 
    각 함수의 동작을 확인하기 위해 필요한 코드만 주석을 해제하세요.
    """

    image_path = "images/kpoptiger.png"
    # image_path = "images/pencils.png"
    image = Image.open(image_path)
    image.show()

# result_img = remove_image_section(image, 450, 650, "vertical")
# result_img = remove_image_section(image, 400, 550, "horizontal")
# result_img = flip_image(image, "horizontal")
# result_img = flip_image(image, "vertical")
# result_img = rotate_image(image, 180)
# result_img = translate_image(image, 300, 100)
# result_img = mosaic_simple(image, 50)
# result_img = mosaic_average(image, 50)

# result_img.save("images/output.png")
# result_img.show()