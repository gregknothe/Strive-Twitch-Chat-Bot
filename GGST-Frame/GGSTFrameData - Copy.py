import pandas as pd
import re
import urllib.request
import difflib
import numpy as np
import sys

'''
To Do List:


3. Create a UI (website/phoneapp/ect) to house said program
'''

charListFinal =  ["Testament", "Jack-O", "Nagoriyuki", "Millia_Rage", "Chipp_Zanuff", "Sol_Badguy", "Ky_Kiske", "May", 
                "Zato-1", "I-No", "Happy_Chaos", "Bedman", "Sin_Kiske", "Baiken", "Anji_Mito", "Leo_Whitefang", "Faust", "Axl_Low", 
                "Potemkin", "Ramlethal_Valentine", "Giovanna", "Goldlewis_Dickinson", "Bridget", "Asuka_R", "Johnny", "Elphelt_Valentine"]

def nameCleaner(char):
    #Takes the user inputed character name and replaces it with a useable character name (hopefully).
    charList = ["Testament", "Jack-O", "Nagoriyuki", "Nago", "Millia", "Millia_Rage", "Chipp", "Chipp_Zanuff", "Sol", "Sol_Badguy", "Ky", "Ky_Kiske", "Kyle", "May", 
                "Zato-1", "I-No", "ino", "Happy", "Chaos", "Happy_Chaos", "Bedman", "Sin", "sin", "Sin_Kiske", "Baiken", "Anji", "Anji_Mito", "Leo", "Leo_Whitefang", "Faust", "Axl", "Axl_Low",
                "Potemkin", "Ramlethal", "Ram", "Ramlethal_Valentine", "Giovanna", "gio", "Gio", "Goldlewis", "Gold", "Goldlewis_Dickinson", "Bridget", "Asuka_R", "Johnny", "Elphelt", "Elphelt_Valentine"]
    #charListLower, char = [x.lower() for x in charList], char.lower()
    char = str(difflib.get_close_matches(char,charList,n=1,cutoff=.3)).replace("['","").replace("']","")
    if char == "Sol":
        char = "Sol_Badguy"
    elif char == "Ky" or char == "Kyle":
        char = "Ky_Kiske"
    elif char == "Happy" or char == "Chaos":
        char = "Happy_Chaos"
    elif char == "Sin" or char == "sin":
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
    elif char == "Gio" or char == "gio":
        char = "Giovanna"
    elif char == "Millia":
        char = "Millia_Rage"
    elif char == "Chipp":
        char = "Chipp_Zanuff"
    elif char == "ino":
        char = "I-No"
    elif char == "Elphelt":
        char = "Elphelt_Valentine"
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
    #print(moveDF["Level"])
    return moveDF, gatlingDF

def update(char):
    data = dataScrape(char)[0]
    data.to_csv("GGST-Frame/RawData-Copy/"+nameCleaner(char)+".txt", sep="/")
    return char +" updated."

def updateAll():
    charList = charListFinal
    for x in charList:
        print(update(x))
    return

