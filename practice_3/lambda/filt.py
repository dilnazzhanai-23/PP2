n=int(input())
l=map(int,input().splite())
x=filter(lambda y: y%2==0, l)
print(list(x))