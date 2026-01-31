# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'doxtool.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import discord
from discord.ext import commands
import requests
import re
from urllib.parse import quote
from bs4 import BeautifulSoup
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json
from colorama import Fore
import sys
import platform
import os
import hashlib
from time import sleep
from datetime import datetime, UTC
BLUE = '[94m'
RED = '[91m'
RESET = '[0m'
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
def clean_username(username):
    return re.sub('#\\d+$', '', username)
async def discord_dox(target_id):
    print(f'{Fore.LIGHTCYAN_EX}[+] Fetching Discord info...{RESET}')
    results = {'discord_info': {}}
    try:
        user = await bot.fetch_user(int(target_id))
        full_username = f'{user.name}#{user.discriminator}'
        results['discord_info'] = {'username': full_username, 'clean_username': clean_username(full_username), 'id': str(user.id), 'created_at': str(user.created_at), 'avatar': str(user.avatar.url) if user.avatar else 'No avatar', 'servers': [guild.name for guild in user.mutual_guilds]}
    except discord.errors.HTTPException as e:
        results['discord_info'] = {'error': f'Error: {str(e)}. Bot must share a server with user.'}
    except Exception as e:
        results['discord_info'] = {'error': f'General error: {str(e)}'}
    return results
def init_driver():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36')
    options.add_argument('--disable-blink-features=AutomationControlled')
    return webdriver.Chrome(options=options)
def external_dox(username):
    print(f'{Fore.LIGHTCYAN_EX}[+] Scanning external platforms...{RESET}')
    clean_name = quote(clean_username(username))
    results = {'youtube': ['No profile found'], 'tiktok': ['No profile found'], 'snapchat': ['No profile found'], 'instagram': ['No profile found'], 'github': ['No profile found']}
    platforms = {'youtube': f'https://www.youtube.com/@{clean_name}', 'tiktok': f'https://www.tiktok.com/@{clean_name}', 'snapchat': f'https://www.snapchat.com/add/{clean_name}', 'instagram': f'https://www.instagram.com/{clean_name}/'}
    driver = init_driver()
    for platform, url in platforms.items():
        print(f'{Fore.LIGHTCYAN_EX}[+] Checking {platform.capitalize()}...{RESET}')
        for attempt in range(2):
            try:
                driver.get(url)
                time.sleep(5)
                page_source = driver.page_source.lower()
                title = driver.title.lower()
                if platform == 'youtube':
                    if '404' not in title:
                        results[platform] = [url]
                else:
                    if platform == 'tiktok':
                        if 'couldn\'t find this account' not in page_source:
                            results[platform] = [url]
                    else:
                        if platform == 'snapchat':
                            if ' on snapchat' in title:
                                results[platform] = [url]
                        else:
                            if platform == 'instagram':
                                if 'page not found' not in title and 'this account is private' not in page_source and ('sorry, this page isn\'t available' not in page_source):
                                            results[platform] = [url]
            except Exception as e:
                print(f'{Fore.LIGHTCYAN_EX}[-] Error checking {platform} (attempt {attempt + 1}): {str(e)}{RESET}')
                if attempt == 1:
                    results[platform] = [f'Error: Failed to check ({str(e)})']
                time.sleep(2)
            else:
                break
    driver.quit()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'}
    print(f'{Fore.LIGHTCYAN_EX}[+] Checking GitHub...{RESET}')
    github_url = f'https://github.com/{clean_name}'
    try:
        r = requests.get(github_url, headers=headers)
        if r.status_code == 200:
            results['github'] = [github_url]
    except Exception:
        pass
    return results
def print_results(discord_data, external_data):
    INTERNAL_WIDTH = 60
    def pad_line(content):
        return content.ljust(INTERNAL_WIDTH)
    print(f'\n{Fore.LIGHTCYAN_EX}Discord Results{RESET}')
    discord_info = discord_data.get('discord_info', {})
    if 'error' not in discord_info:
        print(f'{Fore.LIGHTCYAN_EX}Username: {discord_info['username']}{RESET}')
        print(f'{Fore.LIGHTCYAN_EX}Cleaned Username: {discord_info['clean_username']}{RESET}')
        print(f'{Fore.LIGHTCYAN_EX}ID: {discord_info['id']}{RESET}')
        print(f'{Fore.LIGHTCYAN_EX}Avatar: {discord_info['avatar']}{RESET}')
        print(f'{Fore.LIGHTCYAN_EX}Creation Date: {discord_info['created_at']}{RESET}')
        servers = ', '.join(discord_info['servers']) if discord_info['servers'] else 'None'
        print(f'{Fore.LIGHTCYAN_EX}Common Servers: {servers}{RESET}')
    else:
        print(f'{Fore.LIGHTCYAN_EX}Error: {discord_info['error']}{RESET}')
    print(f'\n{Fore.LIGHTCYAN_EX}External Results{RESET}')
    for platform, links in external_data.items():
        platform_name = platform.capitalize()
        print(f'{Fore.LIGHTCYAN_EX}{platform_name}:{RESET}')
        for link in links:
            print(f'{Fore.LIGHTCYAN_EX}  - URL: {link}{RESET}')
