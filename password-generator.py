import tkinter as tk
from tkinter import ttk, messagebox
import string
import secrets
import pyperclip

class PasswordGeneratorApp(tk.Tk):
    """
    A modern and secure password generator application built with Python and Tkinter.
    This class encapsulates the entire application, including UI elements and logic.
    """
    def __init__(self):
        super().__init__()

        # --- Basic Window Configuration ---
        self.title("Secure Password Generator")
        self.geometry("420x500")
        self.resizable(False, False)

        # --- Style Configuration ---
        self.style = ttk.Style(self)
        # Available themes: 'clam', 'alt', 'default', 'classic'
        self.style.theme_use('clam')
        self.configure(bg="#2E2E2E")

        self.style.configure("TLabel", foreground="#FFFFFF", background="#2E2E2E", font=("Segoe UI", 10))
        self.style.configure("TButton", foreground="#FFFFFF", background="#4A4A4A", font=("Segoe UI", 10, "bold"), borderwidth=0)
        self.style.map("TButton", background=[('active', '#6E6E6E')])
        self.style.configure("TCheckbutton", foreground="#FFFFFF", background="#2E2E2E", font=("Segoe UI", 10))
        self.style.map("TCheckbutton",
                       foreground=[('active', '#FFFFFF')],
                       background=[('active', '#2E2E2E')])
        self.style.configure("TFrame", background="#2E2E2E")

        # --- Application State Variables ---
        self.length_var = tk.IntVar(value=16)
        self.include_uppercase_var = tk.BooleanVar(value=True)
        self.include_lowercase_var = tk.BooleanVar(value=True)
        self.include_numbers_var = tk.BooleanVar(value=True)
        self.include_symbols_var = tk.BooleanVar(value=True)
        self.generated_password_var = tk.StringVar()

        # --- UI Creation ---
        self.create_widgets()

    def create_widgets(self):
        """Creates and lays out all the UI widgets for the application."""
        main_frame = ttk.Frame(self, padding="20 20 20 20")
        main_frame.pack(expand=True, fill="both")

        # --- Title ---
        title_label = ttk.Label(main_frame, text="Password Generator", font=("Segoe UI", 18, "bold"))
        title_label.pack(pady=(0, 20))

        # --- Result Display ---
        result_frame = ttk.Frame(main_frame)
        result_frame.pack(fill='x', pady=10)

        result_entry = ttk.Entry(result_frame, textvariable=self.generated_password_var, state="readonly", font=("Segoe UI", 12))
        result_entry.pack(side="left", expand=True, fill="x", ipady=5)
        
        copy_button = ttk.Button(result_frame, text="Copy", command=self.copy_to_clipboard, width=8)
        copy_button.pack(side="left", padx=(10, 0))

        # --- Length Slider ---
        length_frame = ttk.Frame(main_frame)
        length_frame.pack(fill='x', pady=10)
        
        length_label = ttk.Label(length_frame, text=f"Length: {self.length_var.get()}")
        length_label.pack(side="left")

        length_slider = ttk.Scale(length_frame, from_=8, to=64, orient="horizontal", variable=self.length_var, command=lambda v: length_label.config(text=f"Length: {int(float(v))}"))
        length_slider.pack(side="right", expand=True, fill="x")
        
        # --- Options Checkboxes ---
        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill='x', pady=10, anchor='w')

        ttk.Checkbutton(options_frame, text="Include Uppercase (A-Z)", variable=self.include_uppercase_var).pack(anchor='w', pady=2)
        ttk.Checkbutton(options_frame, text="Include Lowercase (a-z)", variable=self.include_lowercase_var).pack(anchor='w', pady=2)
        ttk.Checkbutton(options_frame, text="Include Numbers (0-9)", variable=self.include_numbers_var).pack(anchor='w', pady=2)
        ttk.Checkbutton(options_frame, text="Include Symbols (!@#$)", variable=self.include_symbols_var).pack(anchor='w', pady=2)

        # --- Generate Button ---
        generate_button = ttk.Button(main_frame, text="Generate Secure Password", command=self.generate_password)
        generate_button.pack(fill='x', ipady=8, pady=20)
        
        # --- Password Strength Indicator ---
        self.strength_label = ttk.Label(main_frame, text="Password Strength: N/A", font=("Segoe UI", 9, "italic"))
        self.strength_label.pack(anchor='center')

    def generate_password(self):
        """Generates a password based on selected criteria and updates the UI."""
        char_pool = []
        guaranteed_chars = []
        length = self.length_var.get()

        if self.include_uppercase_var.get():
            char_pool.extend(string.ascii_uppercase)
            guaranteed_chars.append(secrets.choice(string.ascii_uppercase))
        if self.include_lowercase_var.get():
            char_pool.extend(string.ascii_lowercase)
            guaranteed_chars.append(secrets.choice(string.ascii_lowercase))
        if self.include_numbers_var.get():
            char_pool.extend(string.digits)
            guaranteed_chars.append(secrets.choice(string.digits))
        if self.include_symbols_var.get():
            char_pool.extend(string.punctuation)
            guaranteed_chars.append(secrets.choice(string.punctuation))

        if not char_pool:
            messagebox.showerror("Error", "You must select at least one character type.")
            return

        # Fill the rest of the password length
        remaining_length = length - len(guaranteed_chars)
        password_chars = guaranteed_chars + [secrets.choice(char_pool) for _ in range(remaining_length)]
        
        # Shuffle the list to ensure randomness
        secrets.SystemRandom().shuffle(password_chars)
        
        final_password = "".join(password_chars)
        self.generated_password_var.set(final_password)
        self.update_strength_indicator()

    def update_strength_indicator(self):
        """Analyzes the generated password and updates the strength label."""
        password = self.generated_password_var.get()
        length = len(password)
        variety_score = sum([
            self.include_uppercase_var.get(),
            self.include_lowercase_var.get(),
            self.include_numbers_var.get(),
            self.include_symbols_var.get()
        ])
        
        strength = ""
        color = ""

        if length < 12 or variety_score < 3:
            strength, color = "Weak", "#FF6B6B"
        elif length < 16 or variety_score < 4:
            strength, color = "Medium", "#FFD166"
        else:
            strength, color = "Strong", "#90EE90"

        self.strength_label.config(text=f"Password Strength: {strength}", foreground=color)

    def copy_to_clipboard(self):
        """Copies the generated password to the system clipboard."""
        password = self.generated_password_var.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Copied", "Password has been copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "Nothing to copy. Please generate a password first.")

if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.mainloop()
