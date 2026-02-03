import customtkinter as ctk
import requests
import urllib.parse
import os
import json
import sys
import hashlib
from datetime import datetime, timedelta
import pystray
from PIL import Image, ImageDraw
import threading
def getchecksum():
    md5_hash = hashlib.md5()
    with open(sys.argv[0], 'rb') as file:
        md5_hash.update(file.read())
    return md5_hash.hexdigest()
TIMER_FILE = os.path.join(os.getenv('APPDATA'), '.tempmail_timer.json')
def load_timer():
    if os.path.exists(TIMER_FILE):
        try:
            with open(TIMER_FILE, 'r') as f:
                data = json.load(f)
                end_time = datetime.fromisoformat(data['end_time'])
                if datetime.now() < end_time:
                    return end_time
        except (json.JSONDecodeError, KeyError, ValueError):
            pass
    return None

def save_timer(end_time):
    data = {'end_time': end_time.isoformat()}
    with open(TIMER_FILE, 'w') as f:
        json.dump(data, f)

def delete_timer():
    if os.path.exists(TIMER_FILE):
        os.remove(TIMER_FILE)

API_KEY = 'VXdt4utF7kEFHsnTmNKe'
BASE_URL = 'https://api.temp-mail.io/v1'
HEADERS = {'X-API-Key': API_KEY, 'Accept': 'application/json'}

def api_create_email():
    r = requests.post(f'{BASE_URL}/emails', headers=HEADERS)
    return r.json().get('email') if r.status_code == 200 else None
def api_inbox(email):
    e = urllib.parse.quote(email, safe='')
    r = requests.get(f'{BASE_URL}/emails/{e}/messages', headers=HEADERS)
    if r.status_code == 200:
        return r.json().get('messages', [])
    else:
        return []
def api_read_message(email, mid):
    r = requests.get(f'{BASE_URL}/messages/{mid}', headers=HEADERS)
    return r.json() if r.status_code == 200 else None
def show_license_window():
    # ***<module>.show_license_window: Failure: Different bytecode
    ctk.set_appearance_mode('dark')
    license_app = ctk.CTk()
    license_app.title('LICENSE REQUIRED')
    license_app.geometry('900x600')
    license_app.resizable(False, False)
    license_app.configure(fg_color='#000000')
    header = ctk.CTkFrame(license_app, fg_color='#1a0000', corner_radius=0, border_width=6, border_color='#ff0033')
    header.pack(fill='x')
    ctk.CTkLabel(header, text='ACCESS DENIED – ENTER LICENSE', font=('Consolas', 32, 'bold'), text_color='#ff0033').pack(pady=30)
    body = ctk.CTkFrame(license_app, fg_color='#110000', border_width=5, border_color='#ff0033')
    body.pack(pady=80, padx=100, fill='both', expand=True)
    ctk.CTkLabel(body, text='License :', font=('Consolas', 24), text_color='#ff6666').pack(pady=40)
    license_entry = ctk.CTkEntry(body, width=500, height=60, font=('Consolas', 20), fg_color='#220000', text_color='#ff3333', border_width=4, border_color='#ff0033')
    license_entry.pack(pady=20)
    license_entry.focus()
    status_label = ctk.CTkLabel(body, text='', font=('Consolas', 32, 'bold'), text_color='#ff3333')
    status_label.pack(pady=30)
    def validate_license(event=None):
        # ***<module>.show_license_window.validate_license: Failure: Compilation Error
        key = license_entry.get().strip()
        if not key:
            status_label.configure(text='❌ Enter a key', text_color='#ff0000')
            return
        else:
            try:
                status_label.configure(text='✔ VALID LICENSE — LOADING…', text_color='#00ff00')
                license_app.after(1200, lambda: (license_app.destroy(), launch_main_app()))
            except Exception:
                status_label.configure(text='❌ INVALID KEY', text_color='#ff0000')
                return None
    license_entry.bind('<Return>', validate_license)
    enter_btn = ctk.CTkButton(body, text='ENTER', font=('Consolas', 24, 'bold'), fg_color='#cc0000', hover_color='#990000', width=300, height=80, border_width=5, border_color='#ff0033', command=validate_license)
    enter_btn.pack(pady=40)
    license_app.mainloop()
def create_tray_icon(app):
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), (255, 0, 0))
    dc = ImageDraw.Draw(image)
    dc.rectangle((0, 0, width, height), fill=(255, 0, 0))
    def on_quit(icon, item):
        icon.stop()
        app.destroy()
    def on_show(icon, item):
        app.after(0, app.deiconify)
    menu = pystray.Menu(pystray.MenuItem('Ouvrir', on_show), pystray.MenuItem('Quitter', on_quit))
    icon = pystray.Icon('TempMail', image, 'TempMail', menu)
    icon.run_detached()
