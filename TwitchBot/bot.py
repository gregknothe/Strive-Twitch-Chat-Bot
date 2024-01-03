from twitchio.ext import commands
from twitchio.client import Client
import FrameTrapV2 as fc
import OhHeyStreamer as ohs
import RawDataScrape as rds
import SF6FrameData as SF6
import SinFoodRoll as sfr
import random
import os
import sys
import time
sys.path.insert(0, 'TournamentData')
import StartGGDataScraper as sgg
sys.path.insert(0, 'GGST-Frame')
import GGSTFrameData as ggst
sys.path.insert(0, 'Granblue-Frame')
import GBFrameData as gb
import datetime

modList = ["lastclaire","greedx___","asome26","kyluneena","montepremia"]

bot = commands.Bot(
    token=os.environ['TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=["lastclaire", "montepremia", "bloopybloopz", "frendweeb"]
)
        
@bot.command(name="ft")
async def test(ctx, *, text):
    if text == "format" or text == "Format":
        await ctx.send("Input Format: !ft [character name] [move 1] > [move 2]")
    elif text == "faq" or text == "FAQ" or text == "info" or text == "help":
        await ctx.send("The bot isnt perfect, it does not take into account distance or hitboxes. (Ex: May 6H has a startup of 16f, but doesnt hit most characters till frame 19. So depending on the character you might need to add +3f)")
    elif text == "credit" or text == "author":
        await ctx.send("This bot was made by Asome26. Also thank you DustLoop for supplying the raw data (and for being amazing). :)")
    elif text == "commands":
        await ctx.send("!ft [char] [move1] > [move2], !movelist [char], !dustloop [char], !hey (once per stream), !raffle (mods only)")
    else:
        try:
            userInputs = text.split(" ",1)
            moves = userInputs[1].split(">")
            print(userInputs[0], moves) 
            reply = ggst.frameTrap(userInputs[0], moves[0].rstrip().lstrip(), moves[1].rstrip().lstrip())
        except:
            reply = "Nope. Get owned, nerd. (!ft format/faq or !movelist [char]) OSFrog"
        await ctx.send(reply)

@bot.command(name="movelist")
async def movelist(ctx, *, text):
    await ctx.send(fc.charMoveList(text))

@bot.command(name="gg")
async def gg(ctx, *, text):
    await ctx.send(ggst.moveLookup(text.split(" ",1)[0], text.split(" ",1)[1]))

@bot.command(name="gb")
async def granblue(ctx, *, text):
    await ctx.send(gb.moveLookup(text.split(" ",1)[0], text.split(" ",1)[1]))

heyUserList = []
dailydoubleflag = 0 


@commands.cooldown(rate=1, per=1, bucket=commands.Bucket.channel)
#@commands.command()

@bot.command(name="hey")
async def hey(ctx: commands.Context):
    if ctx.author.name in heyUserList:
        print(str(ctx.author.name) + " attempted an extra !hey.")
        return
    else:
        if ctx.author.name == "life_jam":
           await ctx.send(ohs.ohRanceStreamer())
        heyUserList.append(ctx.author.name)
        print(heyUserList)
        dailydoublevalue = random.randint(1,10)
        global dailydoubleflag
        if dailydoublevalue == 6 and dailydoubleflag == 0:
            heyUserList.remove(ctx.author.name)
            await ctx.send(ohs.ohHeyStreamer()+ " You got the Daily Double! PogBones")
            dailydoubleflag = 1
        else:
            await ctx.send(ohs.ohHeyStreamer())
        return

@bot.command(name="hr")
async def heyRemove(ctx, *, text):
    if ctx.author.name in modList:
        try:
            text = text.lower()
            if text in heyUserList:
                heyUserList.remove(text)
                await ctx.send(text+" has been successfully removed.")
        except:
            await ctx.send("Something went wrong. NotLikeThis")

#idk why but sometimes this causes crashes?
@bot.command(name="heycount")
async def heycount(ctx):
    await ctx.send(ohs.heyLen())

@bot.command(name="goodbye")
async def botoff(ctx):
    if ctx.author.name == "asome26":
        ohs.saveGameList()
        await ctx.send("Goodbye. :)")
        exit()

@bot.command(name="raffle")
async def raffle(ctx):
    if ctx.author.name in modList:
        viewerList = list(ctx.chatters)
        for x in range(len(viewerList)):
            viewerList[x] = str(viewerList[x]).split("name: ",1)[1].split(",",1)[0]
        viewerName = str(random.choice(viewerList))
        print("Raffle: " + str(viewerList))
        await ctx.send("Raffle Winner: " + str(viewerName))
    else:
        return

@bot.command(name="dustloop")
async def dustloop(ctx, *, text):
    await ctx.send(fc.dustloop(text))

@bot.command(name="secretkliff")
async def kliff(ctx):
    if ctx.author.name == "asome26":
        await ctx.send("Not only is Kliff the best parent in all GG Lore, but he is also the coolest and funniest character not currently in GGST. That is why I am here today to announce that Kliff will be the next DLC character for Strive (according to inside sources, trust me frfr). PogChamp")
        return
    else:
        return

@bot.command(name="sf")
async def dustloop(ctx, *, text):
    userInputs = text.split(" ",1)
    if userInputs[0] == "update":
        SF6.scrapeFrameData(userInputs[1])
        await ctx.send(userInputs[1]+" has been updated.")
    else:    
        try:
            await ctx.send(SF6.SF6FrameData(userInputs[0], userInputs[1]))
        except:
            await ctx.send("Nope. Get owned, nerd. (Something went wrong)")

@bot.command(name="granblue")
async def granblue(ctx):
    present = datetime.datetime.now()
    future = datetime.datetime(2023, 12, 13, 21, 0, 0)
    difference = future - present
    diff = str(difference)
    days = diff.split(", ")[0]
    time = diff.split(", ")[1].split(":")
    await ctx.send(days + ", " + time[0] + " hours, " + time[1] + " min, " + str(round(float(time[2]))) + " sec")

@bot.command(name="richpeoplegranblue")
async def granblue(ctx):
    present = datetime.datetime.now()
    future = datetime.datetime(2023, 12, 10, 21, 0, 0)
    difference = future - present
    diff = str(difference)
    days = diff.split(", ")[0]
    time = diff.split(", ")[1].split(":")
    await ctx.send(days + ", " + time[0] + " hours, " + time[1] + " min, " + str(round(float(time[2]))) + " sec")

fortniteFlag = 0
@bot.command(name="fortnite")
async def fortnite(ctx):
    global fortniteFlag
    if fortniteFlag == 0:
        fortniteFlag = 1
        await ctx.send("🚨Attention🚨ALL FORTNITE GAMERS 🎮🎮🎮, John Wake is in great danger🆘, and he needs YOUR help to wipe out 💀 all the squads in THe tilted towers 🏢🏢🏢. To do this, he needs a gold SCAR 🔫 and a couple of chug-jugs🍺🍺. To help him, all he needs is your credit card number 💳 , and the three numbers on the back 3️⃣ and the expiration month and date 📅. But you gotta be quick ⚡so that John can secure the bag 💰, and achieve the epic victory R O Y AL")

peterFlag = 0
@bot.command(name="peter")
async def fortnite(ctx):
    global peterFlag
    if peterFlag == 0:
        peterFlag = 1
        await ctx.send("Holy Crap, Im in fortnite! oh my gosh, this is so friggin epic, angellic sound holy crap, donald trump? hello peter. Weclome to Fontnite.")


#print(ohs.ohRanceStreamer())
#print(ohs.ohRanceStreamer())
#print(ohs.ohRanceStreamer())
#print(ohs.ohRanceStreamer())
#print(ohs.ohHeyStreamer())

if __name__ == "__main__":
    bot.run()

'''
Unused Commands - Good chance they need some touching up to work.

lineCount = [0]
@bot.command(name="misery")
async def misery(ctx):
    line = ohs.ohTheMisery(lineCount[0])
    lineCount.append(lineCount[0]+1)
    lineCount.remove(lineCount[0])
    await ctx.send(line)

@bot.command(name="feedsin")
async def feedSin(ctx):
    await ctx.send(sfr.SinFoodRoll())

@bot.command(name="playerdata")
async def playerdata(ctx, *, text):
    await ctx.send(sgg.playerRecordBotCommand(text, "TournamentData/TNS/TNSSets.txt"))
'''