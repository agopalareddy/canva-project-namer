#!/usr/bin/env python3
"""
File Namer Tool for Canva Designs

This script helps generate consistent filenames for design assets following the convention:
[Event/Project Name]_[Program(s)]_[Posting Date MMDDYY]_[Asset Type]_[Creator/Editor]
"""

import re
import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Lazy import - only import tkcalendar when needed
# This speeds up initial loading time
class LazyDateEntry:
    _module = None
    
    @classmethod
    def get_class(cls):
        if cls._module is None:
            from tkcalendar import DateEntry
            cls._module = DateEntry
        return cls._module

def clean_text(text):
    """Convert lowercase words to title case, remove special characters, and format text for filenames."""
    
    def titlecase_if_lowercase(word):
        """Convert word to title case only if it's all lowercase."""
        return word.title() if word.islower() else word
    
    words = text.split()
    modified_words = [titlecase_if_lowercase(word) for word in words]
    text = ' '.join(modified_words)
    
    # Replace parentheses content with dashes
    text = re.sub(r'\((.*?)\)', r'-\1', text)
    # Replace spaces with nothing
    text = re.sub(r'\s+', '', text)
    # Remove other special characters
    text = re.sub(r'[^\w\s\-]', '', text)
    return text

def format_date(date_obj):
    """Format date object to YYYYMMDD format"""
    return date_obj.strftime("%Y%m%d")

