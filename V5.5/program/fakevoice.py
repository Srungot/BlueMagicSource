# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'fakevoice.py'
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

global _AVAILABLE_VOICE_SHORTNAMES
import os
import sys
import hashlib
import asyncio
import time
from pathlib import Path
import subprocess
from colorama import Fore, Style, init
init(autoreset=True)
try:
    import edge_tts
except ImportError:
    print(f'{Fore.RED}[ERREUR] edge-tts non installé. Installe avec: pip install edge-tts{Style.RESET_ALL}')
    exit(1)
OUTPUT_DIR = Path('output')
OUTPUT_DIR.mkdir(exist_ok=True)
VOIX_FEMMES = {'fr_eloise': 'fr-FR-EloiseNeural', 'fr_denise': 'fr-FR-DeniseNeural', 'fr_claire': 'fr-CA-SylvieNeural', 'fr_sexy': 'fr-FR-DeniseNeural'}
_AVAILABLE_VOICE_SHORTNAMES = None
async def _get_available_voice_shortnames():
    global _AVAILABLE_VOICE_SHORTNAMES
    if _AVAILABLE_VOICE_SHORTNAMES is not None:
        return _AVAILABLE_VOICE_SHORTNAMES
    else:
        try:
            voices = await edge_tts.list_voices()
            _AVAILABLE_VOICE_SHORTNAMES = {v.get('ShortName') for v in voices if v.get('ShortName')}
        except Exception:
            _AVAILABLE_VOICE_SHORTNAMES = set()
        return _AVAILABLE_VOICE_SHORTNAMES
def play_audio(filepath):
    """Joue un fichier audio avec le lecteur par défaut Windows"""
    try:
        os.startfile(filepath)
    except Exception as e:
        print(f'{Fore.RED}[ERREUR] Impossible de jouer : {e}{Style.RESET_ALL}')
async def generate_femme_voice(text, voix='fr_eloise'):
    """Génère une voix de femme naturelle et crédible avec meilleure qualité"""
    try:
        print(f'{Fore.RED}[GENERATION] Synthesizing female voice: \"{text}\"{Style.RESET_ALL}')
        voice = VOIX_FEMMES.get(voix, VOIX_FEMMES['fr_eloise'])
        available = await _get_available_voice_shortnames()
        if available and voice not in available:
            print(f'{Fore.RED}[WARN] Voice \'{voice}\' not available. Falling back to fr-FR-EloiseNeural.{Style.RESET_ALL}')
            voice = 'fr-FR-EloiseNeural'
        filename = OUTPUT_DIR / f'femme_troll_{int(time.time())}.mp3'
        if voix == 'fr_sexy':
            rate = '-15%'
            pitch = '-2Hz'
            print(f'{Fore.RED}[SEXY MODE] Voix adulte sensuelle activée...{Style.RESET_ALL}')
        elif voix == 'fr_denise':
            rate = '-5%'
            pitch = '+2Hz'
        else:
            rate = '-10%'
            pitch = '+8Hz'
        communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate, pitch=pitch)
        await communicate.save(str(filename))
        print(f'{Fore.RED}[OK] File generated: {filename}{Style.RESET_ALL}')
        print(f'{Fore.RED}[PLAYBACK] Playing...{Style.RESET_ALL}')
        play_audio(str(filename))
    except Exception as e:
        msg = str(e)
        if 'No audio was received' in msg and voice != 'fr-FR-EloiseNeural':
            print(f'{Fore.RED}[WARN] No audio received, retry with fr-FR-EloiseNeural...{Style.RESET_ALL}')
            try:
                fallback = edge_tts.Communicate(text=text, voice='fr-FR-EloiseNeural', rate='-5%', pitch='+2Hz')
                await fallback.save(str(filename))
                print(f'{Fore.RED}[OK] File generated: {filename}{Style.RESET_ALL}')
                print(f'{Fore.RED}[PLAYBACK] Playing...{Style.RESET_ALL}')
                play_audio(str(filename))
            except Exception as e2:
                print(f'{Fore.RED}[ERROR] {e2}{Style.RESET_ALL}')
                return None
        else:
            print(f'{Fore.RED}[ERROR] {e}{Style.RESET_ALL}')
            return None
def main():
    ascii_art = '\n                 .#@.           \n               .%@@@.           \n             :@@@@@@.  ...      \n          .:@@@@@@@@. .%@@@=.   \n         -@@@@@@@@@@.    .#@@=. \n-@@@@@@-*@@@@@@@@@@@. .@@: .@@* \n@@@@@@@-*@@@@@@@@@@@.  .%@#..@@+\n@@@@@@@-*@@@@@@@@@@@.   .%@* .@@\n@@@@@@@-*@@@@@@@@@@@.    :@#  @@\n@@@@@@@-*@@@@@@@@@@@.   .%@* .@@\n@@@@@@@-*@@@@@@@@@@@.  .%@#..@@+\n-@@@@@@-*@@@@@@@@@@@. .@@: .@@* \n         -@@@@@@@@@@.    .*@@=. \n          .:@@@@@@@@. .#@@@=.   \n             :@@@@@@.  ...      \n               .%@@@.           \n                 .#@.                                         \n    '
    print(f'{Fore.RED}{ascii_art}{Style.RESET_ALL}')
    print(f'{Fore.RED}' + '══════════════════════════════════════════════════' + f'{Style.RESET_ALL}')
    print(f'{Fore.RED}   FAKE VOICE GENERATOR - ADULT FEMALE VOICE{Style.RESET_ALL}')
    print(f'{Fore.RED}' + '══════════════════════════════════════════════════' + f'{Style.RESET_ALL}')
    print(f'{Fore.RED}\n Voice Options:{Style.RESET_ALL}')
    print(f'{Fore.RED}  1. Natural Young Voice (Eloise) - RECOMMENDED{Style.RESET_ALL}')
    print(f'{Fore.RED}  2. Natural Voice (Denise){Style.RESET_ALL}')
    print(f'{Fore.RED}  3. Quebec Voice (Sylvie) - Very Natural{Style.RESET_ALL}')
    print(f'{Fore.RED}  4. SEXY Adult Voice{Style.RESET_ALL}')
    voix_choice = input(f'\n{Fore.RED}Choose voice (1-4) [1] → {Style.RESET_ALL}').strip() or '1'
    voix_map = {'1': 'fr_eloise', '2': 'fr_denise', '3': 'fr_claire', '4': 'fr_sexy'}
    voix = voix_map.get(voix_choice, 'fr_eloise')
    print(f'\n{Fore.RED}' + '──────────────────────────────────────────────────' + f'{Style.RESET_ALL}')
    text = input(f'{Fore.RED} Fake Voice: {Style.RESET_ALL}').strip()
    print(f'{Fore.RED}' + '──────────────────────────────────────────────────' + f'{Style.RESET_ALL}')
    if not text:
        print(f'{Fore.RED} Text cannot be empty!{Style.RESET_ALL}')
    else:
        asyncio.run(generate_femme_voice(text, voix))
        if input(f'\n{Fore.RED} Generate another voice? (y/n) [n] → {Style.RESET_ALL}').lower() == 'y':
            main()
        else:
            print(f'\n{Fore.RED} Goodbye!{Style.RESET_ALL}')
if __name__ == '__main__':
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')
    clear_screen()
    try:
        main()
    except KeyboardInterrupt:
        print(f'\n\n{Fore.RED} Stopped{Style.RESET_ALL}')
    except Exception as e:
        print(f'{Fore.RED}[ERROR] {e}{Style.RESET_ALL}')