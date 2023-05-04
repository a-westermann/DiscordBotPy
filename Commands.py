import discord
from discord.ext import commands
from discord import app_commands
import discord.ext
import subprocess
import helpers
import datetime
import random
from LeagueModels import League_API



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
        summoner = League_API.LeagueAPI.get_summoner("Vierce")
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
        name = self.get_todays_name()
        search_results = helpers.google_search(search_term= name + " girl's name origin", num_results=1)
        await interaction.response.send_message("Name: " + name + search_results)

    def get_todays_name(self):
        #check date to see if gave one already
        today = str(datetime.date.today())
        used_names_file = open("/home/andweste/Scripts/used_names.txt", "r")
        last_date = str(used_names_file.readline().rstrip())
        print("prev date = " + last_date)
        print("today = " + today)
        if today == last_date:
            # if so, give bottom name from used_names file
            line = ""
            for name in used_names_file:
                line = name
                pass
            last_name = line
            print("Already got a name today. Name =" + last_name)
            return last_name
        else: # if not, pull random name from file, remove it, and add to alt file
            names_list_file = open("/home/andweste/Scripts/girl_names.txt", "r")
            name_list = names_list_file.readlines()
                #read().split("\n")
            todays_name = random.choice(name_list)
            print("today's name = " + todays_name)
            # now remove the name from list and write to the file
            name_list.remove(todays_name)
            names_list_file = open("/home/andweste/Scripts/girl_names.txt", "w") # opening in write mode clears file
            for name in name_list:
                names_list_file.write(f"{name}")
            # finally, add the new name to the bottom of the used_names file
            used_names_file = open("/home/andweste/Scripts/used_names.txt", "r") # open in read, then overwrite all
            used_names_text = used_names_file.read()
            used_names_text = used_names_text.replace(last_date, today)
            used_names_file = open("/home/andweste/Scripts/used_names.txt", "w")
            used_names_file.writelines(used_names_text)
            used_names_file = open("/home/andweste/Scripts/used_names.txt", "a") # open in append mode to add name
            used_names_file.write(todays_name)
        return todays_name



