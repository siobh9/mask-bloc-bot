import discord, os

TOKEN = os.getenv("TOKEN")
REACTION_MESSAGE_ID = os.getenv("REACTION_MESSAGE_ID")

intents = discord.Intents.default()
client = discord.Client(intents=intents)

reactions_to_roles = {
    "🔥": 1252335644651557018,
    "🗓️": 1252336334589132861
}

# EVENTS

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_raw_reaction_add(reaction: discord.RawReactionActionEvent):
    if reaction.message_id != int(REACTION_MESSAGE_ID):
        return
    
    role = client.get_guild(reaction.guild_id).get_role(reactions_to_roles[reaction.emoji.name])
    
    if not role in reaction.member.roles:
        await reaction.member.add_roles(role)

@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

client.run(TOKEN)
