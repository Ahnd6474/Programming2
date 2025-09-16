class Rect:
	def __init__(self,x, y, w, h):
		self._x=x
		self._y=y
		self._w=w
		self._h=h
	def __eq__(self,other):
		if self._x==other._x and self._y==other._y and self._w==other._w and self._h==other._h:
			return True
		else:
			return False
	def collide(self,other):
		if self._x-other._x <= other._w and self._y-other._y<=other._h and other._x-self._x<=other._w and other._y-self._y<=other._h:
			return True
		else:
			return False
	def __str__(self):
		return f'Position({self._x},{self._y}),Size({self._w},{self._h})'
	def move_ip(self,x,y):
		self._x+=x
		self._y+=y
	def move(self,x,y):
		return Rect(self._x+x,self._y+y,self._w,self._h)
	def contain(self,other):
		if self._x<=other._x and self._y<=other._y and self._w>=other._w and self._h>=other._h:
			return True
		return False
	@property
	def x(self):
		return self._x
	@property
	def y(self):
		return self._y
	@property
	def w(self):
		return self._w
	@property
	def h(self):
		return self._h

x1, y1, w1, h1 = map(int, input('r1? ').split()) #생성할 첫 번째 사각형 r1의 x, y, width, height 입력
x2, y2, w2, h2 = map(int, input('r2? ').split()) #생성할 두 번째 사각형 r2의 x, y, width, height 입력
r1 = Rect(x1, y1, w1, h1)
r2 = Rect(x2, y2, w2, h2)
print(f'r1: {r1}')
print(f'r2: {r2}')
print(f'r1과 r2는 같은 사각형인가? {r1 == r2}')
print(f'r1과 r2가 충돌하는가? {r1.collide(r2)}')
r3 = r2.move_ip(-10, 10)
print(f'r3 = r2.move_ip(-10, 10) 후')
print(f'\t-> r2: {r2}')
print(f'\t-> r3: {r3}')
print(f'r1과 r2가 충돌하는가? {r1.collide(r2)}')
mx, my = map(int, input('r1 이동? ').split())
r4 = r1.move(mx, my)
print(f'r4 = r1.move({mx}, {my}) 후')
print(f'\t-> r1: {r1}')
print(f'\t-> r4: {r4}')
print(f'r1과 r2가 충돌하는가? {r1.collide(r2)}')
print(f'r4와 r2가 충돌하는가? {r4.collide(r2)}')
print(f'r2가 r4를 포함하는가? {r2.contain(r4)}')
print(f'r4가 r2를 포함하는가? {r4.contain(r2)}')
