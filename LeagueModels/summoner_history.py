

class SummonerHistory:
    # kills = 0 # can't do this - it makes them static elements for the class, and a change to one 'instance'
    # would change all instances. Instead, see __init__()

    def __init__(self, summoner_name):
        self.summoner_name = summoner_name
        self.kills = 0
        self.deaths = 0
        self.assists = 0


    def add_match_score(self, kills, deaths, assists):
        self.kills += kills
        self.deaths += deaths
        self.assists += assists


