from discord.ext import tasks
import discord, os, logging, time

TOKEN = os.getenv("TOKEN")
REACTION_MESSAGE_ID = os.getenv("REACTION_MESSAGE_ID")
REACTION_ROLE_ID = os.getenv("REACTION_ROLE_ID")
VOUCH_REMINDER_CHANNEL_ID = os.getenv("VOUCH_REMINDER_CHANNEL_ID")

logger = logging.getLogger('discord')

intents = discord.Intents.default()
client = discord.Client(intents=intents)

# EVENTS

@client.event
async def on_ready():
    logger.info(f"We have logged in as {client.user}")
    if not weekly_message.is_running():
        weekly_message.start()

@client.event
async def on_raw_reaction_add(reaction: discord.RawReactionActionEvent):
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

@tasks.loop(seconds=5.0)
async def weekly_message():
    logger.info("Starting sleep...")
    time.sleep(10)
    logger.info("Done sleeping")
    await client.get_channel(int(VOUCH_REMINDER_CHANNEL_ID)).send("Reminder to not vouch for folks in the public channel!")
    logger.info("Sent reminder message")

client.run(TOKEN)
