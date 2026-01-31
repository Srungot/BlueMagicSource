# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'ccvalidator.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import re
import requests
from colorama import Fore
import sys
import time
import platform
import os
import hashlib
from time import sleep
from datetime import datetime, UTC
import random
USER_AGENT_FILE = 'input/user-agents.txt'
DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
def load_user_agents():
    if not os.path.exists(USER_AGENT_FILE):
        print(Fore.YELLOW + f'[!] Fichier {USER_AGENT_FILE} manquant. Utilisation user-agent par défaut.')
        return [DEFAULT_USER_AGENT]
    else:
        with open(USER_AGENT_FILE, 'r') as f, [line.strip() for line in f if line.strip()]:
            pass
def luhn_check(card_number):
    card_number = [int(digit) for digit in str(card_number)]
    checksum = 0
    reverse_digits = card_number[::(-1)]
    for i, digit in enumerate(reverse_digits):
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
    return checksum % 10 == 0
def get_card_brand(card_number):
    brands = {'^4[0-9]{12}(?:[0-9]{3})?$': 'Visa', '^5[1-5][0-9]{14}$': 'MasterCard', '^3[47][0-9]{13}$': 'American Express', '^6(?:011|5[0-9]{2})[0-9]{12}$': 'Discover', '^3(?:0[0-5]|[68][0-9])[0-9]{11}$': 'Diners Club', '^(?:2131|1800|35\\d{3})\\d{11}$': 'JCB'}
    for pattern, brand in brands.items():
        return brand
    return 'Unknown'
def get_bin_info(card_number):
    # irreducible cflow, using cdg fallback
    bin_number = card_number[:6]
    url = f'https://lookup.binlist.net/{bin_number}'
    user_agent = random.choice(load_user_agents())
    response = requests.get(url, headers={'User-Agent': user_agent})
    if response.status_code == 200:
        data = response.json()
        return {'Bank': data.get('bank', {}).get('name', 'Unknown'), 'Country': data.get('country', {}).get('name', 'Unknown'), 'Type': data.get('type', 'Unknown'), 'Brand': data.get('scheme', 'Unknown').capitalize()}
    return {'Error': 'cc invalid'}
def clear_screen():
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')
clear_screen()
print(Fore.RED, '\n                                                       \n                                                        ....-*@@@@@@@+.          \n                                                ...-+@@@@@@@@@@@@@@@@:          \n                                            ..:=%@@@@@@@@@@@@==-@@@%.@@@#          \n                                    ..=@@@@@@@@@@@@@@@@@@@@@@@@@@@::@@@:         \n                            ..-#@@@@@@@@@@@@@@@@@*-.    @@@=+=.@@*.#@@@.        \n                            :@@@@@@@@@@@@@@#=:.           :@@@@@@@@#..@@@-        \n                            -@@@@@%@@@@@#+-..              %@@@@@@@= .+@@@.       \n                            -@@.-%@@@@@@@@@@@@@#=..        .....:+##*#+@@@+.      \n                            .@@@#:-*%@@@@@@@@@@@@@@@@@=. :-*#+-++#**..+-@@@:      \n                            =@@*@%*+**+*=..:=*@@@@@@@@@@%@@#%=--##@*#+:@@@*.     \n                            .@@@@@@@%@@@#-:..::-==-=%@@@:++%*:+++*=....=@@@:     \n                            -@@@@@@@@@@@@@@@%::.:...:*@##*--- .=+#@@@@@+@@*.    \n                            .@@@-@@@@@@@@@@@%--=-. -%@@#.::-- :+@@@@*-@@@@@.    \n                                :@@@+#++=*+-@@@#:...:%@@#-*:++-: .*@#@@@@+@@@@.    \n                                %@@=%%+:-@@@@+:.::-@@@*+:*=:.:=#@@@@@@@@@@@@@.    \n                                :@@@:.-@@@@#-:..=@@@@-:+=+@@@@@@@@@@@@@@@+:.      \n                                .@@@%@@@@*::.:+@@@:@@@@@@@@@@@@@@@#-..            \n                                .-@@@@@*=@%*+@@@@@@@@@@@@@@@=:.                   \n                                .@@@@@@@@@@@@@@@@@@%=:..                         \n                                .-@@@@@@@@@@*-:..                                \n                                                           \n')
card_number = input('[+] card number : ').strip()
card_number = card_number.replace(' ', '').replace('\t', '').replace('\n', '')
if luhn_check(card_number):
    print('[+] Valid Card ')
    print(f'[+] Brand detected : {get_card_brand(card_number)}')
    bin_info = get_bin_info(card_number)
    for key, value in bin_info.items():
        print(f'[+] {key}: {value}')
else:
    print('[+] invalid card !')
input()