import pandas as pd
import re
import urllib.request
import difflib

def nameCleaner(char):
    #Takes the user inputed character name and replaces it with a useable character name (hopefully).
    charList = ["Testament", "Jack-O", "Nagoriyuki", "Nago", "Millia", "Chipp", "Sol", "Ky", "Kyle", "May", 
                "Zato-1", "I-No", "Happy", "Chaos", "Bedman", "Sin", "Baiken", "Anji", "Leo", "Faust", "Axl", 
                "Potemkin", "Ramlethal", "Ram", "Giovanna", "Gio", "Goldlewis", "Gold", "Bridget", "Asuka_R"]
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

def bracketSplitter(moveRow):
    #Splits held moves (noted by "[]") into two seperate entries in the dataframe. WIP
    split = pd.concat([moveRow, moveRow])

    return split

def moveCleaner(moveDF):
    #Cleans the move dataframe to make it more usable down the line
    #ex: Deals with held moves
    moves = moveDF[moveDF.Input != "Input"].reset_index(drop=True)
    for x in range(len(moves.index)):
        if "[" in moves["Startup"][x]:
            print(moves["Input"][x])
    return moves

x = moveCleaner(dataScrape("may")[0])
print(bracketSplitter(x[x.index==18]))
