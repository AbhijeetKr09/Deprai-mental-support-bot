import discord
import openai
import os
from response import ResponseGenerator
from dotenv import load_dotenv


response = ResponseGenerator()
load_dotenv("data.env")
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

openai.api_key = os.getenv("OPENAI_API")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if str(message.channel.id) != '1158090555797016606':
        return

    print(f"Message from {message.author.name}: {message.content}")

    await message.channel.send(response.get_response(message.author, message.content)[0])
client.run(os.getenv("BOT_TOKEN"))
