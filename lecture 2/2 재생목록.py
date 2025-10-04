d={}
with open('data/song.txt', encoding='utf-8') as f:
    t = f.readlines()
    for line in t:
        l=list(line.split('/'))
        d[l[0]]=l[1]
l=list(d.keys())
t=input()
l.sort()

if t!='a':
    l.reverse()
for i in l:
    print(f'{i} | {d[i]}')