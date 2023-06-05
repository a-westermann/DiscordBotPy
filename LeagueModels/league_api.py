from riotwatcher import LolWatcher, ApiError
import helpers
from LeagueModels import summoner_history as s_history, league_chart
import psql
from datetime import datetime
import cassiopeia as cass
import discord
import discord.ext
from discord.ext import commands
from discord import app_commands


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

    def get_recent_matches(self, puuid, count: int, start_index: int = 0):
        print(self.region)
        match_ids = self.lol_watcher.match.matchlist_by_puuid(region=self.region, puuid=puuid, count=count,
                                                              start=start_index)
        return match_ids

    def build_match(self, match_id: str):
        match = self.lol_watcher.match.by_id(self.region, match_id)
        # print("test " + match['metadata']['dataVersion'])  # <-- access nested elements like this
        return match

    def get_item(self, item_id: int) -> cass.Item:
        items = cass.get_items(cass.Region.north_america)
        item_to_find = cass.Item(id=item_id, region=cass.Region.north_america)
        return items.find(item=item_to_find)

    def get_champ(self, champ_id: int) -> cass.Champion:
        champs = cass.get_champions(region=cass.Region.north_america)
        for champ in champs:
            if champ.id == champ_id:
                return champ
        # note cass has get_champions. But what is they key arg? It's not ID.
        # probably have to pass in some function that compares champ.id to champ_id



# major methods

    # get last x matches for each summoner puuid
    # iterate through and build kda, store as a summoner_history object
    # chart the kda's on one line chart
#TODO only include matches w/ 3 of us or more
#TODO when grouping multi summoners aggregate the match list so i don't request same match multiple times
    def individual_kda_chart(self, summoner_name):
        # first fill the psql table with new matches
        matches = self.get_matches(summoner_name, match_count=60)
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
        # now build out the kda averages over time. Each point is the cumulative kda average of the last 10 games
        sql_match_rows = self.psql.get_recent_100_matches()
        print("found " + str(len(sql_match_rows)) + " rows.")
        chart = league_chart.group_plot_kda(sql_match_rows, summoners)
        return chart



    def get_recap_history(self, summoner_name:str, champ_name: str):  #-> discord.Embed: Not working?
        matches = self.get_matches(summoner_name=summoner_name, match_count=60, start_index=0)
        champ = helpers.get_champ_by_partial_string(champ_name)[0]
        # pull the match history averages
        match_rows = self.psql.get_champ_history(summoner_name, champ)
        # Check that this summoner has played this champ in the recorded games
        if(len(match_rows) == 0):
            return "You sure you played that champ recently?"
        # build an embed. Show champ pic + name, (avg k/d/a, kda, total d/t/q/p), date of best match + kda d/t/q/p
        colors = {'Vierce': '#000000', 'The Great Ratsby': '#98c1d9', 'ComradeGiraffe': '#fca311',
                  'Gold Force': '#c01623'}
        embed = discord.Embed(color=discord.Color.from_str(colors[summoner_name]))
        profile_id = cass.get_summoner(id=self.get_puuid(summoner_name)).profile_icon
        profile_pic = cass.get_profile_icons(region=cass.Region.north_america).find(profile_id)
        embed.set_thumbnail(url=champ.image.url)
        embed.image = profile_pic

        # Totals stats
        kills, deaths, assists = match_rows[0]['kills'], match_rows[0]['deaths'], match_rows[0]['assists']
        deaths = 1 if deaths == 0 else deaths
        kda = round((float(kills) + float(assists)) / float(deaths), 2)
        multi_kills = f"DTQP: {match_rows[0]['doubles']} / {match_rows[0]['triples']} / {match_rows[0]['quadras']}" \
                      f" / {match_rows[0]['pentas']}"
        play_rate = str(round((self.psql.percent_played_champ(summoner_name, champ)["play_percent"] * 100), 2))

        description_string = f"**{summoner_name}** - **{champ.name}**\n(play-rate: {play_rate}%)\n\n"\
            f"Totals ({match_rows[0]['match_count']} matches):\n" \
            f"KDA:  **{kda}** ({kills}/{deaths}/{assists})\n" \
            f"{multi_kills}"

        # Best game stats
        best_game = self.psql.get_best_match(summoner_name=summoner_name, champion=champ)
        kills, deaths, assists = best_game[0]['kills'], best_game[0]['deaths'], best_game[0]['assists']
        deaths = 1 if deaths == 0 else deaths
        kda = round((float(kills) + float(assists)) / float(deaths), 2)
        multi_kills = f"DTQP: {best_game[0]['doubles']} / {best_game[0]['triples']} / {best_game[0]['quadras']}" \
                      f" / {best_game[0]['pentas']}"
        best_game_date = str(best_game[0]['date_created']).split(' ')[0]
        items = []
        for i in range(6):
            item_id = best_game[0][f'item_{i}']
            if item_id == 0:
                items.append("")
            else:
                item = self.get_item(item_id)
                tags = f"{item.tags[0]} / {item.tags[1]}" if len(item.tags) > 1 else f"{item.tags[0]}"
                items.append(f"**{item.name}** ---> *{tags}*")
        description_string += f"\n\n**Best game** ({best_game_date}):\n" \
            f"KDA:  **{kda}** ({kills}/{deaths}/{assists})\n" \
            f"{multi_kills}\n" \
            f"\n    {items[0]}  \n    {items[1]}  \n    {items[2]}  \n" \
            f"    {items[3]}  \n    {items[4]}  \n    {items[5]}"
