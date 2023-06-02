from googlesearch import search
from datetime import datetime, timedelta
import discord
from riotwatcher import LolWatcher, ApiError
import cassiopeia as cass
from LeagueModels.league_api import LeagueAPI
from psql import PSQL


users = { 322164425002057728:"Vierce" , 879464051267223572:"Naiyvara",
    159815678508007424:"ComradeGiraffe" , 157183377089363969:"The Great Ratsby" , 238467012399988738:"GoldForce" }

names = {"Naiyvara":"Ashley" , "Vierce":"Andrew"}

# General functions
def google_search(search_term, num_results):
    for url in search(search_term, num_results=num_results):
        return url


def get_date_hour():
    today = datetime.today()
    # strip off the milliseconds then convert back to datetime
    simple_today = datetime.strptime(str(today).split('.')[0], "%Y-%m-%d %H:%M:%S")
    return simple_today


def get_user_name(interaction: discord.Interaction):
    try:
        return users[int(interaction.user.id)]
    except Exception as e:
        print("Error in get_user_name: " + str(e))
        return None

def check_user(interaction: discord.Interaction, allowed_users: []):
    user = get_user_name(interaction)
    # user and user in allowed_users will be None if not found
    return (user is not None and user in allowed_users) is True

def get_name(user_name: str):
    print("Getting name for ... " + user_name)
    try:
        return names[user_name]
    except Exception as e:
        return None

def get_used_babies(user: str, top: bool, number: int, include_score: bool):
    # returns (name: str, score: int)
    print("\nTop names for: " + user)
    used_names_text = open("/home/andweste/Scripts/used_names.txt", "r").readlines()
    name_list = []
    for line in used_names_text[2:]:
        index = 1 if user == "Ashley" else 2
        name = line.split(';')[0]
        name_list.append((name, int(line.split(';')[index].strip())))
    # sort list by score
    sorted_list = sorted(name_list, key=lambda tuple: tuple[1])
    for i in range(len(sorted_list) - number):
        sorted_list.pop(0)
    for s in sorted_list:
        print(s)
    if not include_score:
        for i in range(len(sorted_list)):
            sorted_list[i] = sorted_list[i][0]
    return sorted_list


def get_matching_participant(puuid: str, match):
    participants = match["info"]["participants"]
    for participant in participants:
        if participant["puuid"] == puuid:
            return participant



def get_summoner_name_from_first_letter(letter: str):
    if letter.lower() == "v": return "Vierce"
    if letter.lower() == "t": return "The Great Ratsby"
    if letter.lower() == "c": return "ComradeGiraffe"
    if letter.lower() == "g": return "Gold Force"


def split_sql_matches_summoners(sql_match_rows, summoners: list):
    summoner_match_rows = [[] for _ in range(len(summoners))]
    for i, s in enumerate(summoners):
        for match in sql_match_rows:
            if s == str(match["summoner_name"]):
                summoner_match_rows[i].append(match)

    return summoner_match_rows


def calculate_kda(matches: list): # pass in any list of sql match rows
    kills, deaths, assists = 0, 0, 0
    for match in matches:
        kills += match["kills"]
        deaths += match["deaths"]
        assists += match["assists"]

    deaths = deaths if deaths > 0 else 1  # safeguard
    kda = (kills + assists) / deaths
    return kda

def get_dates_list_between_dates(date_list):
    # fills a list of all dates. Takes a list/set with missing dates
    dates_list = list(date_list)
    dates_list.sort()
    start_date = datetime.strptime(dates_list[0], '%Y-%m-%d')
    end_date = datetime.strptime(dates_list[-1], '%Y-%m-%d')
    print("start = " + str(start_date) + "   end = " + str(end_date))
    dates_list = []
    while start_date <= end_date:  # build the list of dates between start and end dates to use as x-axis
        dates_list.append(start_date)
        start_date += timedelta(days=1)
    return dates_list


def backfill_match_items(start: int, count: int, puuid: str, api: LeagueAPI):
    match_id_list = api.lol_watcher.match.matchlist_by_puuid(region=api.region, puuid=puuid, start=start, count=count)
    psql = PSQL()
    # build the string for the sql statement
    item_keys = [f"item{item_index}" for item_index in range(6)]
    for i, match_id in enumerate(match_id_list):
        match = api.lol_watcher.match.by_id(region=api.region, match_id=match_id)
        participant = get_matching_participant(puuid=puuid, match=match)
        # create the sql SET statement containing all the "item_0 = ABC123, etc...". Just take -1 for the last digit
        participant_items = ", ".join([f"item_{item_key[-1]} = '{participant[item_key]}'" for item_key in item_keys])
        update_result = psql.command(f"UPDATE match_history SET {participant_items} "
                     f"WHERE match_id = '{match_id}' AND summoner_name = '{participant['summonerName']}'")
        print(f"updated db for match index {i} ... {update_result}")

def backfill_match_champs(start: int, count: int, puuid: str, api: LeagueAPI):
    match_id_list = api.lol_watcher.match.matchlist_by_puuid(region=api.region, puuid=puuid, start=start, count=count)
    psql = PSQL()
    for i, match_id in enumerate(match_id_list):
        match = api.lol_watcher.match.by_id(region=api.region, match_id=match_id)
        participant = get_matching_participant(puuid=puuid, match=match)
        champ = participant["championId"]
        update_result = psql.command(f"UPDATE match_history SET champion_id = {champ} "
                                     f"WHERE match_id = '{match_id}' "
                                     f"AND summoner_name = '{participant['summonerName']}'; ")
        print(f"updated db for match index {i} ... champ = {participant['championName']}")


def get_champ_by_partial_string(partial_name: str) -> list[cass.Champion]:
    champs = cass.get_champions(region=cass.Region.north_america)
    matching_champs = []
    for champ in champs:
        if champ.name.__contains__(partial_name):
            matching_champs.append(champ)
    return matching_champs
