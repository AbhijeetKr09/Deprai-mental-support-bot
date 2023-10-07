import discord
import openai
import os
from chatApp import ChatApp
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv("data.env")
intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents)

openai.api_key = os.getenv("OPENAI_API")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.command()
@commands.has_permissions(manage_messages=True)
async def delete(ctx, amount: int):
    await client.purge_from(ctx.message.channel, limit=amount)

@delete.error
async def delete_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure you're using the command correctly: `!delete <number of messages>`")
    else:
        await ctx.send(f"An error occurred: {error}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Ignore commands
    ctx = await client.get_context(message)
    if ctx.valid:
        return

    if str(message.channel.id) != '1159608441577418812':
        return
    chat = ChatApp(message.author.name)
    print(message.author.name)
    print(f"Message from {message.author.name}: {message.content}")

    await message.channel.send(chat.get_response(message.content))

client.run(os.getenv("BOT_TOKEN"))
