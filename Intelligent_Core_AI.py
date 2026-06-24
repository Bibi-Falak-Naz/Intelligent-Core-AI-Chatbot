import os
import time
import tkinter as tk
from tkinter import ttk

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Error: 'google-genai' library not found! Please run 'pip install google-genai' in terminal.")

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Client Initialization inside safe try-except block
try:
    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )
except Exception as e:
    print("Client Initialization Error:", e)
    client = None

THEMES = {
    "Deep Charcoal (Dark)": {
        "bg": "#1e1e2e", 
        "sidebar": "#11111b", 
        "chat_bg": "#181825", 
        "text": "#cdd6f4", 
        "user_tag": "#a6e3a1", 
        "bot_tag": "#89b4fa", 
        "input_bg": "#313244", 
        "input_border": "#11111b"
    },
    "Sophisticated Silver (Light)": {
        "bg": "#f5f5f7", 
        "sidebar": "#e5e5ea", 
        "chat_bg": "#ffffff", 
        "text": "#1c1c1e", 
        "user_tag": "#34c759", 
        "bot_tag": "#007aff", 
        "input_bg": "#e5e5ea",       
        "input_border": "#b1b1b6"    
    }
}

SYSTEM_INSTRUCTION = """
You are the Intelligent Core AI, an automated logic engine gateway. 
Always follow these behavioral rules based on user input:
1. If the user says goodbye, exit, quit, or bye, reply with exactly: "Shutting down pipeline terminal. Goodbye!"
2. If the user says hi, hello, or hey, reply with exactly: "Greetings! I am the automated logic engine gateway. State your requirement."
3. If the user asks how are you, reply with exactly: "Operational status: 100%. All logic systems are running optimal."
4. If the user asks about or mentions the name 'Bibi Falak Naz', reply with exactly: "Bibi Falak Naz is a skilled computer systems engineer and the original developer who built the Intelligent Core AI."
5. For any other inputs, act as a professional enterprise AI assistant and provide detailed answers.
"""

