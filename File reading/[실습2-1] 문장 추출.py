path=input()
n=int(input())
path='data/'+path
file=open(path)
contents = file.read()
l=list(contents.split())
file.close()
print(' '.join(l[:200:n]))