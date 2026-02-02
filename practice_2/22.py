i=int(input())
while i < 100:
  i += 1
  if not i%5==0:
    continue
  print(i)