class PremiumChatbotGUI:
    def __init__(self, window):
        self.window = window
        self.window.title("Intelligent Core AI")
        self.window.geometry("850x550")
        self.threads = {"Conversation Thread 1": []}
        self.current_thread = "Conversation Thread 1"
        self.thread_count = 1
        self.current_theme = "Deep Charcoal (Dark)"
        
        self.sidebar = tk.Frame(window, width=220)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        tk.Button(self.sidebar, text="＋ New Workspace", font=("Arial", 10, "bold"), bg="#10a37f", fg="white", bd=0, cursor="hand2", command=self.add_new_thread).pack(fill=tk.X, padx=12, pady=15)    
        
        self.thread_list_frame = tk.Frame(self.sidebar)
        self.thread_list_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(self.sidebar, text="INTERFACE THEME", font=("Arial", 8, "bold"), fg="#888888").pack(pady=(10, 2), anchor="w", padx=12)
        self.theme_selector = ttk.Combobox(self.sidebar, values=list(THEMES.keys()), state="readonly", width=18)
        self.theme_selector.set(self.current_theme)
        self.theme_selector.pack(pady=(0, 15), padx=12)
        self.theme_selector.bind("<<ComboboxSelected>>", self.change_theme)
        
        tk.Button(self.sidebar, text="✕ Terminate Session", font=("Arial", 9, "bold"), bg="#e11d48", fg="white", bd=0, cursor="hand2", command=window.quit).pack(fill=tk.X, padx=12, pady=12)
        
        self.main_frame = tk.Frame(window)
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.chat_canvas = tk.Canvas(self.main_frame, bd=0, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.chat_canvas.yview)
        self.scrollable_frame = tk.Frame(self.chat_canvas)
        
        self.scrollable_frame.bind("<Configure>", lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all")))
        self.chat_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=600)
        self.chat_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.chat_canvas.pack(side="top", fill="both", expand=True, padx=15, pady=15)
        self.scrollbar.pack(side="right", fill="y")
        
        self.chat_canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)
        self.chat_canvas.bind_all("<Button-4>", self._on_mouse_wheel)
        self.chat_canvas.bind_all("<Button-5>", self._on_mouse_wheel)
        
        self.input_frame = tk.Frame(self.main_frame, padx=10, pady=10)
        self.input_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        self.user_entry = tk.Entry(self.input_frame, font=("Arial", 11), bd=0, highlightthickness=1)
        self.user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 8))
        self.user_entry.bind("<Return>", lambda event: self.process_message()) 
        
        self.btn_send = tk.Button(self.input_frame, text="Send Query", font=("Arial", 10, "bold"), bg="#10a37f", fg="white", bd=0, padx=18, cursor="hand2", command=self.process_message)
        self.btn_send.pack(side=tk.RIGHT, ipady=6)
        
        self.apply_theme_colors()
        self.update_sidebar_ui()
        self.refresh_chat_display()

    def _on_mouse_wheel(self, event):
        if event.num == 4:    
            self.chat_canvas.yview_scroll(-1, "units")
        elif event.num == 5:  
            self.chat_canvas.yview_scroll(1, "units")
        else:                                 
            self.chat_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def change_theme(self, event):
        self.current_theme = self.theme_selector.get()
        self.apply_theme_colors()
        self.update_sidebar_ui()
        self.refresh_chat_display()

    def apply_theme_colors(self):
        t = THEMES[self.current_theme]
        self.sidebar.config(bg=t["sidebar"])
        self.thread_list_frame.config(bg=t["sidebar"])
        self.main_frame.config(bg=t["bg"])
        self.chat_canvas.config(bg=t["chat_bg"])
        self.scrollable_frame.config(bg=t["chat_bg"])
        self.input_frame.config(bg=t["bg"])     
        self.user_entry.config(
            bg=t["input_bg"], 
            fg=t["text"], 
            insertbackground=t["text"], 
            highlightbackground=t["input_border"], 
            highlightcolor="#10a37f"
        )

    def add_new_thread(self):
        self.thread_count += 1
        new_name = f"Conversation Thread {self.thread_count}"
        self.threads[new_name] = []
        self.current_thread = new_name
        self.update_sidebar_ui()
        self.refresh_chat_display()

    def update_sidebar_ui(self):
        for widget in self.thread_list_frame.winfo_children():
            widget.destroy()
        t = THEMES[self.current_theme]
        for name in self.threads.keys():
            bg_color = t["bg"] if name == self.current_thread else t["sidebar"]
            font_weight = "bold" if name == self.current_thread else "normal"
            tk.Button(
                self.thread_list_frame, text=f"◈  {name}", font=("Arial", 9, font_weight),
                bg=bg_color, fg=t["text"], anchor="w", bd=0, cursor="hand2", activebackground=t["bg"], activeforeground=t["text"],
                command=lambda tn=name: self.switch_thread(tn)
            ).pack(fill=tk.X, pady=3, padx=8, ipady=6)

    def switch_thread(self, thread_name):
        self.current_thread = thread_name
        self.update_sidebar_ui()
        self.refresh_chat_display()

    def refresh_chat_display(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        t = THEMES[self.current_theme]
        if not self.threads[self.current_thread]:
            welcome_lbl = tk.Label(self.scrollable_frame, text="🔒 Intelligent Core AI Connected — Ready for Input.", font=("Arial", 9, "italic"), fg="#888888", bg=t["chat_bg"])
            welcome_lbl.pack(pady=20, fill=tk.X)
        for speaker, message in self.threads[self.current_thread]:
            card_frame = tk.Frame(self.scrollable_frame, bg=t["chat_bg"])
            card_frame.pack(fill=tk.X, pady=8, padx=10)
            tag_color = t["user_tag"] if speaker == "You" else t["bot_tag"]         
            lbl_tag = tk.Label(card_frame, text=f"[ {speaker} ]", font=("Arial", 9, "bold"), fg=tag_color, bg=t["chat_bg"])
            lbl_tag.pack(anchor="w", pady=(0, 2))
            lbl_text = tk.Label(card_frame, text=message, font=("Arial", 10), fg=t["text"], bg=t["chat_bg"],
                                justify=tk.LEFT, wraplength=520, anchor="w")
            lbl_text.pack(anchor="w", padx=5)
        self.window.update_idletasks()
        self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
        self.chat_canvas.yview_moveto(1.0)

    def process_message(self):
        user_text = self.user_entry.get()
        clean_text = user_text.lower().strip()
        if not clean_text:
            return

        self.threads[self.current_thread].append(("You", user_text))
        self.refresh_chat_display()
        self.user_entry.delete(0, tk.END)

        if client is None:
            self.threads[self.current_thread].append(("System", "Gemini client initialization failed. Check your API key."))
        else:
            try:
                response_text = None

                ai_call = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=user_text,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION
                    )
                )

                if ai_call:
                    if hasattr(ai_call, "text") and ai_call.text:
                        response_text = ai_call.text

                    elif hasattr(ai_call, "candidates") and ai_call.candidates:
                        candidate = ai_call.candidates[0]

                        if (
                            hasattr(candidate, "content")
                            and candidate.content
                            and candidate.content.parts
                        ):
                            response_text = candidate.content.parts[0].text

                if response_text:
                    self.threads[self.current_thread].append(
                        ("Bot - AI", response_text)
                    )

                    if "shutting down pipeline terminal" in response_text.lower():
                        self.window.after(1500, self.window.quit)

                else:
                    self.threads[self.current_thread].append(
                        ("Bot - System",
                         "No response received from Gemini.")
                    )

            except Exception as e:
                error_text = str(e)

                print("Gemini Error:", error_text)

                if "429" in error_text:
                    reply = (
                        "Gemini API quota reached.\n"
                        "Demo mode activated.\n\n"
                        "Please try again later."
                    )

                elif "503" in error_text:
                    reply = (
                        "Gemini servers are currently busy.\n\n"
                        "Please try again in a few moments."
                    )

                elif "API_KEY" in error_text.upper():
                    reply = (
                        "API key error.\n\n"
                        "Please verify your .env configuration."
                    )

                else:
                    reply = (
                        "Unexpected Gemini error.\n\n"
                        f"{error_text}"
                    )

                self.threads[self.current_thread].append(
                    ("Bot - Error", reply)
                )
        
        self.refresh_chat_display()

if __name__ == "__main__":
    root = tk.Tk()
    app = PremiumChatbotGUI(root)
    root.mainloop()