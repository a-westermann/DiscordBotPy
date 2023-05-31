from riotwatcher import LolWatcher, ApiError

import helpers
from LeagueModels import summoner_history as s_history, league_chart
import psql
from datetime import datetime
import cassiopeia as cass


class LeagueAPI:
    region = 'na1'
    def __init__(self, api_token, psql: psql.PSQL):
        self.token = api_token
        self.lol_watcher = LolWatcher(api_key=self.token)
        self.psql = psql

# helpers
    def get_summoner(self, summoner_name):
        return self.lol_watcher.summoner.by_name(self.region, summoner_name)


    def get_puuid(self, summoner_name):
        text_file = open(r"/home/andweste/Tokens/secret_creds_repo/league_ids.txt").readlines()
        puuid = ""
        for line in text_file:
            if line.split(';')[0] == summoner_name:
                puuid = line.split(';')[1].strip()
                break
        return puuid

    def get_recent_matches(self, puuid, count):
        match_ids = self.lol_watcher.match.matchlist_by_puuid(region=self.region, puuid=puuid, count=count)
        return match_ids

    def build_match(self, match_id: str):
        match = self.lol_watcher.match.by_id(self.region, match_id)
        # print("test " + match['metadata']['dataVersion'])  # <-- access nested elements like this
        return match

    def get_item(self, item_id: int):
        items = cass.get_items(cass.Region.north_america)
        item_to_find = cass.Item(id=item_id, region=cass.Region.north_america)
        return items.find(item=item_to_find)

    def get_champ(self, champ_id: int):
        champs = cass.get_champion(region=cass.Region.north_america)
        return cass.Champions.find(item=champ_id)

        # return cass.get_champion(key=champ_id, region=cass.Region.north_america)



# major methods

    # get last x matches for each summoner puuid
    # iterate through and build kda, store as a summoner_history object
    # chart the kda's on one line chart
#TODO only include matches w/ 3 of us or more
#TODO when grouping multi summoners aggregate the match list so i don't request same match multiple times
    def individual_kda_chart(self, summoner_name):
        # first fill the psql table with new matches
        matches = self.get_matches(summoner_name, match_count=60)
        for match in matches:
            self.fill_match_table(match, summoner_name)
        # now build out the kda averages over time. Each point is the cumulative kda average of the last 10 games
        sql_match_rows = self.psql.get_summoner_matches(summoner_name)
        print("found " + str(len(sql_match_rows)) + " matches.")
        chart = league_chart.plot_kda(sql_match_rows)
        return chart


#TODO: need to ensure I grab matches that are in the top 100 for ALL of us
    def group_kda_chart(self):
        # first fill the psql table with new matches
        summoners = ["Vierce", "The Great Ratsby", "ComradeGiraffe", "Gold Force"]
        for summoner in summoners:
            matches = self.get_matches(summoner, match_count=60)
            for match in matches:
                self.fill_match_table(match, summoner)
        # now build out the kda averages over time. Each point is the cumulative kda average of the last 10 games
        sql_match_rows = self.psql.get_recent_100_matches()
        print("found " + str(len(sql_match_rows)) + " rows.")
        chart = league_chart.group_plot_kda(sql_match_rows, summoners)
        return chart

# this gives 100 rows , seems wrong? Or just coincidence??
    #select match_id FROM match_history GROUP BY match_id HAVING COUNT(match_id)>2



# Every request should probably start with get_matches to fill recent matches
# this includes adding recap later
    def get_matches(self, summoner_name, match_count: int):
        puuid = self.get_puuid(summoner_name)
        # print("puuid for " + summoner_name + " " + puuid)
        match_ids = self.get_recent_matches(puuid=puuid, count=match_count)
        matches = []
#TODO: change the sql to an IN() statement contianing all matches, then do a python compare to determine
#TODO: which ones need to be added. That will cut down on query time when dealing with lots of new matches
        for match_id in match_ids:
            # only build match if it's not on table for summoner
            results = self.psql.get_specific_match(match_id, summoner_name)
            if len(results) > 0: break  # stop looking - hit the most current recorded match
            matches.append(self.build_match(match_id))
        return matches


    def fill_match_table(self, match, summoner_name):
        id = match["metadata"]["matchId"]
        game_timestamp = datetime.utcfromtimestamp(int(match["info"]["gameCreation"])/1000.0)
        summoner_history = self.build_summoner_history(summoner_name, [match])
        self.psql.insert_match(id, summoner_name, summoner_history.kills, summoner_history.deaths,
                               summoner_history.assists, summoner_history.doubles, summoner_history.triples,
                               summoner_history.quadras, summoner_history.pentas, game_timestamp)


    def build_summoner_history(self, summoner_name, matches: list):
        summoner_history = s_history.SummonerHistory(summoner_name)
        puuid = self.get_puuid(summoner_name)
        for match in matches:
            participant = helpers.get_matching_participant(puuid, match)
            summoner_history.add_match_score(participant["kills"],
                                             participant["deaths"],
                                             participant["assists"],
                                             participant["doubleKills"],
                                             participant["tripleKills"],
                                             participant["quadraKills"],
                                             participant["pentaKills"])
        print(str(summoner_history.kills) + "/" + str(summoner_history.deaths) + "/" + str(summoner_history.assists))
        return summoner_history


