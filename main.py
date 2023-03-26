import interactions
import config
import requests
import urllib.parse

from InvalidUser import InvalidUser

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
    try:
        destiny_membership_id = await get_bungie_id(username)
    except InvalidUser as e:
        await ctx.send(e.args[0])
    raid_clears = await get_raid_clears(destiny_membership_id)
    await ctx.send(f"Total amount of Raid Clears: {raid_clears}")


async def get_bungie_id(username):
    url = f"https://www.bungie.net/Platform/Destiny2/SearchDestinyPlayer/-1/{urllib.parse.quote(username)}/"
    headers = {
        "x-api-key":config.BUNGIE_TOKEN,
    }
    response = requests.request(method="GET", url=url, headers=headers)
    response_json = response.json()["Response"]
    if not response_json:
        raise InvalidUser("The user does not exist")

    user_data = None
    for x in response_json:
        membership_type = x["membershipType"]
        if membership_type == 3:
            user_data = x
            break
        user_data = x

    return(user_data["membershipId"])

async def get_raid_clears(membership_id):
    url = f"https://api.raidreport.dev/raid/player/{membership_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    response = requests.request(method="GET", url=url, headers=headers)
    activities = response.json()["response"]["activities"]

    total_clears = 0
    for activity in activities:
        total_clears += activity["values"]["clears"]

    return total_clears

if __name__ == "__main__":
    bot.start()