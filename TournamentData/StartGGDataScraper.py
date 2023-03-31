import pysmashgg
import pandas as pd
import warnings
import time

key = "be97de5b2eb515e5f44d4cd4850d1985"
smash = pysmashgg.SmashGG(key)

#--- Event Placement Section ------------------------------------------------------------------------------------------#
def eventResults(eventFile, tourneyName, eventName, date="1.1.90"):
    #Pulls the placement results from the event
    data = pd.DataFrame.from_dict(smash.tournament_show_lightweight_results(tourneyName, eventName,1))
    placementEmptyFlag = 0
    page = 1
    while placementEmptyFlag == 0:
        page += 1
        newPlacements = pd.DataFrame.from_dict(smash.tournament_show_lightweight_results(tourneyName, eventName,page))
        if newPlacements.empty:
            placementEmptyFlag = 1
        else:
            data = data.append(newPlacements, ignore_index=True)
        print("Page #" + str(page) + " added.")
    df = pd.DataFrame(data, columns = ["placement", "name", "id"])
    charRef = pd.read_csv("TournamentData/playerCharRef.txt",sep=",")
    results = df.merge(charRef, how="left", on="name")
    results["tourney"] = tourneyName
    results["event"] = eventName
    results["date"] = date
    return results

def startEventFile(eventFile, tourneyName, eventName, date="1.1.90"):
    #Starts a csv file to store the event placements
    df = eventResults(eventFile,tourneyName,eventName,date)
    df.to_csv("TournamentData/"+eventFile+"/"+eventFile+"Placement.txt", sep=",", index=False)
    print(eventFile + ".txt has been created")
    return 

def addEventResults(eventFile, tourneyName, eventName, date="1.1.90"):
    #Adds to the already existing event placements file
    results = eventResults(eventFile, tourneyName, eventName, date)
    data = pd.read_csv("TournamentData/"+eventFile+"/"+eventFile+"Placement.txt", sep=",")
    with warnings.catch_warnings():
        warnings.simplefilter(action='ignore', category=FutureWarning)
        data = data.append(results, ignore_index=True)
    data.to_csv("TournamentData/"+eventFile+"/"+eventFile+"Placement.txt", sep=",", index=False)
    print(tourneyName + "/" + eventName + " has been added.")
    return 

def playerResult(playerName, filePath):
    df = pd.read_csv(filePath, sep=",")
    df = df[(df["name"]==playerName)]
    df = df.reset_index(drop=True)
    return df

def updateCharRef(eventFile):
    #Updates the char values of the placement file 
    data = pd.read_csv("TournamentData/"+eventFile+"/"+eventFile+"Placement.txt", sep=",")
    charRef = pd.read_csv("TournamentData/playerCharRef.txt",sep=",")
    data = data.drop(["char1", "char2", "char3"], axis=1)
    updatedData = data.merge(charRef, how="left", on="name")
    updatedData = updatedData.reindex(columns=["placement","name","id","char1","char2","char3","tourney","event","date"])
    updatedData.to_csv("TournamentData/"+eventFile+"/"+eventFile+"Placement.txt", sep=",", index=False)
    print("Character Reference Updated.")
    return

def allPlacementsUpdate():
    CLG = pd.read_csv("TournamentData/CLG/CLGPlacement.txt",sep=",")
    TNS = pd.read_csv("TournamentData/TNS/TNSPlacement.txt",sep=",")
    Moons = pd.read_csv("TournamentData/9Moons/9MoonsPlacement.txt",sep=",")
    df = CLG.append(TNS, ignore_index=True)
    df = df.append(Moons, ignore_index=True)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(by="date", axis=0, ascending=True).reset_index(drop=True)
    df.to_csv("TournamentData/AllPlacements.txt", sep=",", index=False)
    print("AllPlacements.txt has been updated")
    return 


#--- Event Sets Section --------------------------------------------------------------------------------------------------#
def tourneySets(tourneyName, eventName, date="1.1.1990"):
    #Pulls all of the sets from the event
    sets = smash.tournament_show_sets(tourneyName,eventName,1)
    allSets = pd.DataFrame.from_dict(sets)
    setEmptyFlag = 0
    page = 1
    while setEmptyFlag == 0:
        page += 1
        sets = smash.tournament_show_sets(tourneyName,eventName,page)
        setsDF = pd.DataFrame.from_dict(sets)
        if setsDF.empty:
            setEmptyFlag = 1
        else:
            allSets = allSets.append(setsDF, ignore_index=True)
        print("Page #" + str(page) + " added.")
    df = pd.DataFrame(data={"player1": allSets["entrant1Name"], "player2": allSets["entrant2Name"], "score1": allSets["entrant1Score"], "score2": allSets["entrant2Score"], "round": allSets["fullRoundText"]})
    df["player1"] = df["player1"].apply(lambda x: x.split(" | ")[len(x.split(" | "))-1])
    df["player2"] = df["player2"].apply(lambda x: x.split(" | ")[len(x.split(" | "))-1])
    df["tourneyName"] = tourneyName
    df["eventName"] = eventName
    df["date"] = date
    return df

