from discord.ext import tasks
import discord, os, logging, time

TOKEN = os.getenv("TOKEN")
REACTION_MESSAGE_ID = os.getenv("REACTION_MESSAGE_ID")
REACTION_ROLE_ID = os.getenv("REACTION_ROLE_ID")
VOUCH_REMINDER_CHANNEL_ID = os.getenv("VOUCH_REMINDER_CHANNEL_ID")
VOUCH_REMINDER_START = os.getenv("VOUCH_REMINDER_START")
SERVER_ACCESS_ROLE_ID = os.getenv("SERVER_ACCESS_ROLE_ID")
WELCOME_CHANNEL_ID = os.getenv("WELCOME_CHANNEL_ID")

SECONDS_IN_HOUR = 3600
SECONDS_IN_WEEK = 604800
WELCOME_MESSAGE = """

:star: The point of this international server is to help each other out with the various aspects of the mask distro process.

> Feel free to post an intro (can include what you'd like for us to call you, pronouns, where you distribute masks, etc.). You're welcome to post what you'd like to get out of this shared workspace. All intro components are optional.

:star: Take your time exploring our server. Starting with the channels under the Main folder 📂  might be good.
        📌 Look through pinned posts for important info."""

logger = logging.getLogger('discord')

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

# EVENTS

@client.event
async def on_ready():
    logger.info(f"We have logged in as {client.user}")
    if not weekly_message.is_running():
        weekly_message.start()

@client.event
async def on_raw_reaction_add(reaction: discord.RawReactionActionEvent):
    if reaction.message_id == int(REACTION_MESSAGE_ID):
        role = client.get_guild(reaction.guild_id).get_role(int(REACTION_ROLE_ID))
        if not role in reaction.member.roles:
            await reaction.member.add_roles(role)
            logger.info(f"User Id {reaction.member.id}, Name {reaction.member.name} recieved {role.name} role")

@client.event
async def on_member_update(before: discord.Member, after: discord.Member):
    if (not any(role.id == int(SERVER_ACCESS_ROLE_ID) for role in before.roles)) and (any(role.id == int(SERVER_ACCESS_ROLE_ID) for role in after.roles)): # if someone who didn't have it before is recieving the server access role
        await client.get_channel(int(WELCOME_CHANNEL_ID)).send(f"Welcome to Mask Bloc Workspace, <@{after.id}> 🥳 !" + WELCOME_MESSAGE)
        logger.info(f"User Id {after.id}, Name {after.name} recieved server access role and welcome message sent")

@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

# TASKS

@tasks.loop(seconds=SECONDS_IN_HOUR) # will run again after this time elapses *and* the previous execution has completed
async def weekly_message():
    seconds_until_next_reminder = SECONDS_IN_WEEK - ((int(time.time()) - int(VOUCH_REMINDER_START)) % SECONDS_IN_WEEK)
    if seconds_until_next_reminder <= SECONDS_IN_HOUR:
        await client.get_channel(int(VOUCH_REMINDER_CHANNEL_ID)).send("Reminder to please vouch for folks in the welcome and introductions channel!")
        logger.info("Sent reminder message")

client.run(TOKEN)
