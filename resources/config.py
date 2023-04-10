import os
from dotenv import load_dotenv

# Loads the environment variable. The method will search for .env file and load the environment
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
# Needs be changed on release
GUILD_ID = os.getenv("GUILD_ID")
BUNGIE_TOKEN = os.getenv("  BUNGIE_TOKEN")
