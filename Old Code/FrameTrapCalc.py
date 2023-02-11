import pandas as pd
import re

def getCharacterData(charName):
    #Return dfs in order: Normals, Specials, Supers, Throws+Misc, GroundGatlings, AirGatlings
    url = "https://www.dustloop.com/w/GGST/" + charName + "/Frame_Data"
    dfs = pd.read_html(url)
    if charName == "Leo_Whitefang":
        return dfs[5:6][0], dfs[6:7][0], dfs[7:8][0], dfs[8:9][0], pd.concat([dfs[9:10][0], dfs[10:11][0]]), dfs[11:12][0]
    elif charName == "Chipp_Zanuff":
        return dfs[4:5][0], dfs[5:6][0], dfs[6:7][0], dfs[7:8][0], pd.concat([dfs[8:9][0], dfs[9:10][0]]), dfs[10:11][0]
    elif charName == "Happy_Chaos":
        return dfs[4:5][0], dfs[5:6][0], dfs[6:7][0], dfs[7:8][0], dfs[12:13][0], dfs[13:14][0]
    elif charName == "Jack-O":
        return dfs[4:5][0], dfs[5:6][0], dfs[6:7][0], dfs[7:8][0], dfs[11:12][0], dfs[12:13][0]
    elif charName == "Testament":
        return dfs[4:5][0], dfs[5:6][0], dfs[6:7][0], dfs[7:8][0], dfs[9:10][0], dfs[10:11][0]
    else:
        return dfs[4:5][0], dfs[5:6][0], dfs[6:7][0], dfs[7:8][0], dfs[8:9][0], dfs[9:10][0]

#leo = getCharacterData("Jack-O")

def gatlingCleaner(gatlingDataFrame):
    #Inputs a raw gatling dataframe and removes the extra text.
    #Also combines all gatling cells into a single string to search through later. 
    #Moves the inputs into the index values for easier stuff later.
    buttons = []
    gatlingOptions = []
    #for x in range(len(gatlingDataFrame["Unnamed: 0"])):
    for x in gatlingDataFrame["Unnamed: 0"]:
        newValue = x.split("G")
        buttons.append(newValue[0])
        gatlingDataFrame["Unnamed: 0"][x] = newValue[0]
    gatlingDataFrame = gatlingDataFrame.set_index("Unnamed: 0")
    #Compresses the gatling options into a single string for easier parsing later on
    for y in range(len(buttons)):
        gatlingString = str(gatlingDataFrame.iloc[y])
        gatlingString = gatlingString[1:].replace(",","").replace("\nK","").replace("\nS","").replace("\nH","").replace("\nD","").replace("\nCancel","").replace("-","").split("\nName")
        gatlingOptions.append(" ".join(str(gatlingString[0]).split()))
    cleanedDataFrame = pd.DataFrame({"Input": buttons, "gatlingOptions": gatlingOptions})
    cleanedDataFrame = cleanedDataFrame.set_index("Input")
    return cleanedDataFrame

def gatlingTable(groundGatling, airGatling):
    #Combines both ground and air gatling tables together, figure what to do with Leo Later
    dataframes = [gatlingCleaner(groundGatling), gatlingCleaner(airGatling)]
    return pd.concat(dataframes)

def cleanInputs(input):
    input = input.replace(" ","")
    return input

def fullTable(normals, specials, supers, throws, groundGatling, airGatling):
    #Combines all the moves into a single list, then adds on the gatling options to each move that has them. 
    fullCommandList = pd.concat([normals, specials, supers, throws])
    #fullCommandList.index = fullCommandList.index.str.replace(" ","")
    #fullCommandList.index = fullCommandList.index.apply(cleanInputs)
    #fullCommandList["Input"] = fullCommandList["Input"].apply(cleanInputs)
    fullCommandList["Input"] = fullCommandList["Input"].str.replace(" ","")
    fullCommandList = fullCommandList.set_index("Input")
    #print(fullCommandList.index)
    gatlings = gatlingTable(groundGatling, airGatling)
    return fullCommandList.merge(gatlings, how="left", on="Input")

