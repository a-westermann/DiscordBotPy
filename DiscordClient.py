import discord


class Client(discord.Client):
    def on_load(self):
        return 'loading...'


    def receive_tree(self, command_tree):
        self.tree = command_tree


    async def on_ready(self):
        await self.tree.sync()
        print(f'Hedonism bot has entered the chat')

