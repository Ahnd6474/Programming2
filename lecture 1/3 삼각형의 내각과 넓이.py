from math import *

def is_triangle(a, b, c):
    l = [a, b, c]

    if max(l) >= sum(l)-max(l):
        return False
    if min(a,b,c)<=0:
        return False
    return True

def cos2(a,b,c):
    return -(a**2-b**2-c**2)/(2*b*c)
def find_angle(a, b, c):
    if is_triangle(a, b, c):
        s=triangle_area(a, b, c)
        angle=list(map(lambda x: degrees(acos(x)),[cos2(a,b,c),cos2(b,c,a),cos2(c,a,b)]))
        return angle
    return [0,0,0]

def triangle_area(a, b, c):
    l = [a, b, c]
    k = sum(l) / 2
    s=k
    for i in l: s*=(k-i)
    return sqrt(s)


L = input('세 변 a, b, c의 길이를 입력하세요. ')
while L:
    L = list(map(float, L.split()))
    if len(L)!=3:
        print("삼각형이 아닙니다.")
    else:
        if is_triangle(L[0], L[1], L[2]):
            angels=find_angle(L[0], L[1], L[2])
            print(f'각BAC: {angels[0]:.2f}, 각ABC: {angels[1]:.2f}, 각BCA: {angels[2]:.2f}')
            print(f'넓이: {triangle_area(L[0], L[1], L[2]):.2f}')
        else:
            print("삼각형이 아닙니다.")
    L = input('세 변 a, b, c의 길이를 입력하세요. ')