def frameTrap(fullTable, move1, move2):
    #Finds the frames inbetween two moves, somewhat fixed for rekka, but there is prob a issue out there
    #since dustloop has all sorts of differnt notations amoungst different characters.
    groundBlock = [9,11,13,16,18]
    move1Level = fullTable.loc[move1,"Level"]
    #move1Level = move1Level.split(" ")[0]
    #move1Level = move1Level.split(",")[0]
    #print(move1Level)
    move1Level = str(move1Level).replace(",", " ")
    #print(move1Level)
    move1Level = move1Level.replace(" ","")
    #print(move1Level)
    if "[" in move1Level:
        move1Level = move1Level.split("[")[0] 
    elif len(move1Level) >= 2:
        move1Level = move1Level[len(move1Level)-1]
        #print(move1Level)
    else:
        move1Level = move1Level[0]
    
    move2StartUp = fullTable.loc[move2,"Startup"]
    move2StartUp = move2StartUp.split(" ")[0]
    move2StartUp = move2StartUp.split("~")[0]
    move1Gatling = fullTable.loc[move1,"gatlingOptions"]
    move1OnBlock = fullTable.loc[move1,"On-Block"]
    if "j." in move1 and "j." not in move2:
        #print("arial move identified")
        return "'s " + str(move1) + " has " + str(groundBlock[int(move1Level)]) + "f of block stun, while " + str(move2) + " has " + str(move2StartUp) + "f of startup. So at best it's a " + str(int(move2StartUp) - groundBlock[int(move1Level)]) + "f gap.", "aerial flag"
    elif "j." in move1 and "j." in move2 and move2 in str(move1Gatling):
        return int(move2StartUp) - groundBlock[int(move1Level)], "(Gatling)"
    elif "j." in move1 and "j." in move2 and move2 not in str(move1Gatling) and len(move2)<=3:
        return "'s " + str(move1) + " and " + str(move2) + " don't gatling and are both aerial moves. So chances are you can't do both before hitting the ground without some air dash nonsense. (I don't want to program that situation in) DansGame", "aerial flag"
    elif "j." in move1 and "j." in move2 and len(move2) >= 4:
        return int(move2StartUp) - groundBlock[int(move1Level)], "(Gatling)"
    move1OnBlock = move1OnBlock.split(" ")[0]
    move1OnBlock = move1OnBlock.split("~")[0]
    if "+" in move2StartUp:
        move2StartUp = int(move2StartUp.split("+")[0]) + int(move2StartUp.split("+")[1])
    if move2 in str(move1Gatling):
        #print("This is a gatling")
        return int(move2StartUp) - groundBlock[int(move1Level)], "(Gatling)"
    elif "Special" in str(move1Gatling) and len(move2) >= 3:
        #print("its a special cancel")
        return int(move2StartUp) - groundBlock[int(move1Level)], "(Gatling)"
    elif move1.split(" ")[0] in move2 and move1 != move2:
        #print("its a rekka")
        return int(move2StartUp) - groundBlock[int(move1Level)], "(Gatling)"
    else:
        #print("not a gatling")
        return (int(move1OnBlock)*-1) + int(move2StartUp), "(Non-Gatling)"

