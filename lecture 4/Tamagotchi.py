# Tamagotchi ASCII art.
SMALL = r'''

 _____
/ ^_^ \
\_____/
'''[1:-1]
MED = r'''
   _______
  /       \
 /  ^ _ ^  \
 \_________/
    U   U
'''[1:-1]
BIG = r'''
   ___________
  /           \
 /  /\     /\  \
 \      _      /
  \___________/
    \_/   \_/
'''[1:-1]


class Tamagotchi:
    """
    하나의 다마고치를 표현합니다.
    """

    def __init__(self, name):
        """
        이름이 주어지면 기본값으로 초기화된 다마고치를 생성합니다.
        """
        self._name = name
        self._is_dead = False
        self._age = 0
        self._hunger = 5
        self._boredom = 0

    def is_dead(self):
        """
        다마고치가 죽었으면 True, 그렇지 않으면 False를 리턴합니다.
        """
        return self._is_dead

    def feed(self):
        """
        배고픔 수치를 낮춥니다.
        """
        if self.is_dead():
            return

        self._hunger -= 3

        # 너무 많이 먹지 않았는지 확인합니다.
        if self._hunger < 0:
            self._hunger = 0
            self._is_dead = True

    def play(self):
        """
        지루함 수치를 낮춥니다.
        """
        if self.is_dead():
            return

        self._boredom -= 5
        if self._boredom < 0:
            self._boredom = 0

    def increment_time(self):
        """
        시간 흐름에 따른 다마고치의 상태를 변경합니다.
        """
        if self.is_dead():
            return

        self._hunger += 1
        self._age += 1
        self._boredom += 1
        if self._age > 15:
            self._is_dead = True
        if self._hunger > 10:
            self._is_dead = True
        if self._boredom > 10:
            self._is_dead = True

    def __str__(self):
        """
        다마고치의 현재 상태를 표현하는 문자열을 리턴합니다.
        """
        if self.is_dead():
            return f'''
Name:    {self._name}
DEAD
'''

        if self._age < 3:
            picture = SMALL
        elif self._age < 6:
            picture = MED
        else:
            picture = BIG
        return f'''{picture}
Name:    {self._name}
Hunger:  {self._hunger * 'o'}
Boredom: {self._boredom * 'o'}
Age:     {self._age}
'''
def create(name):
    return Tamagotchi(name)
while True:
    c=input()
    if ' ' in c:
        