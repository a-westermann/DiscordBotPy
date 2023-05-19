from riotwatcher import LolWatcher, ApiError
from LeagueModels import summoner_history as s_history
import psql
from datetime import datetime


region = 'na1'

class LeagueAPI:
    def __init__(self, api_token, psql: psql.PSQL):
        self.token = api_token
        self.lol_watcher = LolWatcher(api_key=self.token)
        self.psql = psql

# helpers
    def get_summoner(self, summoner_name):
        return self.lol_watcher.summoner.by_name(region, summoner_name)


    def get_puuid(self, summoner_name):
        text_file = open(r"/home/andweste/Tokens/secret_creds_repo/league_ids.txt").readlines()
        puuid = ""
        for line in text_file:
            if line.split(';')[0] == summoner_name:
                puuid = line.split(';')[1].strip()
                break
        return puuid

    def get_recent_matches(self, puuid, count):
        match_ids = self.lol_watcher.match.matchlist_by_puuid(region=region, puuid=puuid, count=count)
        return match_ids

    def build_match(self, match_id: str):
        match = self.lol_watcher.match.by_id(region, match_id)
        # print("test " + match['metadata']['dataVersion'])  # <-- access nested elements like this
        return match


    # def get_kda(self, match: LolWatcher.match, puuid):



# major methods

    # get last x matches for each summoner puuid
    # iterate through and build kda, store as a summoner_history object
    # chart the kda's on one line chart
    # later on can worry about creating a db
#TODO only include matches w/ 3 of us or more
#TODO when grouping multi summoners aggregate the match list so i don't request same match multiple times
#TODO create sql db to save histories
    def kda_chart(self, summoner_name):
        # first fill the psql table with new matches
        matches = self.get_matches(summoner_name, match_count=50)
        for match in matches:
            self.fill_match_table(match, summoner_name)



    def get_matches(self, summoner_name, match_count: int):
        puuid = self.get_puuid(summoner_name)
        print("puuid for " + summoner_name + " " + puuid)
        match_ids = self.get_recent_matches(puuid=puuid, count=match_count)
        matches = []
#TODO: change the sql to an IN() statement contianing all matches, then do a python compare to determine
# which ones need to be added
        for match_id in match_ids:
            # only build match if it's not on table for summoner
            results = self.psql.get_specific_match(match_id, summoner_name)
            if len(results) > 0: continue  # match already recorded
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
            participant = None
            participants = match["info"]["participants"]
            for i in range(len(participants)):
                if participants[i]["puuid"] == puuid:
                    participant = participants[i]
                    break
            summoner_history.add_match_score(participant["kills"], participant["deaths"], participant["assists"],
                        participant["doubleKills"], participant["tripleKills"], participant["quadraKills"],
                                             participant["pentaKills"])
        print(str(summoner_history.kills) + "/" + str(summoner_history.deaths) + "/" + str(summoner_history.assists))
        return summoner_history


