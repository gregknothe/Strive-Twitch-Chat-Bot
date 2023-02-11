import random

def switch():
    x = ["no","no","yes"]
    y = x.pop(random.randint(0,len(x)-1))
    x.remove("no")
    return x[0]

count = 0
for x in range(1000):
    x = switch()
    if x == "yes":
        count = count + 1

print(count)