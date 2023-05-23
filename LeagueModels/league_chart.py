import helpers
import matplotlib.dates
import pylab
import numpy as np
from matplotlib import pyplot, dates
import discord
import discord.ext
import helpers
import datetime


def plot_kda(sql_match_rows):
    kda_points = []
    match_dates = []
    for i, match in enumerate(sql_match_rows):
        # pull 110 matches from db, but only use the first 10 to add to the average of the early games
        if i < len(sql_match_rows) - 100:
            continue
        # for each match, look at the last 10 and create the kda average
        kills, deaths, assists = 0, 0, 0
        for j in range(10):
            if j > i:
                break
            evaulate_match = sql_match_rows[i - j]
            kills += evaulate_match["kills"]
            deaths +=  evaulate_match["deaths"]
            assists += evaulate_match["assists"]
        deaths = deaths if deaths > 0 else 1
        kda = (kills + assists) / deaths
        match_date = str(evaulate_match["date_created"]).split(' ')[0]
        match_date = datetime.datetime.strptime(match_date, '%Y-%m-%d')
        kda_points.append(round(kda, 2))
        match_dates.append(match_date)

    x = match_dates
    y = kda_points

    days = (x[-1] - x[0]).days #determine how many days in the data set. NOT USING THIS. just as a reminder
    fig, ax = pyplot.subplots()
    ax.plot(x, y)
    # set the formatting and intervals of the dates. evenly space them.
    locator = dates.DayLocator(interval=7)
    formatter = dates.DateFormatter('%m/%d')
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_tick_params(rotation=90)

    pyplot.title(str(sql_match_rows[0]["summoner_name"]) + " KDA")
    chart_file = "kda_chart.png"
    pyplot.savefig(chart_file) # could pass in dpi to savefig as chart's dpi to increase resolution
    chart_image = discord.File(chart_file)
    pyplot.close()
    return chart_image



def group_plot_kda(sql_match_rows, summoners):
    kda_points = [[] for _ in range(len(summoners))]
    match_dates = set()
    # first split the row results into one table for each summoner
    summoner_match_rows = [[] for _ in range(len(summoners))]
    for i, s in enumerate(summoners):
        for match in sql_match_rows:
            if s == str(match["summoner_name"]):
                summoner_match_rows[i].append(match)

    # now iterate through each summoner's table, and each match inside it to build the kda
    for match_table in summoner_match_rows:
        summoner = str(match_table[0]["summoner_name"])
        for i, match in enumerate(match_table):
            # for each match, look at the last 10 and create the kda average
            kills, deaths, assists = 0, 0, 0
            for j in range(10):
                if j > i: # j > i means we are looking at the earliest 10 games on the table, so don't go negative i
                    break
                evaulate_match = match_table[i - j]
                kills += evaulate_match["kills"]
                deaths +=  evaulate_match["deaths"]
                assists += evaulate_match["assists"]

            deaths = deaths if deaths > 0 else 1  # very unlikely safeguard
            kda = (kills + assists) / deaths
            list_index = list(summoners).index(summoner)
            match_date = str(match["date_created"]).split(' ')[0]  # drop hours/minutes/seconds and stringify
            kda_points[list_index].append((match_date, round(kda, 2)))  # append a tuple for (date, kda)
            match_dates.add(match_date)  # add unique match dates to the set for the x-axis

    # get a list of all dates between the first and last matches
    dates_list = list(match_dates)
    dates_list.sort()
    print(str(len(dates_list)) + "  dates with 3+ summoner games")
    start_date = datetime.datetime.strptime(dates_list[0], '%Y-%m-%d')
    end_date = datetime.datetime.strptime(dates_list[-1], '%Y-%m-%d')
    print("start = " + str(start_date) + "   end = " + str(end_date))
    dates_list = []
    while start_date <= end_date:  # build the list of dates between start and end dates to use as x-axis
        dates_list.append(start_date)
        start_date += datetime.timedelta(days=1)
    x = dates_list
    x.sort()
    y_lines = []  # list of 4 y-value lists
    for i, kda_list in enumerate(kda_points):
        # iterate through dates AND the kda match history for this summoner & fill in matches that match the date
        # reverse it so latest game played on that date is the most up-to-date kda for the chart
        kda_list.reverse()
        # get first element (match_date) in the kda_list tuple (match_date, kda)
        kda_dates = [kda_date[0] for kda_date in kda_list]
        mask_counter = 0  # to keep track of how many interpolated points
        y = [np.nan] * len(dates_list) # instantiate a set of nan equal to the # of days in the x-axis set
        for j, date in enumerate(dates_list):
            date = str(date).split(' ')[0]
            if date in kda_dates:  # found 1+ matches on this date. Update y value = kda from the last match that day
                index = kda_dates.index(date)
                y[j] = kda_list[index][1]
            else:  # no match on this date, leave the nan in place for the mask
                mask_counter += 1

        print("\n\nmask count for " + summoners[i] + "  =  " + str(mask_counter))
        y = np.array(y)
        # fill in missing values (nan) with the mask
        mask = np.isnan(y)
        print(str(len(dates_list) - mask_counter) + "  matching dates for " + str(summoners[i]) + "\n")
        y = np.ma.array(y, mask=mask)
        print(y)
        # interpolate missing values for charting continuous lines. ~ means to invert the mask
        num_dates = matplotlib.dates.date2num(x)
        x_interp = np.linspace(num_dates[~mask].min(), num_dates[~mask].max(), len(num_dates))
        y_interp = np.interp(x_interp, num_dates[~mask], y[~mask])
        y_lines.append(y_interp)


    fig, ax = pyplot.subplots()
    # plot each y-value list
    colors = ['#000000', '#98c1d9', '#fca311', '#c01623']
    for i, y in enumerate(y_lines):
        pyplot.plot(x, y, label=list(summoners)[i], color=colors[i])
    ax.legend()
    # reduce # of ticks for dates
    locator = dates.DayLocator(interval=7)
    formatter = dates.DateFormatter('%m/%d')
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_tick_params(rotation=90)
    pyplot.title("KDA last 100 matches")
    chart_file = "kda_chart.png"
    pyplot.savefig(chart_file) # could pass in dpi to savefig as chart's dpi to increase resolution
    chart_image = discord.File(chart_file)
    pyplot.close()
    return chart_image