def moveLookup(char, move):
    char = nameCleaner(char)
    if move.lower() == "info":
        #Looks up character info
        data = pd.read_csv("GGST-Frame/RawData-Copy/"+"characterData"+".csv", sep=",", index_col=["Character"])
        return char + " info | bd: " + str(data.loc[char,"Backdash"]) + ", j: " + str(data.loc[char,"Prejump"]) + ", eHP: " + str(data.loc[char,"EffectiveHP"]) + " (x" + str(data.loc[char,"DamageMod"]) + ", " +  str(data.loc[char,"Guts"]) + ")"
    elif move == "236D" or move == "236[D]" or move == "236d" or move == "236[d]" or move=="wawa" or move == "WA" or move == "wa":
        if char in ["Sol_Badguy", "Ky_Kiske", "May", "Chipp_Zanuff", "Ramlethal_Valentine", "Leo_Whitefang", "Giovanna", "Anji_Mito", "I-No", "Testament", "Sin_Kiske", "Johnny"]:
            return char + " 236D | s: 16 [28], a: 3, r: 20, ob: -4, oh: -1"
        elif char in ["Potemkin", "Nagoriyuki", "Goldlewis_Dickinson", "Bedman"]:
            return char + " 236D | s: 20 [32], a: 3, r: 20, ob: +7 [+12], oh: nan"
        else:
            return char + " 236D | s: 20 [32], a: 3, r: 20, ob: +12 [+17], oh: nan"
    else:
        #Looks up move data from the raw data.
        data = pd.read_csv("GGST-Frame/RawData-Copy/"+char+".txt", sep="/")
        moveList = data["Input"].to_list()
        moveListLower = [str(x).lower() for x in moveList]
        move = move.lower()
        move = str(difflib.get_close_matches(move,moveListLower,n=1,cutoff=.5)).replace("['","").replace("']","")
        moveIndex = moveListLower.index(move)
        moveData = data[data["Input"]==moveList[moveIndex]]
        return char + " " + str(moveData.loc[moveIndex, "Input"]) + " | s: " + str(moveData.loc[moveIndex, "Startup"]) + ", a: " + str(moveData.loc[moveIndex, "Active"]) + ", r: " + str(moveData.loc[moveIndex, "Recovery"]) + ", ob: " + str(moveData.loc[moveIndex, "On-Block"]) + ", oh: " + str(moveData.loc[moveIndex, "On-Hit"])


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
                moveDF.loc[x]["Cancels"] = moveDF.loc[x]["Cancels"] + "236H P,236H K,236H S,236H H"
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
                moveDF.loc[x]["Cancels"] = moveDF.loc[x]["Cancels"] + "214P 214P,214[P] 214[P]"
            if moveDF.loc[x]["Input"] == "214P 214P":
                moveDF.loc[x]["Cancels"] = moveDF.loc[x]["Cancels"] + "214P 214P 214P"
            if moveDF.loc[x]["Input"] == "214[P] 214[P]":
                moveDF.loc[x]["Cancels"] = moveDF.loc[x]["Cancels"] + "214P 214P 214P"
            if moveDF.loc[x]["Input"] == "214[P] 214[P]" or moveDF.loc[x]["Input"] == "214P 214P" or  moveDF.loc[x]["Input"] == "214P 214P 214P":
                moveDF.loc[x]["Type"] = "Rekka Followup"
    if char == "Nagoriyuki":
        for x in range(len(moveDF["Input"])):
            if moveDF.loc[x]["Input"] in ["5P", "5K", "c.S", "2P", "2K"]:
                moveDF.loc[x]["Cancels"] = moveDF.loc[x]["Cancels"].replace("6H", "6H.1,6H.2,6H.3,6H.BR").replace("f.S","f.S.1,f.S.2,f.S.3,f.S.BR").replace("5H","5H.1,5H.2,5H.3,5H.BR").replace("2S","2S.1,2S.2,2S.3,2S.BR")
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
    if char == "Elphelt_Valentine":
        for x in range(len(moveDF["Input"])):
            #Rekka Starter and Mid Rekka extender
            if moveDF.loc[x]["Input"] == "214S":
                moveDF.loc[x]["Cancels"] = moveDF.loc[x]["Cancels"] + "214S,214S~P,214S~K,214S~H"
                #moveDF.loc[x]["Type"] = "Rekka Followup"
            #First low or high in the chain
            if moveDF.loc[x]["Input"] == "214S~P" or moveDF.loc[x]["Input"] == "214S~K":
                moveDF.loc[x]["Cancels"] = moveDF.loc[x]["Cancels"] + "214S,214S~P/K~P,214S~P/K~K,214S~H"
                moveDF.loc[x]["Type"] = "Rekka Followup"
            #The Rekka enders (2nd high/low or H)
            if moveDF.loc[x]["Input"] == "214S~P/K~P" or moveDF.loc[x]["Input"] == "214S~P/K~K" or moveDF.loc[x]["Input"] == "214S~H":
                moveDF.loc[x]["Type"] = "Rekka Followup"
            if moveDF.loc[x]["Input"] == "5HH":
                moveDF.loc[x]["Type"] = "Rekka Followup"
    if char == "Potemkin":
        for x in range(len(moveDF["Input"])):
            if moveDF.loc[x]["Input"] == "6K":
                moveDF.loc[x]["Cancels"] == "Special, Super"
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
        """
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
        """
    Type = []
    for x in range(len(moves.index)):
        #Second run through on the entire dataframe
        if "~" in str(moves.loc[x, "Startup"]) and "[" in str(moves.loc[x, "Startup"]):
            beforeTilda = moves.loc[x, "Startup"].split("~")[0]
            afterTilda = moves.loc[x, "Startup"].split(" ")[1]
            moves.loc[x, "Startup"] = beforeTilda + afterTilda
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
        #if " " in str(moves.loc[x, "On-Block"]):
        #    moves.loc[x, "On-Block"] = moves.loc[x, "On-Block"].split(" ")[0]
        if "~" in str(moves.loc[x, "On-Block"]):
            moves.loc[x, "On-Block"] = moves.loc[x, "On-Block"].split("~")[0]
        #if "+" in str(moves.loc[x, "On-Block"]):
        #    moves.loc[x, "On-Block"] = moves.loc[x, "On-Block"].split("+")[1]
        if "+" in str(moves.loc[x, "On-Block"]):
            moves.loc[x, "On-Block"] = moves.loc[x, "On-Block"].replace("+","")
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
        #Anji formating
        if str(moves.loc[x, "Level"]) == "223":
            moves.loc[x, "Level"] = "2,2,3"
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
        if moves.loc[x, "Level"] != "" and moves.loc[x, "Level"] != "-":#####################################################################################
            level = moves.loc[x, "Level"].split(".")[0]
            '''
            if moves.loc[x,"Input"] == "236K":
                print(moves.loc[x,"Input"])
                print(moves.loc[x, "Level"])
                print(level)
                print(str(level).replace(" ",""))
            '''
            if "[" in str(level):
                levelBrackets = str(level)[str(level).find("[")+1:str(level).find("]")]
                levelBrackets = level[len(level)-2]
                #print(levelBrackets)
                level = str(level).split("[")[0] + " [" + levelBrackets + "]"
                #print(level)
            if "x" in str(level):
                xIndex = str(level).index("x")
                multiplier = str(level)[xIndex+1]
                baseLevel = str(level)[xIndex-1]
                newLevel = ""
                levelFirstHalf = level.split(baseLevel+"x"+multiplier)[0]
                levelSecondHalf = level.split(baseLevel+"x"+multiplier)[1]
                for w in range(int(multiplier)):
                    newLevel = newLevel + baseLevel + ","
                newLevel = newLevel[:-1]
                level = levelFirstHalf + newLevel + levelSecondHalf
                print(level)
            moves.loc[x, "Level"] = str(level).replace(" ","")
        else: 
            moves.loc[x, "Level"] = ""
    moves["Type"] = Type
    moves = moves.merge(addGatling(gatDF), how="left", on="Input").fillna("")
    moves = moves.drop(["Unnamed: 0", "Damage", "Guard", "Invuln", "Proration", "R.I.S.C. Gain", "R.I.S.C. Loss", "Name", "On-Hit", "Counter Type"], axis=1)
    return moves[moves["Input"]!=""].reset_index(drop=True)

