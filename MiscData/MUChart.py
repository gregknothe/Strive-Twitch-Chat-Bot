import pandas as pd 
import numpy as np

data = pd.read_csv("MUData4.csv", header=None)

charList = data[0][1:].to_list()
data = data.T.set_index(0,drop=True)
data.columns = charList
data = data.drop(data.index[:1])
#print(data)

data = data.replace("-2", "-1").replace("2", "1")
finalDF = pd.DataFrame()
noData = []
for x in charList: #dataset for each char
    charData = data[data.index == x].reset_index(drop=True).astype('float')
    if len(charData.index) == 0:
        noData.append(x)
    for y in range(len(charData.index)): #for each entry into the char dataset
        meanCharData = charData.mean()
    finalDF = pd.concat([finalDF, meanCharData], axis=1)
finalDF.columns = charList    
for x in noData:
    finalDF[x] = np.nan
#print(finalDF)

winList, loseList, evenList= [], [], []
for x in charList:
    winCount, loseCount, evenCount = 0, 0, 0
    for y in charList:
        if finalDF.loc[x,y] >= .001:
            winCount += 1
        elif finalDF.loc[x,y] <= -.001:
            loseCount += 1
        else:
            evenCount += 1
    winList.append(winCount)
    evenList.append(evenCount)
    loseList.append(loseCount)

muDiff = []
for x in range(len(winList)):
    muDiff.append(winList[x] - loseList[x])

finalDF["Win"] = winList
finalDF["Even"] = evenList
finalDF["Lose"] = loseList
#finalDF["W/L delta"] = muDiff
'''
winList2, loseList2, evenList2= [], [], []
for x in charList:
    winCount2, loseCount2, evenCount2 = 0, 0, 0
    for y in charList:
        if finalDF.loc[y,x] >= .001:
            winCount2 += 1
        elif finalDF.loc[y,x] <= -.001:
            loseCount2 += 1
        else:
            evenCount2 += 1
    winList2.append(winCount2)
    evenList2.append(evenCount2)
    loseList2.append(loseCount2)

finalDF.loc[len(finalDF)] = winList2
finalDF.loc[len(finalDF)] = evenList2
finalDF.loc[len(finalDF)] = loseList2
print(finalDF)
'''

print(finalDF.round(2))
print("Total Winning MU: " + str(sum(winList)))
print("Total Even MU: " + str(sum(evenList)))
print("Total Loss MU: " + str(sum(loseList)))
#How to read:
#Columns are the is the average player's opinion on all the matchups
#Rows are the other player's opinion on the matchups

'''
char = "May"
charDF = finalDF[char].to_frame()
charDF.columns = [char + " Players"]
opponent = finalDF[finalDF.index==char].T
charDF["Other Players"] = opponent
diff, diffText = [], []
for x in charList:
    if charDF.loc[x,char + " Players"] != np.nan and charDF.loc[x,"Other Players"] != np.nan:
        diff.append(abs(charDF.loc[x,char + " Players"] - (-charDF.loc[x,"Other Players"])))
    else: 
        diff.append(np.nan)
charDF["Diff"] = diff
for x in [char+" Players", "Other Players", "Diff"]:
    charDF[x] = round(charDF[x],2)
for x in charList:
    if charDF.loc[x ,"Diff"] >= 1:
        if charDF.loc[x, char+" Players"] >= .01:
            diffText.append("")

#print(charDF)
'''

