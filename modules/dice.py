import discord
from discord.ext import commands
import asyncio

import re
import random
import json

class dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['r'])
    async def roll(self, ctx, rollString : str):
        diceResult = self.rollDice(rollString)

        if (diceResult != None):
            await ctx.channel.send("{user}: {roll}".format(user = ctx.author.mention, roll = diceResult))
        else:
            await ctx.channel.send("Invalid dice string.")

    def rollDice(self, rollString : str):
        #breaks rollString into matches of [1][d4][+2]
        matches = re.search(r'(^\d{1})([d][^+-]+)([+-]\d+)?', rollString)
        
        if matches == None:
            return None

        simpleDiceMatch = re.search(r'[d](\d+)$', matches.group(2))

        rollResult = None
        if (simpleDiceMatch != None):
            rollResult = self.calculateSimpleDiceRoll(int(matches.group(1)), int(simpleDiceMatch.group(1)), matches.group(3))
        else:
            rollResult = self.calculateAdvancedDiceRoll(int(matches.group(1)), matches.group(2), matches.group(3))

        rollOutput = "`{roll}` = ({rolls}){mod} = {total}"
        rollOutput = rollOutput.format(roll = rollString, rolls = rollResult[1], mod = matches.group(3), total = rollResult[2])
        print(rollOutput)
        return rollOutput
    

    def calculateSimpleDiceRoll(self, count : int, maxRoll : int, modifier : str):
        rolls = []

        for _ in range(count):
            rolls.append(random.randint(1, maxRoll))

        rollString = ", ".join(str(element) for element in rolls)
        rollTotal = self.applyMod(sum(rolls), modifier)

        return (rolls, rollString, rollTotal)

    def calculateAdvancedDiceRoll(self, count : int, diceType : str, modifier : str):
        diceInfo = {}
        with open('config/dice.json', 'r') as diceJson:
            knownDice = json.load(diceJson)
            diceInfo = knownDice[diceType]

        rolls = []
        for _ in range(count):
            rolls.append(random.randint(diceInfo['min'], diceInfo['max']))

        rollValues = map(str, rolls)
        rollValues = [diceInfo["stringFormatting"].get(n, n) for n in rollValues]
        rollString = "{sep}".join(rollValues)
        rollString = rollString.format(sep = diceInfo["separator"])

        rollTotal = self.applyMod(sum(rolls), modifier)

        return (rolls, rollString, rollTotal)

    def applyMod(self, total : int, modifier : str):
        mod = 0
        if modifier != None:
            mod = int(modifier)

        return total + mod

def setup(client):
    client.add_cog(dice(client))