def addWawa(char, df):
    x = len(df["Input"])
    if char in ["Sol_Badguy", "Ky_Kiske", "May", "Chipp_Zanuff", "Ramlethal_Valentine", "Leo_Whitefang", "Giovanna", "Anji_Mito", "I-No", "Testament", "Sin_Kiske", "Johnny", "Elphelt_Valentine"]:
        df.loc[x,:] = ["236D", 16, 3, 20, -4, 4, "Special", "All"]
        df.loc[x+1,:] = ["236[D]", 29, 3, 20, -4, 4, "Special", "All"]
    elif char in ["Potemkin", "Nagoriyuki", "Goldlewis_Dickinson", "Bedman"]:
        df.loc[x,:] = ["236D", 20, 3, 20, 12, 4, "Special", ""] 
        df.loc[x+1,:] = ["236[D]", 32, 3, 20, 17, 4, "Special", ""] 
    else:
        df.loc[x,:] = ["236D", 20, 3, 20, 7, 4, "Special", "All"]
        df.loc[x+1,:] = ["236[D]", 32, 3, 20, 12, 4, "Special", "All"]
    return df

def updateClean(char):
    char = nameCleaner(char)
    data = dataScrape(char)
    df = moveCleaner(data[0], data[1])
    df = addRekkas(char, df)
    df = addWawa(char, df)
    df.to_csv("GGST-Frame/CleanData-Copy/"+nameCleaner(char)+".txt", sep="/")
    return df

