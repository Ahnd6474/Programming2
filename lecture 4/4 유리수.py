# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean
import random
import math


def gcd(a, b):
    """a와 b의 최대공약수(Greatest Common Divisor)를 리턴합니다."""
    while b:
        a, b = b, a % b
    return a


class Rational:
    """분수 형식의 유리수를 나타냅니다."""

    def __init__(self, numerator, denominator=1):
        """주어진 분자와 분모로 유리수를 초기화합니다."""
        self.numerator = int(numerator)
        self.denominator = int(denominator)
        self.simplify()

    def simplify(self):
        """기약분수로 나타냅니다.(return value 없음)"""
        if self.numerator == 0:
            self.denominator = 1
            return
        g = math.gcd(self.numerator, self.denominator)
        self.numerator //= g
        self.denominator //= g

    def __str__(self):
        """이 유리수를 나타내는 문자열을 리턴합니다."""
        num = self.numerator
        neg = ''
        if num < 0:
            neg = '-'
            num = num * -1

        whole = num // self.denominator
        remainder = num % self.denominator
        if remainder == 0:
            return neg + str(whole)
        if whole:
            return f'{neg}{whole}·{remainder}/{self.denominator}'.strip()
        else:
            return f'{neg}{remainder}/{self.denominator}'.strip()

    def __add__(self, other):
        """두 유리수의 덧셈 결과를 리턴합니다.(Rational object)"""
        denom = self.denominator * other.denominator
        num = self.numerator * other.denominator + other.numerator * self.denominator
        return Rational(num, denom)

    def __sub__(self, other):
        """두 유리수의 뺄셈 결과를 리턴합니다.(Rational object)"""
        return Rational(self.numerator*other.denominator - other.numerator*self.denominator, self.denominator*other.denominator)

    def __mul__(self, other):
        """두 유리수의 곱셈 결과를 리턴합니다.(Rational object)"""
        return Rational(self.numerator * other.numerator, self.denominator * other.denominator)


    def __truediv__(self, other):
        """두 유리수의 나눗셈 결과를 리턴합니다.(Rational object)"""
        return Rational(self.numerator * other.denominator, self.denominator * other.numerator)


    def __eq__(self, other):
        """두 유리수가 일치하는지 여부를 리턴합니다.(True/False)"""
        if self.numerator*other.denominator == self.denominator*other.numerator:
            return True
        else: return False


def random_rational():
    num = random.randint(0, 10)
    den = random.randint(1, 10)
    return Rational(num, den)


ADD = '+'
MINUS = '-'
TIMES = '×'
DIVIDE = '÷'

random.seed(10)  # 채점을 위해 랜덤 시드를 정함
user_answer = '0'
while user_answer:
    num1 = random_rational()
    num2 = random_rational()
    operator = random.choice((ADD, MINUS, TIMES, DIVIDE))

    if operator == ADD:
        answer = num1 + num2
    elif operator == MINUS:
        answer = num1 - num2
    elif operator == TIMES:
        answer = num1 * num2
    else:
        while num2 == Rational(0, 1):
            num2 = random_rational()
        answer = num1 / num2

    print()
    print(f'What is {num1} {operator} {num2}?')

    answers = [answer, random_rational(), random_rational(), random_rational()]
    random.shuffle(answers)
    for i, choice in enumerate(answers):
        print('{}) {}'.format(i + 1, choice))
    user_answer = input('> ')
    if user_answer and user_answer.isdigit() and int(user_answer) < 5:
        i = int(user_answer)
        user_answer_rational = answers[i - 1]
        if user_answer_rational == answer:
            print('Correct!')
        else:
            print(f'Incorrect. The correct answer was: {answer}')
    else:
        print(f'Invalid input. The correct answer was: {answer}')