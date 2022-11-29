from discord.ext import commands
from discord import app_commands, Color
import discord
from mcrcon import MCRcon


class WhitelistCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="whitelist-list", description="List whitelisted players")
    async def whitelist_list(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if interaction.user.get_role(self.bot.config["whitelist-role"]) is not None:
            embed = discord.Embed(
                title="List of whitelisted players", color=Color.blue())
            for server_name, server in self.bot.config["whitelist"].items():
                with MCRcon(server["ip"], server["password"]) as mcr:
                    resp = mcr.command("/whitelist list")
                    resp = resp.split(":")[1]
                    embed.add_field(name=server_name, value=resp, inline=False)
        else:
            embed = discord.Embed(
                title="Error", description="you do not have enough permissions", color=Color.red())
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="whitelist-add", description="Add player to whitelist")
    async def whitelist_add(self, interaction: discord.Interaction, player: str):
        await interaction.response.defer()
        if interaction.user.get_role(self.bot.config["whitelist-role"]) is not None:
            for server_name, server in self.bot.config["whitelist"].items():
                with MCRcon(server["ip"], server["password"]) as mcr:
                    resp = mcr.command(f"/whitelist add {player}")
                    if server["op"] and (("Added" in resp) or ("already" in resp)):
                        resp = mcr.command(f"/op {player}")
            if "not exist" in resp:
                embed = discord.Embed(
                    title="Add Player to Whitelist", description="error in one or more servers", color=Color.red())
            else:
                embed = discord.Embed(
                    title="Add Player to Whitelist", description=f"Added {player} to whitelist successfully", color=Color.green())
        else:
            embed = discord.Embed(
                title="Error", description="you do not have enough permissions", color=Color.red())
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="whitelist-remove", description="Remove player from whitelist")
    async def whitelist_remove(self, interaction: discord.Interaction, player: str):
        await interaction.response.defer()
        if interaction.user.get_role(self.bot.config["whitelist-role"]) is not None:
            for server_name, server in self.bot.config["whitelist"].items():
                with MCRcon(server["ip"], server["password"]) as mcr:
                    resp = mcr.command(f"/whitelist remove {player}")
                    if server["op"] and (("Removed" in resp) or ("not" in resp)):
                        resp = mcr.command(f"/deop {player}")
            if "not exist" in resp:
                embed = discord.Embed(
                    title="Remove Player to Whitelist", description="error in one or more servers", color=Color.red())
            else:
                embed = discord.Embed(
                    title="Remove Player to Whitelist", description=f"Removed {player} from whitelist successfully", color=Color.green())
        else:
            embed = discord.Embed(
                title="Error", description="you do not have enough permissions", color=Color.red())
        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(WhitelistCog(bot))