def updateCleanAll():
    charList = charListFinal
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
    print(pd.read_csv("GGST-Frame/CleanData-Copy/"+char+".txt", sep="/").fillna("").reset_index(drop=True).drop(["Unnamed: 0"], axis=1).to_string())
    return

def viewDataAll():
    charList = charListFinal
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
    data = pd.read_csv("GGST-Frame/CleanData-Copy/"+char+".txt", sep="/").fillna("").reset_index(drop=True).drop(["Unnamed: 0"], axis=1)
    dataSU = data[data["Startup"]!=""]
    print(dataSU[dataSU["Startup"]>=30])
    dataOB = data[data["On-Block"]!=""]
    print(dataOB[dataOB["On-Block"]<=-20])
    dataLv = data[data["Level"]!=""]
    print(dataLv[dataLv["Level"]>4])
    return

def dataVerficationAll():
    charList = charListFinal
    for x in charList:
        print("---"+x+"--------------------------------------------------------------------------------------------------------------------")
        dataVerification(x)
    return

def valueFormating(value):
    value = str(value)
    valueList = value.replace("]","").replace("{","")
    for y in [",", "[", "{"]:
        valueList = " ".join(valueList.split(y))
    valueList = valueList.split()
    valueFormat = value
    for x in valueList:
        valueFormat = valueFormat.replace(x,"x",1)
    return valueList, valueFormat

def valueFormatingCombiner(format1, format2):
    format2 = format2.replace("x","y")
    for x in range(format1.count("x")):
        format1 = format1.replace("x", format2, 1)
    return format1.replace("y","x")

def frameTrapCalc(char, move1, move2, cancelType, move1OB, move1Lvl, move2Start): 
    #print(cancelType)
    #Splits the needed strings and notes the "type" of split
    if cancelType == "wawa_anything" or cancelType == "ground_jump_cancel" or cancelType == "air_gatling" or cancelType == "ground_gatling" or cancelType == "Rekka Followup":
        move1List = valueFormating(move1Lvl)
        move2List = valueFormating(move2Start)
        #print("case 1")
    else:
        move1List = valueFormating(move1OB)
        move2List = valueFormating(move2Start)
        #print("case 2")
    gapFormat = valueFormatingCombiner(move1List[1], move2List[1])
###############################
#Make this section into a for loop, find a way to reform it at the end
###############################

    #print(gapFormat)
    gapList = []
    for x in move1List[0]:
        for y in move2List[0]:
            x = int(float(x))
            y = int(float(y))  
            #Wawa Check
            if cancelType == "wawa_anything":
                if "j." in move2:
                    if char in ["Nagoriyuki", "Goldlewis_Dickinson", "Potemkin", "Bedman"]:
                        gap = y + 5 - levelHitstun(x)
                    else:
                        gap = y + 4 - levelHitstun(x)
                else:
                    gap = y - levelHitstun(x)
            #Rekka Check
            elif cancelType == "non_rekka_followup":
                #return char + " " + move1 + " > " + move2 + ": " + move2 + " is a follow-up move that cannot be performed after " + move1 + "."
                return move2 + " is a follow-up move and cannot be done after " + move1
            #Ground Gatling 
            elif cancelType == "ground_gatling":
                gap = y - levelHitstun(x) 
            #Ground Non-gatling
            elif cancelType == "ground_non_gatling":
                gap = y - x
            #Ground to Air (Jump cancelable)
            elif cancelType == "ground_jump_cancel":
                if char in ["Nagoriyuki", "Goldlewis_Dickinson", "Potemkin", "Bedman"]:
                    gap = y + 5 - levelHitstun(x)
                else:
                    gap = y + 5 - levelHitstun(x)
            #Ground to Air (Non-jump cancelable)
            elif cancelType == "ground_non_jump_cancel":
                if char in ["Nagoriyuki", "Goldlewis_Dickinson", "Potemkin", "Bedman"]:
                    gap = y + 5 - x
                else:
                    gap = y + 5 - x
            #Air Gatling
            elif cancelType == "air_gatling":
                gap = y - levelHitstun(x)
            #Air non-gatling and Air to Ground
            else:
                #return char.replace("_", " ") + " " + move1 + " > " + move2 + ": " + move1 + " has " + str(levelHitstun(move1Lvl)) + "f of blockstun, while " + move2 + " has " + str(move2Start) + "f of startup. Air move's frame advantage differs based on height of hit, jump arc, recovery and other factors. "
                gap = move1 + " has " + str(levelHitstun(x)) + "f of blockstun, while " + move2 + " has " + str(y) + "f of startup"
            gapList.append(gap)
    for w in gapList:
        gapFormat = gapFormat.replace("x", str(w)+"f", 1).replace(" ", "").replace(",",", ").replace("[", " [")
    return gapFormat

