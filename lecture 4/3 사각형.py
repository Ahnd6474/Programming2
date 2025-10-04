class Rect:
    def __init__(self, x, y, w, h):
        self._x = x
        self._y = y
        self._w = w
        self._h = h

    # Convenience edges
    @property
    def left(self): return self._x
    @property
    def top(self): return self._y
    @property
    def right(self): return self._x + self._w
    @property
    def bottom(self): return self._y + self._h

    # Public properties
    @property
    def x(self): return self._x
    @x.setter
    def x(self, value): self._x = value

    @property
    def y(self): return self._y
    @y.setter
    def y(self, value): self._y = value

    @property
    def w(self): return self._w
    @w.setter
    def w(self, value):
        if value < 0: raise ValueError("width must be non-negative")
        self._w = value

    @property
    def h(self): return self._h
    @h.setter
    def h(self, value):
        if value < 0: raise ValueError("height must be non-negative")
        self._h = value

    def __eq__(self, other):
        if not isinstance(other, Rect): return NotImplemented
        return (self._x, self._y, self._w, self._h) == (other._x, other._y, other._w, other._h)

    def __str__(self):
        return f'Position ({self._x}, {self._y}), Size ({self._w}, {self._h})'

    def move_ip(self, dx, dy):
        """In-place move; return self for chaining/assignment."""
        self._x += dx
        self._y += dy
        return None

    def move(self, dx, dy):
        """Return a new moved rect (original unchanged)."""
        return Rect(self._x + dx, self._y + dy, self._w, self._h)

    def collide(self, other):
        """Axis-aligned overlap test (edges touching counts as collision)."""
        return not (self.right < other.left or
                    self.left > other.right or
                    self.bottom < other.top or
                    self.top > other.bottom)

    def contain(self, other):
        """True if self fully contains other (edges touching allowed)."""
        return (self.left <= other.left and
                self.top <= other.top and
                self.right >= other.right and
                self.bottom >= other.bottom)


# ---- I/O demo unchanged except: move_ip returns self, so r3 is the moved r2 ----
x1, y1, w1, h1 = map(int, input('r1? ').split())
x2, y2, w2, h2 = map(int, input('r2? ').split())
r1 = Rect(x1, y1, w1, h1)
r2 = Rect(x2, y2, w2, h2)
print(f'r1: {r1}')
print(f'r2: {r2}')
print(f'r1과 r2는 같은 사각형인가? {r1 == r2}')
print(f'r1과 r2가 충돌하는가? {r1.collide(r2)}')

r3 = r2.move_ip(-10, 10)  # r2가 제자리 이동, r3는 r2와 동일 객체
print('r3 = r2.move_ip(-10, 10) 후')
print(f'\t-> r2: {r2}')
print(f'\t-> r3: {r3}')
print(f'r1과 r2가 충돌하는가? {r1.collide(r2)}')

mx, my = map(int, input('r1 이동? ').split())
r4 = r1.move(mx, my)  # r1은 그대로, r4는 이동한 새 사각형
print(f'r4 = r1.move({mx}, {my}) 후')
print(f'\t-> r1: {r1}')
print(f'\t-> r4: {r4}')
print(f'r1과 r2가 충돌하는가? {r1.collide(r2)}')
print(f'r4와 r2가 충돌하는가? {r4.collide(r2)}')
print(f'r2가 r4를 포함하는가? {r2.contain(r4)}')
print(f'r4가 r2를 포함하는가? {r4.contain(r2)}')
