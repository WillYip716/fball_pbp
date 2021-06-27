import pandas as pd
import numpy as np
import random as rnd
import statistics
import csv

data = pd.read_csv("team_mean_std.csv")

def gamesim(t1,t2):
    team1 = data[data["team"]==t1]
    team2 = data[data["team"]==t2]

    team1_yr = (rnd.gauss(team1["o_rmean"].item(),team1["o_rstd"].item()) + rnd.gauss(team2["d_rmean"].item(),team2["d_rstd"].item()))/2
    team1_yp = (rnd.gauss(team1["o_pmean"].item(),team1["o_pstd"].item()) + rnd.gauss(team2["d_pmean"].item(),team2["d_pstd"].item()))/2
    team1_t = (rnd.gauss(team1["o_tmean"].item(),team1["o_tstd"].item()) + rnd.gauss(team2["d_tmean"].item(),team2["d_tstd"].item()))/2
    team1_k = (rnd.gauss(team1["o_kmean"].item(),team1["o_kstd"].item()) + rnd.gauss(team2["d_kmean"].item(),team2["d_kstd"].item()))/2

    team2_yr = (rnd.gauss(team2["o_rmean"].item(),team2["o_rstd"].item()) + rnd.gauss(team1["d_rmean"].item(),team1["d_rstd"].item()))/2
    team2_yp = (rnd.gauss(team2["o_pmean"].item(),team2["o_pstd"].item()) + rnd.gauss(team1["d_pmean"].item(),team1["d_pstd"].item()))/2
    team2_t = (rnd.gauss(team2["o_tmean"].item(),team2["o_tstd"].item()) + rnd.gauss(team1["d_tmean"].item(),team1["d_tstd"].item()))/2
    team2_k = (rnd.gauss(team2["o_kmean"].item(),team2["o_kstd"].item()) + rnd.gauss(team1["d_kmean"].item(),team1["d_kstd"].item()))/2

    score1 = round((team1_yr + team1_yp)*((team1_t * 7) + (team1_k * 3)))
    score2 = round((team2_yr + team2_yp)*((team2_t * 7) + (team2_k * 3)))

    #print(t1 + ": " + str(score1) + "   " + t2 + ": " + str(score2))
    #print(team2["o_rmean"].item())
    return score1,score2
    """if score1 > score2:
        return 1
    elif score2 > score1:
        return -1
    else:
        return""" 

def simulateSeries(t1,t2,ng):
    team1scores = []
    team2scores = []
    team1wins = 0
    team2wins = 0
    ties = 0

    for i in range(ng):
        gm = gamesim(t1,t2)
        team1scores.append(gm[0])
        team2scores.append(gm[1])
        if gm[0] > gm[1]:
            team1wins += 1
        elif gm[1] > gm[0]:
            team2wins += 1
        else:
            ties += 1
    
    print(t1 + " wins ", team1wins/ng,"%")
    print(t2 + " wins ", team2wins/ng,"%")
    print(t1 + " avg score ", round(statistics.mean(team1scores),2))
    print(t2 + " avg score ", round(statistics.mean(team2scores),2))


simulateSeries("BUF","NE",1000)


#team	o_rmean	o_rstd	o_pmean	o_pstd	o_tmean	o_tstd	o_kmean	o_kstd	d_rmean	d_rstd	d_pmean	d_pstd	d_tmean	d_tstd	d_kmean	d_kstd
#LV MIN TB ARI DEN MIA NYJ CLE NYG BAL CIN HOU CHI IND PIT DAL WAS SEA LA CAR TEN BUF KC GB ATL NE JAX SF LAC PHI DET NO 