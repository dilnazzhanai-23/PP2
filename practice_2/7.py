n=int(input())
x=list(map(int, input().split()))
m=x[0]
pos=0
for i in range(n) :
     if x[i]>m:
         m=x[i]
         pos=i
print(pos)
