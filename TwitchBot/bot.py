from twitchio.ext import commands
from twitchio.client import Client
import FrameTrapV2 as fc
import OhHeyStreamer as ohs
import RawDataScrape as rds
import SinFoodRoll as sfr
import random
import os
import sys
sys.path.insert(0, 'TournamentData')
import StartGGDataScraper as sgg

#sys.path.append("/TournamentData/")
#from StartGGDataScraper import *


'''
import imp
module = imp.load_module('TournamentData.StartGGDataScraper.py')
module.function()
'''



modList = ["lastcody","greedx___","asome26","kyluneena","abusywizard"]

bot = commands.Bot(
    token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=["lastcody", "vera_caelestis"]
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
            reply = fc.frameTrapCalc(userInputs[0], moves[0].rstrip().lstrip(), moves[1].rstrip().lstrip())
        except:
            reply = "Nope. Get owned, nerd. (!ft format/faq or !movelist [char]) OSFrog"
        await ctx.send(reply)

@bot.command(name="movelist")
async def movelist(ctx, *, text):
    await ctx.send(fc.charMoveList(text))

heyUserList = []

@bot.command(name="hey")
async def hey(ctx):
    if ctx.author.name in heyUserList:
        print(str(ctx.author.name) + " attempted an extra !hey.")
    else:
        if ctx.author.name == "life_jam":
           await ctx.send(ohs.ohHeyStreamer().replace("Oh hey,","Hey alright,"))
        heyUserList.append(ctx.author.name)
        print(heyUserList)
        await ctx.send(ohs.ohHeyStreamer())

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

@bot.command(name="playerdata")
async def playerdata(ctx, *, text):
    await ctx.send(sgg.playerRecordBotCommand(text, "TournamentData/TNS/TNSSets.txt"))

'''
lineCount = [0]
@bot.command(name="misery")
async def misery(ctx):
    line = ohs.ohTheMisery(lineCount[0])
    lineCount.append(lineCount[0]+1)
    lineCount.remove(lineCount[0])
    await ctx.send(line)

#Enable for new char launches 

@bot.command(name="sin")
async def dustloop(ctx, *, text):
    try:
        print(text)
        await ctx.send(rds.moveLookup("sin", text))
    except:
        await ctx.send("Nope. Get owned, nerd. (Something went wrong)")


@bot.command(name="feedsin")
async def feedSin(ctx):
    await ctx.send(sfr.SinFoodRoll())
'''

if __name__ == "__main__":
    bot.run()

