import time
import sys
import shutil
import os
import hashlib
import subprocess
import msvcrt
import random
import math
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, 'program'))
def rgb_escape(r, g, b):
    return f'[38;2;{r};{g};{b}m'
def bg_escape(r, g, b):
    return f'[48;2;{r};{g};{b}m'
def reset_color():
    return '[0m'
def bold_on():
    return '[1m'
def blend_color(c1, c2, t):
    return (int(c1[0] + (c2[0] - c1[0]) * t), int(c1[1] + (c2[1] - c1[1]) * t), int(c1[2] + (c2[2] - c1[2]) * t))
def gradient(start_color, end_color, steps):
    gradient_colors = []
    for i in range(steps):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * i / (steps - 1))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * i / (steps - 1))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * i / (steps - 1))
        gradient_colors.append((r, g, b))
    return gradient_colors
def adjust_brightness(color, factor):
    r, g, b = color
    return (max(0, min(255, int(r * factor))), max(0, min(255, int(g * factor))), max(0, min(255, int(b * factor))))
GLITCH_CHARS = '@#$%&*+=-?/\\|<>[]{}01'
def glitch_text(line, intensity):
    out = ''
    for c in line:
        if c!= ' ' and random.random() < intensity:
            out += random.choice(GLITCH_CHARS)
        else:
            out += c
    return out
def ascii_glitch_intro(ascii_lines, duration=5.0):
    steps = 60
    delay = duration / steps
    start_color = (138, 43, 226)
    end_color = (0, 120, 255)
    for i in range(steps):
        t = i / (steps - 1)
        intensity = 1.0 - t
        r, g, b = blend_color(start_color, end_color, t)
        sys.stdout.write('[H')
        for line in ascii_lines:
            offset = ' ' * random.randint(0, int(6 * intensity))
            glitched = glitch_text(line, intensity)
            sys.stdout.write(f'{offset}[38;2;{r};{g};{b}m{glitched}[0m\n')
        sys.stdout.flush()
        time.sleep(delay)
    time.sleep(0.2)
    os.system('cls' if os.name == 'nt' else 'clear')
def animate_color_cycle(c1, c2, steps=100):
    step = 0
    direction = 1
    while True:
        t = step / (steps - 1)
        yield blend_color(c1, c2, t)
        step += direction
        if step >= steps - 1:
            direction = (-1)
        else:
            if step <= 0:
                direction = 1
def animate_float_cycle(a, b, steps=100):
    step = 0
    direction = 1
    while True:
        t = step / (steps - 1)
        yield (a + (b - a) * t)
        step += direction
        if step >= steps - 1:
            direction = (-1)
        else:
            if step <= 0:
                direction = 1
def animate_box_edges(box_width, box_height, visible_frac=0.3):
    perim = 2 * (box_width + box_height - 2)
    visible = max(1, int(perim * visible_frac))
    step = 0
    while True:
        mask = [False] * perim
        for i in range(visible):
            mask[(step + i) % perim] = True
        yield mask
        step = (step + 1) % perim
def build_boxes(categories, box_width, box_height, padding=2):
    boxes = []
    inner_w = box_width - 2
    for title, items in categories:
        lines = []
        title_padding = max(padding - 2, 0)
        lines.append(' ' * title_padding + title.center(inner_w))
        lines.append('─' * inner_w)
        for it in items:
            lines.append(' ' * padding + it.ljust(inner_w))
        while len(lines) < box_height:
            lines.append(' ' * padding + ' ' * inner_w)
        boxes.append(lines)
    return boxes
def _shimmer_text(text, base_rgb, phase, spread=10):
    width = len(text)
    if width == 0:
        return text
    else:
        pos = phase % max(1, width)
        out = []
        for idx, ch in enumerate(text):
            dist = abs(idx - pos)
            dist = min(dist, width - dist)
            intensity = 1.0 - dist / max(1, spread)
            if intensity < 0:
                intensity = 0
            factor = 0.65 + 0.95 * intensity
            r, g, b = adjust_brightness(base_rgb, factor)
            out.append(f'{rgb_escape(r, g, b)}{ch}')
        out.append(reset_color())
        return ''.join(out)
