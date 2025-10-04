def read_numbers_from_file(filename):
    '''
    filename으로부터 데이터를 읽어 정수로 변환한 후 리스트에 저장해서 반환합니다.
    '''
    numbers = []
    try:
        f = open(filename)
    except FileNotFoundError:
        print(f'File Not Found: {filename}')
        return []

    for item in f:
        try:
            numbers.append(int(item.strip()))
        except ValueError:
            print(f'Invalid value: {item}')

    f.close()
    return numbers


def calculate_average(numbers):
    '''
    숫자 리스트에서 평균을 구해서 반환합니다.
    '''
    average = None
    try:
        average = sum(numbers) / len(numbers)
        return average
    except ZeroDivisionError:
        print(' Zero Division Error')
        exit()


filename = input()
numbers = read_numbers_from_file(f'data/{filename}')
average = calculate_average(numbers)
if average:
    print(f"{average:.1f}")