import shutil
import os 
shutil.copy('sample.txt','copy.txt')
shutil.copy('sample.txt','copy_2.txt')
delete="copy.txt"

os.remove(delete) 
print("file deleted")