def nameConverter(charName):
    #Converts the user inputed char name into the correct one (with some added named for the funnies)
    charName = charName.lower().replace(" ","")
    #print(charName)
    if charName ==  "anji" or charName == "anjimito" or charName == "anji_mito":
        return "Anji_Mito"
    elif charName == "axl" or charName == "axllow" or charName == "axl_low" or charName == "british":
        return "Axl_Low"
    elif charName == "baiken" or charName == "bacon":
        return "Baiken"   
    elif charName == "bridget" or charName == "brisket" or charName == "bucket" or charName == "bridge":
        return "Bridget"
    elif charName == "chipp" or charName == "crackhead" or charName == "mrpresident" or charName == "chipp_zanuff":
        return "Chipp_Zanuff"   
    elif charName == "faust" or charName == "drbaldhead" or charName == "baldhead":
        return "Faust"
    elif charName == "gio" or charName == "giovanna" or charName == "doglady":
        return "Giovanna"
    elif charName == "goldlewis" or charName == "gold" or charName == "dickinson" or charName == "fatmillia":
        return "Goldlewis_Dickinson"
    elif charName == "happy" or charName == "happychaos" or charName == "chaos" or charName == "gun":
        return "Happy_Chaos"
    elif charName == "ino" or charName == "in-o" or charName == "witch":
        return "I-No"
    elif charName == "jacko" or charName == "jack-o" or charName == "jerryhandler":
        return "Jack-O"
    elif charName == "ky" or charName == "kyle" or charName == "kykiske" or charName == "kylekiske" or charName == "badfather":
        return "Ky_Kiske"
    elif charName == "leo" or charName == "leowhitefang" or charName == "whitefang":
        return "Leo_Whitefang"
    elif charName == "may" or charName == "dolphin" or charName == "cody":
        return "May"
    elif charName == "millia" or charName == "hairlady" or charName == "thingoldlewis" or charName == "millia_rage" or charName == "milliarage":
        return "Millia_Rage"
    elif charName == "nago" or charName == "nagoriyuki" or charName == "hotashi":
        return "Nagoriyuki"
    elif charName == "pot" or charName == "potekmin" or charName == "grappler":
        return "Potemkin"
    elif charName == "ramlethal" or charName == "ramlethalvalentine" or charName == "ramlethal_valentine" or charName == "sq" or charName == "reddito" or charName=='ram' or charName == "Ram":
        return "Ramlethal_Valentine"
    elif charName == "sol" or charName == "solbadguy" or charName == "sol_badguy" or charName == "theflameofcorruption":
        return "Sol_Badguy"
    elif charName == "test" or charName == "testament" or charName == "tophat":
        return "Testament"
    elif charName == "zato" or charName == "zato-1" or charName == "zato1" or charName == "eddie":
        return "Zato-1"
    else:
        return "This is not a valid character"


def frameTrapCalc(charName, move1, move2):
    #The main function, does all the things, very cool.
    df = getCharacterData(nameConverter(charName))
    fulldf = fullTable(df[0], df[1], df[2], df[3], df[4], df[5])
    move1 = move1.replace(" ","").upper().replace("C","c").replace("F","f").replace("J","j")
    move2 = move2.replace(" ","").upper().replace("C","c").replace("F","f").replace("J","j")
    #print(move1 + " " + move2)
    if move1 not in fulldf.index:
        return move1 + " is not a valid move for " + charName
    elif move2 not in fulldf.index:
        return move2 + " is not a valid move for " + charName 
    frame = frameTrap(fulldf, move1, move2)
    name = nameConverter(charName).split("_")
    if frame[1] == "aerial flag":
        return name[0] + frame[0]
    return name[0] + "'s " + move1 + " > " + move2 + " has a " + str(frame[0]) + "f gap. " + frame[1]

def dustloop(charName):
    officalCharName = nameConverter(charName)
    if officalCharName == "This is not a valid character":
        return "This is not a valid character. DansGame"
    else:
        return "https://www.dustloop.com/w/GGST/" + officalCharName + "/Frame_Data"

def charMoveList(charName):
    officalCharName = nameConverter(charName)
    if officalCharName == "This is not a valid character":
        return "This is not a valid character. DansGame" 
    else:
        df = getCharacterData(officalCharName)
        fulldf = fullTable(df[0], df[1], df[2], df[3], df[4], df[5])
        moveList = str(fulldf.index.tolist())
        if len(moveList) >= 450:
            return moveList[:450] + "... (to long for twitch chat) NotLikeThis"
        else:
            return moveList
        
    

#print(charMoveList("gsdfgsd"))
#print(frameTrapCalc("sol", "j.k", "j.236k"))
#print(frameTrapCalc("sol", "2k", "2d"))
#print(frameTrapCalc("sol", "5k", "j.S"))
#print(frameTrapCalc("anji", "2k", "6h"))
#print(frameTrapCalc("chipp", "236S236S", "236S236k"))
#print(frameTrapCalc("ram","2K","2D"))
#print(frameTrapCalc("may", "2k", "6H"))
#print(frameTrapCalc("drbaldhead","5h","41236K"))
#print(charMoveList("nago"))
#print(frameTrapCalc("sol","236K","236KK"))
#print(frameTrapCalc("kyle","6H", "236H"))
#print(frameTrapCalc("ky","5p","6H"))