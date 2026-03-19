from functools import reduce
l=list(map(int, input().split()))
res=reduce(lambda a,b : a+b, filter( lambda x: x%2==0, l))
print(res)