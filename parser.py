import pandas as pd
import numpy as np

data = pd.read_csv("data/pbp-2020.csv")

teams = pd.unique(data["OffenseTeam"].dropna())
games = pd.unique(data["GameId"].dropna())

#print(games.size)

for i in teams:
    print(i)
    tdata = data[data["OffenseTeam"]==i]
    r = tdata[tdata["IsRush"]==1]
    p = tdata[tdata["IsPass"]==1]
    pen = data[(data["PenaltyTeam"]==i) & (data["IsPenaltyAccepted"]==1)]

    #print(len(tdata["OffenseTeam"]))
    print("rushing plays " + str(len(r)))
    print("passing plays " + str(len(p)))
    print("penalties " + str(len(pen)))

#GameId	GameDate	Quarter	Minute	Second	OffenseTeam	DefenseTeam	Down	ToGo	YardLine		SeriesFirstDown		NextScore	Description	TeamWin			SeasonYear	Yards	Formation	PlayType	IsRush	IsPass	IsIncomplete	IsTouchdown	PassType	IsSack	IsChallenge	IsChallengeReversed	Challenger	IsMeasurement	IsInterception	IsFumble	IsPenalty	IsTwoPointConversion	IsTwoPointConversionSuccessful	RushDirection	YardLineFixed	YardLineDirection	IsPenaltyAccepted	PenaltyTeam	IsNoPlay	PenaltyType	PenaltyYards

#teams, rush/pass, formation, yardline, down, quarter
#print(teams.size)
#print(data.head())
#print(teams)