import random as rand
import datetime

'''
###Calc to see how often FT3 matters over FT2
P1perc = .50

setLength = 5
simCount = 100000
winCount = 0
Three_Os = 0
reverseSweep = 0
game5 = 0

for x in range(simCount):
    setValues = []
    for y in range(setLength):
        z = rand.random()
        if z <= P1perc:
            setValues.append(1)
        else: 
            setValues.append(0)
    if setValues[0:3] == [1,1,1] or setValues[0:3] == [0,0,0]:
        Three_Os += 1
    if setValues == [1,1,0,0,0] or setValues == [0,0,1,1,1]:
        reverseSweep += 1
    if sum(setValues[0:4]) == 2:
        game5 += 1
    if sum(setValues) >= 3:
        winCount += 1

#print("Win: " + str(round(winCount/simCount,2)))
#print("3:0: " + str(round(Three_Os/simCount,2)))
#print("Reserve Sweeps: " + str(round(reverseSweep/simCount,2)))
#print("Game 5: " + str(round(game5/simCount,2)))
'''

'''
###League of Legend's Knights Vow damage mitigation calculations
baseDmg = 3000
carryArmor = 100


#No KV involved
dmgTaken = baseDmg * (100/(100+carryArmor))
print("Damage Taken: "+ str(baseDmg) + ", Carry Armor: " + str(carryArmor))
print("No KV: Carry "+str(round(dmgTaken)))

#Old KV
dmgTaken2 = (baseDmg * (100/(100+carryArmor))) * .93
dmgTakenKV = (baseDmg * (100/(100+carryArmor))) * .07
print("Old KV: Carry "+str(round(dmgTaken2))+ ", KVUser "+str(round(dmgTakenKV))+" (Total: "+ str(round(dmgTaken2+dmgTakenKV))+")")

#New KV
dmgTaken3 = (baseDmg * .9) * (100/(100+carryArmor))
dmgTakenKV2 = (baseDmg * .1) 
print("New KV: Carry "+str(round(dmgTaken3))+ ", KVUser "+str(round(dmgTakenKV2))+" (Total: "+ str(round(dmgTaken3+dmgTakenKV2))+")")

print("KV Diff: Carry "+str(round(dmgTaken2-dmgTaken3))+", KVUser "+str(round(dmgTakenKV-dmgTakenKV2)) + " (Total: "+ str(round((dmgTaken2+dmgTakenKV)-(dmgTaken3+dmgTakenKV2)))+")")
'''

'''
###Monty Hall switch calculation
def MontyHall(rep=100, swap=0):
    wins = 0
    for x in range(rep):
        doors = [0,0,1]
        #Selects one of the three doors at random
        #then removes it from the list 
        doorNum = rand.randint(0,2)
        doorChoice = doors.pop(doorNum)
        #Removes one of the 0 values from the list
        if doors[0] == 0:
            doors.pop(0)
        else: 
            doors.pop(1)
        #Swaps if required
        if swap == 0:
            wins = wins + doorChoice
        else: 
            wins = wins + doors[0]
    return round(wins/rep,2) 

print(MontyHall(10000,1))
print(MontyHall(10000,0))
'''
present = datetime.datetime.now()
future = datetime.datetime(2023, 12, 14, 0, 0, 0)
difference = future - present
diff = str(difference)
days = diff.split(", ")[0]
time = diff.split(", ")[1].split(":")
print(days + ", " + time[0] + " hours, " + time[1] + " min, " + str(round(float(time[2]))) + " sec")
