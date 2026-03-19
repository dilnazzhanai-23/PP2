n=int(input())
m=list(map(int, input().split()))
l=list(map(str, input().split()))
z=zip(l,m)
for a,(name,age) in enumerate(z,start=1) :
    print(a,":",name,"age:", age)