import interactions
import requests
import urllib.parse
from resources import *

bot = interactions.Client(token=config.DISCORD_TOKEN)
role_names = [
    "Raid Master",
    "Raid Adept",
    "Raid Expert",
    "Raid Beginner"
]


@bot.command(
    name="create_role",
    description="Creates the Roles in the Discord Server",
    scope=config.GUILD_ID,
)
async def create_role(ctx: interactions.CommandContext):
    print("Receiving create_role request")
    if await check_if_role_exists_in_guild(await ctx.guild.get_all_roles()):
        await ctx.send("One or more roles already exists")
    else:
        for role in role_names:
            await ctx.guild.create_role(name=role)
        await ctx.send("The role has been created")
    print("Successful execution")


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
    print("Receiving get_role request")
    await ctx.defer()
    try:
        if await check_if_role_exists_in_guild(await ctx.guild.get_all_roles()) is False:
            raise RoleException("The roles does not exist, create the roles by doing /create_role")

        destiny_membership_id = await get_bungie_id(username)
        raid_clears = await get_raid_clears(destiny_membership_id)
        role = await give_role(ctx, raid_clears)
        await ctx.send(f"Total amount of Raid Clears: {raid_clears} \nYou earned the title: {role.name}")
        print("Successful execution")
    except (InvalidUser, APIException, RoleException) as e:
        await ctx.send(e.args[0])


async def get_bungie_id(username):
    url = f"https://www.bungie.net/Platform/Destiny2/SearchDestinyPlayer/-1/{urllib.parse.quote(username)}/"
    headers = {
        "x-api-key": config.BUNGIE_TOKEN,
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

    return user_data["membershipId"]


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


async def check_if_role_exists_in_guild(guild_roles: list[interactions.Role]):
    guild_role_names = [x.name for x in guild_roles]
    result = any(role in guild_role_names for role in role_names)
    return result


async def give_role(ctx: interactions.CommandContext, raid_clears: int):
    guild_roles = await ctx.guild.get_all_roles()
    matching_guild_role = [x for x in guild_roles if x.name in role_names]

    for role in matching_guild_role:
        await ctx.author.remove_role(role)

    role = None
    if raid_clears >= 100:
        role = search_role(matching_guild_role, role_names[0])
        await ctx.author.add_role(role)
    elif raid_clears >= 25:
        role = search_role(matching_guild_role, role_names[1])
        await ctx.author.add_role(role)
    elif raid_clears >= 10:
        role = search_role(matching_guild_role, role_names[2])
        await ctx.author.add_role(role)
    elif raid_clears >= 1:
        role = search_role(matching_guild_role, role_names[3])
        await ctx.author.add_role(role)
    else:
        raise RoleException("The user has not completed any raid")
    return role


def search_role(roles: list[interactions.Role], name: str):
    return next(x for x in roles if x.name == name)


if __name__ == "__main__":
    bot.start()
