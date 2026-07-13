#!/usr/bin/env python3
"""
Bank Management System - Main Entry Point
"""
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.console_ui import ConsoleUI

def main():
    """Main application entry point"""
    try:
        ui = ConsoleUI()
        ui.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as error:
        print(f"\n❌ An unexpected error occurred: {error}")
        sys.exit(1)

if __name__ == "__main__":
    main()
