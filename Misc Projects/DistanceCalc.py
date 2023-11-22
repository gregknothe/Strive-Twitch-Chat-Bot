import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
sys.path.insert(0,"TwitchBot/")
import RawDataScrape as rds


df = pd.read_csv("MiscData/dashSpeed.csv")
df = df.set_index("char")
allChars = ["Anji", "Axl", "Baiken", "Bridget", "Chipp", "Faust", "Gold", "Happy", "Jacko", "Ky", "May", "Millia", "Ram", "Sol", "Test", "Zato","Sin"]

def distanceCalc(char="Sol",frames=60):
    char = rds.nameConverter(char)
    dashSpeed = float(df.loc[char,"dashSpeed"])
    dashAccel = float(df.loc[char,"dashAccel"])
    friction = float(df.loc[char,"friction"])
    distance = 0
    distanceList = []
    speedList = []
    for x in range(frames):
        distance = distance + dashSpeed
        speedList.append(dashSpeed)
        distanceList.append(distance)
        dashSpeed = dashSpeed + dashAccel - (dashSpeed / friction)
        if dashSpeed > 38.5:
            dashSpeed = 38.5
    return distanceList, speedList

def distanceGraph(chars=["Sol","Ky","May"], frames=60):
    xValue = range(frames)
    ax = plt.subplot(111)
    for x in chars:
        distance = distanceCalc(x, frames)[0]
        ax.plot(xValue,distance)
        ax.text(frames,distance[frames-1],x+" ("+str(round(distance[frames-1]))+")")
    ax.set_xlabel("Frame")
    ax.set_ylabel("Distance Traveled")
    ax.spines.right.set_visible(False)
    ax.spines.top.set_visible(False)
    ax.legend(chars, loc="upper left")
    plt.show()
    return

def distanceChart(chars=["Sol","Ky","May"], frames=60):
    xValue = range(frames)
    distanceList = []
    for x in chars:
        distance = distanceCalc(x, frames)[0]
        distanceList.append(round(distance[frames-1]))
    df = pd.DataFrame(data={"char": chars, "distance": distanceList})
    df = df.set_index("char").sort_values(by=["distance"], ascending=False)
    mid = round(len(chars)/2)
    medianDistance = df.iloc[mid]["distance"]
    distancePerc = []
    for x in range(len(chars)):
        distancePerc.append(round(df.iloc[x]["distance"] / medianDistance,2))
    df["distPerc"] = distancePerc
    return df

#It takes sol ~55f to run full screen, so by my calc full screen is about 1230 units.
#So half screen would be like 615, most cS proximity range is about 270 units.
#It takes test ~24f to run into the opponent at round start, so RS is about 380 units.
#So pokes like May 2S or Kyle 2S will also be about 380 units.

def frameChart(chars=["Sol","Ky","May"], distance=1230, maxFrames=120):
    frameList = []
    for x in chars:
        distanceList = distanceCalc(x, maxFrames)[0]
        for x in range(len(distanceList)):
            if distanceList[x] >= distance:
                frameList.append(x)
                break
    df = pd.DataFrame(data={"char": chars, "frame": frameList})
    df = df.set_index("char").sort_values(by=["frame"])
    framePerc = []
    mid = round(len(chars)/2)
    medianFrame = df.iloc[mid]["frame"]
    for x in range(len(chars)):
        framePerc.append(round(medianFrame/df.iloc[x]["frame"],2))
    df["framePerc"] = framePerc
    return df


def rangeChart(chars, ranges):
    df = frameChart(chars,ranges[0])
    ranges.pop(0)
    print(ranges)
    for x in ranges:
        y = frameChart(chars, x).rename(index={1: ""})
        print(y)
    return


#distanceGraph(["Ky","Ram", "May"],20)
print(distanceChart(allChars,10))