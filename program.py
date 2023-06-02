import datetime
import discord.ext
import commands
import discord
from discord import app_commands
import discord_client
import threading
import asyncio
from LeagueModels import league_api


on_pi = True


def create_client():
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord_client.Client(intents=intents)
    return client


def get_token(in_rasp_pi):
     path_to_token = "H:\\Coding\Python Projects\DiscordBot\\token.txt" if in_rasp_pi == False \
         else "/home/andweste/Scripts/token.txt"
     print("token =  " + open(path_to_token).read())
     return open(path_to_token).read()


active_client = create_client()
token = get_token(on_pi)
# guilds = active_client.get_guilds(on_pi)
tree = app_commands.CommandTree(active_client)
active_client.receive_tree(tree)

active_client.tree.add_command(commands.OtherCommands(active_client))

# set up league command module & league_api
try:
    league_token = open("/home/andweste/Tokens/secret_creds_repo/token_league.txt").read()
except Exception as e:
    print("Error: " + str(e))
    league_token = ""
active_client.tree.add_command(commands.Lol(active_client, league_token))



if __name__ == "__main__":
    active_client.run(token)
