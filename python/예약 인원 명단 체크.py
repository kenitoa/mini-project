import random

repeat=random.randint(1,10)%5
name=[]
for i in range(repeat):
    write=input("anyone write to virtual name (under the 5 alphabet): ")
    name.append(write)
    name.sort()

if len(name) < repeat:
    print(bool(0))
else:
    print(bool(1))