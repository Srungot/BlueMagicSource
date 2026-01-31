# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'bruteforce_zip.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import zipfile
import os
import time
import psutil
from pystyle import *
from tqdm import tqdm
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor
import sys
import time
import platform
import os
import hashlib
from time import sleep
from datetime import datetime, UTC
def clear_screen():
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')
def get_zip_info(zip_file_path):
    """Récupère des infos sur le fichier ZIP et vérifie le chiffrement."""
    try:
        with zipfile.ZipFile(zip_file_path) as zf:
            num_files = len(zf.namelist())
            if num_files == 0:
                return (0, 'Unknown', False, 'ZIP file is empty')
            
            compression_methods = {zf.getinfo(name).compress_type for name in zf.namelist()}
            if hasattr(zipfile, 'compressor_names'):
                main_method = zipfile.compressor_names.get(max(compression_methods, default=0), 'Unknown')
            else:
                compression_map = {0: 'Stored', 8: 'Deflated', 9: 'Deflate64', 12: 'BZIP2', 14: 'LZMA'}
                main_method = compression_map.get(max(compression_methods, default=0), 'Unknown')
            
            is_encrypted = any((zf.getinfo(name).flag_bits & 1 for name in zf.namelist()))
            
            if not is_encrypted and num_files > 0:
                try:
                    with zf.open(zf.namelist()[0], 'r'):
                        pass
                    is_encrypted = False
                except RuntimeError:
                    is_encrypted = True
            
            return (num_files, main_method, is_encrypted, None)
    except zipfile.BadZipFile:
        return (0, 'Unknown', False, 'Invalid ZIP file')
def estimate_max_time(total_words, words_per_sec=50000):
    """Estime le temps max pour le bruteforce."""
    return total_words / words_per_sec
