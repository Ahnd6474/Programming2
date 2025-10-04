import csv
with open('data/employees.csv') as f:
	reader = csv.reader(f)

	# 헤더(제목줄)을 건너뛴다.(한 줄을 읽으며, 다음 읽기 함수에서는 이 줄 뒤부터 읽게된다.)

	# CSV 파일의 각 줄을 읽어와서 출력한다.
	l=list(reader)
employ=[]
for row in l:
	r=[]
	for word in row:
		word=word.strip()
		r.append(word)
	employ.append(r)
i=0
for emp in employ:
	if not i:
		i+=1
		continue
	emp[0]=int(emp[0])
	emp[3]=int(emp[3])
	emp[4]=int(emp[4])
print(f'Column names: {", ".join(employ[0])}')
d={'employeeID':0,'employeeName':1,'department':2,'salary':3,'yearsOfService':4}
emp=employ[1:]
while True:
	name=input('Column name to sort by? ')
	name=name.strip()
	if name not in employ[0]:
		print('Invalid column name.')
		continue
	emp.sort(key=lambda x:x[d[name]])
	for e in emp:
		e=list(map(str,e))
		print('/'.join(e))
	break

