from riotwatcher import LolWatcher, ApiError
from LeagueModels import summoner_history as s_history


region = 'na1'

class LeagueAPI:
    def __init__(self, api_token):
        self.token = api_token
        self.lol_watcher = LolWatcher(api_key=self.token)

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
        print("test " + match['metadata']['dataVersion'])  # <-- access nested elements like this


    # def get_kda(self, match: LolWatcher.match, puuid):



# major methods

    # get last x matches for each summoner puuid
    # iterate through and build kda, store as a summoner_history object
    # chart the kda's on one line chart
    # later on can worry about creating a db
#TODO only include matches w/ 3 of us or more
#TODO when grouping multi summoners aggregate the match list so i don't request same match multiple times
#TODO create sql db to save histories
    def build_kda(self, summoner_name):
        puuid = self.get_puuid(summoner_name)
        summoner_history = s_history.SummonerHistory(summoner_name)
        match_ids = self.get_recent_matches(puuid=puuid, count=10)
        matches = []
        for match_id in match_ids:
            matches.append(self.build_match(match_id))
            break

        for match in matches:
            # participant = match.info.participants
            # participant = (s for s in match if  match["metadata"]["participants"] if s == puuid)
            participants = match["info"]["participants"]
            for i in range(len(participants)):
                if participants[i] == puuid:
                    participant = participants[i]
                    break
            print("match data kills = " + participant["kills"])
            summoner_history.add_match_score(participant.kills, participant.deaths, participant.assists)
        print(summoner_history.kills + "/" + summoner_history.deaths)


