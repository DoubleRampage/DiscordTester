from colorama import Fore
import discord
import os
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")
SERVER_ID = 799672011265015819
CHANNEL_ID = 1189589759065067580

if not TOKEN:
    print(f"{Fore.WHITE}[ {Fore.RED}E {Fore.WHITE}] {Fore.LIGHTBLACK_EX}DISCORD_TOKEN environment variable is not set\n\n"+Fore.RESET)
    exit(1)

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(
    command_prefix="!",
    self_bot=True,
    intents=intents
)

@client.event
async def on_ready():
    print(f"{Fore.WHITE}[ {Fore.GREEN}+ {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Logged in as {Fore.WHITE}{client.user}")
    
    guild = client.get_guild(SERVER_ID)
    if not guild:
        print(f"{Fore.WHITE}[ {Fore.RED}E {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Server {SERVER_ID} not found")
        await client.close()
        return
    
    channel = guild.get_channel(CHANNEL_ID)
    if not channel:
        print(f"{Fore.WHITE}[ {Fore.RED}E {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Channel {CHANNEL_ID} not found")
        await client.close()
        return
    
    print(f"{Fore.WHITE}[ {Fore.YELLOW}? {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Fetching last 10 messages from {Fore.WHITE}#{channel.name}{Fore.LIGHTBLACK_EX}...\n")
    
    messages = []
    try:
        async for message in channel.history(limit=10):
            messages.append(message)
    except Exception as e:
        print(f"{Fore.WHITE}[ {Fore.RED}E {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Error fetching messages: {Fore.WHITE}{e}")
        await client.close()
        return
    
    for msg in reversed(messages):
        attachments = [attachment.url for attachment in msg.attachments if msg.attachments]
        try:
            if attachments:
                print(f"{Fore.WHITE}[{msg.created_at}] {Fore.CYAN}{msg.author}{Fore.RESET}: {msg.content} {Fore.LIGHTBLACK_EX}({attachments[0]}){Fore.RESET}")
            else:
                print(f"{Fore.WHITE}[{msg.created_at}] {Fore.CYAN}{msg.author}{Fore.RESET}: {msg.content}")
        except Exception as e:
            print(f"{Fore.WHITE}[ {Fore.RED}- {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Cannot display message from {Fore.WHITE}{msg.author}")
    
    print(f"\n{Fore.WHITE}[ {Fore.GREEN}+ {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Successfully scraped {Fore.WHITE}{len(messages)} {Fore.LIGHTBLACK_EX}messages!\n")
    await client.close()

try:
    client.run(TOKEN, reconnect=True)
except discord.errors.LoginFailure:
    print(f"\n\n{Fore.WHITE}[ {Fore.RED}E {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Token is invalid\n\n"+Fore.RESET)
except Exception as e:
    print(f"\n\n{Fore.WHITE}[ {Fore.RED}E {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Error: {Fore.WHITE}{e}\n\n"+Fore.RESET)