def frameTrap(char, move1, move2):
    char = nameCleaner(char)
    data = pd.read_csv("GGST-Frame/CleanData-Copy/"+char+".txt", sep="/").fillna("").reset_index(drop=True).drop(["Unnamed: 0"], axis=1)
    move1 = inputCleaner(move1, data["Input"])
    move2 = inputCleaner(move2, data["Input"])
    move1Index = data.index[data["Input"]==move1].tolist()[0]
    move1Act, move1Rec, move1OB, move1Lvl = data.loc[move1Index, "Active"], data.loc[move1Index, "Recovery"], data.loc[move1Index, "On-Block"], data.loc[move1Index, "Level"]
    move1Cancel = data.loc[move1Index, "Cancels"].split(",")
    move2Index = data.index[data["Input"]==move2].tolist()[0]
    move2Start, move2Type = data.loc[move2Index, "Startup"], data.loc[move2Index, "Type"]

    if "All" in move1Cancel:
        #Wawa Check
        cancelType = "wawa_anything"
        gap = frameTrapCalc(char, move1, move2, cancelType, move1OB, move1Lvl, move2Start)
    elif move2Type == "Rekka Followup" and move2 not in move1Cancel:
        #Rekka Check
        cancelType = "non_rekka_followup"
        #print(move1Cancel)
        #print(cancelType)
        gap = frameTrapCalc(char, move1, move2, cancelType, move1OB, move1Lvl, move2Start)
    elif (move2 in move1Cancel or move2Type in move1Cancel) and "j." not in move1 and "j." not in move2:
        #Ground Gatling
        cancelType = "ground_gatling"
        if char == "Elphelt_Valentine" and  move1 in ["214S", "214S~P", "214S~K"]:
            gap = int(move2Start) - int(levelHitstun(move1Lvl)) + 2
            gap = str(gap)+"f"
        else:
            gap = frameTrapCalc(char, move1, move2, cancelType, move1OB, move1Lvl, move2Start)
    elif (move2 not in move1Cancel and move2Type not in move1Cancel) and "j." not in move1 and "j." not in move2:
        #Ground non-gatling
        cancelType = "ground_non_gatling"
        gap = frameTrapCalc(char, move1, move2, cancelType, move1OB, move1Lvl, move2Start)
    elif "j." not in move1 and "j." in move2 and "Jump" in move1Cancel:
        #Ground to Air (Jump Cancel)
        cancelType = "ground_jump_cancel"
        gap = frameTrapCalc(char, move1, move2, cancelType, move1OB, move1Lvl, move2Start)
    elif "j." not in move1 and "j." in move2 and "Jump" not in move1Cancel:
        #Ground to Air (Non-jump cancelable)
        cancelType = "ground_non_jump_cancel"
        gap = frameTrapCalc(char, move1, move2, cancelType, move1OB, move1Lvl, move2Start)
    elif "j." in move1 and "j." in move2 and (move2 in move1Cancel or move2Type in move1Cancel):
        #Air Gatling
        cancelType = "air_gatling"
        gap = frameTrapCalc(char, move1, move2, cancelType, move1OB, move1Lvl, move2Start)
    else:
        #Air to ground
        cancelType = "air_to_ground"
        gap = frameTrapCalc(char, move1, move2, cancelType, move1OB, move1Lvl, move2Start)
    
    # move1: Attack level of each hit, 
    # move2: Startup (different variations)


    return gap



