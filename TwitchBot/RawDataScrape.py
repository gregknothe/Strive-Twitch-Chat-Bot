import pandas as pd
import re

def nameConverter(charName):
    #Converts the user inputed char name into the correct one (with some added named for the funnies)
    charName = charName.lower().replace(" ","")
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
    elif charName == "goldlewis" or charName == "gold":
        return "Goldlewis_Dickinson"
    elif charName == "sin" or charName == "sin_kiske" or charName == "flagboy":
        return "Sin_Kiske"
    else:
        return "This is not a valid character"

def scrapeCharacterData(charName):
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

def gatlingCleaner(gatlingDataFrame):
    #Inputs a raw gatling dataframe and removes the extra text.
    #Also combines all gatling cells into a single string to search through later. 
    buttons = []
    gatlingOptions = []
    for x in gatlingDataFrame["Unnamed: 0"]:
        newValue = x.split("G")
        buttons.append(newValue[0])
        gatlingDataFrame["Unnamed: 0"][x] = newValue[0]
    gatlingDataFrame = gatlingDataFrame.set_index("Unnamed: 0")
    for y in range(len(buttons)):
        gatlingString = str(gatlingDataFrame.iloc[y])
        gatlingString = gatlingString[1:].replace(",","").replace("\nK","").replace("\nS","").replace("\nH","").replace("\nD","").replace("\nCancel","").replace("-","").split("\nName")
        gatlingOptions.append(" ".join(str(gatlingString[0]).split()))
    cleanedDataFrame = pd.DataFrame({"Input": buttons, "gatlingOptions": gatlingOptions})
    cleanedDataFrame = cleanedDataFrame.set_index("Input")
    return cleanedDataFrame

def gatlingTable(groundGatling, airGatling):
    #Combines both ground and air gatling tables together
    dataframes = [gatlingCleaner(groundGatling), gatlingCleaner(airGatling)]
    return pd.concat(dataframes)

def fullTable(charName):
    #Combines all the moves into a single list, then adds on the gatling options to each move that has them. 
    charData = scrapeCharacterData(nameConverter(charName))
    normals, specials, supers, throws, groundGatling, airGatling = charData[0], charData[1], charData[2], charData[3], charData[4], charData[5]   
    fullCommandList = pd.concat([normals, specials, supers, throws])
    fullCommandList["Input"] = fullCommandList["Input"].str.replace(" ","")
    fullCommandList = fullCommandList.set_index("Input")
    gatlings = gatlingTable(groundGatling, airGatling)
    return fullCommandList.merge(gatlings, how="left", on="Input")

def saveRawTable(charName):
    #Pulls and saves the raw dustloop framedata DF to a file in the local RawFrameData folder.
    df = fullTable(charName)
    df = df.drop(columns=['Unnamed: 0', 'R.I.S.C. Gain', 'R.I.S.C Loss'])
    df.to_csv("RawFrameData/"+nameConverter(charName)+".txt", sep="/")
    return

#saveRawTable("sin")
def saveAllCharRawTables():
    #Pulls the data for all chars and saves them
    charList = ["Anji", "Axl", "Baiken", "Bridget", "Chipp", "Faust", "Gio", "Gold", "Happy", "Ino", "Jacko", "Ky", "Leo", "May", "Millia", "Nago", "Pot", "Ram", "Sol", "Test", "Zato", "Sin"]
    for x in charList:
        saveRawTable(x)
    return

#saveAllCharRawTables()
def moveInputCleaner(moveName):
    moveName = moveName.replace(" ","").upper().replace("C","c").replace("F","f").replace("J","j")
    if "c" in moveName and "c." not in moveName:
        moveName = moveName.replace("c","c.")
    if "f" in moveName and "f." not in moveName:
        moveName = moveName.replace("f","f.")
    if "j" in moveName and "j." not in moveName:
        moveName = moveName.replace("j","j.") 
    return moveName

def moveLookup(char='sol',move="5P"):
    #Doesnt work with nagos fucked up notation due to input cleaning fuck that character frfr
    df = fullTable(char)
    df = df.drop(index="Input")
    move = moveInputCleaner(move)
    damage = str(df.loc[move]["Damage"])
    startUp = str(df.loc[move]["Startup"])
    active = str(df.loc[move]["Active"])
    recovery = str(df.loc[move]["Recovery"])
    onBlock = str(df.loc[move]["On-Block"])
    onHit = str(df.loc[move]["On-Hit"])
    level = str(df.loc[move]["Level"])
    invul = str(df.loc[move]["Invuln"])
    shortName = nameConverter(char).split("_")[0]
    output =  shortName+" "+move+" | D:"+damage+" S:"+startUp+" A:"+active+" R:"+recovery+" OB:"+onBlock+" OH:"+onHit+" L:"+level+" I:"+invul
    return output.replace("nan ","- ")

#text = "sin 6K"
#text = text.split(" ",1)
#print(moveLookup(text[0],text[1]))