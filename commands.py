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
from Baby import baby, baby_view



# League
class Lol(app_commands.Group):
    def __init__(self, bot: commands.Bot, token):
        super().__init__()  # this is to call the parent class's __init__() (parentclass=app_commands.Group)
        if token != "":
            self.token = token
            self.league_api = league_api.LeagueAPI(token)
        self.bot = bot

    @app_commands.command(name="test")
    async def test(self, interaction: discord.Interaction):
        if self.token == "":
            await interaction.response.send_message("token invalid")
            return
        summoner = self.league_api.LeagueAPI.get_summoner("Vierce")
        await interaction.response.send_message()



    @app_commands.command(name="recap", description="Get a recap of your history with a champ")
    async def recap(self, interaction: discord.Interaction):
        if self.token == "":
            await interaction.response.send_message("token invalid")
            return
        await interaction.response.send_message("in development")





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
        name, got_new_name = await self.baby.get_todays_name()
        print(str(name).strip() + " = name")
        print(str(got_new_name) + " got new name")
        search_results = helpers.google_search(search_term= name + " girl's name origin", num_results=1)
        regave_name = "" if got_new_name else " (this name was already chosen) "
        message_content = "Name: " + name + regave_name + "\n" + search_results
        await interaction.response.send_message(message_content)
        if got_new_name:
            await asyncio.sleep(1)
            view = Baby.baby_view.BabyView(self.baby, str(name).strip(), "Ashley", interaction)
            await interaction.followup.send("Ashley\nRate the name: ", view=view, timeout=5)
            view = Baby.baby_view.BabyView(self.baby, str(name).strip(), "Andrew", interaction)
            await interaction.followup.send("Andrew\nRate the name: ", view=view)


    @app_commands.command(name="baby_name_summary", description="get the top rated names")
    async  def baby_name_summary(self, interaction: discord.Interaction):
        await interaction.response.send_message("")