def dropDownListGenerator(char):
    data = pd.read_csv("GGST-Frame/CleanData-Copy/"+char+".txt", sep="/").fillna("").reset_index(drop=True).drop(["Unnamed: 0"], axis=1)
    moveList = data["Input"].to_list()
    print("<!-- "+char+" Move List -->")
    print("<select id='" + char + "_List' class='characterHidden'>")
    for x in moveList:
        print("     <option value='" + x + "'>" + x + "</option>")
    print("</select>")
    print("")
    print("<select id='" + char + "_List2' class='characterHidden'>")
    for x in moveList:
        print("     <option value='" + x + "'>" + x + "</option>")
    print("</select>")
    return

def dropDownListGeneratorAll():
    #Make sure to remove hidden from the first list when updating.
    charList =  charListFinal
    original_stdout = sys.stdout
    with open("testDropDown.text", "w") as f:
        sys.stdout = f
        for x in charList:
            dropDownListGenerator(x)
            print("")
        sys.stdout = original_stdout
    return

def frameTrapAll(char):
    df = pd.read_csv("GGST-Frame/CleanData-Copy/"+char+".txt", sep="/").fillna("").reset_index(drop=True).drop(["Unnamed: 0"], axis=1)
    moveList = df["Input"].to_list()
    move1List, move2List, gapList = [], [], []
    for x in moveList:
        #print("current move: " + x)
        for y in moveList: 
            try:
                result = frameTrap(char, x, y)
                move1List.append(x)
                move2List.append(y)
                gapList.append(result)
            except:
                move1List.append(x)
                move2List.append(y)
                gapList.append("N/A")
    gapTable = pd.DataFrame(data={"move1": move1List, "move2": move2List, "gap": gapList})
    gapTable.to_csv("GGST-Frame/GapData-Copy/"+nameCleaner(char)+".txt", sep="/")
    print(char + " gap table is complete.")
    return 

def frameTrapAllCharacters():
    charList =  charListFinal
    for character in charList:
        frameTrapAll(character)
    return

#frameTrapAllCharacters()
#updateCleanAll()

#print(frameTrap("may","cS","2K"))
#dropDownListGeneratorAll()

#print(moveLookup("Asuka","Accipiter"))
#print(moveLookup("gio","5p"))

#updateCleanAll()

#dataScrape("Anji_Mito")


def rawDataVerificationAll():
    charList = charListFinal
    for x in charList:
        print("---" + x + "---")
        data = pd.read_csv("GGST-Frame/RawData-Copy/"+x+".txt", sep="/").fillna("").reset_index(drop=True).drop(["Unnamed: 0"], axis=1)
        print(data["On-Block"])
    return
    


#updateAll()
#updateCleanAll()

#print(frameTrap("pot","6k","214H"))
#frameTrapAllCharacters()
#dropDownListGeneratorAll()
'''
print("2D > 214S: " + frameTrap("Elphelt","2D","214S"))
print("5H > 214S: " + frameTrap("Elphelt","5H","214S"))
print("214S > 214S~P: " + frameTrap("Elphelt","214S","214S~P"))
print("214S > 214S~K: " + frameTrap("Elphelt","214S","214S~K"))
print("214S > 214S: " + frameTrap("Elphelt","214S", "214S"))
print("214S > 214S~H: " + frameTrap("Elphelt","214S", "214S~H"))
print("214S~P > 214S~P/K~P: " + frameTrap("Elphelt","214S~P", "214S~P/K~P"))
print("214S~K > 214S~P/K~P: " + frameTrap("Elphelt","214S~K", "214S~P/K~P"))
print("214S~P > 214S~H: " + frameTrap("Elphelt","214S~P", "214S~H"))
print("214S~K > 214S~H: " + frameTrap("Elphelt","214S~K", "214S~H"))
'''

#print(frameTrap("elphelt","cs","5p"))

