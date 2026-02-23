x=int(input())
l=list(map(int, input().split()))
lam=list(map( lambda y: y%2==0, l))
print(lam)