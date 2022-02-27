import os

import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

client = commands.Bot(command_prefix="/")
slash = SlashCommand(client, sync_commands=True)


@client.event
async def on_ready():
    print(f"{client.user} is initiated!")


@slash.slash(name="get_role",
             description="Get your raid role by typing in your Bungie id",
             options=[
                 create_option(
                     name="username",
                     description="Type in your Bungie username, including the numbers after #",
                     required=True,
                     option_type=3
                 )
             ]
             )
async def _get_role(ctx: SlashContext, username: str):
    await ctx.send(username)


client.run(os.getenv("TOKEN"))
