import helpers
import pylab
import numpy as np
import matplotlib.pyplot as pyplot
import discord
import discord.ext
import helpers


def plot_kda(sql_match_rows):
    kda_points = []
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
        match_date = str(evaulate_match["date_created"])
        kda_points.append(tuple((round(kda, 2), match_date)))

    x = kda_points[1]
    y = kda_points[0]

    pyplot.plot(x, y)
    pyplot.title(str(sql_match_rows[0]["summoner_name"]) + " KDA")
    chart_file = "kda_chart.png"
    pyplot.savefig(chart_file) # could pass in dpi to savefig as chart's dpi to increase resolution
    chart_image = discord.File(chart_file)
    return chart_image