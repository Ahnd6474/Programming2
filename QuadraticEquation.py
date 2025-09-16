import math

class QuadraticEquation:
	def __init__(self,a,b,c):
		self._a=a
		self._b=b
		self._c=c
	def getDiscriminant(self):
		return self._b**2-4*self._a*self._c if self._a!=0 else -1111
	def getRoot1(self):
		z=self.getDiscriminant()
		if z>=0:
			return (-self._b+math.sqrt(z))/(2*self._a)
		else:
			return 0
	def getRoot2(self):
		z=self.getDiscriminant()
		if z>=0:
			return (-self._b-math.sqrt(z))/(2*self._a)
		else:
			return 0	
	@property
	def getA(self):
		return self._a
	@property
	def getB(self):
		return self._b
	@property
	def getC(self):
		return self._c

a, b, c = map(int, input().split())
equation = QuadraticEquation(a, b, c)
discriminant = equation.getDiscriminant()

if discriminant < 0:
		print("The equation has no roots")
elif discriminant == 0:
		print("The root is", equation.getRoot1())
else: # (discriminant >= 0)
		print("The roots are", equation.getRoot1(), "and", equation.getRoot2())
