import random

iceCream = ["+3%","+6%","+9%","+12%","+15%"]
lizard = ["+1.19%","+2.38%","+3.57%","+4.76%","+5.95%"]
meat = ["+2%","+4%","+6%","+8%","+10%"]
lobster = ["-2%","-4%","-6%","-8%","-10%"]
fish = ["+3.5%","+7%","+10.5%","+14%","+17.5%"]
durr = [2,3,4,5,6]
food = [iceCream, lizard, meat, lobster, fish]
foodName = ["ice cream", "lizard", "meat", "lobster", "fish"]
foodBuff = ["tension", "health", "damage done", "damage taken", "dash speed"]

def SinFoodRoll():
    foodRoll = random.randint(0,4)
    levelRoll = random.choices([0,1,2,3,4],weights=[5,4,3,2,1],k=1)[0]
    durrRoll = random.choices([0,1,2,3,4],weights=[5,4,3,2,1],k=1)[0]
    if foodRoll <= 1:
        return "Sin ate Lv"+ str(levelRoll+1) + " " + foodName[foodRoll] + ". He gained " + food[foodRoll][levelRoll] + " " + foodBuff[foodRoll] + "!"
    else:
        return "Sin ate Lv"+ str(levelRoll+1) + " " + foodName[foodRoll] + ". He gained " + food[foodRoll][levelRoll] + " " + foodBuff[foodRoll] + " for " + str(durr[durrRoll])+" sec!"

def SinFoodRolls(count):
    foodRolls = []
    levelRolls = []
    durrRolls = []
    for x in range(count):
        foodRolls.append(random.randint(0,4))
        levelRolls.append(random.choices([0,1,2,3,4],weights=[5,4,3,2,1],k=1)[0])
        durrRolls.append(random.choices([0,1,2,3,4],weights=[5,4,3,2,1],k=1)[0])
    return foodRolls, levelRolls, durrRolls

def isItWorth(foodRolls,levelRolls,durrRolls):
    worth = []
    for x in range(len(foodRolls)):
        if foodRolls[x] == 0:
        #Tension ["+3%","+6%","+9%","+12%","+15%"]
            if levelRolls[x] > 2:
                worth.append("yes")
            elif levelRolls[x] == 2:
                worth.append("maybe")
            else:
                worth.append("no")
        if foodRolls[x] == 1:
        #Health ["+1.19%","+2.38%","+3.57%","+4.76%","+5.95%"]
            if levelRolls[x] == 4:
                worth.append("yes")
            elif levelRolls[x] == 3 or levelRolls[x] == 2:
                worth.append("maybe")
            else:
                worth.append("no")
        if foodRolls[x] == 2:
        #Damage done ["+2%","+4%","+6%","+8%","+10%"]
            if levelRolls[x] <= 1:
                worth.append("no")
            else:
                if durrRolls[x] == 1:
                    worth.append("maybe")
                else:
                    worth.append("yes")
        if foodRolls[x] ==3:
        #Damage reduction ["-2%","-4%","-6%","-8%","-10%"]
            if levelRolls[x] >= 3:
                if durrRolls[x] >= 2:
                    worth.append("maybe")
                else:
                    worth.append("no")
            else:
                worth.append("no")
        if foodRolls[x] == 4:
            worth.append("no")
    yes = str(round(worth.count("yes")/len(foodRolls)*100,2))+"%"
    maybe = str(round(worth.count("maybe")/len(foodRolls)*100,2))+"%"
    no = str(round(worth.count("no")/len(foodRolls)*100,2))+"%"
    return "Y: " + yes + " - M: " + maybe + " - N: " + no


#rolls = SinFoodRolls(100000)
#worth = isItWorth(rolls[0],rolls[1],rolls[2])
#print(worth)