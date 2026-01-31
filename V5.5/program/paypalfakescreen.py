from timeit import main
import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont
import random
import string
import os
import hashlib
import sys
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')
IMAGE_PATH = 'input/paypal.png'
OUTPUT_PATH = 'output/paypal_sortie.png'
BG_COLOR = (245, 247, 252)
os.makedirs('output', exist_ok=True)
PREVIEW_HEIGHT = 170
RED_COLOR = '#ff0033'
RED_HOVER = '#cc0028'
TEXT_RED = '#ff3366'
positions = {
    'amount': {
        'x1': 43,
        'y1': 116,
        'x2': 123,
        'y2': 155,
        'font_size': 31,
        'font_path': 'arialbd.ttf' },
    'name': {
        'x1': 297,
        'y1': 121,
        'x2': 529,
        'y2': 149,
        'font_size': 38,
        'font_path': 'arialbd.ttf' },
    'date': {
        'x1': 436,
        'y1': 258,
        'x2': 533,
        'y2': 269,
        'font_size': 11,
        'font_path': 'arial.ttf' },
    'id': {
        'x1': 36,
        'y1': 259,
        'x2': 163,
        'y2': 270,
        'font_size': 11,
        'font_path': 'arialbd.ttf' },
    'eur1': {
        'x1': 470,
        'y1': 325,
        'x2': 494,
        'y2': 337,
        'font_size': 19,
        'font_path': 'MA_POLICE_EUR.ttf' },
    'eur2': {
        'x1': 470,
        'y1': 419,
        'x2': 495,
        'y2': 434,
        'font_size': 19,
        'font_path': 'MA_POLICE_EUR.ttf' },
    'eur3': {
        'x1': 472,
        'y1': 480,
        'x2': 494,
        'y2': 491,
        'font_size': 19,
        'font_path': 'MA_POLICE_EUR.ttf' },
    'payment': {
        'x1': 38,
        'y1': 421,
        'x2': 166,
        'y2': 431,
        'font_size': 11,
        'font_path': 'arialbd.ttf' } }

def add_small_spacing(text):
    return ' '.join(list(text))
def generate_random_id(length=16):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
def generate_random_last4():
    return ''.join((random.choice(string.digits) for _ in range(4)))
def draw_text(draw, key, text, subtle_bold=False, y_offset=0, align='center', extra_dx=0):
    if not text:
        return
    else:
        info = positions[key]
        x1, y1, x2, y2 = (info['x1'], info['y1'], info['x2'], info['y2'])
        font_size = info['font_size']
        try:
            font = ImageFont.truetype(info['font_path'], font_size)
        except:
            font = ImageFont.load_default()
        draw.rectangle([x1, y1, x2, y2], fill=BG_COLOR)
        if key == 'name' and len(text.strip()) < 10:
                extra_dx -= 32
        cx = (x1 + x2) / 2 + extra_dx
        cy = (y1 + y2) / 2 + y_offset
        anchor = 'mm'
        if align == 'right':
            cx = x2 - 2 + extra_dx
            anchor = 'rm'
        color = (0, 102, 204) if key == 'id' else (0, 0, 0)
        draw.text((cx, cy), text, font=font, fill=color, anchor=anchor, stroke_width=1 if subtle_bold else 0, stroke_fill=color)
        if key == 'id':
            bbox = draw.textbbox((cx, cy), text, font=font, anchor=anchor)
            underline_y = bbox[3] + 1
            draw.line([(bbox[0], underline_y), (bbox[2], underline_y)], fill=color, width=1)
def generate_image(amount, date, payment, id_text, eur_text, name_text, preview_only):
    img = Image.open(IMAGE_PATH).convert('RGB')
    draw = ImageDraw.Draw(img)
    draw_text(draw, 'amount', add_small_spacing(amount), subtle_bold=True, align='right')
    draw_text(draw, 'name', name_text, subtle_bold=True)
    draw_text(draw, 'date', date)
    draw_text(draw, 'payment', payment, y_offset=(-3))
    draw_text(draw, 'id', id_text)
    if not preview_only:
        for k in ['eur1', 'eur2', 'eur3']:
            draw_text(draw, k, eur_text, align='right')
    if preview_only:
        crop_width = min(img.width, 600)
        img = img.crop((0, 0, crop_width, PREVIEW_HEIGHT))
    img.save(OUTPUT_PATH)
