# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'email_tool.py'
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import time
from colorama import Fore
import random
import sys
import time
import platform
import os
import hashlib
from time import sleep
from datetime import datetime, UTC
with open('input\\user-agents.txt', 'r', encoding='utf-8') as f:
    user_agents = [line.strip() for line in f if line.strip()]
user_agent = random.choice(user_agents)
def Instagram(email):
    session = requests.Session()
    headers = {'User-Agent': user_agent, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Origin': 'https://www.instagram.com', 'Connection': 'keep-alive', 'Referer': 'https://www.instagram.com/'}
    data = {'email': email}
    response = session.get('https://www.instagram.com/accounts/emailsignup/', headers=headers)
    if response.status_code != 200:
        return False
    token = session.cookies.get('csrftoken')
    if not token:
        return False
    headers['x-csrftoken'] = token
    headers['Referer'] = 'https://www.instagram.com/accounts/emailsignup/'
    response = session.post(url='https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/', headers=headers, data=data)
    if response.status_code == 200:
        if 'Another account is using the same email.' in response.text or 'email_is_taken' in response.text:
            return True
        return False
    return False
def Twitter(email):
    # irreducible cflow, using cdg fallback
    response = requests.get('https://api.twitter.com/i/users/email_available.json', params={'email': email})
    if response.status_code == 200:
        return response.json()['taken']
    return False
def Pinterest(email):
    # irreducible cflow, using cdg fallback
    response = requests.get('https://www.pinterest.com/_ngjs/resource/EmailExistsResource/get/', params={'source_url': '/', 'data': '{\"options\": {\"email\": \"' + email + '\"}, \"context\": {}}'})
    if response.status_code == 200:
        data = response.json()['resource_response']
        if data['message'] == 'Invalid email.':
            return False
            return data['data'] is not False
        return False
    return False
def Imgur(email):
    # irreducible cflow, using cdg fallback
    headers = {'User-Agent': user_agent}
    data = {'email': email}
    response = requests.post('https://imgur.com/signin/ajax_email_available', headers=headers, data=data)
    if response.status_code == 200:
        data = response.json()['data']
        if data['available']:
            return False
            return True
        return False
    return False
def Patreon(email):
    # irreducible cflow, using cdg fallback
    headers = {'User-Agent': user_agent}
    data = {'email': email}
    response = requests.post('https://www.plurk.com/Users/isEmailFound', headers=headers, data=data)
    if response.status_code == 200:
        return 'True' in response.text
    return False
def Spotify(email):
    # irreducible cflow, using cdg fallback
    headers = {'User-Agent': user_agent}
    params = {'validate': '1', 'email': email}
    response = requests.get('https://spclient.wg.spotify.com/signup/public/v1/account', headers=headers, params=params)
    if response.status_code == 200:
        status = response.json()['status']
        return status == 20
    return False
def FireFox(email):
    # irreducible cflow, using cdg fallback
    data = {'email': email}
    response = requests.post('https://api.accounts.firefox.com/v1/account/status', data=data)
    if response.status_code == 200:
        return 'false' not in response.text
    return False
def LastPass(email):
    # irreducible cflow, using cdg fallback
    response = requests.get('https://lastpass.com/create_account.php', params={'check': 'avail', 'username': email})
    if response.status_code == 200:
        return 'no' in response.text
    return False
def Archive(email):
    # irreducible cflow, using cdg fallback
    data = {'input_name': 'username', 'input_value': email, 'input_validator': 'true', 'submit_by_js': 'true'}
    response = requests.post('https://archive.org/account/signup', data=data)
    if response.status_code == 200:
        return 'is already taken.' in response.text
    return False
def ProtonMail(email):
    # irreducible cflow, using cdg fallback
    data = {'Address': email}
    response = requests.post('https://account.proton.me/api/users/exists', json=data)
    if response.status_code == 200:
        return response.json().get('Exists', False)
    return False
sites = [Instagram, Twitter, Pinterest, Imgur, Patreon, Spotify, FireFox, LastPass, Archive, ProtonMail]
def email_tracker():
    print('=== Email Tracker ===')
    email = input('Enter email -> ')
    for site in sites:
        result = site(email)
        if result:
            print(f'{site.__name__}: Found ✅')
        else:
            print(f'{site.__name__}: Not Found ❌')
    print('=== Tracker finished ===\n')
    input()
try:
    import dns.resolver
    import re
except Exception as e:
    print('Error importing modules:', e)
def run_email_lookup():
    email = input('Enter Email -> ')
    print('Recovering information...\n')
    info = {}
    try:
        domain_all = email.split('@')[-1]
    except:
        domain_all = None
    try:
        name = email.split('@')[0]
    except:
        name = None
    try:
        domain = re.search('@([^@.]+)\\.', email).group(1)
    except:
        domain = None
    try:
        tld = f".{email.split('.')[-1]}"
    except:
        tld = None
    try:
        mx_records = dns.resolver.resolve(domain_all, 'MX')
        mx_servers = [str(record.exchange) for record in mx_records]
        info['mx_servers'] = mx_servers
    except dns.resolver.NoAnswer:
        mx_servers = None
        info['mx_servers'] = None
    except dns.resolver.NXDOMAIN:
        mx_servers = None
        info['mx_servers'] = None
    except:
        mx_servers = None
        info['mx_servers'] = None
    try:
        spf_records_raw = dns.resolver.resolve(domain_all, 'TXT')
        spf_records = [str(r) for r in spf_records_raw if 'spf' in str(r).lower()]
        info['spf_records'] = spf_records if spf_records else None
    except dns.resolver.NoAnswer:
        spf_records = None
        info['spf_records'] = None
    except dns.resolver.NXDOMAIN:
        spf_records = None
        info['spf_records'] = None
    except:
        spf_records = None
        info['spf_records'] = None
    try:
        dmarc_records_raw = dns.resolver.resolve(f'_dmarc.{domain_all}', 'TXT')
        dmarc_records = [r.strings[0].decode('utf-8') if r.strings else '' for r in dmarc_records_raw]
        info['dmarc_records'] = dmarc_records
    except dns.resolver.NoAnswer:
        dmarc_records = None
        info['dmarc_records'] = None
    except dns.resolver.NXDOMAIN:
        dmarc_records = None
        info['dmarc_records'] = None
    except:
        dmarc_records = None
        info['dmarc_records'] = None
    if mx_servers:
        info['google_workspace'] = any('google.com' in s for s in mx_servers)
        info['microsoft_365'] = any('outlook.com' in s for s in mx_servers)
    else:
        info['google_workspace'] = None
        info['microsoft_365'] = None
    print(f"\n──────────────────────────────────────────────────────────────────────────────\nEmail      : {email}\nName       : {name}\nDomain     : {domain}\nTLD        : {tld}\nDomain All : {domain_all}\nServers    : {(' / '.join(mx_servers) if mx_servers else None)}\nSPF        : {spf_records}\nDMARC      : {(' / '.join(dmarc_records) if dmarc_records else None)}\nWorkspace  : {info['google_workspace']}\nMicrosoft  : {info['microsoft_365']}\n──────────────────────────────────────────────────────────────────────────────\n")
    input()
def start():
    print(Fore.GREEN, '                                                                                                                                      \n                                    :*%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%*:              \n                                  =%%-...................................-%%+             \n                                  *%%%+.                               .+%%%*             \n                                  *%:=%%*.                           .*%%=.%*             \n                                  *%. .:@%#.                       .#%@-. .%*             \n                                  *%.    .#%%-                   -%%#:    .%*             \n                                  *%.      .*%%=               =%%#.      .%*             \n                                  *%.        .-%%%.         .#%%=.        .%*             \n                                  *%.           :@%%       %%@:           .%*             \n                                  *%.          .@%@%%@: :@%%@%@.          .%*             \n                                  *%.       .-%%#.  .*%%%#.  .#%%-.       .%*             \n                                  *%.     .+%%*.      ...      .*%%+.     .%*             \n                                  *%.   .%%%-                     :%%%.   .%*             \n                                  *%..:%%#:                         :#%%-..%*             \n                                  *%=%%#.                             .#%%=%*             \n                                  =%%*...................................*%%+             \n                                    :*%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%*:              \n                                                                                        \n                                \n                                  ---------                          --------\n                        [3] Tracker Email  | [1] Spoofer Email       |   [4] Lockup Email  \n                                           |                         |       \n                                           | [2] Personalized Email  |       \n                                           |                         |       \n                                           | [0] Exit                |                                                                                                                                   \n')
    choice = input('Choice : ')
    if choice == '1':
        while True:
            victim_email = input(' [1] victim\'s email : ')
            if victim_email != '':
                break
            else:
                print(Fore.RED)
                input('ERROR: Please enter an email')
                print(Fore.GREEN)
        
        try:
            Valeur = input(' [2] number of messages sent : ')
            Valeur = int(Valeur)
            
            objet = input(' [3] Subject : ')
            while True:
                e_mail_message = input(' [4] Message to send : ')
                if e_mail_message != '':
                    break
                else:
                    print(Fore.RED)
                    input('ERROR: Please enter an message')
                    print(Fore.GREEN)
            
            config_email = 'bluemagicdiscord@gmail.com'
            config_password = 'vdiyamviyzooclcm'
            config_server = 'smtp.gmail.com'
            config_server_port = 587
            
            def send_email():
                try:
                    multipart_message = MIMEMultipart()
                    multipart_message['Subject'] = objet
                    multipart_message['From'] = config_email
                    multipart_message['To'] = victim_email
                    multipart_message.attach(MIMEText(e_mail_message, 'plain'))
                    serveur_mail = smtplib.SMTP(config_server, config_server_port)
                    serveur_mail.starttls()
                    serveur_mail.login(config_email, config_password)
                    serveur_mail.sendmail(config_email, victim_email, multipart_message.as_string())
                    serveur_mail.quit()
                    return True
                except smtplib.SMTPAuthenticationError:
                    print(Fore.RED, '\n  ERROR: the password app or email address is expired\n    \n  Please contact the creator(x1b) or there were too many messages at once, try again later\n           \n          [1] main_menu \n\n          [2] exit  \n              \n              ')
                    print(Fore.GREEN)
                    choice = input('Choice : ')
                    if choice == '1':
                        start()
                    else:
                        exit()
                    return False
                except smtplib.SMTPRecipientsRefused:
                    print(Fore.RED, ' ERROR: the recipient\'s email is invalid\n\n          [1] main_menu \n\n          [2] exit  \n              \n              ')
                    print(Fore.GREEN)
                    choice = input('Choice : ')
                    if choice == '1':
                        start()
                    else:
                        exit()
                    return False
            
            counter = 0
            while counter < Valeur:
                if send_email():
                    print(Fore.GREEN, 'email send ! ')
                    time.sleep(3)
                    counter += 1
                else:
                    break
            
            print(Fore.GREEN)
            choice = input('\n      [1] main_menu\n      \n      [2] exit\n      ')
            if choice == '1':
                start()
            else:
                exit()
        except ValueError:
            print(Fore.RED)
            input('ERROR: enter a number')
            print(Fore.GREEN)
            start()
    
    elif choice == '2':
        while True:
            email_send = input(' [1] email address sending the message : ')
            if email_send != '':
                break
            else:
                print(Fore.RED)
                input('ERROR: Please enter an email')
                print(Fore.GREEN)
        
        while True:
            password_email = input(' [2] app password : ')
            if len(password_email) == 16:
                break
            else:
                print(Fore.RED)
                input('ERROR : the password app must contain 16 characters ')
                print(Fore.GREEN)
        
        while True:
            victim_email = input(' [3] victim\'s email : ')
            if victim_email != '':
                break
            else:
                print(Fore.RED)
                input('ERROR: Please enter an email')
                print(Fore.GREEN)
        
        try:
            Valeur = input(' [4] number of messages sent : ')
            Valeur = int(Valeur)
            
            objet = input(' [5] Subject : ')
            while True:
                e_mail_message = input(' [6] Message to send : ')
                if e_mail_message != '':
                    break
                else:
                    print(Fore.RED)
                    input('ERROR: Please enter an message')
                    print(Fore.GREEN)
            
            config_email = email_send
            config_password = password_email
            config_server = 'smtp.gmail.com'
            config_server_port = 587
            
            def send_email():
                try:
                    multipart_message = MIMEMultipart()
                    multipart_message['Subject'] = objet
                    multipart_message['From'] = config_email
                    multipart_message['To'] = victim_email
                    multipart_message.attach(MIMEText(e_mail_message, 'plain'))
                    serveur_mail = smtplib.SMTP(config_server, config_server_port)
                    serveur_mail.starttls()
                    serveur_mail.login(config_email, config_password)
                    serveur_mail.sendmail(config_email, victim_email, multipart_message.as_string())
                    serveur_mail.quit()
                    return True
                except smtplib.SMTPAuthenticationError:
                    print(Fore.RED, 'ERROR: the password app or email address is invalid\n\n          [1] main_menu \n\n          [2] exit  \n              \n              ')
                    print(Fore.GREEN)
                    choice = input('Choice : ')
                    if choice == '1':
                        start()
                    else:
                        exit()
                    return False
                except smtplib.SMTPRecipientsRefused:
                    print(Fore.RED, ' \n  ERROR: the recipient\'s email is invalid\n\n          [1] main_menu \n\n          [2] exit  \n              \n              ')
                    print(Fore.GREEN)
                    choice = input('Choice : ')
                    if choice == '1':
                        start()
                    else:
                        exit()
                    return False
            
            counter = 0
            while counter < Valeur:
                if send_email():
                    print(Fore.GREEN, 'email send ! ')
                    time.sleep(3)
                    counter += 1
                else:
                    break
            
            print(Fore.GREEN)
            choice = input('\n      [1] main_menu\n      \n      [2] exit\n      ')
            if choice == '1':
                start()
            else:
                exit()
        except ValueError:
            print(Fore.RED)
            input('ERROR: enter a number')
            print(Fore.GREEN)
            start()
    
    elif choice == '3':
        email_tracker()
    
    elif choice == '4':
        run_email_lookup()
    
    elif choice == '0':
        exit()
    
    else:
        exit()

def clear_screen():
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')

if __name__ == '__main__':
    def clear_screen():
        if os.name == 'posix':
            os.system('clear')
        else:
            os.system('cls')
    clear_screen()
    start()