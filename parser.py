import pandas as pd
import numpy as np
import statistics
import csv


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




def y_td_parse():
    data = pd.read_csv("data/pbp-2020.csv")
    subset = data.groupby(["GameId"])
    gid = pd.unique(data["GameId"].dropna())
    teamnames = pd.unique(data["OffenseTeam"].dropna())
    output = {"year":2020,"teams":[]}
    teamsarray = {}
    for i in gid:

        game = subset.get_group(i)
        teams = pd.unique(game["OffenseTeam"].dropna())

        offr = game[(game["OffenseTeam"]==teams[0])&((game["PlayType"]=="RUSH") | (game["PlayType"]=="SCRAMBLE")) & (game["IsPenaltyAccepted"]==0)]["Yards"].sum()
        offp = game[(game["OffenseTeam"]==teams[0])&((game["PlayType"]=="PASS") | (game["PlayType"]=="SACK")) & (game["IsPenaltyAccepted"]==0)]["Yards"].sum()
        offt = game[(game["OffenseTeam"]==teams[0])&((game["IsTouchdown"]==1) & (game["IsFumble"]==0) & (game["IsInterception"]==0)) & (game["IsPenaltyAccepted"]==0)]["IsTouchdown"].sum()
        offk = len(game[(game["OffenseTeam"]==teams[0])&((game["PlayType"]=="FIELD GOAL") & (str(game["Description"]).find("GOAL IS GOOD")))& (game["IsPenaltyAccepted"]==0)])

        defr = game[(game["OffenseTeam"]==teams[1])&((game["PlayType"]=="RUSH") | (game["PlayType"]=="SCRAMBLE")) & (game["IsPenaltyAccepted"]==0)]["Yards"].sum()
        defp = game[(game["OffenseTeam"]==teams[1])&((game["PlayType"]=="PASS") | (game["PlayType"]=="SACK")) & (game["IsPenaltyAccepted"]==0)]["Yards"].sum()
        deft = game[(game["OffenseTeam"]==teams[1])&((game["IsTouchdown"]==1) & (game["IsFumble"]==0) & (game["IsInterception"]==0)) & (game["IsPenaltyAccepted"]==0)]["IsTouchdown"].sum()
        defk = len(game[(game["OffenseTeam"]==teams[1])&((game["PlayType"]=="FIELD GOAL") & (str(game["Description"]).find("GOAL IS GOOD")))& (game["IsPenaltyAccepted"]==0)])

        if teams[0] in teamsarray:
            teamsarray[teams[0]]["o_rush"].append(offr)
            teamsarray[teams[0]]["o_pass"].append(offp)
            teamsarray[teams[0]]["o_td_y"].append(round(offt/(offr+offp),4))
            teamsarray[teams[0]]["o_k_y"].append(round(offk/(offr+offp),4))
            teamsarray[teams[0]]["d_rush"].append(defr)
            teamsarray[teams[0]]["d_pass"].append(defp)
            teamsarray[teams[0]]["d_td_y"].append(round(offt/(defr+defp),4))
            teamsarray[teams[0]]["d_k_y"].append(round(offk/(defr+defp),4))
        else:
            teamsarray[teams[0]] = {}
            teamsarray[teams[0]]["o_rush"] = [offr]
            teamsarray[teams[0]]["o_pass"] = [offp]
            teamsarray[teams[0]]["o_td_y"] = [round(offt/(offr+offp),4)]
            teamsarray[teams[0]]["o_k_y"] = [round(offk/(offr+offp),4)]
            teamsarray[teams[0]]["d_rush"] = [defr]
            teamsarray[teams[0]]["d_pass"] = [defp]
            teamsarray[teams[0]]["d_td_y"] = [round(offt/(defr+defp),4)]
            teamsarray[teams[0]]["d_k_y"] =  [round(offk/(defr+defp),4)]
        
        if teams[1] in teamsarray:
            teamsarray[teams[1]]["o_rush"].append(defr)
            teamsarray[teams[1]]["o_pass"].append(defp)
            teamsarray[teams[1]]["o_td_y"].append(round(deft/(defr+defp),4))
            teamsarray[teams[1]]["o_k_y"].append(round(defk/(defr+defp),4))
            teamsarray[teams[1]]["d_rush"].append(offr)
            teamsarray[teams[1]]["d_pass"].append(offp)
            teamsarray[teams[1]]["d_td_y"].append(round(offt/(offr+offp),4))
            teamsarray[teams[1]]["d_k_y"].append(round(offk/(offr+offp),4))
        else:
            teamsarray[teams[1]] = {}
            teamsarray[teams[1]]["o_rush"] = [defr]
            teamsarray[teams[1]]["o_pass"] = [defp]
            teamsarray[teams[1]]["o_td_y"] = [round(deft/(defr+defp),4)]
            teamsarray[teams[1]]["o_k_y"] = [round(defk/(defr+defp),4)]
            teamsarray[teams[1]]["d_rush"] = [offr]
            teamsarray[teams[1]]["d_pass"] = [offp]
            teamsarray[teams[1]]["d_td_y"] = [round(offt/(offr+offp),4)]
            teamsarray[teams[1]]["d_k_y"] =  [round(offk/(offr+offp),4)]
        
    for j in teamnames:
        teamstats = {"team":j}
        teamstats["o_rmean"] = round(statistics.mean(teamsarray[j]["o_rush"]),4)
        teamstats["o_rstd"] = round(statistics.stdev(teamsarray[j]["o_rush"]),4)
        teamstats["o_pmean"] = round(statistics.mean(teamsarray[j]["o_pass"]),4)
        teamstats["o_pstd"] = round(statistics.stdev(teamsarray[j]["o_pass"]),4)
        teamstats["o_tmean"] = round(statistics.mean(teamsarray[j]["o_td_y"]),4)
        teamstats["o_tstd"] = round(statistics.stdev(teamsarray[j]["o_td_y"]),4)
        teamstats["o_kmean"] = round(statistics.mean(teamsarray[j]["o_k_y"]),4)
        teamstats["o_kstd"] = round(statistics.stdev(teamsarray[j]["o_k_y"]),4)
        teamstats["d_rmean"] = round(statistics.mean(teamsarray[j]["d_rush"]),4)
        teamstats["d_rstd"] = round(statistics.stdev(teamsarray[j]["d_rush"]),4)
        teamstats["d_pmean"] = round(statistics.mean(teamsarray[j]["d_pass"]),4)
        teamstats["d_pstd"] = round(statistics.stdev(teamsarray[j]["d_pass"]),4)
        teamstats["d_tmean"] = round(statistics.mean(teamsarray[j]["d_td_y"]),4)
        teamstats["d_tstd"] = round(statistics.stdev(teamsarray[j]["d_td_y"]),4)
        teamstats["d_kmean"] = round(statistics.mean(teamsarray[j]["d_k_y"]),4)
        teamstats["d_kstd"] = round(statistics.stdev(teamsarray[j]["d_k_y"]),4)

        output["teams"].append(teamstats)
    

    #print(output)
    keys = output["teams"][0].keys()
    with open('team_mean_std.csv', 'w', newline='')  as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(output["teams"])
    """with open('team_mean_std.json', 'w') as outfile:
            json.dump(output, outfile)
            print("file complete")"""

y_td_parse()    
    
#df.to_csv(file_name, encoding='utf-8', index=False)

#GameId	GameDate	Quarter	Minute	Second	OffenseTeam	DefenseTeam	Down	ToGo	YardLine		SeriesFirstDown		NextScore	Description	TeamWin			SeasonYear	Yards	Formation	PlayType	IsRush	IsPass	IsIncomplete	IsTouchdown	PassType	IsSack	IsChallenge	IsChallengeReversed	Challenger	IsMeasurement	IsInterception	IsFumble	IsPenalty	IsTwoPointConversion	IsTwoPointConversionSuccessful	RushDirection	YardLineFixed	YardLineDirection	IsPenaltyAccepted	PenaltyTeam	IsNoPlay	PenaltyType	PenaltyYards

#team
#redzone/standard

#1,2,3,4 down
#formations

#direction
#yards per drive, yards allowed per drive

