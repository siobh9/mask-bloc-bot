import discord, os
from dotenv import load_dotenv

load_dotenv() # so we can easily access env vars
TOKEN = os.getenv("TOKEN")

client = discord.Client()

# EVENTS

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await message.channel.send("Hello!")

client.run(TOKEN)