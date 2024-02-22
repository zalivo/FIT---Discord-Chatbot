import os
from discord import Intents, Client, Message
from dotenv import load_dotenv

# LOAD OUR TOKEN
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

# BOT STARTUP
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')

client.run(TOKEN)

# MAIN
def main() -> None:
    client.run(TOKEN)

if __name__ == '__main__':
    main()