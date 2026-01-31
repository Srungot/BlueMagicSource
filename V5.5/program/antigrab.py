import os
import sys
import time
import ctypes
from colorama import Fore, Style, init
import hashlib
init(autoreset=True)
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
def relaunch_as_admin():
    params = ' '.join([f'\"{arg}\"' for arg in sys.argv])
    ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, params, None, 1)
    sys.exit(0)
if not is_admin():
    print(Fore.LIGHTCYAN_EX + '[*] Administrator privileges required, relaunching...')
    relaunch_as_admin()
def cyan(text):
    print(Fore.LIGHTCYAN_EX + text + Style.RESET_ALL)
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
def slow_print(text, delay=0.002):
    for c in text:
        print(Fore.LIGHTCYAN_EX + c, end='', flush=True)
        time.sleep(delay)
    print()
import msvcrt
locked_files = []
def lock_file(path):
    try:
        f = open(path, 'rb')
        msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, os.path.getsize(path))
        locked_files.append(f)
    except:
        return None
def protect_discord():
    base = os.getenv('APPDATA')
    leveldb = os.path.join(base, 'discord', 'Local Storage', 'leveldb')
    if os.path.exists(leveldb):
        for file in os.listdir(leveldb):
            if file.endswith('.ldb') or file.endswith('.log'):
                lock_file(os.path.join(leveldb, file))
    cyan('[+] Anti-Grabb Discord enabled')
def protect_telegram():
    base = os.getenv('APPDATA')
    tdata = os.path.join(base, 'Telegram Desktop', 'tdata')
    if os.path.exists(tdata):
        for root, _, files in os.walk(tdata):
            for f in files:
                lock_file(os.path.join(root, f))
    cyan('[+] Anti-Grabb Telegram enabled')
def protect_browsers():
    paths = [os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data', 'Default'), os.path.join(os.getenv('LOCALAPPDATA'), 'Microsoft', 'Edge', 'User Data', 'Default'), os.path.join(os.getenv('LOCALAPPDATA'), 'BraveSoftware', 'Brave-Browser', 'User Data', 'Default')]
    targets = ['Login Data', 'History', 'Cookies', 'Web Data']
    for path in paths:
        if os.path.exists(path):
            for t in targets:
                lock_file(os.path.join(path, t))
    cyan('[+] Anti-Grabb Browsers enabled')
def banner():
    slow_print('\n __    __  __  __  __           ______                      __        __       \n|  \\  /  \\|  \\|  \\|  \\         /      \\                    |  \\      |  \\      \n| $$ /  $$ \\$$| $$| $$        |  $$$$$$\\  ______   ______  | $$____  | $$____  \n| $$/  $$ |  \\| $$| $$ ______ | $$ __\\$$ /      \\ |      \\ | $$    \\ | $$    \\ \n| $$  $$  | $$| $$| $$|      \\| $$|    \\|  $$$$$$\\ \\$$$$$$\\| $$$$$$$\\| $$$$$$$\\\n| $$$$$\\  | $$| $$| $$ \\$$$$$$| $$ \\$$$$| $$   \\$$/      $$| $$  | $$| $$  | $$\n| $$ \\$$\\ | $$| $$| $$        | $$__| $$| $$     |  $$$$$$$| $$__/ $$| $$__/ $$\n| $$  \\$$\\| $$| $$| $$         \\$$    $$| $$      \\$$    $$| $$    $$| $$    $$\n \\$$   \\$$ \\$$ \\$$ \\$$          \\$$$$$$  \\$$       \\$$$$$$$ \\$$$$$$$  \\$$$$$$$ \n                                                                               \n========================= ANTI-GRABB TOOL =========================\n\n Temporary anti-grabber & anti-exfiltration tool\n No data collection - No persistence - Session based\n\n===================================================================\n')
def menu():
    cyan('[1] Anti-Grabb Discord')
    cyan('[2] Anti-Grabb Telegram')
    cyan('[3] Anti-Grabb Browsers')
    cyan('[4] Anti-Grabb ALL')
    cyan('[0] Quit')
    return input(Fore.LIGHTCYAN_EX + '\nSelect option: ').lower()
def main():
    clear()
    banner()
    choice = menu()
    if choice == '1':
        protect_discord()
    else:
        if choice == '2':
            protect_telegram()
        else:
            if choice == '3':
                protect_browsers()
            else:
                if choice == '4':
                    protect_discord()
                    protect_telegram()
                    protect_browsers()
                    cyan('[+] ANTI-GRABB ALL ENABLED')
                else:
                    if choice == '0':
                        return
    cyan('\n[+] Anti-Grabb active - Close the tool to restore system')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        cyan('[+] Anti-Grabb disabled, system restored')
if __name__ == '__main__':
    def clear_screen():
        if os.name == 'posix':
            os.system('clear')
        else:
            os.system('cls')
    clear_screen()
    main()