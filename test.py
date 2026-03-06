def d(m,n) :
    for _ in range(n) :
        for i in m :
            yield i
m=input().split()
n=int(input())
for i in d(m,n) :
    print(i,end=" ")