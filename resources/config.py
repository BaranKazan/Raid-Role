import os
from dotenv import load_dotenv

#Load the enviorment variables below
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
# Needs be changed on release
GUILD_ID = os.getenv("GUILD_ID")
BUNGIE_TOKEN = os.getenv("  BUNGIE_TOKEN")