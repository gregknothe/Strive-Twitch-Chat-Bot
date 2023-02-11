import pandas as pd
import RawDataScrape as rds
import numpy as np
import re
from datetime import date



chars = ["SO","KY","MA","AX","CH","PO","FA","MI","ZA","RA","LE","NA","GI","AN","IN","GO","JC","HA","BA","TE","BI","SI"]

def getRatings(char="SO"):
    df = pd.read_html("http://ratingupdate.info/top/"+char)[0]
    BaseRating = []
    for x in range(len(df["Rating"])):
        BaseRating.append(int(str(df["Rating"][x].split(" ")[0])))
    return BaseRating

def getValues(char="SO",breakpoints=[2200,2100,2000,1900,1800]):
    ratings = getRatings(char)
    values = [char]
    for x in breakpoints:
        values.append(len([i for i in ratings if i > x]))
    return values

def createTable(chars=["SO","KY","MA"], breakpoints=[2200,2100,2000,1900,1800]):
    df = pd.DataFrame(columns=["char"]+breakpoints)
    for x in chars:
        #print(x)
        values = getValues(x,breakpoints)
        df.loc[len(df.index)] = values
    return df.set_index("char")

def saveTable(chars=["SO","KY","MA"], breakpoints=[2200,2100,2000,1900,1800]):
    df = createTable(chars, breakpoints)
    print(df)
    df.to_csv("MiscData/RatingUpdate/"+str(date.today())+".txt", sep=",")
    return

saveTable(chars)