def startSets(eventFile, tourneyName, eventName, date="1.1.1990"):
    #Start a csv file to store the sets
    df = tourneySets(tourneyName,eventName,date)
    df.to_csv("TournamentData/"+eventFile+"/"+eventFile+"Sets.txt", sep=",", index=False)
    print(eventFile + ".txt has been created")
    return 

def addSets(eventFile, tourneyName, eventName, date="1.1.1990"):
    #Adds to an already existing event sets file
    df = tourneySets(tourneyName,eventName,date)
    data = pd.read_csv("TournamentData/"+eventFile+"/"+eventFile+"Sets.txt", sep=",")
    with warnings.catch_warnings():
        warnings.simplefilter(action='ignore', category=FutureWarning)
        data = data.append(df, ignore_index=True)
    data.to_csv("TournamentData/"+eventFile+"/"+eventFile+"Sets.txt", sep=",", index=False)
    print(tourneyName + "/" + eventName + " Sets has been added.")
    return 

def playerMatchHistory(playerName, filePath):
    #Singles out one players sets from an event sets file
    df = pd.read_csv(filePath,sep=",")
    df = df[(df["player1"]==playerName) | (df["player2"]==playerName)]
    df = df.reset_index()
    opponentName, score, result,= [], [], []
    for x in range(len(df["player1"])):
        if df["player1"][x] == playerName:
            opponentName.append(df["player2"][x])
            score.append(str(df["score1"][x])+"-"+str(df["score2"][x]))
            if df["score1"][x] > df["score2"][x]:
                result.append("win")
            else:
                result.append("loss")
        else:
            opponentName.append(df["player1"][x])
            score.append(str(df["score2"][x])+"-"+str(df["score1"][x]))
            if df["score2"][x] > df["score1"][x]:
                result.append("win")
            else:
                result.append("loss")            
    matchHistory = pd.DataFrame(data={"opponent": opponentName, "result": result, "score": score, "round": df["round"], "tourneyName": df["tourneyName"], "eventName": df["eventName"], "date": df["date"]})
    matchHistory = matchHistory[matchHistory.score != "-1-0"]
    matchHistory = matchHistory[matchHistory.score != "0--1"]
    matchHistory = matchHistory[matchHistory.score != "-1--1"]   
    return matchHistory.reset_index(drop=True)

def playerRecords(playerName, filePath):
    #Creates a table of running set/game counts against each unique opponent a player has had a set with
    df = playerMatchHistory(playerName, filePath)
    name, setCountWin, setCountLoss, gameCountWin, gameCountLoss, lastPlayed = [], [], [], [], [], []
    for x in range(len(df["opponent"])):
        scoreList = df["score"][x].split("-")
        if (df["opponent"][x] in name) == False:
            #Adds a new player
            name.append(df["opponent"][x])
            gameCountWin.append(int(scoreList[0]))
            gameCountLoss.append(int(scoreList[1]))
            lastPlayed.append(df["date"][x])
            if scoreList[0] > scoreList[1]:
                setCountWin.append(1)
                setCountLoss.append(0)
            else:
                setCountWin.append(0)
                setCountLoss.append(1)
        else:
            #Alters an existing character
            nameLoc = name.index(df["opponent"][x])
            gameCountWin[nameLoc] = gameCountWin[nameLoc] + int(scoreList[0])
            gameCountLoss[nameLoc] = gameCountLoss[nameLoc] + int(scoreList[1])
            lastPlayed[nameLoc] = df["date"][x]
            if scoreList[0] > scoreList[1]:
                setCountWin[nameLoc] += 1
            else:
                setCountLoss[nameLoc] += 1
    setCount, gameCount, setPerc, gamePerc, totalSetCount = [], [], [], [], []
    for x in range(len(name)):
        setCount.append(str(setCountWin[x])+"-"+str(setCountLoss[x])+" ("+str(format(round(setCountWin[x]/(setCountWin[x]+setCountLoss[x]),2),".2f"))+")")
        gameCount.append(str(gameCountWin[x])+"-"+str(gameCountLoss[x])+" ("+str(format(round(gameCountWin[x]/(gameCountWin[x]+gameCountLoss[x]),2),".2f"))+")")
        totalSetCount.append(setCountWin[x]+setCountLoss[x])
    playerRecord = pd.DataFrame(data={"name": name, "sets": setCount, "games": gameCount, "totalSetCount": totalSetCount, "lastPlayed": lastPlayed})
    playerRecord = playerRecord.sort_values(by="totalSetCount", axis=0, ascending=False).drop("totalSetCount", axis=1).reset_index(drop=True)
    totalSetCount = str(sum(setCountWin)) + "-" + str(sum(setCountLoss)) + "("+str(format(round(sum(setCountWin)/(sum(setCountWin)+sum(setCountLoss)),2),".2f"))+")"
    totalGameCount = str(sum(gameCountWin)) + "-" + str(sum(gameCountLoss)) + "("+str(format(round(sum(gameCountWin)/(sum(gameCountWin)+sum(gameCountLoss)),2),".2f"))+")"
    playerRecord.loc[len(playerRecord.index)] = ["====Total====", totalSetCount, totalGameCount, "======"]
    return playerRecord

