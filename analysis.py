import pandas as pd
import matplotlib.pyplot as plt
mvps = pd.read_csv("mvps.csv")
# print(mvps)
mvps = mvps[["Player", "Year", "Pts Won", "Pts Max", "Share"]]
# print(mvps)
#print(mvps.head())
players = pd.read_csv("players.csv")
del players["Unnamed: 0"]
del players["Rk"]
players["Player"] = players["Player"].str.replace("*","", regex=False)
#print(players.head())
def single_team(df):
    if df.shape[0]==1:
        return df
    else:
        row = df[df["Tm"]=="TOT"]
        row["Tm"] = df.iloc[-1,:]["Tm"]
        return row

players = players.groupby(["Player", "Year"]).apply(single_team)
# print(players)

players.index = players.index.droplevel()
players.index = players.index.droplevel()
#print(players)
combined = players.merge(mvps, how="outer", on=["Player", "Year"])
combined[["Pts Won", "Pts Max", "Share"]] = combined[["Pts Won", "Pts Max", "Share"]].fillna(0)
teams = pd.read_csv("teams.csv")
teams = teams[~teams["W"].str.contains("Division")].copy()
teams["Team"] = teams["Team"].str.replace("*", "", regex=False)
sorted(teams["Team"].unique())
sorted(combined["Tm"].unique())
nicknames = {}
with open("nicknames.csv") as f:
    lines = f.readlines()
    for line in lines[1:]:
        abbrev,name = line.replace("\n","").split(",")
        nicknames[abbrev] = name
combined["Team"] = combined["Tm"].map(nicknames)
train = combined.merge(teams, how="outer",on=["Team", "Year"])
del train["Unnamed: 0"]
train = train.apply(pd.to_numeric, errors='ignore')
train["GB"].unique()
train["GB"] = pd.to_numeric(train["GB"].str.replace("—","0"))
#print(train.head())
train.to_csv("player_mvp_stats.csv")
highest_scoring = train[train["G"] > 70].sort_values("PTS", ascending=False).head(10)
highest_scoring.plot.bar("Player", "PTS")
highest_scoring_by_year = train.groupby("Year").apply(lambda x: x.sort_values("PTS", ascending=False).head(1))
highest_scoring_by_year.plot.bar("Year", "PTS")
train.groupby("Year").apply(lambda x: x.shape[0])
train.corr()["Share"]
train.corr()["Share"].plot.bar()