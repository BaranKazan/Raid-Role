import interactions
import config
import requests

bot = interactions.Client(token=config.DISCORD_TOKEN)

@bot.command(
    name="get_role",
    description="Gives you the role you deserve depending on amount of raid clears",
    scope=config.GUILD_ID,
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
    url = f"https://www.bungie.net/Platform/Destiny2/SearchDestinyPlayer/-1/{username}/"
    payload = {}
    headers = {
        "x-api-key":config.BUNGIE_TOKEN
    }
    response = requests.request(method="GET", url=url, headers=headers, data=payload)
    print(response.content)


bot.start()
