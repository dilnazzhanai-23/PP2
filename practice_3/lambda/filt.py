n=int(input())
l=map(int,input().split())
x=filter(lambda y: y%2==0, l)
print(list(x))