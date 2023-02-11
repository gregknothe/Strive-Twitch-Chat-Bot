import pandas as pd
import numpy as np
from tabulate import tabulate

def importData(tourney=""):
    #Tourney can be a single tournament (str), arc world tour events ("AWT"), A list of tourney (list)
    if tourney == "":
        return pd.read_csv("MiscData/StriveS2Results.txt", sep=" ")
    elif tourney == "AWT":
        tourney = ["EVO2022", "VSFighting2022", "RevMajor2022", "CEOtaku2022", "Mixup2022", "FighersSpirit2022", "ARCREVOJapan2022", "FrostyFaustings2022"]
        data = pd.read_csv("MiscData/StriveS2Results.txt", sep=" ")
        dataNew = data.loc[data["tournament"] == tourney[0]]
        for x in tourney:
            if x != tourney[0]:
                dataTourney = data.loc[data["tournament"] == x]
                dataNew = pd.concat([dataNew, dataTourney])
        return dataNew
    elif isinstance(tourney, str):
        print("String")
        data = pd.read_csv("MiscData/StriveS2Results.txt", sep=" ")
        return data.loc[data["tournament"] == tourney]
    elif isinstance(tourney, list):
        print("List")
        data = pd.read_csv("MiscData/StriveS2Results.txt", sep=" ")
        dataNew = data.loc[data["tournament"] == tourney[0]]
        for x in tourney:
            if x != tourney[0]:
                dataTourney = data.loc[data["tournament"] == x]
                dataNew = pd.concat([dataNew, dataTourney])
        return dataNew
    return "Something went wrong"

def charLookup(data, charName):
    charTable16 = data.loc[data["char"] == charName]
    unique16 = pd.unique(charTable16["player"])
    uniqueCount16 = len(unique16)
    unique16 = str(unique16).replace("[","").replace("]","").replace("'","").replace(" ",", ")
    count16 = len(charTable16["player"])
    charTable8 = charTable16.loc[data["placement"]<=8]
    unique8 = pd.unique(charTable8["player"])
    uniqueCount8 = len(unique8)
    unique8 = str(unique8).replace("[","").replace("]","").replace("'","").replace(" ",", ")
    count8 = len(charTable8["player"])
    data = pd.DataFrame(data={"character": charName, "Top 8": count8, "Top 16": count16, "Top 8 Unique": uniqueCount8, "Top 16 Unique": uniqueCount16, "Top 8 Players": [unique8], "Top 16 Players": [unique16]})
    return data

def charDataTable(tourney=""):
    data = importData(tourney)
    charList = ["Axl", "Baiken", "Bridget", "Chipp", "Faust", "Gio", "Gold", "Happy", "Ino", "Jacko", "Ky", "Leo", "May", "Millia", "Nago", "Pot", "Ram", "Sol", "Test", "Zato", "Sin"]
    table = charLookup(data, "Anji")
    for x in charList:
        table = pd.concat([table, charLookup(data, x)])
    return table.set_index("character").sort_values(["Top 8","Top 16", "Top 8 Unique", "Top 16 Unique"], ascending = False)

def tournamentWinners(tourney=""):
    data = importData(tourney)
    return data.loc[data["placement"]==1]

def charDataframe(char, tourney=""):
    data = importData(tourney)
    return data.loc[data["char"]==char]

#print(charDataTable())
#print(charDataTable("AWT"))
#print(tournamentWinners())
#print(charDataframe("Happy","AWT"))

#Character Player list 
#print(charDataTable(importData()).loc["Zato"]["Top 8 Players"])

print(charDataTable())