def bruteforce():
    clear_screen()
    num_workers = 4
    ascii_art = f'{Fore.LIGHTCYAN_EX}\n    ▓█████▄ ▓█████   ██████ ▄▄▄█████▓ ██▀███   ▒█████ ▓██   ██▓   ▒███████▒ ██▓ ██▓███  \n    ▒██▀ ██▌▓█   ▀ ▒██    ▒ ▓  ██▒ ▓▒▓██ ▒ ██▒▒██▒  ██▒▒██  ██▒   ▒ ▒ ▒ ▄▀░▓██▒▓██░  ██▒\n    ░██   █▌▒███   ░ ▓██▄   ▒ ▓██░ ▒░▓██ ░▄█ ▒▒██░  ██▒ ▒██ ██░   ░ ▒ ▄▀▒░ ▒██▒▓██░ ██▓▒\n    ░▓█▄   ▌▒▓█  ▄   ▒   ██▒░ ▓██▓ ░ ▒██▀▀█▄  ▒██   ██░ ░ ▐██▓░     ▄▀▒   ░░██░▒██▄█▓▒ ▒\n    ░▒████▓ ░▒████▒▒██████▒▒  ▒██▒ ░ ░██▓ ▒██▒░ ████▓▒░ ░ ██▒▓░   ▒███████▒░██░▒██▒ ░  ░\n    ▒▒▓  ▒ ░░ ▒░ ░▒ ▒▓▒ ▒ ░  ▒ ░░   ░ ▒▓ ░▒▓░░ ▒░▒░▒░   ██▒▒▒    ░▒▒ ▓░▒░▒░▓  ▒▓▒░ ░  ░\n    ░ ▒  ▒  ░ ░  ░░ ░▒  ░ ░    ░      ░▒ ░ ▒░  ░ ▒ ▒░ ▓██ ░▒░    ░░▒ ▒ ░ ▒ ▒ ░░▒ ░     \n    ░ ░  ░    ░   ░  ░  ░    ░        ░░   ░ ░ ░ ░ ▒  ▒ ▒ ░░     ░ ░ ░ ░ ░ ▒ ░░░       \n    ░       ░  ░      ░              ░         ░ ░  ░ ░          ░ ░     ░           \n    \n    ___________________________________________________________________________________\n    \n    \n    - ZIP Bruteforce Tool\n    - Ultra-fast dictionary attack for password-protected ZIP files.\n    - Multithreading with {num_workers} workers for extreme performance.\n    - Handles massive dictionaries and complex ZIPs with robust validation.\n    - Tracks advanced stats: words tested, speed, per-thread efficiency, CPU/memory usage.\n    - Saves comprehensive results to \'output/passwords.txt\'.\n    - Press \'Q\' to quit or \'R\' to retry if the password is not found.\n    \n    ___________________________________________________________________________________\n    '
    print(ascii_art)
    zip_file_path = ''
    while not zip_file_path:
        zip_file_path = input(Fore.LIGHTCYAN_EX + '\nEnter ZIP file path: ')
        if not zip_file_path:
            print(Fore.RED + '[ERROR] Input cannot be empty.')
        elif not os.path.exists(zip_file_path):
            print(Fore.RED + '[ERROR] ZIP file not found.')
            zip_file_path = ''
        else:
            num_files, compression_method, is_encrypted, error = get_zip_info(zip_file_path)
            if error:
                print(Fore.RED + f'[ERROR] {error}')
                zip_file_path = ''
            elif not is_encrypted:
                print(Fore.RED + '[ERROR] ZIP file is not password-protected.')
                zip_file_path = ''
            else:
                zip_size = os.path.getsize(zip_file_path) / 1048576
    dict_path = ''
    if not dict_path:
        dict_path = input(Fore.LIGHTCYAN_EX + 'Enter dictionary file path: ')
        if not dict_path:
            print(Fore.RED + '[ERROR] Input cannot be empty.')
        else:
            if not os.path.exists(dict_path):
                print(Fore.RED + '[ERROR] Dictionary file not found.')
                dict_path = ''
    with open(dict_path, 'r', encoding='utf-8', errors='ignore') as f:
        total_lines = sum((1 for _ in f))
        dict_size = os.path.getsize(dict_path) / 1048576
        f.seek(0)
    est_time = estimate_max_time(total_lines)
    cpu_count = os.cpu_count() or 1
    print(Fore.LIGHTCYAN_EX + f'\n[STATS] ZIP file size: {zip_size:.2f} MB')
    print(Fore.LIGHTCYAN_EX + f'[STATS] Number of files in ZIP: {num_files}')
    print(Fore.LIGHTCYAN_EX + f'[STATS] ZIP compression method: {compression_method}')
    print(Fore.LIGHTCYAN_EX + f'[STATS] ZIP is encrypted: {is_encrypted}')
    print(Fore.LIGHTCYAN_EX + f'[STATS] Dictionary size: {dict_size:.2f} MB, {total_lines} words')
    print(Fore.LIGHTCYAN_EX + f'[STATS] Using {num_workers} threads (CPU cores available: {cpu_count})')
    print(Fore.LIGHTCYAN_EX + f'[STATS] Estimated max time: {est_time:.2f} seconds (at 50k words/sec)')
    start_time = time.time()
    words_tested = 0
    cpu_times_start = psutil.cpu_times_percent()
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    def try_password(word, zip_file):
        try:
            zip_file.extractall(path=output_dir, pwd=word.encode())
            return word
        except RuntimeError:
            return
        except Exception as e:
            print(Fore.RED + f'[ERROR] Unexpected error: {e}')
    with zipfile.ZipFile(zip_file_path) as zip_file:
        pass
    with open(dict_path, 'r', encoding='utf-8', errors='ignore') as f:
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            for word in tqdm(f, desc='Bruteforcing ZIP', total=total_lines, unit='word'):
                    word = word.strip()
                    if not word:
                        continue
                    words_tested += 1
                    result = try_password(word, zip_file)
                    if result:
                        end_time = time.time()
                        elapsed_time = end_time - start_time
                        words_per_sec = words_tested / elapsed_time if elapsed_time > 0 else 0
                        words_per_thread = words_per_sec / num_workers if num_workers > 0 else 0
                        mem_usage = psutil.Process().memory_info().rss / 1048576
                        cpu_times_end = psutil.cpu_times_percent()
                        cpu_usage = (cpu_times_end.user - cpu_times_start.user) / elapsed_time * 100 if elapsed_time > 0 else 0
                        print(Fore.GREEN + f'\n[SUCCESS] Password found: {word}')
                        print(Fore.GREEN + f'[INFO] Time taken: {elapsed_time:.2f} seconds')
                        print(Fore.GREEN + f'[STATS] Words tested: {words_tested} ({words_tested / total_lines * 100:.2f}%)')
                        print(Fore.GREEN + f'[STATS] Average speed: {words_per_sec:.2f} words/sec')
                        print(Fore.GREEN + f'[STATS] Speed per thread: {words_per_thread:.2f} words/sec')
                        print(Fore.GREEN + f'[STATS] Approx. CPU usage: {cpu_usage:.2f}%')
                        print(Fore.GREEN + f'[STATS] Approx. memory usage: {mem_usage:.2f} MB')
                        print(Fore.GREEN + f'[STATS] ZIP files extracted: {num_files}')
                        print(Fore.GREEN + f'[STATS] ZIP compression method: {compression_method}')
                        with open(os.path.join(output_dir, 'passwords.txt'), 'w') as out_file:
                            out_file.write(f'Password: {word}\n')
                            out_file.write(f'Time taken: {elapsed_time:.2f} seconds\n')
                            out_file.write(f'Words tested: {words_tested} ({words_tested / total_lines * 100:.2f}%)\n')
                            out_file.write(f'Average speed: {words_per_sec:.2f} words/sec\n')
                            out_file.write(f'Speed per thread: {words_per_thread:.2f} words/sec\n')
                            out_file.write(f'Approx. CPU usage: {cpu_usage:.2f}%\n')
                            out_file.write(f'Approx. memory usage: {mem_usage:.2f} MB\n')
                            out_file.write(f'ZIP files extracted: {num_files}\n')
                            out_file.write(f'ZIP compression method: {compression_method}\n')
                        input(Fore.GREEN + '[INFO] Data saved to output/passwords.txt. Press Enter to continue.')
                        return True
        end_time = time.time()
        elapsed_time = end_time - start_time
        words_per_sec = words_tested / elapsed_time if elapsed_time > 0 else 0
        words_per_thread = words_per_sec / num_workers if num_workers > 0 else 0
        mem_usage = psutil.Process().memory_info().rss / 1048576
        cpu_times_end = psutil.cpu_times_percent()
        cpu_usage = (cpu_times_end.user - cpu_times_start.user) / elapsed_time * 100 if elapsed_time > 0 else 0
        print(Fore.RED + '\n[ERROR] Password not found in the provided dictionary.')
        print(Fore.RED + f'[STATS] Words tested: {words_tested} ({words_tested / total_lines * 100:.2f}%)')
        print(Fore.RED + f'[STATS] Time taken: {elapsed_time:.2f} seconds')
        print(Fore.RED + f'[STATS] Average speed: {words_per_sec:.2f} words/sec')
        print(Fore.RED + f'[STATS] Speed per thread: {words_per_thread:.2f} words/sec')
        print(Fore.RED + f'[STATS] Approx. CPU usage: {cpu_usage:.2f}%')
        print(Fore.RED + f'[STATS] Approx. memory usage: {mem_usage:.2f} MB')
        choice = input(Fore.LIGHTCYAN_EX + 'Retry [R] or Quit [Q]? ').lower()
        if choice == 'q':
            print(Fore.LIGHTCYAN_EX + '[INFO] Exiting program.')
            exit()
        return False
def main():
    while True:
        if bruteforce():
            return None
if __name__ == '__main__':
    def clear_screen():
        if os.name == 'posix':
            os.system('clear')
        else:
            os.system('cls')
    clear_screen()
    main()