#TODO: Add Win rate (would need to update the table. What else?
#TODO: Could set the Image for the embed to the champ, then the thumbnail to the Mythic item
        embed.add_field(name='', value=description_string, inline=False) # inline only affects Name, so doesn't work
        return embed


# Every request should probably start with get_matches to fill recent matches
    def get_matches(self, summoner_name, match_count: int, start_index: int = 0):
        puuid = self.get_puuid(summoner_name)
        match_ids = self.get_recent_matches(puuid=puuid, count=match_count, start_index=start_index)
        matches = []
#TODO: change the sql to an IN() statement contianing all matches, then do a python compare to determine
#TODO: which ones need to be added. This will allow me to not worry about the match index. It will add ones
#TODO: inside gaps.
        for match_id in match_ids:
            # only build match if it's not on table for summoner
            results = self.psql.get_specific_match(match_id, summoner_name)
            if len(results) > 0:
                print("hit a recorded match.")
                break  # stop looking - hit the most current recorded match
            matches.append(self.build_match(match_id))
            print(f"adding match... {match_id}")
        print(f"match list complete. Filling {str(len(matches))} matches.")
        for match in matches:
            self.fill_match_table(match, summoner_name)
        return matches


    def fill_match_table(self, match, summoner_name):
        id = match["metadata"]["matchId"]
        game_timestamp = datetime.utcfromtimestamp(int(match["info"]["gameCreation"])/1000.0)
        summoner_history = self.build_summoner_history_from_api_matches(summoner_name, [match])
        participant = helpers.get_matching_participant(self.get_puuid(summoner_name), match)
        self.psql.insert_match(id, summoner_name, summoner_history.kills, summoner_history.deaths,
                               summoner_history.assists, summoner_history.doubles, summoner_history.triples,
                               summoner_history.quadras, summoner_history.pentas, game_timestamp,
                               participant['item0'], participant['item1'], participant['item2'],
                               participant['item3'], participant['item4'], participant['item5'],
                               participant['championId'])


# actually only pass in one match at a time right now. Could update it to only accept one match
    def build_summoner_history_from_api_matches(self, summoner_name, matches: list):
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
        # print(str(summoner_history.kills) + "/" + str(summoner_history.deaths) + "/" + str(summoner_history.assists))
        return summoner_history
