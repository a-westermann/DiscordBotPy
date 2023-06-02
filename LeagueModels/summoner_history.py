

class SummonerHistory:
    # kills = 0 # can't do this - it makes them static elements for the class, and a change to one 'instance'
    # would change all instances. Instead, see __init__()

    def __init__(self, summoner_name):
        self.summoner_name = summoner_name
        self.kills = 0
        self.deaths = 0
        self.assists = 0
        self.doubles = 0
        self.triples = 0
        self.quadras = 0
        self.pentas = 0

        # # below only used for the best game in recap. Create a separate summoner history class instance
        # self.item_0 = 0
        # self.item_1 = 0
        # self.item_2 = 0
        # self.item_3 = 0
        # self.item_4 = 0
        # self.item_5 = 0


    def add_match_score(self, kills, deaths, assists, doubles, triples, quadras, pentas):
        # should change this to allow passing in a Participant
        self.kills += kills
        self.deaths += deaths
        self.assists += assists
        self.doubles += doubles
        self.triples += triples
        self.quadras += quadras
        self.pentas += pentas


