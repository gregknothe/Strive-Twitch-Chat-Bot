import matplotlib.pyplot as plt

def subtractList(list1, list2):
    newList = []
    for x in range(len(list1)):
        newList.append(list1[x]-list2[x])
    return newList

def percDelta(list2, deltaList):
    newList = []
    for x in range(len(list2)):
        newList.append(f"{deltaList[x]/list2[x]:.1%}")
    return newList

def highestPoint(list1, list2):
    newList = []
    for x in range(len(list1)):
        newList.append(max(list1[x], list2[x]))
    return newList

Values = [100, 70, 60, 50, 40, 30, 20, 10]
Zero = [1, .97, .92, .89, .84, .76, .66, .56]
One = [1, .96, .91, .87, .82, .73, .63, .53]
Two = [1, .95, .90, .85, .80, .70, .60, .50]
Three = [1, .94, .89, .83, .78, .67, .57, .47]
Four = [1, .93, .88, .81, .76, .64, .53, .44]
Five = [1, .92, .87, .79, .74, .60, .50, .41]

def gutsGraph(char1, dmgMult1, guts1, char2, dmgMult2, guts2):
    char1List = [i * dmgMult1 for i in guts1]
    char2List = [i * dmgMult2 for i in guts2]

    effectiveHP1 = (1/char1List[0]*126) + (1/char1List[1]*42) + (1/char1List[2]*42) + (1/char1List[3]*42) + (1/char1List[4]*42) + (1/char1List[5]*42) + (1/char1List[6]*42) + (1/char1List[7]*42)
    effectiveHP2 = (1/char2List[0]*126) + (1/char2List[1]*42) + (1/char2List[2]*42) + (1/char2List[3]*42) + (1/char2List[4]*42) + (1/char2List[5]*42) + (1/char2List[6]*42) + (1/char2List[7]*42)

    deltaList = subtractList(char1List,char2List)
    percList = percDelta(char2List,deltaList)
    highList= highestPoint(char1List,char2List)

    plt.plot(Values,char1List, linestyle="--", marker="o", label=char1+" [eHP: "+str(round(effectiveHP1))+"]")
    plt.plot(Values,char2List, linestyle="--", marker="o", label=char2+" [eHP: "+str(round(effectiveHP2))+"]")
    plt.xticks(Values, Values)
    plt.xlabel("HP%")
    plt.ylabel("Damage Multiplier")
    for x in range(len(deltaList)):
        plt.text(Values[x]-2.4, highList[x]+.04, round(deltaList[x],3), size=6)
        plt.text(Values[x]-2.5, highList[x]+.02, "("+percList[x]+")", size=6)
    plt.legend()
    plt.show()
    return 

#gutsGraph("Chipp",1.2656, Four, "Millia", 1.1875, Two)
gutsGraph("Anji", 1.0625, Five, "Kyle", 1.0000, Two) 
#gutsGraph("May", 1.0625, Four, "Kyle", 1.0000, Two) 