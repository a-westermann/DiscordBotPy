import discord
from discord.ext import commands
from discord import app_commands
import subprocess
from googlesearch import search


class OtherCommands(app_commands.Group):
    def __init__(self, bot: discord.ext.commands.Bot):
        super().__init__()
        self.bot = bot


    def set_up(self, client):
        self.tree = app_commands.CommandTree(client)
        return self.tree


    def google_search(self, search_term):
        for url in search(search_term, num_results=1):
            return url


# commands
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


    @app_commands.command(name="baby_name", description="gives today's baby name")
    async def baby_name(self, interaction: discord.Interaction):
        #check date to see if gave one already
        #if so, give bottom name from alt file
        #if not, pull random name from file, remove it, and add to alt file
        await interaction.response.send_message(self.google_search("evelyn" + "girl's name origin"))