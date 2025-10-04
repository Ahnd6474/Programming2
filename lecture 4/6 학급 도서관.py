class Queue:
    def __init__(self):
        self.__elements = []

    def __str__(self):
        return ' '.join(map(str, self.__elements))

    def empty(self):
        return len(self.__elements) == 0

    def size(self):
        return len(self.__elements)

    '''enqueue 메소드: 맨 뒤에 데이터를 추가한다.'''
    def enqueue(self, data):
        self.__elements.append(data)

    '''dequeue 메소드: 맨 앞의 데이터를 삭제하고, 삭제한 
    데이터를 리턴한다. 단, 큐가 빈 경우 None을 리턴한다.'''
    def dequeue(self):
        if self.empty():
            return None
        return self.__elements.pop(0)


class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.state = '대출 가능'
        self.borrower = None
        self.waiting = Queue()

    def __str__(self):
        info = f'\n제목: {self.title}\n저자: {self.author}\n상태: {self.state}'
        if self.borrower:
            info += f'\n대출자: {self.borrower}'
        if not self.waiting.empty():
            info += f'\n예약자: {self.waiting}'
        return info

    ''' borrow 메소드
     - '대출 가능'이면 대출 처리
     - '대출 중'이면 예약 처리 및 예약 순위 출력(기존 예약자 수 + 1)
    '''
    def borrow(self, borrower):
        if self.borrower is None:  # 대출 가능
            self.borrower = borrower
            self.state = '대출 중'  # 공백 포함
            print(f'{borrower}님에게 대출되었습니다.')
            return
        # 대출 중 → 예약
        self.waiting.enqueue(borrower)
        print(f'{borrower}님 예약 순위: {self.waiting.size()}')

    ''' back 메소드
     - '대출 중'이면 반납 처리
     - 예약자가 있으면 1순위에게 즉시 대출하고 상태 유지('대출 중')
     - 예약자가 없으면 상태를 '대출 가능'으로 전환
     - 대출 중이 아니면 경고 출력
    '''
    def back(self):
        if self.borrower is None:
            print('대출된 도서가 아닙니다.')
            return
        print(f'{self.borrower}님, 반납되었습니다.')
        if self.waiting.empty():
            self.borrower = None
            self.state = '대출 가능'
        else:
            self.borrower = self.waiting.dequeue()
            self.state = '대출 중'
            print(f'{self.borrower}님에게 대출되었습니다.')


books = {}

while cmd := input('? '):
    valid = True
    cmd = cmd.split('/')

    if cmd[0] == '등록':
        if cmd[1] in books:
            valid = False
            print('이미 등록된 책입니다.')
        else:
            books[cmd[1]] = Book(cmd[1], cmd[2])

    elif cmd[0] in ['대출', '반납']:
        if cmd[1] not in books:
            valid = False
            print('등록되지 않은 책입니다.')
        elif cmd[0] == '대출':
            books[cmd[1]].borrow(cmd[2])
        elif cmd[0] == '반납':
            books[cmd[1]].back()

    if valid:
        for title in sorted(books):
            print(books[title])
    print()
