books = {}
friends = []

while True:
	try:
		line = input()
		book, student = map(str, line.split(':', 1))
	except:
		break
	books.setdefault(book, set()).add(student)
	friends.append(student)

friends = list(set(friends))
friends.sort()

rec = {
    book: [f for f in friends if f not in readers] for book, readers in books.items()
}

books=list(rec.keys())
books.sort()
for book in books:
	print(f'{book}:',end=' ')
	if len(rec[book])==0:
		print('Everyone did!')
	else:
		print(', '.join(rec[book]))
