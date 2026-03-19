import os
os.mkdir("Example")
#os.makedirs("111/222/333")
print(os.listdir())
print(os.getcwd())
files=os.listdir()
for file in files:
    if file.endswith('.txt') :
        print(file)