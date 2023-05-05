import discord
from discord.ext import commands
from discord import app_commands
import discord.ext
import subprocess
import helpers
from LeagueModels import league_api
import Baby.baby


# League
class Lol(app_commands.Group):
    def __init__(self, discord_bot: discord.ext.commands.Bot):
        super().__init__()
        global bot
        bot = discord_bot




    @app_commands.command(name="recap", description="Get a recap of your history with a champ")
    async def recap(self, interaction: discord.Interaction):
        await interaction.response.send_message("in development")

    @app_commands.command(name="test")
    async def test(self, interaction: discord.Interaction):
        summoner = league_api.LeagueAPI.get_summoner("Vierce")
        await interaction.response.send_message()






# Other
class OtherCommands(app_commands.Group):
    def __init__(self, bot: discord.ext.commands.Bot):
        super().__init__()
        self.bot = bot


    @app_commands.command(name="hello")
    async def say_hello(self, interaction: discord.Interaction):
        print('saying hello')
        await interaction.response.send_message("hello")


    @app_commands.command(name="start_program", description="starts a program") # need to check if user=me
    async  def start_program(self, interaction: discord.Interaction, name: str, start: bool):
        if interaction.user.id != 322164425002057728:
            await interaction.response.send_message("unauthorized!")
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


    @app_commands.command(name="baby_name", description="get specific baby name")
    async def baby_name(self, interaction: discord.Interaction, name: str):
        search_results = helpers.google_search(search_term=name + " girl's name origin", num_results=1)
        await interaction.response.send_message(search_results)


    @app_commands.command(name="todays_baby_name", description="gives today's baby name")
    async def todays_baby_name(self, interaction: discord.Interaction):
        name = Baby.baby.BabyStuff.get_todays_name()
        search_results = helpers.google_search(search_term= name + " girl's name origin", num_results=1)
        await interaction.response.send_message("Name: " + name + search_results)