def playerRecordBotCommand(playerName, filePath):
    df = playerRecords(playerName, filePath)
    totalLoc = len(df["name"]) - 1 
    return playerName + " - sets: " + str(df["sets"][totalLoc]) + " games: " + str(df["games"][totalLoc])

def playerStatsByMonth(playerName, filePath):
    #Creates table for each month
    months = ["Jun22","Jul22","Aug22","Sep22","Oct22","Nov22","Dec22","Jan23","Feb23","Mar23","Apr23"]
    monthsNum = ["6.1.22","7.1.22","8.1.22","9.1.22","10.1.22","11.1.22","12.1.22","1.1.23","2.1.23","3.1.23","4.1.23"]
    monthsNum = pd.to_datetime(monthsNum)
    sets = playerMatchHistory(playerName, filePath)
    sets["date"] = pd.to_datetime(sets["date"])
    setResult, gameCount = [], []
    for x in range(len(monthsNum)-1):
        print(months[x])
        df = sets[sets["date"]>monthsNum[x]]
        df = df[df["date"]<monthsNum[x+1]].reset_index()
        if df.empty:
            setResult.append("-")
            gameCount.append("-")
        else:
            try:
                setWin = df["result"].value_counts()["win"]
            except:
                setWin = 0
            try:
                setLoss = df["result"].value_counts()["loss"]
            except:
                setLoss = 0
            setResult.append(str(setWin)+"-"+str(setLoss) + " ("+str(format(round(setWin/(setWin+setLoss),2),".2f"))+")")
            win, loss = 0, 0
            for x in range(len(df["date"])):
                scoreList = df["score"][x].split("-")
                win = win + int(scoreList[0])
                loss = loss + int(scoreList[1])
            gameCount.append(str(win) + "-" + str(loss) + " ("+str(format(round(win/(win+loss),2),".2f"))+")")
    months.pop()
    playerData = pd.DataFrame(data={"month": months, "sets": setResult, "games": gameCount})
    return playerData

def allSetsUpdate():
    CLG = pd.read_csv("TournamentData/CLG/CLGSets.txt",sep=",")
    TNS = pd.read_csv("TournamentData/TNS/TNSSets.txt",sep=",")
    Moons = pd.read_csv("TournamentData/9Moons/9MoonsSets.txt",sep=",")
    df = CLG.append(TNS, ignore_index=True)
    df = df.append(Moons, ignore_index=True)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(by="date", axis=0, ascending=True).reset_index(drop=True)
    df.to_csv("TournamentData/AllSets.txt", sep=",", index=False)
    print("AllSets.txt has been updated")
    return 

#allSetsUpdate()
#allPlacementsUpdate()
#player = "Vera Caelestis"
#player = "DomiWurld"
#x = playerMatchHistory(player,"TournamentData/AllSets.txt")
#y = playerRecords(player,"TournamentData/AllSets.txt")
#print(y.to_string())
#print(len(pd.unique(x["tourneyName"])))
#print(playerStatsByMonth(player,"TournamentData/AllSets.txt"))

def addNewCharRef():
    allSets = pd.read_csv("TournamentData/AllSets.txt", sep=",")
    allPlayers = allSets["player1"].tolist() + allSets["player2"].tolist()
    allPlayers = sorted(list(set(allPlayers)))
    oldRefTable = pd.read_csv("TournamentData/playerCharRef.txt", sep=",", keep_default_na=False)
    oldPlayer = oldRefTable["name"].tolist()
    newPlayers = list(set(allPlayers) - set(oldPlayer))
    print("Existing Players: "+ str(len(oldPlayer)))
    print("New Players added: "+ str(len(newPlayers)))
    newLen = len(newPlayers)
    char1, char2, char3 = [""]*newLen, [""]*newLen, [""]*newLen, 
    newDF = pd.DataFrame(data={"name": newPlayers, "char1": char1, "char2": char2, "char3": char3})
    data = oldRefTable.append(newDF, ignore_index=True)
    data = data.sort_values("name", ascending=True)
    data.to_csv("TournamentData/playerCharRef.txt", sep=",", index=False)
    return

#addNewCharRef()
#print(pd.DataFrame.from_dict(smash.tournament_show_lightweight_results("tns-guilty-gear-strive-45-pc","guilty-gear-strive-pc",1)))
print(playerResult("DomiWurld", "TournamentData/AllPlacements.txt"))
