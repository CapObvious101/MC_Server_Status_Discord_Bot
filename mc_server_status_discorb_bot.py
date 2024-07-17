import os
from dotenv import load_dotenv
from discord import Intents, Client
import json
import asyncio
import aiohttp  

# Load token
load_dotenv()
TOKEN = os.getenv('Discord_Token')

# Setup
intents = Intents.default()
intents.messages = True
client = Client(intents=intents)

async def api_fetch():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.mcsrvstat.us/3/mc.hypixel.net') as res:  #insert your server IP
            if res.status == 200:
                jsonfile = await res.json()
                if jsonfile["online"] == False:
                    user_id = "000000000000000000"  # Replace with the ID of the user you want to tag
                    return f"<@{user_id}> Server is offline"
                else:
                    IP = jsonfile["ip"]
                    motd = jsonfile["motd"]["html"]
                    players = jsonfile["players"]["online"]
                    version = jsonfile["version"]

                    if jsonfile["players"]["online"] > 0:
                        namelist = jsonfile["players"]["list"][0]["name"]
                       
                        message_content = f"--------------------------------\nIP: {IP}\nMOTD: {motd}\nPlayers Online: {namelist}\nVersion: {version}\n--------------------------------"
                    else:

                        message_content = f"--------------------------------\nIP: {IP}\nMOTD: {motd}\nPlayers Online: {players}/20\nVersion: {version}\n--------------------------------"
                    return message_content
            else:
                return "Failed to fetch data, mcsrvstat.us API may be down"

async def send_message_continuously(channel_id, interval=3600):
    channel = client.get_channel(channel_id)  
    while True:
        message_content = await api_fetch()  # Fetch the latest data
        try:
            await channel.send(message_content)
        except Exception as e:
            print(f"Failed to send message: {e}")
        await asyncio.sleep(interval)  # Wait for the specified interval

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    # Start the message sending loop for a specific channel
    asyncio.ensure_future(send_message_continuously(channel_id=000000000000000000000000))  # Replace with the ID of the channel you want to send messages to

client.run(TOKEN)