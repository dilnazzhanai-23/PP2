with open("input.txt",'a') as f:
    s=input()
    f.write('\n'+ s) 
    
with open('input.txt', "r") as f:
    out=f.read()
    print(out)