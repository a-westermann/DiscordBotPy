


class Summoner:
    def __init__(self, summoner_name, puuid):
        self.summoner_name = summoner_name
        self.puuid = puuid

    def get_history(self):
        history = self.puuid.etc