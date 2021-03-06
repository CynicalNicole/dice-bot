import discord
from discord.ext import commands
import asyncio
import sys

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["stop"])
    @commands.is_owner()
    async def shutdown(self, ctx):
        await self.bot.logout()
        await self.bot.close()
        sys.exit()

def setup(client):
    client.add_cog(admin(client))