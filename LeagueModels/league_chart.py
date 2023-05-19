import helpers
import pylab
import matplotlib.pyplot as pyplot
import discord
import discord.ext
import helpers


def plot_kda(sql_match_rows):
    for match in sql_match_rows:
        print("kills = " + match["kills"])
        break