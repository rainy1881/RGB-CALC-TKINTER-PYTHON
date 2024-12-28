import tkinter as tk
import colorsys
import time
import threading
from tkinter import font

class RGBCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("RGB Calculator")
        self.root.geometry("450x650")
        self.root.resizable(False, False)
        self.root.configure(bg='#0A0A0A')
        
        self.hue = 0
        self.running = True
        
        self.glow_frames = []
        current_frame = self.root
        
        for i in range(3):
            frame = tk.Frame(current_frame, bg='#0A0A0A')
            frame.pack(expand=True, fill='both', padx=2, pady=2)
            self.glow_frames.append(frame)
            current_frame = frame
        
        self.main_frame = tk.Frame(current_frame, bg='#0A0A0A', padx=20, pady=20)
        self.main_frame.pack(expand=True, fill='both')
        
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        
        self.display_frame = tk.Frame(self.main_frame, bg='#0A0A0A', pady=30)
        self.display_frame.pack(fill='x')
        
        self.display_glow = tk.Frame(self.display_frame, bg='#00FF00', padx=3, pady=3)
        self.display_glow.pack(fill='x')
        
        self.display = tk.Label(
            self.display_glow,
            textvariable=self.display_var,
            font=("Arial", 52, "bold"),
            anchor='e',
            bg='#0A0A0A',
            fg='#00FF00',
            height=1,
            padx=15
        )
        self.display.pack(fill='x')
        
        self.buttons_frame = tk.Frame(self.main_frame, bg='#0A0A0A')
        self.buttons_frame.pack(expand=True, fill='both')
        
        buttons = [
            ('C', 0, 0, '#1A1A1A', '#FF0000'),
            ('±', 0, 1, '#1A1A1A', '#00FF00'),
            ('^', 0, 2, '#1A1A1A', '#00FF00'),
            ('/', 0, 3, '#1A1A1A', '#00FFFF'),
            ('7', 1, 0, '#1A1A1A', '#00FF00'),
            ('8', 1, 1, '#1A1A1A', '#00FF00'),
            ('9', 1, 2, '#1A1A1A', '#00FF00'),
            ('×', 1, 3, '#1A1A1A', '#00FFFF'),
            ('4', 2, 0, '#1A1A1A', '#00FF00'),
            ('5', 2, 1, '#1A1A1A', '#00FF00'),
            ('6', 2, 2, '#1A1A1A', '#00FF00'),
            ('-', 2, 3, '#1A1A1A', '#00FFFF'),
            ('1', 3, 0, '#1A1A1A', '#00FF00'),
            ('2', 3, 1, '#1A1A1A', '#00FF00'),
            ('3', 3, 2, '#1A1A1A', '#00FF00'),
            ('+', 3, 3, '#1A1A1A', '#00FFFF'),
            ('0', 4, 0, '#1A1A1A', '#00FF00'),
            ('.', 4, 1, '#1A1A1A', '#00FF00'),
            ('⌫', 4, 2, '#1A1A1A', '#FF0000'),
            ('=', 4, 3, '#000080', '#00FFFF'),
        ]
        
        self.buttons = {}
        for (text, row, col, bg_color, fg_color) in buttons:
            outer_glow = tk.Frame(self.buttons_frame, bg=fg_color)
            outer_glow.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")
            
            inner_glow = tk.Frame(outer_glow, bg=fg_color, padx=2, pady=2)
            inner_glow.pack(expand=True, fill='both', padx=1, pady=1)
            
            button = tk.Button(
                inner_glow,
                text=text,
                font=("Arial", 20, "bold"),
                bg=bg_color,
                fg=fg_color,
                borderwidth=0,
                command=lambda t=text: self.button_click(t),
                relief='flat',
                width=3,
                height=1
            )
            button.pack(expand=True, fill='both')
            
            self.buttons[text] = (button, outer_glow, inner_glow, fg_color)
            button.bind("<Enter>", lambda e, btn=button, fg=fg_color: self.on_hover(btn, fg))
            button.bind("<Leave>", lambda e, btn=button, fg=fg_color: self.on_leave(btn, fg))
        
        for i in range(5):
            self.buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.buttons_frame.grid_columnconfigure(i, weight=1)
        
        self.current = ""
        self.operation = ""
        self.first_number = None
        
        self.animation_thread = threading.Thread(target=self.rgb_animation, daemon=True)
        self.animation_thread.start()

    def rgb_animation(self):
        while self.running:
            self.hue = (self.hue + 0.001) % 1.0
            rgb = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(self.hue, 1, 1))
            color = f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
            
            try:
                for frame in self.glow_frames:
                    frame.configure(bg=color)
                for button_text, (button, outer, inner, orig_color) in self.buttons.items():
                    if button_text in ['+', '-', '×', '/', '=']:
                        outer.configure(bg=color)
                        inner.configure(bg=color)
                self.display_glow.configure(bg=color)
            except:
                pass
            time.sleep(0.01)

    def on_hover(self, button, fg_color):
        button.configure(bg='#2A2A2A', fg=fg_color)

    def on_leave(self, button, fg_color):
        button.configure(bg='#1A1A1A', fg=fg_color)

    def button_click(self, value):
        if value == '×': value = '*'
        if value == '⌫': value = '←'
        
        if value.isdigit() or value == '.':
            if len(self.current) < 12:
                self.current += value
                self.display_var.set(self.current)
        elif value in ['+', '-', '*', '/', '^']:
            if self.current:
                if self.first_number is not None:
                    self.calculate()
                self.first_number = float(self.current)
                self.operation = value
                self.current = ""
        elif value == '=':
            self.calculate()
        elif value == 'C':
            self.clear()
        elif value == '←':
            self.current = self.current[:-1]
            self.display_var.set(self.current if self.current else "0")
        elif value == '±':
            if self.current:
                if self.current[0] == '-':
                    self.current = self.current[1:]
                else:
                    self.current = '-' + self.current
                self.display_var.set(self.current)

    def calculate(self):
        if self.first_number is not None and self.current and self.operation:
            try:
                second_number = float(self.current)
                if self.operation == '+': result = self.first_number + second_number
                elif self.operation == '-': result = self.first_number - second_number
                elif self.operation == '*': result = self.first_number * second_number
                elif self.operation == '/':
                    if second_number == 0: raise ZeroDivisionError
                    result = self.first_number / second_number
                elif self.operation == '^': result = self.first_number ** second_number
                
                if isinstance(result, float):
                    if result.is_integer(): result = int(result)
                    else: result = round(result, 8)
                
                self.current = str(result)
                if len(self.current) > 12: self.current = "Error"
                self.display_var.set(self.current)
            except:
                self.current = "Error"
                self.display_var.set("Error")
            self.first_number = None
            self.operation = ""

    def clear(self):
        self.current = ""
        self.first_number = None
        self.operation = ""
        self.display_var.set("0")

if __name__ == "__main__":
    root = tk.Tk()
    calculator = RGBCalculator(root)
    root.mainloop()