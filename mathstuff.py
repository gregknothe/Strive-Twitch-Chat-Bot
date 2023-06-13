import random as rand

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

print("Win: " + str(round(winCount/simCount,2)))
print("3:0: " + str(round(Three_Os/simCount,2)))
print("Reserve Sweeps: " + str(round(reverseSweep/simCount,2)))
print("Game 5: " + str(round(game5/simCount,2)))