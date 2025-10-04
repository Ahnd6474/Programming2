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
	def enqueue(self,data):
		self.__elements.append(data)


	'''dequeue 메소드: 맨 앞의 데이터를 삭제하고, 삭제한 
	데이터를 리턴한다. 단, 큐가 빈 경우 None을 리턴한다.'''
	def dequeue(self):
		return self.__elements.pop(0)


q = Queue()
while line := input("Command? "):
	if line.startswith('in'):
		cmd, data = line.split()
		q.enqueue(data)
	elif line.startswith('out'):
		data = q.dequeue()
		print(f'Out: {data}')
	print(f"Queue's state: {q}\n")
