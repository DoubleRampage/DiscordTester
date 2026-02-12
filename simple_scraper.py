from colorama import Fore
import discord
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
if TOKEN:
    TOKEN = TOKEN.strip()

SERVER_ID = 799672011265015819
CHANNEL_ID = 1189589759065067580

if not TOKEN:
    print(f"{Fore.WHITE}[ {Fore.RED}E {Fore.WHITE}] {Fore.LIGHTBLACK_EX}DISCORD_TOKEN not found. Set it in .env file or environment variable\n\n"+Fore.RESET)
    exit(1)

client = discord.Client()

@client.event
async def on_ready():
    print(f"{Fore.WHITE}[ {Fore.GREEN}+ {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Logged in as {Fore.WHITE}{client.user}")
    print(f"{Fore.WHITE}[ {Fore.GREEN}+ {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Monitoring for new messages...\n")

@client.event
async def on_message(message):
    if message.author.bot:
        return
    
    channel_name = message.channel.name if hasattr(message.channel, 'name') else 'DM'
    server_name = message.guild.name if message.guild else 'Direct Message'
    
    attachments = [attachment.url for attachment in message.attachments] if message.attachments else []
    
    print(f"{Fore.WHITE}[{message.created_at.strftime('%Y-%m-%d %H:%M:%S')}]")
    print(f"  {Fore.CYAN}Channel{Fore.RESET}: {Fore.YELLOW}#{channel_name}{Fore.RESET} ({Fore.LIGHTBLACK_EX}{server_name}{Fore.RESET})")
    print(f"  {Fore.CYAN}From{Fore.RESET}: {Fore.GREEN}{message.author}{Fore.RESET}")
    print(f"  {Fore.CYAN}Content{Fore.RESET}: {message.content if message.content else '(empty)'}")
    if attachments:
        print(f"  {Fore.CYAN}Attachments{Fore.RESET}: {Fore.LIGHTBLACK_EX}{', '.join(attachments)}{Fore.RESET}")
    print()

try:
    client.run(TOKEN, reconnect=True)
except discord.errors.LoginFailure as e:
    print(f"\n\n{Fore.WHITE}[ {Fore.RED}E {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Token is invalid or expired. Please check your .env file.\n")
    print(f"{Fore.WHITE}[ {Fore.YELLOW}? {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Make sure your .env file contains: DISCORD_TOKEN=your_token_here\n")
    print(f"{Fore.WHITE}[ {Fore.YELLOW}? {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Error details: {Fore.WHITE}{e}\n\n"+Fore.RESET)
except Exception as e:
    print(f"\n\n{Fore.WHITE}[ {Fore.RED}E {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Error: {Fore.WHITE}{e}\n\n"+Fore.RESET)

