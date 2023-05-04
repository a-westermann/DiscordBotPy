import datetime
import discord.ext
import Commands
import discord
import DiscordClient
import threading
import asyncio


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
command_module = Commands.Commands(active_client)


# lol_group = discord.ext.commands.Bot.create_group("lol")
# other_group = discord.ext.commands.Bot.create_group("other")
tree = command_module.set_up(active_client)
active_client.receive_tree(tree)

@command_module.bot.group(name='other', invoke_without_command=True)
async def other(self, interaction:discord.Interaction):
    pass
@command_module.bot.group(name='lol', invoke_without_command=True)
async def lol(self, interaction:discord.Interaction):
    pass


active_client.tree.add_command(command_module)
active_client.tree.add_command(Commands.Lol(active_client))

if __name__ == "__main__":
    active_client.run(token)
