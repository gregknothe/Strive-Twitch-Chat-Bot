import pandas as pd
import re
import urllib.request
import difflib
import numpy as np

'''
To Do List:
1. Add in Rekka gatling options, prob by hand 
2. Do the math part of the frame trap, test it, update the 
   twitch bot to utilize it
3. Create a UI (website/phoneapp/ect) to house said program
'''

def nameCleaner(char):
    #Takes the user inputed character name and replaces it with a useable character name (hopefully).
    charList = ["Testament", "Jack-O", "Nagoriyuki", "Nago", "Millia", "Millia_Rage", "Chipp", "Chipp_Zanuff", "Sol", "Sol_Badguy", "Ky", "Ky_Kiske", "Kyle", "May", 
                "Zato-1", "I-No", "Happy", "Chaos", "Happy_Chaos", "Bedman", "Sin", "Sin_Kiske", "Baiken", "Anji", "Anji_Mito", "Leo", "Leo_Whitefang", "Faust", "Axl", "Axl_Low",
                "Potemkin", "Ramlethal", "Ram", "Ramlethal_Valentine", "Giovanna", "Gio", "Goldlewis", "Gold", "Goldlewis_Dickinson", "Bridget", "Asuka_R"]
    char = str(difflib.get_close_matches(char,charList,n=1,cutoff=.3)).replace("['","").replace("']","")
    if char == "Sol":
        char = "Sol_Badguy"
    elif char == "Ky" or char == "Kyle":
        char = "Ky_Kiske"
    elif char == "Happy" or char == "Chaos":
        char = "Happy_Chaos"
    elif char == "Sin":
        char = "Sin_Kiske"
    elif char == "Leo":
        char = "Leo_Whitefang"
    elif char == "Anji":
        char = "Anji_Mito"
    elif char == "Axl":
        char = "Axl_Low"
    elif char == "Ramelthal" or char == "Ram":
        char = "Ramlethal_Valentine"
    elif char == "Goldlewis" or char == "Gold":
        char = "Goldlewis_Dickinson"
    elif char == "Nago":
        char = "Nagoriyuki"
    elif char == "Gio":
        char = "Giovanna"
    elif char == "Millia":
        char = "Millia_Rage"
    return char

def dataScrape(char):
    #scrapes dustloop for the move and gatling tables (still needs cleaning)
    charName = nameCleaner(char)
    url = "https://www.dustloop.com/w/GGST/" + charName + "/Frame_Data"
    data = pd.read_html(url)
    moves, gatling = [], []
    for x in data:
        if "Input" in x.columns:
            moves.append(x)
        if "P" in x.columns:
            gatling.append(x)
    moveDF = pd.concat(moves)
    gatlingDF = pd.concat(gatling)
    return moveDF, gatlingDF

def update(char):
    data = dataScrape(char)[0]
    data.to_csv("GGST-Frame/RawData/"+nameCleaner(char)+".txt", sep="/")
    return char +" updated."

def updateAll():
    charList =  ["Testament", "Jack-O", "Nagoriyuki", "Millia_Rage", "Chipp_Zanuff", "Sol_Badguy", "Ky_Kiske", "May", 
                "Zato-1", "I-No", "Happy_Chaos", "Bedman", "Sin_Kiske", "Baiken", "Anji_Mito", "Leo_Whitefang", "Faust", "Axl_Low", 
                "Potemkin", "Ramlethal_Valentine", "Giovanna", "Goldlewis_Dickinson", "Bridget", "Asuka_R"]
    for x in charList:
        print(update(x))
    return

def moveLookup(char, move):
    #Looks up move data from the raw data.
    char = nameCleaner(char)
    data = pd.read_csv("GGST-Frame/RawData/"+char+".txt", sep="/")
    moveList = data["Input"].to_list()
    moveListLower = [x.lower() for x in moveList]
    move = move.lower()
    move = str(difflib.get_close_matches(move,moveListLower,n=1,cutoff=.5)).replace("['","").replace("']","")
    moveIndex = moveListLower.index(move)
    moveData = data[data["Input"]==moveList[moveIndex]]
    return char + " " + moveData.loc[moveIndex, "Input"] + " | s: " + moveData.loc[moveIndex, "Startup"] + ", a: " + moveData.loc[moveIndex, "Active"] + ", r: " + moveData.loc[moveIndex, "Recovery"] + ", ob: " + moveData.loc[moveIndex, "On-Block"] + ", oh: " + moveData.loc[moveIndex, "On-Hit"]

