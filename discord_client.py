import discord


class Client(discord.Client):
    def on_load(self):
        return 'loading...'


    def receive_tree(self, command_tree):
        self.tree = command_tree


    async def on_ready(self):
        # guild = discord.utils.find(lambda g: g.name == "bot tester", self.guilds)
        # print(guild)
        await self.tree.sync()
        print(f'Hedonism bot has entered the chat')


    # async def get_guilds(self, in_rasp_pi):
    #     path_to_guilds = "H:\\Coding\Python Projects\DiscordBot\\guild_ids.txt" if in_rasp_pi == False else "guild_ids.txt"
    #     list = open(path_to_guilds).readlines()
    #     id_array = []
    #     for id in list:
    #         guild_id = await self.get_guild(id)
    #         id_array.append(guild_id)
    #         print(guild_id)
    #         print(id_array)
    #     return id_array

