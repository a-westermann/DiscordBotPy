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
        if i < 10:
            continue
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



#sql_match_rows will include duplicates, each match has rows for each summoner
def group_plot_kda(sql_match_rows, summoners):

    kda_points = [[] for _ in range(len(summoners))]
    # first_date = sql_match_rows[0]["date_created"].split(' ')[0]
    # datetime.datetime.strptime(first_date, '%Y-%m-%d')
    # last_date = sql_match_rows[-1]["date_created"].split(' ')[0]
    # datetime.datetime.strptime(last_date, '%Y-%m-%d')
    # date_range = [first_date, last_date]
    match_dates = set()
    # for s in summoners:
    #     kda_points.append([])
    for i, match in enumerate(sql_match_rows):
        summoner = str(match["summoner_name"])
        # pull 110 matches from db, but only use the first 10 to add to the average of the early games
        if i < 10:
            continue
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
        list_index = list(summoners).index(summoner)
        match_date = str(evaulate_match["date_created"]).split(' ')[0]
        match_date = datetime.datetime.strptime(match_date, '%Y-%m-%d')
        kda_points[list_index].append((match_date, round(kda, 2)))
        match_dates.add(match_date)


    # get a list of all dates between the first and last matches
    dates_list = list(match_dates)
    dates_list.sort()
    start_date = dates_list[0]
    end_date = dates_list[-1]
    dates_list = []
    while start_date <= end_date:
        dates_list.append(start_date)
        start_date += datetime.timedelta(days=1)

    x = dates_list
    x.sort()
    y_lines = []
    for i, kda_list in enumerate(kda_points):  # add the kda_list for each summoner to the y_values list
        # y = np.full(len(x), np.nan)  # np.nan fill in values = to # of x values. We will replace them w/ Y values
        # create a mask instead to fill in missing points
        # mask = np.ones(len(x), dtype=bool)
        # iterate through dates AND the kda match history for this summoner & fill in matches that match the date
        # reverse it so latest game played on that date is first for the match
        kda_list.reverse()
        # get first element (match_date) in the kda_list tuple (match_date, kda)
        kda_dates = [kda_date[0] for kda_date in kda_list]
        print(kda_dates[0])
        y = []
        for j, date in enumerate(dates_list):
            # if there is a match on this date, add the kda on that index
            # (note it will be ONE of the matches on that date)
            if date in kda_dates:
                index = kda_dates.index(date)
                y.append(kda_list[index][1])
            else:  # no match on this date, append a nan
                y.append(np.nan)
            # for k, m_date in enumerate(kda_dates):
            #     m_date = str(m_date).split(' ')[0]
            #     if date == m_date:
            #         mask[j] = False # turn off mask, found match for this point

        # kda_scores = [kda_score[1] for kda_score in kda_list]
        y = np.array(y)
        # y = np.insert(y, 0, np.nan)
        # y = np.insert(y, len(y), np.nan)
        # fill in missing values with the mask
        mask = np.isnan(y)
        y = np.ma.array(y, mask=mask)
        y_lines.append(y)

        # y_values.append(np.array(kda_list))

    fig, ax = pyplot.subplots()
    # plot each y-value list
    for i, y in enumerate(y_lines):
        pyplot.plot(x, y, label=list(summoners)[i])
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