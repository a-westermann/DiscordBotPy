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






# @tree.command()  # add guild id here as arg
# async def slash_command(interaction: discord.Interaction, number: int, string: str):  # example args
#     print('slash command')
#     await interaction.response.send_message("hello there")
#
# active_client.tree.add_command(command_module)