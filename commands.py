import datetime
import asyncio
import Baby.baby_view
import LeagueModels.league_api
import discord
from discord.ext import commands
from discord import app_commands
import discord.ext
import subprocess
import helpers
from LeagueModels import league_api
from Baby import baby, baby_view, baby_chart
import psql


# League
class Lol(app_commands.Group):
    def __init__(self, bot: commands.Bot, token):
        super().__init__()  # this is to call the parent class's __init__() (parentclass=app_commands.Group)
        self.psql = psql.PSQL()
        if token != "":
            self.token = token
            self.league_api = league_api.LeagueAPI(token, self.psql)
        self.bot = bot


    @app_commands.command(name="test")
    async def test(self, interaction: discord.Interaction):
        if self.token == "":
            await interaction.response.send_message("token invalid")
            return
        # summoner = self.league_api.get_summoner("Vierce")
        self.psql.get_summoner_matches("Vierce")
        # await interaction.response.send_message(str(summoner))



    @app_commands.command(name="summoner_kda_chart", description="see your recent kda changes")
    async def summoner_kda_chart(self, interaction: discord.Interaction, summoner_first_letter: str):
        if self.token == "":
            await interaction.response.send_message("token invalid")
            return
        await interaction.response.defer()  # ensures bot has enough time to answer
        summoner_name = helpers.get_summoner_name_from_first_letter(summoner_first_letter)
        # kda is a place holder. Will eventually return a line chart for all 4 boyz
        chart = self.league_api.individual_kda_chart(summoner_name)
        embed = discord.Embed(color=discord.Color.from_str(r"#FFD700"))
        embed.set_image(url="attachment://kda_chart.png")
        embed.description = "*each point is the kda average from the last 10 games played from that match"
        await interaction.followup.send(embed=embed, file=chart)


    @app_commands.command(name="kda_chart", description="see kda's over time for boys")
    async  def kda_chart(self, interaction: discord.Interaction):
        if self.token == "":
            await interaction.response.send_message("token invalid")
            return
        await interaction.response.defer()  # ensures bot has enough time to answer
        # kda is a place holder. Will eventually return a line chart for all 4 boyz
        chart = self.league_api.group_kda_chart()
        embed = discord.Embed(color=discord.Color.from_str(r"#FFD700"))
        embed.set_image(url="attachment://kda_chart.png")
        embed.description = "*each point is the kda average from the last 10 games played from that match"
        await interaction.followup.send(embed=embed, file=chart)



    # @app_commands.command(name="recap", description="Get a recap of your history with a champ")
    # async def recap(self, interaction: discord.Interaction):
    #     if self.token == "":
    #         await interaction.response.send_message("token invalid")
    #         return
    #     await interaction.response.send_message("in development")


    # @app_commands.command(name="chart", description="See a chart of recent match history for the boys")





# Other
class OtherCommands(app_commands.Group):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        # self.client = client
        self.baby = Baby.baby.BabyStuff(self)


    @app_commands.command(name="ping")
    async def say_hello(self, interaction: discord.Interaction):
        print('pinging server')
        await interaction.response.send_message("ultra low latency")


    @app_commands.command(name="start_program", description="starts a program") # need to check if user=me
    async  def start_program(self, interaction: discord.Interaction, name: str, start: bool):
        if helpers.check_user(interaction, ["Vierce"]) is False:
            await interaction.response.send_message("Unauthorized")
            return
        try:
            if start == True:
                file_dirs = {"qbittorrent" : "C:\\Program Files\qBittorrent\qbittorrent.exe" ,
                             "league" : "C:\\Riot Games\League of Legends\LeagueClient.exe" ,
                             }
                subprocess.Popen([file_dirs[name]])
            else:
                await interaction.response.send_message("stop not available yet")
            await interaction.response.send_message("complete")
        except:
            await interaction.response.send_message("failed")


    @app_commands.command(name="baby_name", description="get specific baby name's origin")
    async def baby_name(self, interaction: discord.Interaction, name: str):
        if helpers.check_user(interaction, ["Vierce", "Naiyvara"]) is False:
            await interaction.response.send_message("Unauthorized")
            return
        search_results = helpers.google_search(search_term=name + " girl's name origin", num_results=1)
        await interaction.response.send_message(search_results)


    @app_commands.command(name="todays_baby_name", description="gives today's baby name. Times are midnight, noon, 5pm")
    async def todays_baby_name(self, interaction: discord.Interaction):
        if helpers.check_user(interaction, [ "Vierce", "Naiyvara"]) is False:
            await interaction.response.send_message("Unauthorized")
            return
        await interaction.response.defer()  # ensures bot has enough time to answer
        self.baby.backup_used_names()  # back up the file first
        name, got_new_name = await self.baby.get_todays_name()
        print(str(name).strip() + " = name")
        print(str(got_new_name) + " got new name")
        search_results = ""
        try:
            search_results = helpers.google_search(search_term= name + " girl's name origin", num_results=1)
        except:
            search_results = "google rejected the search"
        regave_name = "" if got_new_name else " (this name was already chosen) "
        message_content = "Name: " + name + regave_name + "\n" + search_results
        await interaction.response.send_message(message_content)
        if got_new_name:
            await asyncio.sleep(1)
            view = Baby.baby_view.BabyView(self.baby, str(name).strip(), "Ashley", interaction)
            await interaction.followup.send("Ashley\nRate the name: ", view=view)
            view = Baby.baby_view.BabyView(self.baby, str(name).strip(), "Andrew", interaction)
            await interaction.followup.send("Andrew\nRate the name: ", view=view)


    @app_commands.command(name="baby_name_summary", description="get the top rated names")
    async def baby_name_summary(self, interaction: discord.Interaction):
        # embed = discord.Embed(color=discord.Color.from_str(r"#FFD700"), title="Top choices",
        #                       description="This is a test embed" )
        # embed.set_thumbnail(url="http://clipart-library.com/img/1751191.png")
        # await interaction.response.send_message(embed=embed)
        chart = baby_chart.get_baby_venn()
        embed = discord.Embed(color=discord.Color.from_str(r"#FFD700"))
        embed.set_image(url="attachment://names_diagram.png")
        await interaction.response.send_message(embed=embed, file=chart)



    @app_commands.command(name="backfill_baby_scores", description="fill in any name scores you missed")
    async def backfill_baby_scores(self, interaction: discord.Interaction):
        # pops up a baby_view for one name for the user that commanded, waits for a score, moves on to the next one
        command_user = helpers.get_user_name(interaction)
        users_real_name = helpers.get_name(command_user)
        # get the used names list as-is. Make a backup first
        self.baby.backup_used_names()
        used_names_file = open("used_names.txt", "r").readlines()
        # find all the 0 names for the user
        score_index = 1 if users_real_name == "Ashley" else 2
        rescore_names = []
        for line in used_names_file[2:]:
            if line.split(';')[score_index] == str(0):
                rescore_names.append(line.split(';')[0])
        # now I need to have this method wait on the view to trigger a proceed

        view = Baby.baby_view.BabyView(self.baby, str(name).strip(), users_real_name, interaction)

