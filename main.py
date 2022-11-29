import discord
from discord.ext import commands
import json

f = open("config.json")


class client(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=discord.Intents.default()
        )
    config = json.load(f)

    async def setup_hook(self):
        await self.load_extension("whitelist_ext")


client().run(
    client.config["token"])
