import pandas as pd
import RawDataScrape as rds
import re


def openCharFile(charName):
    df = pd.read_csv("FrameData/"+rds.nameConverter(charName)+".txt", sep="/")
    return df.set_index("Input")

def gapConverter(frameTrap):
    if int(frameTrap)<=0:
        frameTrap = int(frameTrap) * -1
        return "no gap (+"+str(frameTrap)+"f)"
    else:
        return str(frameTrap)+"f gap"

#move1 = move1.replace(" ","").upper().replace("C","c").replace("F","f").replace("J","j")

def moveInputCleaner(moveName):
    moveName = moveName.replace(" ","").upper().replace("C","c").replace("F","f").replace("J","j")
    if "c" in moveName and "c." not in moveName:
        moveName = moveName.replace("c","c.")
    if "f" in moveName and "f." not in moveName:
        moveName = moveName.replace("f","f.")
    if "j" in moveName and "j." not in moveName:
        moveName = moveName.replace("j","j.") 
    return moveName

def moveCleaner(moveName):
    moveName = moveName.replace(" ","")
    if "(" in moveName:
        nameParts = moveName.split("(")
        return moveInputCleaner(nameParts[0])+"("+nameParts[1]
    else:
        return moveInputCleaner(moveName)

def frameTrapCalc(charName, move1, move2):
    displayName = rds.nameConverter(charName).split("_")[0]
    df = openCharFile(charName)
    move1 = moveCleaner(move1)
    move2 = moveCleaner(move2)
    #print(move1)
    #print(move2)
    #print(df)
    groundBlock = [9,11,13,16,18]
    try:
        move1Level = int(df.loc[move1,"Level"])
    except:
        return displayName+"'s "+move1+" does not have blockstun value, so this calculation could not be done."
    move2StartUp = int(df.loc[move2,"Startup"])
    move1Gatling = str(df.loc[move1,"gatlingOptions"]).split(" ")
    move2Name = str(df.loc[move2,"Name"])
    #print("move2Name = "+ str(move2Name))
    if "Special" in move1Gatling and move2Name != "nan":
        #adds special/super move to gatling list if "special" or "super" are in the list
        move1Gatling.append(df[df["Name"]==move2Name].index.values.astype(str)[0])
    #print(move1Gatling)
    move1BlockStun = groundBlock[move1Level]
    if "j." in move1 and "j." not in move2: 
        #aerial > ground
        gap = str(move2StartUp - move1BlockStun)
        print("Air>Ground")
        return displayName+"'s "+move1+" > "+move2+": "+gapConverter(gap)+" (assuming "+move1+" is done at the lowest possible height)."
    elif "j." in move1 and "j." in move2 and move2 in move1Gatling:
        #aerial > aerial (gatling)
        print("Air>Air(Gatling)")
        gap = str(move2StartUp - move1BlockStun)
        return displayName+"'s "+move1+" > "+move2+": "+gapConverter(gap)+"."
    elif "j." in move1 and "j." in move2 and move2 not in move1Gatling:
        #aerial > aerial (non gatling)
        print("Air>Air(NonGatling")
        return "These are non-gatling/cancelable aerial moves. Chances are it is not possible to do both before hitting the ground."
    elif "j." not in move1 and "j." in move2:
        #ground > aerial
        if displayName == "Nagoriyuki" or displayName == "Goldlewis" or displayName == "Potemkin":
            preJump = 5
        else:
            preJump = 4
        if "Jump" in move1Gatling:
            print("grond>air(jump cancelable)")
            gap = str(move2StartUp - move1BlockStun + preJump)
            return displayName+"'s "+move1+" > "+move2+": "+gapConverter(gap)+" (assuming "+move2+" hits after jumping)."   
        else:
            print("ground>air(not jump cancelable)")
            move1OB = str(df.loc[move1,"On-Block"]).replace("+","").split(".")[0]
            gap = str(move2StartUp - int(move1OB) + preJump)
            return displayName+"'s "+move1+" > "+move2+": "+gapConverter(gap)+" (assuming "+move2+" hits after jumping)." 
    elif "j." not in move1 and "j." not in move2 and move2 not in move1Gatling:
        #ground > ground (non gatling)
        print("ground>ground(nongatling)")
        move1OB = str(df.loc[move1,"On-Block"]).replace("+","").split(".")[0]
        if move1OB == "nan":
            return displayName+"'s "+move1+" does not have a OB value, so this calculation could not be done."
        #print(int(move1OB))
        gap = str(move2StartUp - int(move1OB))
        return displayName+"'s "+move1+" > "+move2+": "+gapConverter(gap)+"."
    else:
        #ground>ground(gatling)
        print("ground > ground (gatling)")
        gap = str(move2StartUp - move1BlockStun)
        return  displayName+"'s "+move1+" > "+move2+": "+gapConverter(gap)+"."

def dustloop(charName):
    officalCharName = rds.nameConverter(charName)
    if officalCharName == "This is not a valid character":
        return "This is not a valid character. DansGame"
    else:
        return "https://www.dustloop.com/w/GGST/" + officalCharName + "/Frame_Data"

def charMoveList(charName):
    officalCharName = charName
    if officalCharName == "This is not a valid character":
        return "This is not a valid character. DansGame" 
    else:
        df = openCharFile(officalCharName)
        moveList = str(df.index.tolist()).replace("'","").replace(",","")[1:-1]
        if len(moveList) >= 497:
            return moveList[:497] + "..."
        else:
            return moveList

#print(charMoveList("ram"))

#To do:
#test differnt characters and stuff
#delete unneeded moves (like HC conc super)
#rename x.# variables to something more meaningful
#impliment it into the bots code
#char = "may"
#print(openCharFile(char)[["Startup","On-Block","Level","Name","gatlingOptions"]])
#print(frameTrapCalc(char, "C.s","6h"))
#print(frameTrapCalc("axl", "c.S", "2369H"))

#print(charMoveList("gold"))
print(frameTrapCalc("may", "5K", "6H"))
#$print(charMoveList("gold"))