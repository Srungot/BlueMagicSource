import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk
import qrcode
import random
import os
import sys
import time
import platform
import os
import hashlib
from time import sleep
from datetime import datetime, UTC
class IDCardCreator:
    def __init__(self, root):
        self.root = root
        self.root.title('🪪 ID Card Fraud Master')
        self.root.geometry('900x500')
        self.root.configure(bg='#1a1a1a')
        self.bg_color = '#ffffff'
        self.text_color = '#000000'
        self.font_path = 'arial.ttf'
        self.use_qr = ctk.BooleanVar(value=True)
        self.qr_url = ctk.StringVar(value='')
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('dark-blue')
        main_frame = ctk.CTkFrame(root, fg_color='#2c2c2c', corner_radius=10)
        main_frame.pack(padx=20, pady=20, fill='both', expand=True)
        title = ctk.CTkLabel(main_frame, text='🪪 ID Card Fraud Master', font=ctk.CTkFont(family='Arial', size=24, weight='bold'), text_color='#ff3333')
        title.pack(pady=10)
        form_frame = ctk.CTkFrame(main_frame, fg_color='#333333')
        form_frame.pack(padx=20, pady=10, fill='x')
        fields = [('Company', 'company'), ('Full Name', 'name'), ('Gender', 'gender'), ('Age', 'age'), ('DOB', 'dob'), ('Blood', 'blood'), ('Mobile', 'mobile'), ('Address', 'address')]
        self.entries = {}
        for i, (label, key) in enumerate(fields):
            row = ctk.CTkFrame(form_frame, fg_color='#333333')
            row.pack(fill='x', pady=2)
            ctk.CTkLabel(row, text=label, font=ctk.CTkFont(size=12), text_color='white').pack(side='left', padx=5)
            entry = ctk.CTkEntry(row, width=200, font=ctk.CTkFont(size=12), fg_color='#444444', text_color='white')
            entry.pack(side='right', padx=5)
            self.entries[key] = entry
        qr_frame = ctk.CTkFrame(main_frame, fg_color='#333333')
        qr_frame.pack(padx=20, pady=10, fill='x')
        ctk.CTkCheckBox(qr_frame, text='Add QR Code', variable=self.use_qr, fg_color='#ff3333', hover_color='#cc0000', font=ctk.CTkFont(size=12)).pack(side='left', padx=5)
        ctk.CTkLabel(qr_frame, text='URL (opt):', font=ctk.CTkFont(size=12), text_color='white').pack(side='left', padx=5)
        ctk.CTkEntry(qr_frame, textvariable=self.qr_url, width=200, font=ctk.CTkFont(size=12), fg_color='#444444', text_color='white').pack(side='left', padx=5)
        btn_frame = ctk.CTkFrame(main_frame, fg_color='#333333')
        btn_frame.pack(padx=20, pady=10, fill='x')
        ctk.CTkButton(btn_frame, text='🪄 Generate', command=self.generate_card, fg_color='#ff4500', text_color='white', font=ctk.CTkFont(size=12, weight='bold')).pack(fill='x', pady=5)
    def generate_card(self):
        data = {key: e.get().strip() for key, e in self.entries.items()}
        if not all(data.values()):
            messagebox.showerror('Error', 'All fields required, Boss!')
            return
        else:
            image = Image.new('RGB', (800, 600), self.bg_color)
            draw = ImageDraw.Draw(image)
            font_title = ImageFont.truetype(self.font_path, 50)
            font_text = ImageFont.truetype(self.font_path, 30)
            font_small = ImageFont.truetype(self.font_path, 25)
            draw.text((30, 20), data['company'], fill=self.text_color, font=font_title)
            idno = random.randint(100000, 999999)
            draw.text((550, 30), f'ID {idno}', fill=self.text_color, font=font_text)
            y = 120
            spacing = 50
            for label, key in [('Name', 'name'), ('Gender', 'gender'), ('Age', 'age'), ('DOB', 'dob'), ('Blood', 'blood'), ('Mobile', 'mobile'), ('Address', 'address')]:
                draw.text((30, y), f'{label}: {data[key]}', fill=self.text_color, font=font_small)
                y += spacing
            if self.use_qr.get():
                qr_data = self.qr_url.get().strip() if self.qr_url.get().strip() else f'{data['company']} | {data['name']} | ID: {idno}'
                qr = qrcode.make(qr_data).resize((150, 150))
                image.paste(qr, (600, 400))
            output_dir = 'output'
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            filename = os.path.join(output_dir, f'id_card_{idno}.png')
            image.save(filename)
            messagebox.showinfo('Success', f'Card saved to: {filename}')
if __name__ == '__main__':
    def clear_screen():
        if os.name == 'posix':
            os.system('clear')
        else:
            os.system('cls')
    clear_screen()
    root = ctk.CTk()
    app = IDCardCreator(root)
    root.mainloop()