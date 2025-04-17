import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from main import LiveMatchScraper
import threading
import sys
import io
import os

class ScraperUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Live Match Data Scraper")
        self.root.geometry("800x750")
        
        # Configure style
        style = ttk.Style()
        style.configure('Title.TLabel', font=('Helvetica', 16, 'bold'))
        style.configure('Header.TLabel', font=('Helvetica', 12, 'bold'))
        style.configure('TLabel', font=('Helvetica', 10))
        style.configure('TEntry', font=('Helvetica', 10))
        style.configure('TButton', font=('Helvetica', 10))
        style.configure('Start.TButton', font=('Helvetica', 12, 'bold'))
        
        # Create main frame with padding
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Live Match Data Scraper", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Create input frame
        input_frame = ttk.LabelFrame(main_frame, text="Configuration", padding="10")
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        input_frame.columnconfigure(1, weight=1)
        
        # URL input
        ttk.Label(input_frame, text="Website URL:", style='TLabel').grid(row=0, column=0, sticky=tk.W, pady=5)
        self.url_var = tk.StringVar(value="https://taj777.now")
        ttk.Entry(input_frame, textvariable=self.url_var, width=50).grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        # Username input
        ttk.Label(input_frame, text="Username:", style='TLabel').grid(row=1, column=0, sticky=tk.W, pady=5)
        self.username_var = tk.StringVar(value="Demo258")
        ttk.Entry(input_frame, textvariable=self.username_var).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        # Password input
        ttk.Label(input_frame, text="Password:", style='TLabel').grid(row=2, column=0, sticky=tk.W, pady=5)
        self.password_var = tk.StringVar(value="Asdf@1122")
        ttk.Entry(input_frame, textvariable=self.password_var, show="*").grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        # Sport name input
        ttk.Label(input_frame, text="Sport Name:", style='TLabel').grid(row=3, column=0, sticky=tk.W, pady=5)
        self.sport_var = tk.StringVar(value="cricket")
        ttk.Entry(input_frame, textvariable=self.sport_var).grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        # Save Location
        ttk.Label(input_frame, text="Save Location:", style='TLabel').grid(row=4, column=0, sticky=tk.W, pady=5)
        self.save_location_var = tk.StringVar(value=os.getcwd())
        save_location_entry = ttk.Entry(input_frame, textvariable=self.save_location_var)
        save_location_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        ttk.Button(input_frame, text="Browse", command=self.browse_save_location).grid(row=4, column=2, padx=5, pady=5)
        
        # Headless mode checkbox
        self.headless_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(input_frame, text="Headless Mode", variable=self.headless_var, style='TCheckbutton').grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=10)
        
        # Start button with custom style
        self.start_button = ttk.Button(main_frame, text="Start Scraping", command=self.start_scraping, style='Start.TButton')
        self.start_button.grid(row=2, column=0, columnspan=3, pady=20)
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        status_frame.columnconfigure(1, weight=1)
        
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(status_frame, textvariable=self.status_var, style='TLabel').grid(row=0, column=0, sticky=tk.W)
        
        # Log frame
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="10")
        log_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Log text area with custom font
        self.log_text = tk.Text(log_frame, height=15, width=70, font=('Consolas', 9))
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for text area
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        # Redirect stdout to our log
        sys.stdout = self.StdoutRedirector(self.log_text)
        
    class StdoutRedirector:
        def __init__(self, text_widget):
            self.text_widget = text_widget
            self.buffer = io.StringIO()
            
        def write(self, str):
            self.buffer.write(str)
            self.text_widget.insert(tk.END, str)
            self.text_widget.see(tk.END)
            
        def flush(self):
            self.buffer.flush()
    
    def browse_save_location(self):
        """Open file dialog to select save location"""
        directory = filedialog.askdirectory(
            initialdir=self.save_location_var.get(),
            title="Select Save Location"
        )
        if directory:  # If a directory was selected
            self.save_location_var.set(directory)
            print(f"Save location set to: {directory}")
    
    def start_scraping(self):
        # Disable the start button
        self.start_button.configure(state='disabled')
        self.status_var.set("Scraping in progress...")
        
        # Clear log
        self.log_text.delete(1.0, tk.END)
        
        # Start scraping in a separate thread
        thread = threading.Thread(target=self.run_scraper)
        thread.daemon = True
        thread.start()
    
    def run_scraper(self):
        try:
            # Get values from UI
            url = self.url_var.get()
            username = self.username_var.get()
            password = self.password_var.get()
            sport = self.sport_var.get()
            headless = self.headless_var.get()
            save_location = self.save_location_var.get()
            
            print(f"Starting scraper with headless mode: {'enabled' if headless else 'disabled'}")
            
            # Initialize and run scraper
            scraper = LiveMatchScraper(url=url, headless=headless)
            
            if not headless:
                print("Running in visible mode - please complete Cloudflare verification when prompted...")
            
            live_data = scraper.scrape_all_live_matches(sport)
            
            if live_data:
                filename = os.path.join(save_location, f"live_{sport.lower()}_data.json")
                scraper.save_to_json(live_data, filename)
                self.status_var.set(f"Successfully saved data to {filename}")
                print(f"\nData successfully saved to {filename}")
            else:
                self.status_var.set("No data was scraped")
                print("\nNo data was scraped")
                
        except Exception as e:
            error_msg = str(e)
            self.status_var.set(f"Error: {error_msg}")
            print(f"\nError occurred: {error_msg}")
            messagebox.showerror("Error", error_msg)
            
        finally:
            # Re-enable the start button
            self.start_button.configure(state='normal')
            print("\nScraping process completed")

def main():
    root = tk.Tk()
    app = ScraperUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 