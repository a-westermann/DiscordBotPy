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