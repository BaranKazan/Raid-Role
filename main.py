import interactions
import config
import requests
import urllib.parse

from Exceptions import InvalidUser, APIException, RoleException

bot = interactions.Client(token=config.DISCORD_TOKEN)
roles_name = [
    "a",
    "b",
    "c",
    "d"
    "e"
]

@bot.command(
    name="create_role",
    description="Creates the Roles in the Discord Server",
    scope=config.GUILD_ID,
)
async def create_role(ctx: interactions.CommandContext):
    guild = await ctx.get_guild()
    if await check_if_role_exists(guild):
        await ctx.send("The roles already exists")
    else:
        await ctx.send("Creating the roles...")

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
        if await check_if_role_exists(await ctx.get_guild()) is False:
            raise RoleException("The roles does not exist, create the roles by doing /create_role")

        destiny_membership_id = await get_bungie_id(username)
        raid_clears = await get_raid_clears(destiny_membership_id)
        await ctx.send(f"Total amount of Raid Clears: {raid_clears}")
    except (InvalidUser, APIException, RoleException) as e:
        await ctx.send(e.args[0])


async def get_bungie_id(username):
    url = f"https://www.bungie.net/Platform/Destiny2/SearchDestinyPlayer/-1/{urllib.parse.quote(username)}/"
    headers = {
        "x-api-key":config.BUNGIE_TOKEN,
    }

    response = requests.request(method="GET", url=url, headers=headers)
    if response.status_code != 200:
        raise APIException("Something is wrong with Bungie API, servers might be down.")
    response_json = response.json()["Response"]
    if not response_json:
        raise InvalidUser("The user does not exist.")

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
    if response.status_code != 200:
        raise APIException("The API is down, contact the Developer!")
    activities = response.json()["response"]["activities"]

    total_clears = 0
    for activity in activities:
        total_clears += activity["values"]["clears"]
    return total_clears

async def check_if_role_exists(guild: interactions.Guild):
    guild_roles = await guild.get_all_roles()
    guild_role_names = [x.name for x in guild_roles]
    return all(role in roles_name for role in guild_role_names)


if __name__ == "__main__":
    bot.start()