from discord.ext import tasks
import discord, os

TOKEN = os.getenv("TOKEN")
REACTION_MESSAGE_ID = os.getenv("REACTION_MESSAGE_ID")
REACTION_ROLE_ID = os.getenv("REACTION_ROLE_ID")
VOUCH_REMINDER_CHANNEL_ID = os.getenv("VOUCH_REMINDER_CHANNEL_ID")

intents = discord.Intents.default()
client = discord.Client(intents=intents)

# EVENTS

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}", flush=True)
    if not weekly_message.is_running():
        weekly_message.start()

@client.event
async def on_raw_reaction_add(reaction: discord.RawReactionActionEvent):
    print("reaction recieved", flush=True)

    if reaction.message_id != int(REACTION_MESSAGE_ID):
        return
    
    role = client.get_guild(reaction.guild_id).get_role(int(REACTION_ROLE_ID))
    
    if not role in reaction.member.roles:
        await reaction.member.add_roles(role)

@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

# TASKS

@tasks.loop(seconds=10.0)
async def weekly_message():
    client.channels.get(VOUCH_REMINDER_CHANNEL_ID).send("message")
    print(f"Sending message", flush=True)

client.run(TOKEN)
