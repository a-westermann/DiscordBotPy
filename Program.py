import discord
import DiscordClient
import threading
import asyncio


on_pi = False


def create_client():
    intents = discord.Intents.default()
    intents.message_content = True
    client = DiscordClient.Client(intents=intents)
    return client


def get_token(in_rasp_pi):
     path_to_token = "H:\\Coding\Python Projects\DiscordBot\\token.txt" if in_rasp_pi == False else "token.txt"
     return open(path_to_token).read()


active_client = create_client()
token = get_token(on_pi)
active_client.run(token)


# @active_client.event
# def hello():
#     print('hello')
#     print(active_client.on_load(active_client))
#

# asyncio.run(active_client.on_load())
# # thread = threading.Thread(target=active_client.on_load)
# # thread.start()