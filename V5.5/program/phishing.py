import requests
import random
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
from concurrent.futures import ThreadPoolExecutor
import re
from colorama import Fore
import sys
import time
import platform
import hashlib
from time import sleep
from datetime import datetime, UTC

def clear_screen():
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')

clear_screen()

with open('input/user-agents.txt', 'r', encoding='utf-8') as f:
    user_agents = f.read().splitlines()

if user_agents:
    user_agent = random.choice(user_agents)
else:
    user_agent = 'Mozilla/5.0'

headers = {'User-Agent': user_agent}

print(Fore.RED, '\n                                                       \n                                    ............=@@@@@@*@@@+@@@@@+............       \n                                    ............:@@@@@%@@@@@@@@=@@@@@=............     \n                                ............-@@@@+@@@#=**-@@@@@@@@@@............    \n                                ...........*@@@*@@@@%#++###@@@@@#@@@@=...........   \n                                ..........=@@@:@@@@@##@@#%@@@@@@@@%@@@@..........   \n                                .........#@@@@@@@@@@@@@@@@%@@@@@@@@@=@@@@:.......   \n                                ........=@@@%@@@@@@@@@%=..:..-+%@@@@@@@*@@@*........ \n                                .......%@@%@@@@@*--:-%@@@@@@@@@*:==+*@@@@=@@+....... \n                                ......+@@@@@@*:.  .*@@@@*:+@@@@@@=.   .=@@@@@:...... \n                                ......@@@@@+.    .=@@#:=@@@#..=@@@:    .:#@*@-... .. \n                                ......@*@%.      .*@@:.=@+@@: .:@@:      .@+@-....   \n                                ......@+@+.      .=@@@@@@-@%: .=@@:    .:*%-#:...... \n                                ......#%+@-.     .:+@@@@+%@*.=@@@#.   .-*#.%=....    \n                                .....-@**#-..     ..:.-@@#=@@@@#:  ..-#+-%+....     \n                                    .....=%++@*..       .*@@+@@@#-.  .:*@@@%-.....     \n                                    ...-@@@@@@*:..     :#@#@@+.    .:*@@@@@@@+...     \n                                    -@@@@@@+*@@*:..   .+@@-#@@-.  .:*@@@:+@@@@@@=     \n                                :@@@@@#%@@@++#+-.. .=@@@%@@@@: .:+#@@#-@@@#@@@@@-   \n                                -@@@@+@@@@#--=-==:. .*@@:..-@@- .-#-%@@%@@@@@@%@@@:  \n                                =@@@%@@@@@#*=-=-.+-...+@@@%%@@@:..:@=@%@@#=%@@@@@@@#  \n                                @@@@@@@@@#-++-=-=*+::.:*@@@@@@+.-=-@-@-+@@#=@%%@@@@@+ \n                                @@@@@@@@@-.=+---+=#:.:..:+#*=..:+==@:@=:=@@*@-+@@@@@@ \n                                @#@@**@%@:.:=---+:*-....     ..:+:-@:@::.-@@%-+#%%@@@ \n                                @@@#=-##+: .:--=+-*-....     ..-=--@-@:...-*---***@@@ \n                                @@@-:::-:: ...:-+-=:....       :---@-@..::.==----=*#+      \n      \n      \n      ')
print(f'[+] Selected User-Agent : {user_agent}')
url = input('[+] URL : ').strip()

if 'https://' not in url and 'http://' not in url:
    url = 'https://' + url

try:
    session = requests.Session()
    session.headers.update(headers)
    resp = session.get(url, timeout=10)
    resp.raise_for_status()
    html = resp.text
    soup = BeautifulSoup(html, 'html.parser')
    css_links = soup.find_all('link', rel='stylesheet')
    script_links = soup.find_all('script', src=True)
    css_urls = [urljoin(url, link['href']) for link in css_links]
    js_urls = [urljoin(url, script['src']) for script in script_links]

    def fetch_text(u):
        try:
            return session.get(u, timeout=10).text
        except:
            return ''

    with ThreadPoolExecutor() as pool:
        css_contents = list(pool.map(fetch_text, css_urls))
        js_contents = list(pool.map(fetch_text, js_urls))

    if css_contents:
        style_tag = soup.new_tag('style')
        style_tag.string = '\n'.join(css_contents)
        if soup.head:
            soup.head.append(style_tag)
        for link in css_links:
            link.decompose()

    if js_contents:
        script_tag = soup.new_tag('script')
        script_tag.string = '\n'.join(js_contents)
        if soup.body:
            soup.body.append(script_tag)
        for script in script_links:
            script.decompose()

    parsed_url = urlparse(url)
    domain = parsed_url.netloc.replace('www.', '')
    save_path = 'output'
    os.makedirs(save_path, exist_ok=True)
    file_name = re.sub('[\\\\/:*?\"<>|]', '-', domain if domain else 'page_complet') + '.html'
    file_html = os.path.join(save_path, file_name)

    with open(file_html, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

    print(f'[+] successful phishing attack : {file_html}')
    input()

except Exception as e:
    print('[+] phishing attack fail')
    input()