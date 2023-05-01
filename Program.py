import Commands
import discord
import DiscordClient
import threading
import asyncio


on_pi = True

# I just changed this to test pulling to the pi via ssh

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
command_module = Commands.SlashCommands(active_client)
tree = command_module.set_up(active_client)
active_client.receive_tree(tree)


active_client.tree.add_command(command_module)


if __name__ == "__main__":
    active_client.run(token)


# @active_client.event
# def hello():
#     print('hello')
#     print(active_client.on_load(active_client))
#

# asyncio.run(active_client.on_load())
# # thread = threading.Thread(target=active_client.on_load)
# # thread.start()