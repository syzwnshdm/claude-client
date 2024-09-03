# gui.py
import tkinter as tk
from tkinter import ttk, font
from datetime import datetime

class ChatBubble(tk.Frame):
    def __init__(self, master, message, is_user=True, config=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.message = message
        self.is_user = is_user
        self.config = config

        text_color = config.get('CHAT', 'text_color')
        bg_color = config.get('CHAT', 'user_bubble_color') if is_user else config.get('CHAT', 'ai_bubble_color')
        align = tk.RIGHT if is_user else tk.LEFT

        self.bubble = tk.Frame(self, bg=bg_color)
        self.bubble.pack(side=align, anchor="e" if is_user else "w", pady=5, padx=(20 if is_user else 5, 5 if is_user else 20), fill=tk.X)

        font_family = config.get('CHAT', 'font_family')
        font_size = config.getint('CHAT', 'font_size')
        
        self.txt = tk.Text(self.bubble, wrap=tk.WORD, bg=bg_color, borderwidth=0, highlightthickness=0, fg=text_color, font=(font_family, font_size), width=50)  # Set a default width
        self.txt.insert(tk.END, message)
        self.txt.config(state=tk.DISABLED)
        self.txt.pack(padx=10, pady=5)

        self.update_idletasks()
        self.adjust_text_widget()

        timestamp = datetime.now().strftime("%H:%M")
        tk.Label(self.bubble, text=timestamp, bg=bg_color, fg="gray", font=(font_family, font_size - 4)).pack(anchor="se", padx=5, pady=2)

    def adjust_text_widget(self):
        width = int(self.txt.cget("width"))
        height = (int(self.txt.count("1.0", "end", "displaylines")[0]) * 0.1) / 2.8
        self.txt.config(height=height, width=width)
        if self.txt.winfo_reqwidth() > self.master.winfo_width() * 0.8:
            self.txt.config(width=int(self.master.winfo_width() * 0.8 / self.txt.font.measure('0')))


class ChatGUI:
    def __init__(self, master, claude_client, config):
        self.master = master
        self.claude_client = claude_client
        self.config = config
        
        self.master.title("Claude API Client")
        
        self.create_widgets()
        self.configure_layout()

    def create_widgets(self):
        self.style = ttk.Style()
        self.style.theme_use(self.config.get('GUI', 'theme'))

        self.main_frame = ttk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.chat_frame = ttk.Frame(self.main_frame)
        self.chat_frame.pack(fill=tk.BOTH, expand=True)

        self.chat_canvas = tk.Canvas(self.chat_frame)
        self.chat_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.chat_frame, orient=tk.VERTICAL, command=self.chat_canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.chat_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.chat_canvas.bind('<Configure>', lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all")))

        self.chat_window = ttk.Frame(self.chat_canvas)
        self.chat_canvas_window = self.chat_canvas.create_window((0, 0), window=self.chat_window, anchor="nw", width=self.chat_canvas.winfo_width())
        
        self.chat_canvas.bind('<Configure>', self.on_canvas_configure)
        self.chat_window.bind('<Configure>', self.on_frame_configure)

        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.pack(fill=tk.X, pady=(10, 0))

        font_family = self.config.get('CHAT', 'font_family')
        font_size = self.config.getint('CHAT', 'font_size')

        self.message_entry = tk.Text(self.input_frame, wrap=tk.WORD, height=3, font=(font_family, font_size))
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.message_entry.bind("<Return>", self.send_message)
        self.message_entry.bind("<Shift-Return>", self.new_line)

        self.send_button = ttk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=(10, 0))

    def on_canvas_configure(self, event):
        self.chat_canvas.itemconfig(self.chat_canvas_window, width=event.width)

    def on_frame_configure(self, event):
        self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))

    def add_message(self, message, is_user=True):
        bubble = ChatBubble(self.chat_window, message, is_user, self.config)
        bubble.pack(fill=tk.X, expand=True, pady=5)
        self.chat_canvas.update_idletasks()
        self.chat_canvas.yview_moveto(1.0)

    def configure_layout(self):
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        self.chat_frame.columnconfigure(0, weight=1)
        self.chat_frame.rowconfigure(0, weight=1)

    def send_message(self, event=None):
        user_message = self.message_entry.get("1.0", tk.END).strip()
        if user_message:
            self.add_message(user_message, is_user=True)
            self.message_entry.delete("1.0", tk.END)

            response = self.claude_client.send_message(user_message)
            self.add_message(response, is_user=False)
        
        return "break"

    def new_line(self, event):
        self.message_entry.insert(tk.INSERT, '\n')
        return "break"