class App(ctk.CTk):
    # ***<module>.App: Failure: Different bytecode
    def __init__(self):
        super().__init__()
        self.title('PayPal Template Generator')
        self.configure(fg_color='#0b0b0b')
        self.full_mode = ctk.BooleanVar(value=False)
        self.generated_id = generate_random_id()
        self.generated_payment = f'MASTER_CARD x-{generate_random_last4()}'
        self.generated_date = '05 Jan 2026'
        self.generate_count = 0
        self.build_ui()
        self.apply_mode()
    def build_ui(self):
        self.geometry('780x320')
        self.resizable(False, False)
        self.main = ctk.CTkFrame(self, fg_color='transparent')
        self.main.pack(fill='both', expand=True, padx=10, pady=10)
        self.left = ctk.CTkFrame(self.main, fg_color='transparent')
        self.left.pack(side='left', fill='y')
        self.right = ctk.CTkFrame(self.main, fg_color='transparent')
        self.right.pack(side='left', fill='both', expand=True)
        ctk.CTkCheckBox(self.left, text='Full mode', variable=self.full_mode, command=self.apply_mode, text_color=TEXT_RED, fg_color=RED_COLOR, hover_color=RED_HOVER).pack(anchor='w', pady=(0, 15))
        def field(label):
            f = ctk.CTkFrame(self.left, fg_color='transparent')
            ctk.CTkLabel(f, text=label, text_color=TEXT_RED).pack(anchor='w')
            e = ctk.CTkEntry(f, width=220, border_color=RED_COLOR, fg_color='#1a1a1a', text_color='white')
            e.pack(pady=(0, 8))
            return (f, e)
        self.f_amount, self.e_amount = field('Amount')
        self.f_name, self.e_name = field('Name')
        self.f_date, self.e_date = field('Date')
        self.f_payment, self.e_payment = field('Payment')
        self.f_id, self.e_id = field('Transaction ID')
        self.f_eur, self.e_eur = field('Currency')
        self.e_payment.insert(0, self.generated_payment)
        self.e_payment.configure(state='disabled')
        self.e_id.insert(0, self.generated_id)
        self.e_id.configure(state='disabled')
        self.btn = ctk.CTkButton(self.left, text='GENERATE', fg_color=RED_COLOR, hover_color=RED_HOVER, command=self.generate, width=215, height=5, font=('Arial', 13, 'bold'), text_color='white')
        self.status_label = ctk.CTkLabel(self.left, text='', text_color='#00ff66', font=('Arial', 12, 'bold'))
        self.preview = ctk.CTkLabel(self.right, text='')
        self.preview.pack(expand=True)
    def apply_mode(self):
        for f in [self.f_amount, self.f_name, self.f_date, self.f_payment, self.f_id, self.f_eur]:
            f.pack_forget()
        self.btn.pack_forget()
        self.status_label.pack_forget()
        if not self.full_mode.get():
            self.geometry('780x320')
            self.f_amount.pack(anchor='w', pady=3)
            self.f_name.pack(anchor='w', pady=3)
            self.btn.pack(anchor='w', pady=(30, 5))
            self.status_label.pack(anchor='w')
        else:
            self.geometry('780x720')
            for f in [self.f_amount, self.f_name, self.f_date, self.f_payment, self.f_id, self.f_eur]:
                f.pack(anchor='w', pady=3)
            self.btn.pack(anchor='w', pady=(40, 5))
            self.status_label.pack(anchor='w')
        self.generate()
    def generate(self):
        self.generate_count += 1
        generate_image(amount=self.e_amount.get().replace('.', ','), date=self.e_date.get() or self.generated_date, payment=self.generated_payment, id_text=self.generated_id, eur_text=self.e_eur.get() or '€', name_text=self.e_name.get(), preview_only=not self.full_mode.get())
        if self.generate_count >= 2:
            self.status_label.configure(text='screen generate !')
        self.update_preview()
    def update_preview(self):
        img = Image.open(OUTPUT_PATH)
        max_width = 550
        max_height = 600 if self.full_mode.get() else 160
        scale = min(max_width / img.width, max_height / img.height, 1.0)
        new_size = (int(img.width * scale), int(img.height * scale))
        img_resized = img.resize(new_size, Image.LANCZOS)
        self.tkimg = ctk.CTkImage(light_image=img_resized, dark_image=img_resized, size=new_size)
        self.preview.configure(image=self.tkimg)
if __name__ == '__main__':
    def clear_screen():
        # ***<module>.clear_screen: Failure: Missing bytecode
        os.system('cls' if os.name == 'nt' else 'clear')
    clear_screen()
    main()
    App().mainloop()