"""
Formatting utilities for display
"""
import os
from datetime import datetime

class Formatters:
    """Collection of formatting methods"""
    
    @staticmethod
    def clear_screen():
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def print_header(title):
        """Print a formatted header"""
        print("\n" + "="*60)
        print(f"  {title}")
        print("="*60 + "\n")
    
    @staticmethod
    def print_success(message):
        """Print success message"""
        print(f"✅ {message}")
    
    @staticmethod
    def print_error(message):
        """Print error message"""
        print(f"❌ {message}")
    
    @staticmethod
    def print_info(message):
        """Print info message"""
        print(f"ℹ️  {message}")
    
    @staticmethod
    def print_warning(message):
        """Print warning message"""
        print(f"⚠️  {message}")
    
    @staticmethod
    def print_separator():
        """Print a separator line"""
        print("-"*60)
    
    @staticmethod
    def format_currency(amount):
        """Format amount as currency"""
        return f"₹{amount:,.2f}"
    
    @staticmethod
    def format_date(date_string):
        """Format date string for display"""
        try:
            date_object = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
            return date_object.strftime('%B %d, %Y at %I:%M %p')
        except:
            return date_string
    
    @staticmethod
    def pause():
        """Pause and wait for user input"""
        input("\nPress Enter to continue...")
    
    @staticmethod
    def get_input(prompt, validator=None, error_message=None):
        """Get validated input from user"""
        while True:
            value = input(prompt)
            if not validator:
                return value
            is_valid, message = validator(value)
            if is_valid:
                return value
            print(f"❌ {message if error_message is None else error_message}")
