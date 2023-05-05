from riotwatcher import LolWatcher, ApiError


region = 'na1'

class LeagueAPI:
    def __init__(self, api_token):
        global token
        token = api_token
        global lol_watcher
        lol_watcher = LolWatcher(token)

    def get_summoner(self, summoner_name):
        return lol_watcher.summoner.by_name(region, summoner_name)