async def main():
    art = f'{Fore.LIGHTCYAN_EX}     \n ▄▀▀█▄▄   ▄▀▀▀▀▄   ▄▀▀▄  ▄▀▄      ▄▀▀▀█▀▀▄  ▄▀▀▄▀▀▀▄  ▄▀▀█▄   ▄▀▄▄▄▄   ▄▀▀▄ █  ▄▀▀█▄▄▄▄  ▄▀▀▄▀▀▀▄ \n█ ▄▀   █ █      █ █    █   █     █    █  ▐ █   █   █ ▐ ▄▀ ▀▄ █ █    ▌ █  █ ▄▀ ▐  ▄▀   ▐ █   █   █ \n▐ █    █ █      █ ▐     ▀▄▀      ▐   █     ▐  █▀▀█▀    █▄▄▄█ ▐ █      ▐  █▀▄    █▄▄▄▄▄  ▐  █▀▀█▀  \n  █    █ ▀▄    ▄▀      ▄▀ █         █       ▄▀    █   ▄▀   █   █        █   █   █    ▌   ▄▀    █  \n ▄▀▄▄▄▄▀   ▀▀▀▀       █  ▄▀       ▄▀       █     █   █   ▄▀   ▄▀▄▄▄▄▀ ▄▀   █   ▄▀▄▄▄▄   █     █   \n█     ▐             ▄▀  ▄▀       █         ▐     ▐   ▐   ▐   █     ▐  █    ▐   █    ▐   ▐     ▐   \n▐                  █    ▐        ▐                           ▐        ▐        ▐                  \n\n              .+#.                          \n             :#:-*:                         \n             *%+*#=                         __________________________________________________________________________\n   .:..    .:+@#%#:                          \n ..-:.-:. .*%%%%%%%*.                       [+] Uses headless Selenium to bypass protections\n..-:.  .:=%@@%%%%%@%=.                      \n.::.     *@%%%%%%%@@#:                      [+] Clean formatting: fast/efficient results\n.:.      :%@@%%%%%%@#:                      \n.:.       .*#%%%%%%@#:                      [+] Discord bot required, simple commands, secure token\n...        .*%%%%%###.                      \n           .*%%%%%* .--.                    [+] No shared server? Manual bypass with username\n           .*%%%@%*   .:.                   \n           .*%%%@@#.                        [+] Retrieves username, ID, creation date, and avatar via Discord ID\n           .*%%%%@%.                        \n           .*%%%%@@-                        [+] Scans YouTube, TikTok, Snapchat, Instagram, and GitHub in stealth\n           :%%%%%@@=.                       \n          .#%*###+#%-.                      ___________________________________________________________________________\n\n          \n'
    print(art)
    DISCORD_TOKEN = input(f'{Fore.LIGHTCYAN_EX}[+] Enter Discord bot token: {RESET}')
    try:
        await bot.start(DISCORD_TOKEN)
    except discord.errors.LoginFailure:
        print(f'{Fore.LIGHTCYAN_EX}[-] Invalid token. Get it from https://discord.com/developers/applications > Bot tab.{RESET}')
    except Exception as e:
        print(f'{Fore.LIGHTCYAN_EX}[-] Startup error: {str(e)}{RESET}')
@bot.event
async def on_ready():
    print(f'{Fore.LIGHTCYAN_EX}✅ Bot connected: {bot.user.name}{RESET}')
    while True:
        target_id = input(f'{Fore.LIGHTCYAN_EX}[+] Enter Discord ID (or \'quit\'): {RESET}')
        if target_id.lower() == 'quit':
            print(f'{Fore.LIGHTCYAN_EX}[+] Shutting down... 🔥{RESET}')
            await bot.close()
            return
        else:
            if not re.match('^\\d{18,19}$', target_id):
                print(f'{Fore.LIGHTCYAN_EX}[-] Invalid ID: Must be 18-19 digits. Ex: 1424308189377331231{RESET}')
                continue
            else:
                discord_data = await discord_dox(target_id)
                username = discord_data.get('discord_info', {}).get('clean_username', target_id)
                if 'error' in discord_data['discord_info']:
                    print(f'{Fore.LIGHTCYAN_EX}[-] No Discord username found. Enter manually?{RESET}')
                    username = input(f'{Fore.LIGHTCYAN_EX}[+] Username (or \'skip\'): {RESET}')
                    if username.lower() == 'skip':
                        username = target_id
                    else:
                        username = clean_username(username)
                external_data = external_dox(username)
                print_results(discord_data, external_data)
if __name__ == '__main__':
    def clear_screen():
        if os.name == 'posix':
            os.system('clear')
        else:
            os.system('cls')
    clear_screen()
    asyncio.run(main())