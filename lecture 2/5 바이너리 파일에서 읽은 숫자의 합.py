import pickle
file=input()
path='data/'+file
l=[]
with open(path, 'rb') as f:
	while True:
		try:
			data = pickle.load(f)
		except:
			break
		l.append(float(data))
print(sum(l))