import pandas as pd 
import datetime
from collections import Counter

def playerLookup(playerName, event="TNS", startDate="6.1.22", endDate="6.1.23"):
    df = pd.read_csv("TournamentData/" + event + ".txt", sep=",")
    df = df[df["name"]==playerName]
    df["dateTime"] = pd.to_datetime(df["date"], format="%m.%d.%y")
    df = df.loc[df["dateTime"]>=startDate]
    df = df.loc[df["dateTime"]<=endDate]
    df = df.drop("dateTime", axis=1)
    return df

def charLookup(charName, event="TNS", minPlacement=16, startDate="6.1.22", endDate="6.1.23"):
    df = pd.read_csv("TournamentData/" + event + ".txt", sep=",")
    df = df[(df["char1"]==charName) | (df["char2"]==charName) | (df["char3"]==charName)]
    df["dateTime"] = pd.to_datetime(df["date"], format="%m.%d.%y")
    df = df.loc[df["dateTime"]>=startDate]
    df = df.loc[df["dateTime"]<=endDate]
    df = df.loc[df["placement"]<=minPlacement]
    df = df.drop("dateTime", axis=1)
    return df
#print(charLookup("Anji","TNS",8))

def charTable(event="TNS", startDate="6.1.22", endDate="6.1.23"):
    charList = ["Anji", "Axl", "Baiken", "Bridget", "Chipp", "Faust", "Gio", "Gold", "Happy", "Ino", "Jacko", "Ky", "Leo", "May", "Millia", "Nago", "Pot", "Ram", "Sol", "Test", "Zato", "Sin"]
    top8Count, top8Players, top8Unique, top16Count, top16Players, top16Unique= [], [], [], [], [], []
    for char in charList:
        top16 = charLookup(char,event,16,startDate,endDate)
        top8 = top16[top16["placement"]<=8]
        top16Count.append(len(top16["name"]))
        top8Count.append(len(top8["name"]))
        unique16 = top16["name"].unique() 
        unique8 = top8["name"].unique()

        count16 = Counter(top16["name"])
        playerList16 = list(count16.keys())
        countList16 = list(count16.values())
        playerList16 = [x for _, x in sorted(zip(countList16, playerList16), reverse=True)]
        countList16.sort(reverse=True)
        playerCountList16 = []
        for x in range(len(countList16)):
            playerCount = str(playerList16[x]) + "(" + str(countList16[x]) + ")"
            playerCountList16.append(playerCount)

        count8 = Counter(top8["name"])
        playerList8 = list(count8.keys())
        countList8 = list(count8.values())
        playerList8 = [x for _, x in sorted(zip(countList8, playerList8), reverse=True)]
        countList8.sort(reverse=True)
        playerCountList8 = []
        for x in range(len(countList8)):
            playerCount = str(playerList8[x]) + "(" + str(countList8[x]) + ")"
            playerCountList8.append(playerCount)

        top16Players.append(", ".join(playerCountList16))
        top8Players.append(", ".join(playerCountList8))
        top16Unique.append(len(unique16))
        top8Unique.append(len(unique8))
    df = pd.DataFrame(data={"char": charList, "top 8": top8Count, "unique(8)": top8Unique, "top 16": top16Count, "unique(16)": top16Unique, "top 8 Players": top8Players, "top 16 Players": top16Players})
    return df.sort_values(by=["top 8", "top 16", "unique(8)", "unique(16)"], ascending=False).reset_index(drop=True)

x = charTable()
print(x["top 8 Players"][0])