def render_frame(ascii_lines, boxes, color_escape, edge_mask, box_width, box_height, padding, left_margin=2, box_colors=None, selected_box=None, shimmer_phase=0, pulse=1.0, ascii_offset_x=0, ascii_offset_y=0):
    if box_colors is None:
        box_colors = [None] * len(boxes)
    out = []
    for _ in range(max(0, int(ascii_offset_y))):
        out.append('')
    for line in ascii_lines:
        out.append(f"{color_escape}{' ' * max(0, int(ascii_offset_x))}{line}{reset_color()}")
    out.append('')
    for y in range(box_height + 2):
        parts = []
        for i, box in enumerate(boxes):
            specific_color = box_colors[i]
            base_rgb = None
            if isinstance(specific_color, list):
                grad_index = min(y, len(specific_color) - 1)
                base_rgb = specific_color[grad_index]
                box_color_escape = rgb_escape(*base_rgb)
            else:
                if specific_color is not None:
                    base_rgb = specific_color
                    box_color_escape = rgb_escape(*base_rgb)
                else:
                    box_color_escape = color_escape
                    base_rgb = (135, 206, 250)
            if selected_box is not None and i == selected_box:
                    br = 1.05 + 0.35 * max(0.0, min(1.0, pulse))
                    base_rgb = adjust_brightness(base_rgb, br)
                    box_color_escape = rgb_escape(*base_rgb)
            if y == 0:
                seg = ['─' if edge_mask[x] else ' ' for x in range(box_width - 2)]
                row = f"╭{''.join(seg)}╮"
                parts.append(f'{box_color_escape}{row}{reset_color()}')
            else:
                if y == box_height + 1:
                    seg = []
                    for x in range(box_width - 2):
                        idx = box_width - 2 + (box_height - 1) + (box_width - 2 - x)
                        seg.append('─' if edge_mask[idx] else ' ')
                    row = f"╰{''.join(seg)}╯"
                    parts.append(f'{box_color_escape}{row}{reset_color()}')
                else:
                    content = box[y - 1][:box_width - 2].ljust(box_width - 2)
                    left_idx = box_width - 2 + (y - 1)
                    right_idx = box_width - 2 + (box_height - 1) + (box_width - 2) + (box_height - 1 - (y - 1))
                    left_pipe = '│' if edge_mask[left_idx] else ' '
                    right_pipe = '│' if edge_mask[right_idx] else ' '
                    if y - 1 == 0:
                        title = content.strip('\n')
                        pad_left = len(content) - len(content.lstrip(' '))
                        pad_right = len(content) - len(content.rstrip(' '))
                        inner = content[pad_left:len(content) - pad_right] if pad_right > 0 else content[pad_left:]
                        shimmer = _shimmer_text(inner, base_rgb, shimmer_phase + i * 7, spread=8)
                        row = f"{left_pipe}{' ' * pad_left}{shimmer}{' ' * pad_right}{right_pipe}"
                        parts.append(f'{box_color_escape}{row}{reset_color()}')
                    else:
                        if content.lstrip().startswith('▶'):
                            pad_left = len(content) - len(content.lstrip(' '))
                            pad_right = len(content) - len(content.rstrip(' '))
                            inner = content[pad_left:len(content) - pad_right] if pad_right > 0 else content[pad_left:]
                            shimmer = _shimmer_text(inner, base_rgb, shimmer_phase * 2 + i * 11, spread=6)
                            row = f"{left_pipe}{' ' * pad_left}{shimmer}{' ' * pad_right}{right_pipe}"
                            parts.append(f'{box_color_escape}{row}{reset_color()}')
                        else:
                            row = f'{left_pipe}{content}{right_pipe}'
                            parts.append(f'{box_color_escape}{row}{reset_color()}')
        out.append(' ' * left_margin + (' ' * padding).join(parts))
    out.append(reset_color())
    return '\n'.join(out)
