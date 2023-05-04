import datetime
import discord.ext
import Commands
import discord
from discord import app_commands
import DiscordClient
import threading
import asyncio
from LeagueModels import League_API


on_pi = True


def create_client():
    intents = discord.Intents.default()
    intents.message_content = True
    client = DiscordClient.Client(intents=intents)
    return client


def get_token(in_rasp_pi):
     path_to_token = "H:\\Coding\Python Projects\DiscordBot\\token.txt" if in_rasp_pi == False \
         else "/home/andweste/Scripts/token.txt"
     return open(path_to_token).read()


active_client = create_client()
token = get_token(on_pi)
# guilds = active_client.get_guilds(on_pi)
tree = app_commands.CommandTree(active_client)
active_client.receive_tree(tree)

active_client.tree.add_command(Commands.OtherCommands(active_client))
active_client.tree.add_command(Commands.Lol(active_client))

# set up league api
token = open("/home/andweste/Scripts.league_token.txt").read()
league_api = League_API.LeagueAPI(token)


if __name__ == "__main__":
    active_client.run(token)
