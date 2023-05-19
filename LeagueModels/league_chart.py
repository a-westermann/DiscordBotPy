import helpers
import pylab
import matplotlib.pyplot as pyplot
import discord
import discord.ext
import helpers


def plot_kda(sql_match_rows):
    kda_points = []
    for i, match in enumerate(sql_match_rows):
        # for each match, look at the last 10 and create the kda average
        for j in range(10):
            if j > i:
                break  # ensures for the first 10 games in the list we don't try to go negative i
            evaulate_match = sql_match_rows[i - j]
            kda = (evaulate_match["kills"] + evaulate_match["assists"]) / evaulate_match["deaths"]
            kda_points.append(round(kda, 2))

    for kda in kda_points:
        print(kda)