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

    @discord.ui.button(label="3", style=discord.ButtonStyle.red)
    async def three(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.score = 3
        print("scored 3")
        self.stop()

    @discord.ui.button(label="4", style=discord.Button.style.blurple)
    async def four(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.score = 4
        print("scored 4")
        self.stop()

    @discord.ui.button(label="5", style=discord.ButtonStyle.blurple)
    async def five(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.score = 5
        print("scored 5")
        self.stop()

    @discord.ui.button(label="6", style=discord.ButtonStyle.blurple)
    async def six(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.score = 6
        print("scored 6")
        self.stop()

    @discord.ui.button(label="7", style=discord.ButtonStyle.green)
    async def seven(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.score = 7
        print("scored 7")
        self.stop()

    @discord.ui.button(label="8", style=discord.ButtonStyle.green)
    async def eight(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.score = 8
        print("scored 8")
        self.stop()

    @discord.ui.button(label="9", style=discord.ButtonStyle.green)
    async def nine(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.score = 9
        print("scored 9")
        self.stop()

    @discord.ui.button(label="10", style=discord.ButtonStyle.green)
    async def ten(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.score = 10
        print("scored 10")
        self.stop()