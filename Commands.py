import discord
from discord.ext import commands
from discord import app_commands
import subprocess
from googlesearch import search
import datetime


class OtherCommands(app_commands.Group):
    def __init__(self, bot: discord.ext.commands.Bot):
        super().__init__()
        self.bot = bot


    def set_up(self, client):
        self.tree = app_commands.CommandTree(client)
        return self.tree


# General functions
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
        name = self.get_todays_name()
        await interaction.response.send_message(self.google_search(name + "girl's name origin"))

    def get_todays_name(self):
        #check date to see if gave one already
        today = str(datetime.date.today())
        used_names_file = open("/home/andweste/Scripts/used_names.txt", "r")
        last_date = str(used_names_file.readline())
        if today == last_date:
            # if so, give bottom name from used_names file
            for line in used_names_file:
                pass
            last_name = line
        #if not, pull random name from file, remove it, and add to alt file
        else:
            names_list_file = open("/home/andweste/Scripts/girl_names.txt", "r")
            name_list = names_list_file.readlines()
            todays_name = random.choice(names_list)
            # now remove the name from list and write to the file
            name_list.remove(todays_name)
            names_list_file = open("/home/andweste/Scripts/girl_names.txt", "w") # opening in write mode clears file
            for name in name_list:
                names_list_file.write(f"{name}\n")
            # finally, add the new name to the bottom of the used_names file
            used_names_file = open("/home/andweste/Scripts/used_names.txt", "a") # append mode
            used_names_file.write(todays_name)