def main():
    ascii_block = '\n                                            .       ✦       .         *        .  \n                                    *           .         ·      .         .   \n                                        .     ✦      .         *     .        \n                                                *     .       .     \n\n                    ▄▄▄▄    ██▓     █    ██ ▓█████     ███▄ ▄███▓ ▄▄▄         ▄████  ██▓ ▄████▄            \n                    ▓█████▄ ▓██▒     ██  ▓██▒▓█   ▀    ▓██▒▀█▀ ██▒▒████▄     ██▒ ▀█▒▓██▒▒██▀ ▀█            \n                    ▒██▒ ▄██▒██░    ▓██  ▒██░▒███      ▓██   ▓██░▒██  ▀█▄  ▒██░▄▄▄░▒██▒▒▓█    ▄            \n                    ▒██░█▀  ▒██░    ▓▓█  ░██░▒▓█  ▄    ▒██   ▒██ ░██▄▄▄▄██ ░▓█  ██▓░██░▒▓▓▄ ▄██▒            \n                    ░▓█  ▀█▓░██████▒▒▒█████▓ ░▒████▒   ▒██▒   ░██▒ ▓█   ▓██▒░▒▓███▀▒░██░▒ ▓███▀ ░            \n                    ░▒▓███▀▒░ ▒░▓  ░░▒▓▒ ▒ ▒ ░░ ▒░ ░   ░ ▒░   ░  ░ ▒▒   ▓▒█░ ░▒   ▒ ░▓  ░ ░▒ ▒  ░            \n                    ▒░▒   ░ ░ ░ ▒  ░░░▒░ ░ ░   ░  ░   ░  ░      ░  ▒   ▒▒ ░  ░   ░  ▒ ░  ░  ▒                \n                    ░    ░   ░ ░     ░░░ ░ ░   ░      ░      ░     ░   ▒   ░ ░   ░  ░  ░ ░                   \n                        ░         ░       ░       ░               ░          ░         ░       \n'
    ascii_lines = ascii_block.rstrip('\n').splitlines()
    sys.stdout.write('[2J[H')
    sys.stdout.flush()
    ascii_glitch_intro(ascii_lines, duration=5.0)
    categories = [
        ('MALWARE Build', [
            '[01] RAT Build',
            '[02] Keylogger Build',
            '[03] Stealer Build',
            '[04] Grabber Build',
            '[05] Ransomware Build',
            '[06] Wifi Stealer Build',
            '[07] Virus Build',
            '[08] Tlg Stealer Build',
            '[09] Injector.Py Build'
        ]),
        ('Scam', [
            '[10] Id Card Fraud',
            '[11] CC Validator',
            '[12] Phishing Attack',
            '[13] FakeAddress',
            '[14] Spoofer',
            '[15] Iban Generator',
            '[16] Fake Exodus',
            '[17] Fake Paypal Screen',
            '[18] Fake Voice'
        ]),
        ('Panel & Tools', [
            '[19] Discord Dox Track',
            '[20] Bruteforce Zip',
            '[21] Obsfucator',
            '[22] Discord Bot Pannel',
            '[23] Token Pannel',
            '[24] Usb Tool',
            '[25] Exe to Image',
            '[26] Anti-Grabb',
            '[27] Self Bot Advanced'
        ]),
        ('NETWORK', [
            '[28] Ip Tool',
            '[29] Email Tool',
            '[30] Ddos',
            '[31] Phone Lookup',
            '[32] Web Scanner',
            '[33] Man Of The Middle',
            '[34] TempMail',
            '[35] Cleaner Magic',
            '[36] Dark Gpt'
        ])
    ]
    padding = 3
    term_cols, term_rows = shutil.get_terminal_size(fallback=(120, 40))
    total_available = term_cols - padding * (len(categories) - 1)
    box_width = total_available // len(categories)
    box_height = max((len(items) + 2 for _, items in categories))
    boxes = build_boxes(categories, box_width, box_height)
    base_gradient = gradient((255, 140, 0), (138, 43, 226), box_height + 2)
    color_anim = animate_color_cycle((135, 206, 250), (138, 43, 226), steps=100)
    brightness_anim = animate_float_cycle(0.5, 1.2, steps=100)
    edge_anim = animate_box_edges(box_width, box_height, visible_frac=0.25)
    selected_box = 0
    selected_item = 0
    items_per_box = [len(items) for _, items in categories]
    box_count = len(categories)
    tick = 0
    sys.stdout.write('[2J[H')
    sys.stdout.flush()
    PYTHON_311 = 'C:\\Users\\{}\\AppData\\Local\\Programs\\Python\\Python311\\python.exe'.format(os.getlogin())
    try:
        while True:
            r, g, b = next(color_anim)
            bright = next(brightness_anim)
            mask = next(edge_anim)
            inverted_bright = 1.7 - bright
            malware_grad = [adjust_brightness(c, inverted_bright) for c in base_gradient]
            scam_color = adjust_brightness((255, 0, 0), inverted_bright)
            pannel_color = adjust_brightness((0, 255, 255), inverted_bright)
            network_color = adjust_brightness((0, 255, 0), inverted_bright)
            box_colors = [malware_grad, scam_color, pannel_color, network_color]
            display_boxes = [list(b) for b in boxes]
            item_line_index = 2 + selected_item
            selected_box %= box_count
            if selected_item < 0:
                selected_item = 0
            if selected_item >= items_per_box[selected_box]:
                selected_item = items_per_box[selected_box] - 1
            line = display_boxes[selected_box][item_line_index]
            if len(line) > 0:
                cursor_char = '▶'
                new_line = cursor_char + line[len(cursor_char):]
                display_boxes[selected_box][item_line_index] = new_line
            pulse = (bright - 0.5) / 0.7
            ascii_offset_x = int((math.sin(tick * 0.07) + 1.0) / 2.0 * 2.0)
            ascii_offset_y = int((math.sin(tick * 0.05) + 1.0) / 2.0 * 1.0)
            frame = render_frame(ascii_lines, display_boxes, rgb_escape(r, g, b), mask, box_width, box_height, padding, left_margin=2, box_colors=box_colors, selected_box=selected_box, shimmer_phase=tick, pulse=pulse, ascii_offset_x=ascii_offset_x, ascii_offset_y=ascii_offset_y)
            sys.stdout.write('[H')
            sys.stdout.write(frame)
            sys.stdout.flush()
            tick = (tick + 1) % 1000000
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key in (b'\x00', b'\xe0'):
                    key2 = msvcrt.getch()
                    if key2 == b'H':
                        selected_item = (selected_item - 1) % items_per_box[selected_box]
                    else:
                        if key2 == b'P':
                            selected_item = (selected_item + 1) % items_per_box[selected_box]
                        else:
                            if key2 == b'K':
                                prev_box = (selected_box - 1) % box_count
                                selected_box = prev_box
                                if selected_item >= items_per_box[selected_box]:
                                    selected_item = items_per_box[selected_box] - 1
                            else:
                                if key2 == b'M':
                                    nxt_box = (selected_box + 1) % box_count
                                    selected_box = nxt_box
                                    if selected_item >= items_per_box[selected_box]:
                                        selected_item = items_per_box[selected_box] - 1
                else:
                    try:
                        ch = key.decode('utf-8', errors='ignore').lower()
                    except Exception:
                        ch = ''
                    if ch in ['w', 'k']:
                        selected_item = (selected_item - 1) % items_per_box[selected_box]
                    else:
                        if ch in ['s', 'j']:
                            selected_item = (selected_item + 1) % items_per_box[selected_box]
                        else:
                            if ch in ['a', 'h']:
                                prev_box = (selected_box - 1) % box_count
                                selected_box = prev_box
                                if selected_item >= items_per_box[selected_box]:
                                    selected_item = items_per_box[selected_box] - 1
                            else:
                                if ch in ['d', 'l']:
                                    nxt_box = (selected_box + 1) % box_count
                                    selected_box = nxt_box
                                    if selected_item >= items_per_box[selected_box]:
                                        selected_item = items_per_box[selected_box] - 1
                                else:
                                    if key == b'\r':
                                        chosen = categories[selected_box][1][selected_item]
                                        executable_map = {
                                            '[01] RAT Build': 'rat_builder/rat_builder.py',
                                            '[02] Keylogger Build': 'keylogger/Keylogger.py',
                                            '[03] Stealer Build': 'stealer/stealer.py',
                                            '[04] Grabber Build': 'grabber/grabber.py',
                                            '[05] Ransomware Build': 'ransomwarebuild/ransom_build.py',
                                            '[06] Wifi Stealer Build': 'wifi/wifi.py',
                                            '[07] Virus Build': 'virus/virus_builder.py',
                                            '[08] Tlg Stealer Build': 'telegram/telegrambuild.py',
                                            '[09] Injector.Py Build': 'buildtest.py',
                                            '[10] Id Card Fraud': 'fraude.py',
                                            '[11] CC Validator': 'ccvalidator.py',
                                            '[12] Phishing Attack': 'phishing.py',
                                            '[13] FakeAddress': 'fakeadresse.py',
                                            '[14] Spoofer': 'spoofer.py',
                                            '[15] Iban Generator': 'ibangenerator.py',
                                            '[16] Fake Exodus': 'fake_exodus.py',
                                            '[17] Fake Paypal Screen': 'paypalfakescreen.py',
                                            '[18] Fake Voice': 'fakevoice.py',
                                            '[19] Discord Dox Track': 'doxtool.py',
                                            '[20] Bruteforce Zip': 'bruteforce_zip.py',
                                            '[21] Obsfucator': 'obfuscator.py',
                                            '[22] Discord Bot Pannel': 'discordtool.py',
                                            '[23] Token Pannel': 'Token Tool.py',
                                            '[24] Usb Tool': 'usbtoolkit.py',
                                            '[25] Exe to Image': 'exe-to-image.py',
                                            '[26] Anti-Grabb': 'antigrab.py',
                                            '[27] Self Bot Advanced': 'selfbot.py',
                                            '[28] Ip Tool': 'iptool.py',
                                            '[29] Email Tool': 'email_tool.py',
                                            '[30] Ddos': 'ddos.py',
                                            '[31] Phone Lookup': 'phonenumber.py',
                                            '[32] Web Scanner': 'websitescan.py',
                                            '[33] Man Of The Middle': 'arpspoofing.py',
                                            '[34] TempMail': 'tempmail.py',
                                            '[35] Cleaner Magic': 'ccleaner.py',
                                            '[36] Dark Gpt': 'darkgpt.py'
                                        }
                                        program_dir = os.path.join(os.getcwd(), 'program')
                                        relative_path = executable_map.get(chosen)
                                        if relative_path:
                                            exe_path = os.path.join(program_dir, relative_path)
                                            if os.path.exists(exe_path):
                                                is_malware_build = chosen in ['[01] RAT Build', '[02] Keylogger Build', '[03] Stealer Build', '[04] Grabber Build', '[05] Ransomware Build', '[06] Wifi Stealer Build', '[07] Virus Build', '[08] Tlg Stealer Build', '[09] Injector.Py Build']
                                                if is_malware_build:
                                                    os.system('cls' if os.name == 'nt' else 'clear')
                                                    time.sleep(0.1)
                                                if not is_malware_build:
                                                    sys.stdout.write(reset_color() + f'\nLancement: {relative_path}\n')
                                                    sys.stdout.flush()
                                                try:
                                                    if exe_path.lower().endswith('.py'):
                                                        if os.path.exists(PYTHON_311):
                                                            subprocess.run([PYTHON_311, '-u', exe_path], cwd=BASE_DIR, check=True)
                                                        else:
                                                            subprocess.run(['py', '-3.11', '-u', exe_path], cwd=BASE_DIR, check=True)
                                                    else:
                                                        script_dir = os.path.dirname(exe_path)
                                                        subprocess.run([exe_path], cwd=script_dir, check=True)
                                                except subprocess.CalledProcessError as e:
                                                    sys.stdout.write(f'Erreur lors de l\'exécution : {e}\n')
                                                except FileNotFoundError:
                                                    sys.stdout.write(f'Erreur : {relative_path} introuvable ou Python 3.11 absent.\n')
                                                except Exception as e:
                                                    sys.stdout.write(f'Erreur inattendue : {e}\n')
                                                time.sleep(0.5)
                                                os.system('cls' if os.name == 'nt' else 'clear')
                                                sys.stdout.write('[H')
                                                sys.stdout.flush()
                                            else:
                                                sys.stdout.write(f'Erreur : {relative_path} introuvable\n')
                                                time.sleep(2)
                                        else:
                                            sys.stdout.write(f'Erreur : Aucun fichier associé à {chosen}\n')
                                            time.sleep(2)
            time.sleep(0.05)
    except KeyboardInterrupt:
        sys.stdout.write(reset_color() + '\n')
if __name__ == '__main__':
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')
    def getchecksum():
        md5_hash = hashlib.md5()
        with open(sys.argv[0], 'rb') as f:
            md5_hash.update(f.read())
        return md5_hash.hexdigest()
    clear_screen()
    main()
