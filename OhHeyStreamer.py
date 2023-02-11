import pandas as pd
import random

#---Old Code------------------------------------------------------------------------------------------------
'''
gamefile = open("MiscData/gameList_old.txt","r")
rawGameFile = gamefile.read()
gamefile.close()
gameList = rawGameFile.split(",")

def ohHeyStreamer():
    game = random.choice(gameList)
    return "Oh hey, it's my favorite" + game + " streamer."
'''

#--List Collection------------------------------------------------------------------------------------------
#n64, gc, wii, gbc, gba, ds
#ps1, ps2
"""
data = pd.read_csv("GamesList/ps2.csv")
titles = data["title"].values.tolist()
for x in range(len(titles)):
    titles[x] = titles[x].split("\r\n")[0].replace(" NA, PAL","").replace(" NA","").replace(" DE","").replace(" JP","").replace(" PAL","").replace(" EU","")
#print(titles)
dates = data["date"].values.tolist()
for x in range(len(dates)):
    newDates = str(dates[x]).split(" (")[0]
    newDates = newDates.split("-")[0]
    if "," in newDates:
        dates[x] = newDates[-4:]
    else:
        dates[x] = newDates
#print(dates)
console = []
for x in range(len(titles)):
    console.append("PS2")
#print(console)
d = {"title": titles, "date": dates, "console": console}
df = pd.DataFrame(data=d)
#print(df)

df.to_csv("GamesListRaw/ps2.csv")

df = pd.read_csv("gameList.csv")
df.drop(df.loc[df["date"]=="Unreleased"].index, inplace=True)
df.to_csv("GamesListRaw/gameList.csv")
"""
#---------------------------------------------------------------------------------------------------------

df = pd.read_csv("MiscData/gameList.csv")

def heyLen():
    return "There are " + str(len(df["title"])) + " remaining games."

dropValues = []
def ohHeyStreamer():
    jackpot = random.randint(1,10000)
    if jackpot == 69:
        return "@Lastcody it is mandated by law that you play Ultimate Chicken Horse today. If you refuse, then the bot will self destruct, destroying all the games and killing Mr Sever in the process. Please do not disapoint the great Bot the Woz."
    if jackpot == 333:
        return "Oh hey, it's my favorite 'The Legend of Heroes: Kuro no Kiseki' (Originally planned to come out on the PS2 in 2002) streamer." 
    values = df.sample()
    title = str(values["title"].values).replace("[","").replace("]","")
    date = str(values["date"].values).replace("[","").replace("]","").replace("'","")
    console = str(values["console"].values).replace("[","").replace("]","").replace("'","")
    #df.drop(index=values.index.values, axis=0)
    dropValues.append(values.index.values)
    return "Oh hey, it's my favorite " + title[1:-1] + " (" + console + " " + date + ") streamer."

def saveGameList():
    for x in dropValues:
        print(x)
        try:
            df.drop(index=x, axis=0, inplace=True)
        except:
            print("Duplicate found")
    df.to_csv("MiscData/gameList.csv",index=False)
    print("Game Removal Finsihed")
    return