from discord.ext import commands
import discord
from discord import app_commands
import discord.ext


class BabyView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.score = None

    @discord.ui.button(label="1", style=discord.ButtonStyle.red)
    async def one(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.score = 1
        print("scored 1")
        self.stop()

    @discord.ui.button(label="2", style=discord.ButtonStyle.red)
    async def two(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.score = 2
        print("scored 2")
        self.stop()