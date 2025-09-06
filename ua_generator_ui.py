#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip
from ua_generator import UserAgentGenerator
import random

class UserAgentGeneratorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("User Agent Generator")
        self.root.geometry("800x400")
        self.root.resizable(True, True)
        
        # Initialize the generator
        self.generator = UserAgentGenerator()
        
        # Create and configure main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Style configuration
        style = ttk.Style()
        style.configure("Generate.TButton", padding=10, font=('Helvetica', 10, 'bold'))
        style.configure("Copy.TButton", padding=10, font=('Helvetica', 10))
        
        # Device type selection
        self.device_frame = ttk.LabelFrame(self.main_frame, text="Device Type", padding="5")
        self.device_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.device_type = tk.StringVar(value="both")
        ttk.Radiobutton(self.device_frame, text="Both", variable=self.device_type, 
                       value="both").grid(row=0, column=0, padx=5)
        ttk.Radiobutton(self.device_frame, text="Android", variable=self.device_type,
                       value="android").grid(row=0, column=1, padx=5)
        ttk.Radiobutton(self.device_frame, text="iOS", variable=self.device_type,
                       value="ios").grid(row=0, column=2, padx=5)
        
        # User Agent Display
        self.ua_frame = ttk.LabelFrame(self.main_frame, text="Generated User Agent", padding="5")
        self.ua_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        self.ua_frame.columnconfigure(0, weight=1)
        self.ua_frame.rowconfigure(0, weight=1)
        
        self.ua_text = tk.Text(self.ua_frame, height=4, wrap=tk.WORD)
        self.ua_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.ua_text.config(state='disabled')
        
        # Entropy Score Display
        self.entropy_frame = ttk.Frame(self.ua_frame)
        self.entropy_frame.grid(row=1, column=0, sticky=(tk.E), pady=(5,0))
        
        ttk.Label(self.entropy_frame, text="Entropy Score: ").grid(row=0, column=0)
        self.entropy_label = ttk.Label(self.entropy_frame, text="", font=('Helvetica', 10, 'bold'))
        self.entropy_label.grid(row=0, column=1)
        
        # Scrollbar for text
        scrollbar = ttk.Scrollbar(self.ua_frame, orient=tk.VERTICAL, command=self.ua_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.ua_text['yscrollcommand'] = scrollbar.set
        
        # Buttons
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.generate_btn = ttk.Button(self.button_frame, text="Generate New", 
                                     command=self.generate_ua, style="Generate.TButton")
        self.generate_btn.grid(row=0, column=0, padx=5)
        
        self.copy_btn = ttk.Button(self.button_frame, text="Copy to Clipboard",
                                  command=self.copy_ua, style="Copy.TButton")
        self.copy_btn.grid(row=0, column=1, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self.main_frame, textvariable=self.status_var)
        self.status_bar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Initialize with first user agent
        self.generate_ua()
    
    def generate_ua(self):
        """Generate a new unique user agent"""
        device_type = self.device_type.get()
        
        try:
            if device_type == 'android':
                ua = self.generator.generate_android_ua()
            elif device_type == 'ios':
                ua = self.generator.generate_ios_ua()
            else:
                ua = self.generator.generate_android_ua() if random.random() < 0.5 else self.generator.generate_ios_ua()
            
            # Save to database and update UI
            self.generator.save_generated_ua(ua, 'android' if 'Android' in ua else 'ios')
            
            # Calculate entropy score and regenerate if too low
            max_attempts = 5
            attempts = 0
            while attempts < max_attempts:
                entropy_score = self.generator.calculate_entropy_score(ua)
                if entropy_score >= 90:
                    break
                ua = self.generator.generate_android_ua() if device_type == 'android' else self.generator.generate_ios_ua() if device_type == 'ios' else (
                    self.generator.generate_android_ua() if random.random() < 0.5 else self.generator.generate_ios_ua()
                )
                attempts += 1
            
            if entropy_score >= 90:
                # Update UA text
                self.ua_text.config(state='normal')
                self.ua_text.delete(1.0, tk.END)
                self.ua_text.insert(tk.END, ua)
                self.ua_text.config(state='disabled')
                
                # Update entropy score with color (only green since we filter for 90+)
                self.entropy_label.config(text=f"{entropy_score}%", foreground='#00aa00')
            else:
                # Try again if entropy is too low
                self.generate_ua()
            
            self.status_var.set("New user agent generated successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate user agent: {str(e)}")
            self.status_var.set("Error generating user agent!")
    
    def copy_ua(self):
        """Copy the current user agent to clipboard"""
        ua = self.ua_text.get(1.0, tk.END).strip()
        if ua:
            pyperclip.copy(ua)
            self.status_var.set("User agent copied to clipboard!")
            self.generate_ua()  # Generate new one automatically after copying
        else:
            self.status_var.set("No user agent to copy!")

def main():
    root = tk.Tk()
    app = UserAgentGeneratorUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
