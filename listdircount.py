import os

path = os.getcwd()
types = os.listdir()
count = 0

for typ in types:
    if os.path.isdir(path+'/'+typ):
        print(typ, len(os.listdir(path+'/'+typ)))
        count += len(os.listdir(path+'/'+typ))
print('count :' + str(count))
