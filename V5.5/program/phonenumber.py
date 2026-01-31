import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from colorama import Fore
import sys
import time
import platform
import os
import hashlib
from time import sleep
from datetime import datetime, UTC

def get_phone_info(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        if phonenumbers.is_valid_number(parsed_number):
            status = 'Valid'
        else:
            print('Invalid')
            input()
            return
        country_code = f'+{parsed_number.country_code}' if parsed_number.country_code else 'None'
        operator = carrier.name_for_number(parsed_number, 'fr') or 'None'
        number_type = phonenumbers.number_type(parsed_number)
        type_number = 'Mobile' if number_type == phonenumbers.PhoneNumberType.MOBILE else 'Fixe'
        timezones = timezone.time_zones_for_number(parsed_number)
        timezone_info = timezones[0] if timezones else 'None'
        country = phonenumbers.region_code_for_number(parsed_number) or 'None'
        region = geocoder.description_for_number(parsed_number, 'fr') or 'None'
        formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL) or 'None'
        print(f'\n[+] Status       : {status}\n[+] Formatted    : {formatted_number}\n[+] Country Code : {country_code}\n[+] Country      : {country}\n[+] Region       : {region}\n[+] Timezone     : {timezone_info}\n[+] Operator     : {operator}\n[+] Type Number  : {type_number}\n    ')
        input()
    except:
        print('[+] Invalid format !')

def clear_screen():
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')


clear_screen()
print(Fore.GREEN, '\n                                                  \n                                 .                                \n                              .-+##+.                             \n                          ..=*%%%%%%#=.                           \n                     ...-*%%%@@%%#%%%%+:.                         \n                   .:+*%%%%%%%%%%*::#%%%*.                        \n                  .+%%%%##%%%*-=+=+::-%%%#+.                      \n                  .-%%%%%%=:=-+=*+:::::+%%%+-.                    \n                    :#@%%%%#**+=-::::::::#%%%*..                  \n                     .+%%%%%%*=:::::::::-=+%%%*+.                 \n                       :#%%%%%#::::::::=#%%%%%%+%=                \n                        .+%@#%%%=:--=%%%%%%%%%%%%%#.              \n                         ..#@%%%%%%%%%%%%%%##%##-+%%*.            \n                           .+%@#%%%%%%%%#+%%%#+%**#%%%=..         \n                            .:%@%++%%%#%*%%##%%%%%%%%#%#:.        \n                               +%@#%##=:##=++=%%%%%%@%%%%*.       \n                                :#@@%%###%%%%%#*#%%%%##@%%%=.     \n                                 .+%@%%%%%%#%%%%%%#%%%%*##%%#:.   \n                                   :%@%%##%%%%%*#%%%%%%%%%%##%#.. \n                                   .+%@%%*%*%%#%%*%@%%%%%%@%%%#. \n                                     .:#%@*%%%##%%%%#%*%%%%%%%#.. \n                                       .+%@%%#@%%%%%%@@%%%%#=..   \n                                        .:%%%%**%%@%@%%%%=...     \n                                          .*%@%%%%%%%#+..         \n                                            :#%@%%#+..            \n                                             ..--...                   \n')
tel = input('[+] Phone Number : ')
get_phone_info(tel)