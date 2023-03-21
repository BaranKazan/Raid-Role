import interactions
from config import *
import requests

bot = interactions.Client(token=DISCORD_TOKEN)

@bot.command(
    name="get_role",
    description="Gives you the role you deserve depending on amount of raid clears",
    scope=GUILD_ID,
    options=[
        interactions.Option(
            name="username",
            description="Bungie username with hashtag numbers after",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def get_role(ctx: interactions.CommandContext, username: str):
    await ctx.send(username)
    destiny_membership_id = await get_bungie_id(username)


async def get_bungie_id(username):
    print(username)


bot.start()
