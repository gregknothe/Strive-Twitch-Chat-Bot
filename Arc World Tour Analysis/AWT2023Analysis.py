import pandas as pd
import numpy as np

def dataTable():
    data = pd.read_csv("Arc World Tour Analysis/Arc World Tour 2023 Character Data.csv")
    charList = ["Anji", "Axl", "Baiken", "Bridget", "Chipp", "Faust", "Gio", "Gold", "Happy", "Ino", "Jacko", "Ky", "Leo", "May", "Millia", "Nago", "Pot", "Ram", "Sol", "Test", "Zato", "Sin", "Bedman", "Asuka", "Johnny"]
    top8CountList, top8UniqueCountList, top8UniquePlayerList, top16CountList, top16UniqueCountList, top16UniquePlayerList = [], [], [], [], [], []
    for char in charList:
        
        #Top 8 calculations
        table8 = data.loc[((data["Char1"]==char) | (data["Char2"]==char)) & (data["Placement"]<=8)].reset_index(drop=True)
        playerList, top8Count, top8UniqueCount, top8UniquePlayer = [], 0, 0, []
        if table8.empty:
            pass
        else:
            playerList = list(table8["Player"])
            top8Count = len(playerList)
            top8UniqueCount = len(pd.unique(playerList))
            for player in pd.unique(playerList):
                top8UniquePlayer.append(player + "(" + str(playerList.count(player)) + ")")
        
        #Top 16 calculations
        table16 = data.loc[((data["Char1"]==char) | (data["Char2"]==char))].reset_index(drop=True)
        playerList, top16Count, top16UniqueCount, top16UniquePlayer = [], 0, 0, []
        if table16.empty:
            pass
        else:
            playerList = list(table16["Player"])
            top16Count = len(playerList)
            top16UniqueCount = len(pd.unique(playerList))
            for player in pd.unique(playerList):
                top16UniquePlayer.append(player + "(" + str(playerList.count(player)) + ")")
        
        #Finalizing Appends
        top8CountList.append(top8Count)
        top8UniqueCountList.append(top8UniqueCount)
        top8UniquePlayerList.append(str(top8UniquePlayer).replace("[","").replace("]","").replace("'",""))
        top16CountList.append(top16Count)
        top16UniqueCountList.append(top16UniqueCount)
        top16UniquePlayerList.append(str(top16UniquePlayer).replace("[","").replace("]","").replace("'",""))
    '''
    for x in range(len(charList)):
        print(charList[x])
        print(top8CountList[x])
        print(top8UniqueCountList[x])
        print(top8UniquePlayerList[x])
    '''

    df = pd.DataFrame(data={"Character": charList, "Top 8": top8CountList, "Top 8 Unique": top8UniqueCountList, "Top 8 Players": top8UniquePlayerList,
                            "Top 16": top16CountList, "Top 16 Unique": top16UniqueCountList, "Top 16 Players": top16UniquePlayerList})
    return df.set_index("Character").sort_values(["Top 8","Top 16", "Top 8 Unique", "Top 16 Unique"], ascending = False)
    
def saveDataTable():
    dataTable().to_csv("Arc World Tour Analysis/AWT2023CharDataTable.csv")
    return

def validateData():
    data = pd.read_csv("Arc World Tour Analysis/Arc World Tour 2023 Character Data.csv").fillna("None")
    charList = ["Anji", "Axl", "Baiken", "Bridget", "Chipp", "Faust", "Gio", "Gold", "Happy", "Ino", "Jacko", "Ky", "Leo", "May", "Millia", "Nago", "Pot", "Ram", "Sol", "Test", "Zato", "Sin", "Bedman", "Asuka", "Johnny"]
    for x in range(len(data["Player"])):
        if (data.loc[x,"Char1"] not in charList) and (data.loc[x,"Char1"] != "None"):
            print(str(x+2) + " char1")
        if (data.loc[x,"Char2"] not in charList) and (data.loc[x,"Char2"] != "None"):
            print(str(x+2) + " char2")
    return

#validateData()
#print(dataTable())

saveDataTable()
    