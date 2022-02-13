import os

import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option

client = commands.Bot(command_prefix="/")
slash = SlashCommand(client, sync_commands=True)

@client.event
async def on_ready():
    print(f"{client.user} is initiated!")

@slash.slash(name="hello",
             description="Sends Hello message!")
async def _hello(ctx:SlashContext):
    await ctx.send("Hello!")

client.run(os.getenv("TOKEN"))