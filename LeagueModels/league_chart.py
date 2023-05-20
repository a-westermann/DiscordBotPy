import helpers
import pylab
import numpy as np
import matplotlib.pyplot as pyplot
import discord
import discord.ext
import helpers
import datetime


def plot_kda(sql_match_rows):
    kda_points = []
    dates = []
    for i, match in enumerate(sql_match_rows):
        # for each match, look at the last 10 and create the kda average
        kills, deaths, assists = 0, 0, 0
        for j in range(10):
            if j > i:
                break  # ensures for the first 10 games in the list we don't try to go negative i
            evaulate_match = sql_match_rows[i - j]
            kills += evaulate_match["kills"]
            deaths +=  evaulate_match["deaths"]
            assists += evaulate_match["assists"]
        deaths = deaths if deaths > 0 else 1
        kda = (kills + assists) / deaths
        match_date = str(evaulate_match["date_created"]).split(' ')[0]
        # match_date = match_date.split('-')[1] + match_date.split('-')[2]
        match_date = datetime.datetime.strptime(match_date, '%Y-%m-%d')
        match_date = match_date.strftime('%m/%d')
        kda_points.append(round(kda, 2))
        dates.append(match_date)

    x = dates
    y = kda_points

    pyplot.plot(x, y)
    # reduce # of ticks for dates
    pyplot.xticks(x[::5], rotation="vertical")
    pyplot.title(str(sql_match_rows[0]["summoner_name"]) + " KDA")
    chart_file = "kda_chart.png"
    pyplot.savefig(chart_file) # could pass in dpi to savefig as chart's dpi to increase resolution
    chart_image = discord.File(chart_file)
    pyplot.close()
    return chart_image



#sql_match_rows will include duplicates, each match has rows for each summoner
def group_plot_kda(sql_match_rows, summoners: [str]):
    kda_points = [[]]
    dates = [[]]
    for s in summoners:
        kda_points.append(s)
        dates.append(s)
    for i, match in enumerate(sql_match_rows):
        summoner = match["summoner_name"]
        # for each match, look at the last 10 and create the kda average
        kills, deaths, assists = 0, 0, 0
        for j in range(10):
            if j > i:
                break  # ensures for the first 10 games in the list we don't try to go negative i
            evaulate_match = sql_match_rows[i - j]
            kills += evaulate_match["kills"]
            deaths +=  evaulate_match["deaths"]
            assists += evaulate_match["assists"]
        deaths = deaths if deaths > 0 else 1
        kda = (kills + assists) / deaths
        match_date = str(evaulate_match["date_created"]).split(' ')[0]
        # match_date = match_date.split('-')[1] + match_date.split('-')[2]
        match_date = datetime.datetime.strptime(match_date, '%Y-%m-%d')
        match_date = match_date.strftime('%m/%d')
        list = [s for s in kda_points if s == summoner]
        for l in list:
            print(str(l) + " list")
        [s for s in kda_points if s == summoner].append(round(kda, 2))
        [s for s in dates if s == summoner].append(match_date)

    x1, x2, x3, x4 = dates[0], dates[1], dates[2], dates[3]
    y1, y2, y3, y4 = kda_points[0], kda_points[1], kda_points[2], kda_points[3]
    for x in kda_points[0]:
        print(x)

    pyplot.plot(x1, y1)
    pyplot.plot(x2, y2)
    pyplot.plot(x3, y3)
    pyplot.plot(x4, y4)
    # reduce # of ticks for dates
    pyplot.xticks(x1[::5], rotation="vertical")
    pyplot.xticks(x2[::0])
    pyplot.xticks(x3[::0])
    pyplot.xticks(x4[::0])
    pyplot.title("KDA last 100 matches")
    chart_file = "kda_chart.png"
    pyplot.savefig(chart_file) # could pass in dpi to savefig as chart's dpi to increase resolution
    chart_image = discord.File(chart_file)
    pyplot.close()
    return chart_image