def bracketSplitter(moveRow):
    #Splits held moves (noted by "[]") into two seperate entries in the dataframe. WIP
    i = moveRow.index[0]
    #print(moveRow)
    if "[" in moveRow.loc[i]["Startup"] or "[" in moveRow.loc[i]["On-Block"]:
        bRow = moveRow 
        if "[" in bRow.loc[i, "Startup"]:
            bRow.loc[i, "Startup"] = bRow.loc[i]["Startup"].split("[")[1].split("]")[0]
        if "[" in bRow.loc[i, "On-Block"]:
            bRow.loc[i, "On-Block"] = bRow.loc[i]["On-Block"].split("[")[1].split("]")[0]
        if "[" in bRow.loc[i, "Level"]:
            bRow.loc[i, "Level"] = bRow.loc[i]["Level"].split("[")[1].split("]")[0]
        bRow.loc[i, "Input"] = bRow.loc[i]["Input"].replace("P","[P]").replace("K","[K]").replace("S","[S]").replace("H","[H]")
    return bRow

def curlySplitter(moveRow):
    i = moveRow.index[0]
    if "{" in moveRow.loc[i]["Startup"] or "{" in moveRow.loc[i]["On-Block"]:
        cRow = moveRow 
        if "{" in cRow.loc[i, "Startup"]:
            cRow.loc[i, "Startup"] = cRow.loc[i]["Startup"].split("{")[1].split("}")[0]
        if "{" in cRow.loc[i, "On-Block"]:
            cRow.loc[i, "On-Block"] = cRow.loc[i]["On-Block"].split("{")[1].split("}")[0]
        if "{" in cRow.loc[i, "Level"]:
            cRow.loc[i, "Level"] = cRow.loc[i]["Level"].split("{")[1].split("}")[0]   
        cRow.loc[i, "Input"] = cRow.loc[i]["Input"].replace("P","{P}").replace("K","{K}").replace("S","{S}").replace("H","{H}")
    return cRow

def addGatling(gatDF):
    #Formats the gatling table
    gatDF = gatDF.reset_index(drop=True)
    inputs, gats = [], []
    for x in range(len(gatDF)):
        inputs.append(gatDF.loc[x]["Unnamed: 0"].split("Guard:")[0].replace("No results",""))
        cancels = gatDF.loc[x]["P"] +" "+ gatDF.loc[x]["K"] +" "+ gatDF.loc[x]["S"] +" "+ gatDF.loc[x]["H"] +" "+ gatDF.loc[x]["D"] +" "+ gatDF.loc[x]["Cancel"]
        cancels = re.sub(" +", " ", cancels.replace("-"," ").replace(","," "))
        gats.append(cancels)
    newDF = pd.DataFrame(data={"Input": inputs, "Cancels": gats})
    return newDF

def moveCleaner(moveDF, gatDF):
    #Cleans the move dataframe to make it more usable down the line
    #ex: Deals with held moves
    moves = moveDF[moveDF.Input != "Input"].reset_index(drop=True)
    moves = moves.merge(addGatling(gatDF), how="left", on="Input").fillna("")
    for x in range(len(moves.index)):
        #First run through, adding new rows to the dataframe
        clFlag = 0
        if "[" in str(moves["Startup"][x]) or "[" in str(moves["On-Block"][x]):
            moves.loc[len(moves.index)] = bracketSplitter(moves.loc[[x]]).loc[x]
            clFlag = 1
        if "{" in str(moves["Startup"][x]) or "{" in str(moves["On-Block"][x]):
            moves.loc[len(moves.index)] = curlySplitter(moves.loc[[x]]).loc[x]
            clFlag = 1
        if clFlag == 1:
            moves.loc[x, "Startup"] = str(moves.loc[x, "Startup"]).split(" ")[0]
            moves.loc[x, "On-Block"] = str(moves.loc[x, "On-Block"]).split(" ")[0]
            moves.loc[x, "Level"] = str(moves.loc[x, "Level"]).split(" ")[0]
    Type = []
    for x in range(len(moves.index)):
        #Second run through on the entire dataframe
        if "(" in str(moves["Startup"][x]):
            newStartup = moves.loc[x, "Startup"].split("(")[0] + moves.loc[x, "Startup"].split(")")[1]
            moves.loc[x, "Startup"] = newStartup
        if "+" in str(moves.loc[x, "Startup"]):
            newStartup = re.sub(' +', ' ', moves.loc[x, "Startup"].replace("+"," "))
            newStartup = int(newStartup.split(" ")[0]) + int(newStartup.split(" ")[1])
            moves.loc[x, "Startup"] = newStartup
        if "~" in str(moves.loc[x, "Startup"]):
            moves.loc[x, "Startup"] = moves.loc[x, "Startup"].split("~")[0]
        if pd.isnull(moves.loc[x, "Name"]) == True:
            if "j." in moves.loc[x,"Input"]:
                Type.append("jump normal")
            else:
                Type.append("Normal")
        else:
            Type.append("Special")
    moves["Type"] = Type
    moves = moves.drop(["Unnamed: 0", "Damage", "Guard", "Invuln", "Proration", "R.I.S.C. Gain", "R.I.S.C. Loss", "Name", "On-Hit", "Counter Type", "Active"], axis=1)
    return moves

#char = "ram"
#x = moveCleaner(dataScrape(char)[0], dataScrape(char)[1])
#y = addGatling(x)
#print(x)



