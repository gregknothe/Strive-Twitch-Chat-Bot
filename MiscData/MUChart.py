import pandas as pd 
import numpy as np

data = pd.read_csv("MUData2.csv", header=None)

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
    

#How to read:
#Columns are the is the average player's opinion on all the matchups
#Rows are the other player's opinion on the matchups

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

print(charDF)


