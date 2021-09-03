# !clearmessages spam 1000
import os
import re
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    text = message.content

    # !
    if text[0] != "!":
        return

    # !clmsg
    if not text.startswith('!clmsg'):
        return

    # mod
    mod = False
    for role in message.author.roles:
        roleName = role.name.lower()
        if "moderator" in roleName:
            mod = True

    if not mod:
        await message.channel.send("Moderator role is needed!")
        return

    # !clmsg askljdfalksfj 1000
    keyword, count = parseCommand(text)
    count = int(count) + 1

    history = await message.channel.history(limit=count).flatten()
    deletedMessages = 0

    for msg in history:
        if keyword in msg.content:
            deletedMessages += 1
            await msg.delete()

    await message.channel.send("Stufi bot deleted " + str(deletedMessages) + " messages!")

def parseCommand(s):
    mo = re.match("!clmsg (.*) (.*)", s)
    if mo: 
        return mo.groups ()
    return []

client.run(TOKEN)