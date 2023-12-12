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

charList =  ["Testament", "Jack-O", "Nagoriyuki", "Millia_Rage", "Chipp_Zanuff", "Sol_Badguy", "Ky_Kiske", "May", 
                "Zato-1", "I-No", "Happy_Chaos", "Bedman", "Sin_Kiske", "Baiken", "Anji_Mito", "Leo_Whitefang", "Faust", "Axl_Low", 
                "Potemkin", "Ramlethal_Valentine", "Giovanna", "Goldlewis_Dickinson", "Bridget", "Asuka_R", "Johnny", "Elphelt_Valentine"]

def nameCleaner(char):
    #Takes the user inputed character name and replaces it with a useable character name (hopefully).
    charList = ["Gran", "Djeeta", "Katalina", "Charlotta", "Lancelot", "Percival", "Ladiva", "Metera", "Lowain",
                "Ferry", "Zeta", "Vaseraga", "Narmaya", "Soriz", "Zooey", "Cagliostro", "Yuel", "Anre",
                "Eustace", "Seox", "Vira", "Beelzebub", "Belial", "Avatar_Belial", "Anila", "Siegfried", "Grimnir", "Nier"]
    #charListLower, char = [x.lower() for x in charList], char.lower()
    char = str(difflib.get_close_matches(char,charList,n=1,cutoff=.3)).replace("['","").replace("']","")
    '''
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
    '''
    return char

def dataScrape(char):
    #scrapes dustloop for the move and gatling tables (still needs cleaning)
    charName = nameCleaner(char)
    url = "https://www.dustloop.com/w/GBVSR/" + charName + "/Frame_Data"
    data = pd.read_html(url)
    moves= []
    for x in data:
        if "input" in x.columns:
            moves.append(x)
    moveDF = pd.concat(moves)
    return moveDF

def update(char):
    try:
        data = dataScrape(char)
        data.to_csv("Granblue-Frame/RawData/"+nameCleaner(char)+".txt", sep="/")
        return char +" updated."
    except:
        return char + " didnt work."

#update("Ladiva")
#update("Metera")

def updateAll():
    charList = ["Gran", "Djeeta", "Katalina", "Charlotta", "Lancelot", "Percival", "Ladiva", "Metera", "Lowain",
                "Ferry", "Zeta", "Vaseraga", "Narmaya", "Soriz", "Zooey", "Cagliostro", "Yuel", "Anre",
                "Eustace", "Seox", "Vira", "Beelzebub", "Belial", "Avatar_Belial", "Anila", "Siegfried", "Grimnir", "Nier"]
    for x in charList:
        print(update(x))
    return

#updateAll()

def moveLookup(char, move):
    char = nameCleaner(char)
    data = pd.read_csv("Granblue-Frame/RawData/"+char+".txt", sep="/")
    moveList = data["input"].to_list()
    moveListLower = [str(x).lower() for x in moveList]
    move = move.lower()
    move = str(difflib.get_close_matches(move,moveListLower,n=1,cutoff=.5)).replace("['","").replace("']","")
    moveIndex = moveListLower.index(move)
    moveData = data[data["input"]==moveList[moveIndex]]
    return char + " " + str(moveData.loc[moveIndex, "input"]) + " | s: " + str(moveData.loc[moveIndex, "startup"]) + ", a: " + str(moveData.loc[moveIndex, "active"]) + ", r: " + str(moveData.loc[moveIndex, "recovery"]) + ", ob: " + str(moveData.loc[moveIndex, "onBlock"]) + ", oh: " + str(moveData.loc[moveIndex, "onHit"])


#print(moveLookup("charlotta","c.xxx"))