import discord
from discord.ext import commands
from discord import app_commands


class SlashCommands(app_commands.Group):
    def __init__(self, bot: discord.ext.commands.Bot):
        super().__init__()
        self.bot = bot


    def set_up(self, client):
        tree = app_commands.CommandTree(client)
        return tree


# commands
    @app_commands.command()
    async def say_hello(self, interaction: discord.Interaction):
        print('saying hello')
        await interaction.response.send_message("hello")
    # async def say_hi(context, user_name):
    #     context.send('hi', user_name)
