import pandas as pd
import re
import urllib.request
import difflib

def nameCleaner(char):
    charList = ["Blanka", "Cammy", "Chun-Li", "Dee_Jay", "Dhalsim", "E.Honda", "Guile", "Jamie", "JP", "Juri", "Ken", "Kimberly", "Lily", "Luke", "Manon", "Marisa", "Ryu", "Zangief"]
    char = str(difflib.get_close_matches(char,charList,n=1,cutoff=.3)).replace("['","").replace("']","")
    return char

def scrapeFrameData(charName):
    charName = nameCleaner(charName)
    url = "https://wiki.supercombo.gg/w/Street_Fighter_6/" + charName + "/Frame_data"
    page=urllib.request.Request(url,headers={'User-Agent': 'Mozilla/5.0'}) 
    infile=urllib.request.urlopen(page).read()
    data = pd.read_html(infile.decode('ISO-8859-1'))
    data = pd.concat([data[1], data[3], data[4], data[5], data[7]])
    data = data[data["input"]!="input"]
    data = data.set_index("input")
    data = data[~data.index.duplicated(keep='first')]
    data.to_csv("SF6Data/"+charName+".txt", sep="/")
    print(charName + " framedata saved.")
    return

def SF6FrameData(char, move):
    move = move.upper()
    char = nameCleaner(char)
    pd.set_option('display.max_colwidth', None)
    df = pd.read_csv("SF6Data/"+char+".txt", sep="/")
    fd = df[df["input"]==move]
    text = char + " " + move + " | s: " + fd["startup"] + ", a: " + fd["active"] + ", r: " + fd["recovery"] + ", oh: " + fd["hitAdv"] + ", ob: " + fd["blockAdv"] + ", c: " + fd["cancel"]
    text = str(text).replace("input","").replace("dtype: object","").replace("\n","")
    return text.split(" ",1)[1]

'''
charList = ["Blanka", "Cammy", "Chun-Li", "Dee_Jay", "Dhalsim", "E.Honda", "Guile", "Jamie", "JP", "Juri", "Ken", "Kimberly", "Lily", "Luke", "Manon", "Marisa", "Ryu", "Zangief"]
for x in charList:
    scrapeFrameData(x)
'''

print(SF6FrameData("jamie", "5lp"))
#print(SF6FrameData("lily", "5lk"))
