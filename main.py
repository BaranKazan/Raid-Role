import interactions
from config import *
import os

bot = interactions.Client(token=DISCORD_TOKEN)

@bot.command(
    name="my_first_command",
    description="This is the first command I made!",
    scope=GUILD_ID,
)
async def my_first_command(ctx: interactions.CommandContext):
    await ctx.send("Hi there!")

bot.start()