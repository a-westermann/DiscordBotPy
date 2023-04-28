import discord


class Client(discord.Client):
    def on_load(self):
        return 'loading...'

    async def on_ready(self):
        print(f'Hedonism bot has entered the chat')