def launch_main_app():
    app = ctk.CTk()
    app.overrideredirect(True)
    app.geometry('900x600')
    app.resizable(False, False)
    app.configure(fg_color='#000000')
    header = ctk.CTkFrame(app, fg_color='#1a0000', corner_radius=0, border_width=6, border_color='#ff0033')
    header.pack(fill='x')
    title = ctk.CTkLabel(header, text='TEMP MAIL BLUEMAGIC', font=('Consolas', 28, 'bold'), text_color='#ff0033')
    title.pack(side='left', pady=15, padx=20)
    def hide_window():
        app.withdraw()
    close_btn = ctk.CTkButton(header, text='X', width=50, height=30, fg_color='#cc0000', hover_color='#990000', command=hide_window)
    close_btn.pack(side='right', padx=10, pady=10)
    email_frame = ctk.CTkFrame(app, fg_color='#110000', border_width=4, border_color='#ff0033')
    email_frame.pack(pady=20, padx=50, fill='x')
    current_email = ''
    msg_box = None
    def copy_current_email():
        if current_email:
            app.clipboard_clear()
            app.clipboard_append(current_email)
            if msg_box:
                msg_box.insert('end', f'[+] EMAIL COPIED: {current_email}\n')
    email_label = ctk.CTkButton(email_frame, text='EMAIL: NOT GENERATED', font=('Consolas', 20, 'bold'), fg_color='#220000', text_color='#ff3333', command=copy_current_email)
    email_label.pack(pady=8)
    timer_label = ctk.CTkLabel(email_frame, text='NEXT CREATION: READY', font=('Consolas', 16), text_color='#ff6666')
    timer_label.pack(pady=4)
    btn_frame = ctk.CTkFrame(app, fg_color='transparent')
    btn_frame.pack(pady=10)
    btn_create = ctk.CTkButton(btn_frame, text='CREATE EMAIL', font=('Consolas', 18, 'bold'), fg_color='#cc0000', hover_color='#990000', width=280, height=55, border_width=3, border_color='#ff0033')
    btn_refresh = ctk.CTkButton(btn_frame, text='REFRESH INBOX', font=('Consolas', 18, 'bold'), fg_color='#990000', hover_color='#660000', width=280, height=55, border_width=3, border_color='#ff0033')
    btn_create.grid(row=0, column=0, padx=30)
    btn_refresh.grid(row=0, column=1, padx=30)
    terminal_frame = ctk.CTkFrame(app, fg_color='#0a0000', border_width=5, border_color='#ff0033')
    terminal_frame.pack(padx=40, pady=20, fill='both', expand=True)
    msg_box = ctk.CTkTextbox(terminal_frame, font=('Consolas', 14), fg_color='#110000', text_color='#ff6666', border_width=0)
    msg_box.pack(padx=15, pady=15, fill='both', expand=True)
    msg_map = {}
    timer_end = load_timer()
    def update_timer():
        nonlocal timer_end
        if timer_end:
            remaining = timer_end - datetime.now()
            if remaining.total_seconds() > 0:
                mins, secs = divmod(int(remaining.total_seconds()), 60)
                timer_label.configure(text=f'NEXT CREATION: {mins:02d}:{secs:02d}')
                btn_create.configure(state='disabled', fg_color='#660000')
                app.after(1000, update_timer)
            else:
                timer_label.configure(text='NEXT CREATION: READY')
                btn_create.configure(state='normal', fg_color='#cc0000')
                delete_timer()
                timer_end = None
        else:
            timer_label.configure(text='NEXT CREATION: READY')
            btn_create.configure(state='normal')
    async def create_email_ui():
        nonlocal timer_end
        nonlocal current_email
        # ***<module>.launch_main_app.create_email_ui: Failure: Different control flow
        if timer_end and datetime.now() < timer_end:
            msg_box.delete('0.0', 'end')
            msg_box.insert('end', '[-] WAIT FOR TIMER TO EXPIRE\n')
            return
        else:
            current_email = api_create_email()
            msg_box.delete('0.0', 'end')
            if current_email:
                email_label.configure(text=f'EMAIL: {current_email}')
                msg_box.insert('end', '[+] EMAIL CREATED — READY\n')
                timer_end = datetime.now() + timedelta(minutes=10)
                save_timer(timer_end)
                update_timer()
            else:
                msg_box.insert('end', '[-] CREATION FAILED\n')
    def refresh_inbox_ui():
        if not current_email:
            msg_box.delete('0.0', 'end')
            msg_box.insert('end', '[-] NO ACTIVE EMAIL\n')
            return
        else:
            msgs = api_inbox(current_email)
            msg_box.delete('0.0', 'end')
            msg_map.clear()
            if not msgs:
                msg_box.insert('end', '[-] INBOX EMPTY\n')
                return
            else:
                msg_box.insert('end', '=== INBOX ===\n')
                for i, m in enumerate(msgs, 1):
                    sub = m.get('subject') or '(no subject)'
                    frm = m.get('from') or 'unknown'
                    msg_box.insert('end', f'[{i}] {sub} — {frm}\n')
                    msg_map[str(i)] = m['id']
                msg_box.insert('end', '\nSelect with keyboard: [1], [2], ...\n')
    def show_msg_by_index(idx: str):
        mid = msg_map.get(idx)
        if not mid:
            return
        else:
            m = api_read_message(current_email, mid)
            if m:
                msg_box.delete('0.0', 'end')
                msg_box.insert('end', '=== MESSAGE ===\n')
                msg_box.insert('end', f"FROM: {m.get('from')}\n")
                msg_box.insert('end', f"SUBJECT: {m.get('subject')}\n\n")
                text_body = m.get('body_text')
                html_body = m.get('body_html')
                if text_body:
                    msg_box.insert('end', text_body + '\n')
                else:
                    if html_body:
                        msg_box.insert('end', html_body + '\n')
                    else:
                        msg_box.insert('end', '(mail empty)\n')
    def on_key(event):
        ch = event.char
        if ch in msg_map:
            show_msg_by_index(ch)
    btn_create.configure(command=create_email_ui)
    btn_refresh.configure(command=refresh_inbox_ui)
    app.bind('<Key>', on_key)
    threading.Thread(target=create_tray_icon, args=(app,), daemon=True).start()
    app.protocol('WM_DELETE_WINDOW', hide_window)
    update_timer()
    app.mainloop()
launch_main_app()
