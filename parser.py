import pandas as pd
import numpy as np
import json


def rpHelper(data):

    rushdat = data[(data["IsRush"]==1) & (data["IsPenaltyAccepted"]==0)]
    rdir = pd.unique(rushdat["RushDirection"].dropna())
    rdat = {"total":len(rushdat),"avg": round(rushdat["Yards"].mean(),3)}
    for j in rdir:
        info = rushdat[rushdat["RushDirection"]==j]
        rdat[j + "plays"] = len(info)
        rdat[j + "avg"] = round(info["Yards"].mean(),3)
    
    pasdat = data[(data["IsPass"]==1) & (data["IsPenaltyAccepted"]==0)]
    pdir = pd.unique(pasdat["PassType"].dropna())
    pdat = {"total":len(pasdat),"avg": round(pasdat["Yards"].mean(),3)}
    for j in pdir:
        info = pasdat[pasdat["PassType"]==j]
        pdat[j + "plays"] = len(info)
        pdat[j + "avg"] = round(info["Yards"].mean(),3)
    
    out = {"rush":rdat,"pass":pdat}
    return out

def rankHelper(data):
    for i in data["teams"]:
        print(i["off"]["norm"]["rush"]["total"])

"""{
      "team": "LV",
      "off": {
        "norm": {
          "rush": {
            "total": 342,
            "avg": 4.684,"""


def run():
    data = pd.read_csv("data/pbp-2020.csv")
    teams = pd.unique(data["OffenseTeam"].dropna())
    output = {"year":2020}
    teamsarray = []
    for i in teams:
        teaminfo = {"team":i}
        #print(i)
        odata = data[data["OffenseTeam"]==i]
        ored = odata[(odata["YardLine"]>=80) & (odata["YardLine"]!=100)]
        ored = rpHelper(ored)


        onorm = odata[(odata["YardLine"]==100)|((odata["YardLine"]>=10)&(odata["YardLine"]<80))]
        onorm = rpHelper(onorm)
        offense = {"norm": onorm,"red":ored}

        ddata = data[data["DefenseTeam"]==i]
        dred = ddata[(ddata["YardLine"]>=80) & (ddata["YardLine"]!=100)]
        dred = rpHelper(dred)

        dnorm = ddata[(ddata["YardLine"]==100)|((ddata["YardLine"]>=10)&(ddata["YardLine"]<80))]
        dnorm = rpHelper(dnorm)
        defense = {"norm": dnorm,"red":dred}

        teaminfo["off"] = offense
        teaminfo["def"] = defense

        teamsarray.append(teaminfo)
    
    output["teams"] = teamsarray

    rankHelper(output)
    
    """with open('data.json', 'w') as outfile:
        json.dump(output, outfile)
        print("file complete")"""



run()    
    
#df.to_csv(file_name, encoding='utf-8', index=False)

#GameId	GameDate	Quarter	Minute	Second	OffenseTeam	DefenseTeam	Down	ToGo	YardLine		SeriesFirstDown		NextScore	Description	TeamWin			SeasonYear	Yards	Formation	PlayType	IsRush	IsPass	IsIncomplete	IsTouchdown	PassType	IsSack	IsChallenge	IsChallengeReversed	Challenger	IsMeasurement	IsInterception	IsFumble	IsPenalty	IsTwoPointConversion	IsTwoPointConversionSuccessful	RushDirection	YardLineFixed	YardLineDirection	IsPenaltyAccepted	PenaltyTeam	IsNoPlay	PenaltyType	PenaltyYards

#team
#redzone/standard

#1,2,3,4 down
#formations

#direction
#yards