import pandas as pd
import re
import urllib.request
import difflib
import numpy as np

'''
To Do List:

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
    elif char == "Chipp":
        char = "Chipp_Zanuff"
    return char

def dataScrape(char):
    #scrapes dustloop for the move and gatling tables (still needs cleaning)
    charName = nameCleaner(char)
    url = "https://www.dustloop.com/w/GGST/" + charName + "/Frame_Data"
    data = pd.read_html(url)
    moves, gatling = [], []
    for x in data:
        if "Damage" in x.columns:
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
    if "[" in moveRow.loc[i]["Startup"] or "[" in moveRow.loc[i]["On-Block"] or "[" in moveRow.loc[i]["Level"]: ##########################################
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

def addRekkas(char, moveDF):
    #Adds rekka gattlings to the dataframe
    if char == "Chipp_Zanuff":
        for x in range(len(moveDF["Input"])):
            if moveDF.loc[x]["Input"] == "236S":
                moveDF.loc[x]["Cancels"] = moveDF.loc[x]["Cancels"] + "236S 236S,236S 236K"
            if moveDF.loc[x]["Input"] == "236S 236S" or moveDF.loc[x]["Input"] == "236S 236K":
                moveDF.loc[x]["Type"] = "Rekka Followup"
    if char == "Sol_Badguy":
        for x in range(len(moveDF["Input"])):
            if moveDF.loc[x]["Input"] == "236K":
                moveDF.loc[x]["Cancels"] = moveDF.loc[x]["Cancels"] + "236KK"
            if moveDF.loc[x]["Input"] == "236KK":
                moveDF.loc[x]["Type"] = "Rekka Followup"
    if char == "Anji_Mito":
        for x in range(len(moveDF["Input"])):
            if moveDF.loc[x]["Input"] == "236H" or moveDF.loc[x]["Input"] == "236[H]":
                moveDF.loc[x]["Cancels"] = moveDF.loc[x]["Cancels"] + "236H P, 236H K, 236H S, 236H H"
            if moveDF.loc[x]["Input"] == "236H P" or moveDF.loc[x]["Input"] == "236H K" or moveDF.loc[x]["Input"] == "236H S" or moveDF.loc[x]["Input"] == "236H H":
                moveDF.loc[x]["Type"] = "Rekka Followup"
    if char == "Bridget":
        for x in range(len(moveDF["Input"])):
            if moveDF.loc[x]["Input"] == "f.S" or moveDF.loc[x]["Input"] == "2S":
                moveDF.loc[x]["Cancels"] = moveDF.loc[x]["Cancels"].replace("SFollowUp","S")
            if moveDF.loc[x]["Input"] == "5H" or moveDF.loc[x]["Input"] == "2H":
                moveDF.loc[x]["Cancels"] = moveDF.loc[x]["Cancels"].replace("HFollowUp","H")
            if moveDF.loc[x]["Input"] == "SFollowUp" or moveDF.loc[x]["Input"] == "HFollowUp":
                moveDF.loc[x]["Type"] = "Rekka Followup"
    if char == "Ramlethal_Valentine":
        for x in range(len(moveDF["Input"])):
            if moveDF.loc[x]["Input"] == "214P":
                moveDF.loc[x]["Cancels"] = moveDF.loc[x]["Cancels"] + "214P 214P"
            if moveDF.loc[x]["Input"] == "214P 214P":
                moveDF.loc[x]["Cancels"] = moveDF.loc[x]["Cancels"] + "214P 214P 214P"
            if moveDF.loc[x]["Input"] == "214[P] 214[P]":
                moveDF.loc[x]["Cancels"] = moveDF.loc[x]["Cancels"] + "214P 214P 214P"
            if moveDF.loc[x]["Input"] == "214[P] 214[P]" or moveDF.loc[x]["Input"] == "214P 214P" or  moveDF.loc[x]["Input"] == "214P 214P 214P":
                moveDF.loc[x]["Type"] = "Rekka Followup"
    if char == "Nagoriyuki":
        for x in range(len(moveDF["Input"])):
            if moveDF.loc[x]["Input"] == "236S":
                moveDF.loc[x]["Cancels"] = moveDF.loc[x]["Cancels"] + "214H,623H"
            if moveDF.loc[x]["Input"] == "214H":
                moveDF.loc[x]["Cancels"] = moveDF.loc[x]["Cancels"] + "236S,623H"
            if moveDF.loc[x]["Input"] == "623H":
                moveDF.loc[x]["Cancels"] = moveDF.loc[x]["Cancels"] + "236S,214H,623HH"
            if moveDF.loc[x]["Input"] == "623HH":
                moveDF.loc[x]["Cancels"] = moveDF.loc[x]["Cancels"] + "236S,214H"
            if "f.S" in moveDF.loc[x]["Input"]:
                level = moveDF.loc[x]["Input"].split(".")[2]
                moveDF.loc[x]["Cancels"] = "f.SS." + level + ",5H." + level + ",2H." + level 
            if "f.SS" in moveDF.loc[x]["Input"]:
                level = moveDF.loc[x]["Input"].split(".")[2]
                moveDF.loc[x]["Cancels"] = "f.SSS." + level
            if "5H" in moveDF.loc[x]["Input"] or "2H" in moveDF.loc[x]["Input"] or "6H" in moveDF.loc[x]["Input"]:
                moveDF.loc[x]["Cancels"] = "Special,Super"
                moveDF.loc[x]["Type"] = "Normal"
            if "2S" in moveDF.loc[x]["Input"]:
                level = moveDF.loc[x]["Input"].split(".")[1]
                moveDF.loc[x]["Cancels"] = "5H." + level + ",2H." + level + ",Special,Super"
                moveDF.loc[x]["Type"] = "Normal"
            if "j.S" in moveDF.loc[x]["Input"]:
                level = moveDF.loc[x]["Input"].split(".")[2]
                moveDF.loc[x]["Cancels"] = "j.H." + level + ",j.D." + level 
            if "j.H" in moveDF.loc[x]["Input"]:
                level = moveDF.loc[x]["Input"].split(".")[2]
                moveDF.loc[x]["Cancels"] = "j.D." + level     
            if moveDF.loc[x]["Input"] == "623HH" or moveDF.loc[x]["Input"] == "f.SS.1" or moveDF.loc[x]["Input"] == "f.SSS.1" or moveDF.loc[x]["Input"] == "f.SS.2" or moveDF.loc[x]["Input"] == "f.SSS.2"\
                or moveDF.loc[x]["Input"] == "f.SS.3" or moveDF.loc[x]["Input"] == "f.SSS.3" or moveDF.loc[x]["Input"] == "f.SS.BR" or moveDF.loc[x]["Input"] == "f.SSS.BR": 
                moveDF.loc[x]["Type"] = "Rekka Followup"
    return moveDF

def addGatling(gatDF):
    #Formats the gatling table
    gatDF = gatDF.reset_index(drop=True)
    inputs, gats = [], []
    for x in range(len(gatDF)):
        inputs.append(gatDF.loc[x]["Unnamed: 0"].split("Guard")[0].replace("No results",""))
        cancels = gatDF.loc[x]["P"] +", "+ gatDF.loc[x]["K"] +", "+ gatDF.loc[x]["S"] +", "+ gatDF.loc[x]["H"] +", "+ gatDF.loc[x]["D"] +", "+ gatDF.loc[x]["Cancel"]
        cancels = re.sub(" +", " ", cancels.replace("-"," ").replace(" ,","")).replace(" ","")
        gats.append(cancels)
    newDF = pd.DataFrame(data={"Input": inputs, "Cancels": gats})
    #print(newDF)
    return newDF

def moveCleaner(moveDF, gatDF):
    #Cleans the move dataframe to make it more usable down the line
    #ex: Deals with held moves
    moves = moveDF[moveDF.Input != "Input"].reset_index(drop=True).fillna("")
    for x in range(len(moves.index)):
        #First run through, adding new rows to the dataframe
        clFlag = 0
        if "bt." in moves["Name"][x]:
            #Applies an Input value to Leo's backturn normals for later use
            moves["Input"][x] = moves["Name"][x]
        if " Level " in moves["Input"][x]:
            moves.loc[x, "Input"] = moves.loc[x, "Input"].replace(" Level ",".")
        if "[" in str(moves["Startup"][x]) or "[" in str(moves["On-Block"][x]) or "[" in str(moves["Level"][x]):##################################
            if str(moves.loc[x, "Startup"])[0] == "[":
                moves.loc[x, "Startup"] = moves.loc[x]["Startup"].split("]")[1]
            else:
                moves.loc[len(moves.index)] = bracketSplitter(moves.loc[[x]]).loc[x]
                clFlag = 1
        if "{" in str(moves["Startup"][x]) or "{" in str(moves["On-Block"][x]):
            moves.loc[len(moves.index)] = curlySplitter(moves.loc[[x]]).loc[x]
            clFlag = 1
        if clFlag == 1:
            moves.loc[x, "Startup"] = str(moves.loc[x, "Startup"]).split(" ")[0]
            moves.loc[x, "On-Block"] = str(moves.loc[x, "On-Block"]).split(" ")[0]
            moves.loc[x, "Level"] = str(moves.loc[x, "Level"]).split(" ")[0]
            moves.loc[x, "Level"] = str(moves.loc[x, "Level"]).split("[")[0]
    Type = []
    for x in range(len(moves.index)):
        #Second run through on the entire dataframe
        if "~" in str(moves.loc[x, "Startup"]):
            moves.loc[x, "Startup"] = moves.loc[x, "Startup"].split("~")[0]
        if "(" in str(moves["Startup"][x]):
            newStartup = moves.loc[x, "Startup"].split("(")[0] + moves.loc[x, "Startup"].split(")")[1]
            moves.loc[x, "Startup"] = newStartup
        if "+" in str(moves.loc[x, "Startup"]):
            newStartup = re.sub(' +', ' ', moves.loc[x, "Startup"].replace("+"," ")).split(" ")
            if newStartup[0] != "" and newStartup[1] != "":
                newStartup = int(newStartup[0]) + int(newStartup[1])
            else:
                newStartup = newStartup[0]
            moves.loc[x, "Startup"] = newStartup
        if moves.loc[x, "Startup"] == "-":
            moves.loc[x, "Startup"] = ""
        if "-" in str(moves.loc[x, "Startup"]):
            moves.loc[x, "Startup"] = str(moves.loc[x,"Startup"]).split("-")[0]
        if "," in str(moves.loc[x, "On-Block"]):
            moves.loc[x, "On-Block"] = moves.loc[x, "On-Block"].replace(",","")
        if " " in str(moves.loc[x, "On-Block"]):
            moves.loc[x, "On-Block"] = moves.loc[x, "On-Block"].split(" ")[0]
        if "~" in str(moves.loc[x, "On-Block"]):
            moves.loc[x, "On-Block"] = moves.loc[x, "On-Block"].split("~")[0]
        if "+" in str(moves.loc[x, "On-Block"]):
            moves.loc[x, "On-Block"] = moves.loc[x, "On-Block"].split("+")[1]
        if moves.loc[x, "On-Block"] == "-" or moves.loc[x, "On-Block"] == "See" or moves.loc[x, "On-Block"] == "More" or moves.loc[x, "On-Block"] == "-":
            moves.loc[x, "On-Block"] = ""
        numCount = sum(c.isdigit() for c in moves.loc[x, "Input"])
        #Since Jack-o's tables are poorly formated.
        if moves.loc[x, "Input"] == "6H" and moves.loc[x,"Startup"] == "819":
            moves.loc[x, "Startup"] = 27
        if moves.loc[x, "Input"] == "214H" and moves.loc[x,"Active"] == "19":
            moves.loc[x, "Startup"] = 208
        #Zato formating
        if "Total" in str(moves.loc[x, "Startup"]):
            moves.loc[x, "Startup"] = moves.loc[x, "Startup"].replace(" Total","")
        #I-no formating
        if moves.loc[x,"Input"] == "632146H" and moves.loc[x,"Damage"] == "13×18 (17×11)":
            moves.loc[x,"On-Block"] = "-18"
            moves.loc[x, "Level"] = "2"
        #Asuka Spell Formating 
        if ", " in str(moves.loc[x, "Startup"]):
            moves.loc[x, "Startup"] = str(moves.loc[x, "Startup"]).split(", ")[0]
        if "/" in str(moves.loc[x, "On-Block"]):
            moves.loc[x, "On-Block"] = str(moves.loc[x, "On-Block"]).split("/")[0]
        asukaSpells = ["Howling Metron", "Delayed Howling Metron", "Delayed Howling Metron", "Howling Metron MS Processing",
                       "Metron Screamer 808", "Metron Arpeggio", "Delayed Tardus Metron", "Terra Metron", "Accipiter Metron",
                       "Aquila Metron", "Bit Shift Metron", "Bit Shift Metron", "RMS Boost Metron"]
        if numCount == 1 or numCount == 0:
            if moves.loc[x, "Input"] in asukaSpells:
                Type.append("Special")
            elif "j." in moves.loc[x, "Input"]:
                Type.append("jump Normal")
            else:
                Type.append("Normal")
        elif numCount == 2 or numCount == 3 or numCount == 4 or numCount == 5:
            if "j." in moves.loc[x, "Input"]:
                Type.append("jump Special")
            else:
                Type.append("Special")
        else:
            if "j." in moves.loc[x, "Input"]:
                Type.append("jump Super")
            else:
                Type.append("Super")
        if moves.loc[x, "Level"] != "" and moves.loc[x, "Level"] != "-":
            level = moves.loc[x, "Level"].split(".")[0]
            moves.loc[x, "Level"] = level[len(level)-1]
        else: 
            moves.loc[x, "Level"] = ""
    moves["Type"] = Type
    moves = moves.merge(addGatling(gatDF), how="left", on="Input").fillna("")
    moves = moves.drop(["Unnamed: 0", "Damage", "Guard", "Invuln", "Proration", "R.I.S.C. Gain", "R.I.S.C. Loss", "Name", "On-Hit", "Counter Type"], axis=1)
    return moves[moves["Input"]!=""].reset_index(drop=True)

def updateClean(char):
    char = nameCleaner(char)
    data = dataScrape(char)
    df = moveCleaner(data[0], data[1])
    df = addRekkas(char, df)
    df.to_csv("GGST-Frame/CleanData/"+nameCleaner(char)+".txt", sep="/")
    return df

def updateCleanAll():
    charList = ["Testament", "Jack-O", "Nagoriyuki", "Millia_Rage", "Chipp_Zanuff", "Sol_Badguy", "Ky_Kiske", "May",
                "Zato-1", "I-No", "Happy_Chaos", "Bedman", "Sin_Kiske", "Baiken", "Anji_Mito", "Leo_Whitefang", 
                "Faust", "Axl_Low", "Potemkin", "Ramlethal_Valentine", "Giovanna", "Goldlewis_Dickinson", "Bridget", "Asuka_R"]
    for x in charList:
        updateClean(x)
        print(x+" Clean Data Updated.")
    return 

def inputCleaner(move, moveList):
    moveList = moveList.to_list()
    moveListLower = [x.lower() for x in moveList]
    move = move.lower()
    move = str(difflib.get_close_matches(move,moveListLower,n=1,cutoff=.5)).replace("['","").replace("']","")
    moveIndex = moveListLower.index(move)
    return moveList[moveIndex]

def viewData(char):
    print(pd.read_csv("GGST-Frame/CleanData/"+char+".txt", sep="/").fillna("").reset_index(drop=True).drop(["Unnamed: 0"], axis=1).to_string())
    return

def viewDataAll():
    charList = ["Testament", "Jack-O", "Nagoriyuki", "Millia_Rage", "Chipp_Zanuff", "Sol_Badguy", "Ky_Kiske", "May",
                "Zato-1", "I-No", "Happy_Chaos", "Bedman", "Sin_Kiske", "Baiken", "Anji_Mito", "Leo_Whitefang", 
                "Faust", "Axl_Low", "Potemkin", "Ramlethal_Valentine", "Giovanna", "Goldlewis_Dickinson", "Bridget", "Asuka_R"]
    for x in charList:
        print("---"+x+"--------------------------------------------------------------------------------------------------------------------")
        viewData(x)
    return

def levelHitstun(level):
    if level == 0:
        return 9
    elif level == 1:
        return 11
    elif level == 2:
        return 13
    elif level == 3:
        return 16
    elif level == 4:
        return 18
    else:
        print("Attack does not have an attack level.")
        return 1000000

def dataVerification(char):
    data = pd.read_csv("GGST-Frame/CleanData/"+char+".txt", sep="/").fillna("").reset_index(drop=True).drop(["Unnamed: 0"], axis=1)
    dataSU = data[data["Startup"]!=""]
    print(dataSU[dataSU["Startup"]>=30])
    dataOB = data[data["On-Block"]!=""]
    print(dataOB[dataOB["On-Block"]<=-20])
    dataLv = data[data["Level"]!=""]
    print(dataLv[dataLv["Level"]>4])
    return

def dataVerficationAll():
    charList = ["Testament", "Jack-O", "Nagoriyuki", "Millia_Rage", "Chipp_Zanuff", "Sol_Badguy", "Ky_Kiske", "May",
                "Zato-1", "I-No", "Happy_Chaos", "Bedman", "Sin_Kiske", "Baiken", "Anji_Mito", "Leo_Whitefang", 
                "Faust", "Axl_Low", "Potemkin", "Ramlethal_Valentine", "Giovanna", "Goldlewis_Dickinson", "Bridget", "Asuka_R"]
    for x in charList:
        print("---"+x+"--------------------------------------------------------------------------------------------------------------------")
        dataVerification(x)
    return

def frameTrap(char, move1, move2):
    char = nameCleaner(char)
    data = pd.read_csv("GGST-Frame/CleanData/"+char+".txt", sep="/").fillna("").reset_index(drop=True).drop(["Unnamed: 0"], axis=1)
    move1 = inputCleaner(move1, data["Input"])
    move2 = inputCleaner(move2, data["Input"])
    move1Index = data.index[data["Input"]==move1].tolist()[0]
    move1Act, move1Rec, move1OB, move1Lvl, move1Cancel = data.loc[move1Index, "Active"], data.loc[move1Index, "Recovery"], data.loc[move1Index, "On-Block"], data.loc[move1Index, "Level"], data.loc[move1Index, "Cancels"]
    move2Index = data.index[data["Input"]==move2].tolist()[0]
    move2Start, move2Type = data.loc[move2Index, "Startup"], data.loc[move2Index, "Type"]
    #Rekka Check
    if move2Type == "Rekka Followup" and move2 not in move1Cancel:
        return char + " " + move1 + " > " + move2 + ": " + move2 + " is a follow-up move that cannot be performed after " + move1 + "."
    #Ground Gatling 
    elif (move2 in move1Cancel or move2Type in move1Cancel) and "j." not in move1 and "j." not in move2:
        gap = move2Start - levelHitstun(move1Lvl) 
    #Ground Non-gatling
    elif (move2 not in move1Cancel and move2Type not in move1Cancel) and "j." not in move1 and "j." not in move2:
        gap = move2Start - move1OB
    #Ground to Air (Jump cancelable)
    elif "j." not in move1 and "j." in move2 and "Jump" in move1Cancel:
        if char in ["Nagoriyuki", "Goldlewis_Dickinson", "Potemkin", "Bedman"]:
            gap = move2Start + 5 - levelHitstun(move1Lvl)
        else:
            gap = move2Start + 5 - levelHitstun(move1Lvl)
    #Ground to Air (Non-jump cancelable)
    elif "j." not in move1 and "j." in move2 and "Jump" not in move1Cancel:
        if char in ["Nagoriyuki", "Goldlewis_Dickinson", "Potemkin", "Bedman"]:
            gap = move2Start + 5 - move1OB
        else:
            gap = move2Start + 5 - move1OB
    #Air Gatling
    elif "j." in move1 and "j." in move2 and (move2 in move1Cancel or move2Type in move1Cancel):
        gap = move2Start - levelHitstun(move1Lvl)
    #Air non-gatling and Air to Ground
    else:
        return char + " " + move1 + " > " + move2 + ": " + move1 + " has " + str(levelHitstun(move1Lvl)) + "f of blockstun, while " + move2 + " has " + str(move2Start) + "f of startup. Air move's frame advantage differs based on height of hit, jump arc, recovery and other factors. "
    return char + " " + move1 + " > " + move2 + ": " + str(round(gap)) + "f gap."

#viewData("Anji_Mito")
print(frameTrap("chipp", "jh", "236s"))

