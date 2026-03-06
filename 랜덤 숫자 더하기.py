import random

number=random.randint(1,100) %16
b=0

for i in range(number):
    a=(int(input("write to number: ")))
    b+=a

print(b)