def parse_date(date_str):
    """Attempt to parse a date string in various formats"""
    formats = [
        "%m/%d/%Y", "%m-%d-%Y", "%Y-%m-%d", "%Y/%m/%d", 
        "%m/%d/%y", "%m-%d-%y", "%d/%m/%Y", "%d-%m-%Y"
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    raise ValueError(f"Cannot parse date: {date_str}")

class FileNamerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Canva Design File Namer")
        self.master.geometry("600x450")
        self.master.resizable(True, True)
        
        # Configure for better performance
        self.master.update_idletasks()
        
        # Apply a theme - 'default' is faster to load than 'clam'
        style = ttk.Style()
        style.theme_use('default')
        
        # Create main frame
        main_frame = ttk.Frame(self.master, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Canva Design File Namer", font=("Helvetica", 16))
        title_label.pack(pady=(0, 20))
        
        # Create form frame
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create string variables for tracking changes
        self.event_name_var = tk.StringVar()
        self.programs_var = tk.StringVar()
        self.asset_type_var = tk.StringVar()
        self.creator_var = tk.StringVar()
        self.use_date = tk.BooleanVar(value=True)
        self.date_var = tk.StringVar()  # New variable for date entry
        
        # Set default date
        today = datetime.now()
        self.date_var.set(today.strftime("%m/%d/%Y"))
        self.current_date_obj = today
        
        # Register callbacks for each variable
        self.event_name_var.trace_add("write", self.update_filename)
        self.programs_var.trace_add("write", self.update_filename)
        self.asset_type_var.trace_add("write", self.update_filename)
        self.creator_var.trace_add("write", self.update_filename)
        self.use_date.trace_add("write", self.update_filename)
        
        # Event Name
        ttk.Label(form_frame, text="Event/Project Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.event_name = ttk.Entry(form_frame, width=40, textvariable=self.event_name_var)
        self.event_name.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Programs
        ttk.Label(form_frame, text="Program(s):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.programs = ttk.Entry(form_frame, width=40, textvariable=self.programs_var)
        self.programs.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Date section frame (to contain date entry and related buttons)
        date_frame = ttk.Frame(form_frame)
        date_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Date picker label
        ttk.Label(form_frame, text="Posting Date:").grid(row=2, column=0, sticky=tk.W, pady=5)
        
        # Date checkbox
        self.date_checkbox = ttk.Checkbutton(
            date_frame, 
            text="Include date", 
            variable=self.use_date,
            command=self.toggle_date_entry
        )
        self.date_checkbox.pack(side=tk.LEFT, padx=(0, 5))
        
        # Date entry field
        self.date_entry = ttk.Entry(
            date_frame,
            width=15,
            textvariable=self.date_var
        )
        self.date_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        # Date picker button
        self.calendar_btn = ttk.Button(
            date_frame,
            text="📅",
            width=3,
            command=self.show_calendar
        )
        self.calendar_btn.pack(side=tk.LEFT, padx=2)
        
        # Clear date button
        self.clear_date_btn = ttk.Button(
            date_frame,
            text="✕",
            width=3,
            command=self.clear_date
        )
        self.clear_date_btn.pack(side=tk.LEFT, padx=2)
        
        # Confirm date button
        self.confirm_date_btn = ttk.Button(
            date_frame,
            text="✓",
            width=3,
            command=self.confirm_date
        )
        self.confirm_date_btn.pack(side=tk.LEFT, padx=2)
        
        # Bind Enter key to confirm date
        self.date_entry.bind("<Return>", lambda e: self.confirm_date())
        
        # Asset Type
        ttk.Label(form_frame, text="Asset Type:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.asset_type = ttk.Entry(form_frame, width=40, textvariable=self.asset_type_var)
        self.asset_type.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Creator
        ttk.Label(form_frame, text="Creator/Editor:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.creator = ttk.Entry(form_frame, width=40, textvariable=self.creator_var)
        self.creator.grid(row=4, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Configure grid column weights
        form_frame.columnconfigure(1, weight=1)
        
        # Result frame
        result_frame = ttk.LabelFrame(main_frame, text="Generated Filename", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Result field - using Text widget with limited height for better performance
        self.result = tk.Text(result_frame, height=4, wrap=tk.WORD, font=("Consolas", 10))
        self.result.pack(fill=tk.BOTH, expand=True)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Copy button
        copy_btn = ttk.Button(button_frame, text="Copy to Clipboard", command=self.copy_to_clipboard)
        copy_btn.pack(side=tk.LEFT, padx=5)
        
        # Reset button
        reset_btn = ttk.Button(button_frame, text="Reset Form", command=self.reset_form)
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        # Exit button
        exit_btn = ttk.Button(button_frame, text="Exit", command=self.master.quit)
        exit_btn.pack(side=tk.RIGHT, padx=5)
        
        # Generate the initial filename
        self.update_filename()

    def toggle_date_entry(self):
        """Toggle date entry enabled/disabled state based on checkbox"""
        state = "normal" if self.use_date.get() else "disabled"
        self.date_entry.configure(state=state)
        self.calendar_btn.configure(state=state)
        self.clear_date_btn.configure(state=state)
        self.confirm_date_btn.configure(state=state)
        
        # Update the filename when checkbox changes
        self.update_filename()

    def show_calendar(self):
        """Display date picker calendar in a popup"""
        # Create a top-level window for the calendar
        top = tk.Toplevel(self.master)
        top.title("Select Date")
        top.transient(self.master)  # Set to be transient for main window
        top.grab_set()  # Modal behavior
        
        # Position near the date entry
        x = self.master.winfo_rootx() + self.date_entry.winfo_x() + 50
        y = self.master.winfo_rooty() + self.date_entry.winfo_y() + 50
        top.geometry(f"+{x}+{y}")
        
        # Get the DateEntry class
        DateEntry = LazyDateEntry.get_class()
        
        # Try to get the current date from the entry field
        try:
            current_date = parse_date(self.date_var.get())
        except ValueError:
            current_date = datetime.now()
        
        # Create the calendar widget
        cal = DateEntry(
            top,
            width=12,
            background="darkblue",
            foreground="white",
            borderwidth=2,
            date_pattern="mm/dd/yyyy",
            year=current_date.year,
            month=current_date.month,
            day=current_date.day
        )
        cal.pack(padx=10, pady=10)
        
        # Add OK button
        def set_date():
            self.date_var.set(cal.get_date().strftime("%m/%d/%Y"))
            self.current_date_obj = cal.get_date()
            self.update_filename()
            top.destroy()
            
        ttk.Button(top, text="OK", command=set_date).pack(pady=5)

    def clear_date(self):
        """Clear the date field"""
        self.date_var.set("")
        self.update_filename()

    def confirm_date(self):
        """Validate and confirm the manually entered date"""
        date_str = self.date_var.get()
        
        if not date_str:
            # If date is empty, use NA
            self.current_date_obj = None
            self.update_filename()
            return
            
        try:
            # Try to parse the date
            self.current_date_obj = parse_date(date_str)
            # Update the field with the standardized format
            self.date_var.set(self.current_date_obj.strftime("%m/%d/%Y"))
            self.update_filename()
        except ValueError:
            messagebox.showerror(
                "Invalid Date", 
                "Please enter a valid date in format MM/DD/YYYY or leave blank."
            )
            # Focus back on the date entry
            self.date_entry.focus_set()
            # Select all text to facilitate correcting the date
            self.date_entry.select_range(0, tk.END)

    def update_filename(self, *args):
        """Generate filename based on form data and update the display"""
        event_name = clean_text(self.event_name_var.get().strip())
        programs = self.programs_var.get().strip()
        
        # Handle date - use "NA" if checkbox is unchecked or date is empty
        if self.use_date.get():
            if not self.date_var.get():
                formatted_date = "NA"
            else:
                try:
                    # Check if we have a current_date_obj
                    if self.current_date_obj:
                        formatted_date = format_date(self.current_date_obj)
                    else:
                        # Try to parse the date string
                        date_obj = parse_date(self.date_var.get())
                        formatted_date = format_date(date_obj)
                except:
                    # Fallback if date is invalid
                    formatted_date = "NA"
        else:
            formatted_date = "NA"
            
        asset_type = clean_text(self.asset_type_var.get().strip())
        creator = self.creator_var.get().strip()
        
        if not creator:
            creator = "NA"
        
        # Build the filename
        filename = f"{event_name}_{programs}_{formatted_date}_{asset_type}_{creator}"
        
        # Display the result
        self.result.delete(1.0, tk.END)
        self.result.insert(tk.END, filename)
        return filename

    def generate_filename(self):
        """Legacy method for backward compatibility"""
        return self.update_filename()

    def copy_to_clipboard(self):
        """Copy the generated filename to clipboard"""
        filename = self.result.get(1.0, tk.END).strip()
        if filename:
            self.master.clipboard_clear()
            self.master.clipboard_append(filename)
        else:
            messagebox.showwarning("Warning", "Generate a filename first!")

    def reset_form(self):
        """Reset all form fields"""
        self.event_name_var.set("")
        self.programs_var.set("")
        # Reset date checkbox and date picker
        self.use_date.set(True)
        self.toggle_date_entry()
        self.date_var.set(datetime.now().strftime("%m/%d/%Y"))
        self.current_date_obj = datetime.now()
        self.asset_type_var.set("")
        self.creator_var.set("")
        # The filename will be updated automatically due to the trace callbacks

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def main():
    """Main function to run the file namer tool with GUI"""
    try:
        # Initialize tkinter
        root = tk.Tk()
        app = FileNamerApp(root)
        
        # Process idle tasks before showing window for faster perceived startup
        root.update_idletasks()
        root.deiconify()
        
        # Set DPI awareness for better display on Windows
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except:
            pass
            
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    try:
        import os
        # Required for packaging with PyInstaller
        os.environ['PYTHONIOENCODING'] = 'utf-8'
        main()
    except Exception as e:
        # Show error message if something goes wrong
        import traceback
        error_message = f"An unexpected error occurred:\n{str(e)}\n\n{traceback.format_exc()}"
        
        # Try to show GUI error if possible
        try:
            import tkinter.messagebox as msgbox
            msgbox.showerror("Error", error_message)
        except:
            # Fallback to console
            print(error_message)
            input("Press Enter to exit...")