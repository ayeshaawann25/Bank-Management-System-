"""
Menu definitions for the Bank Management System
"""
from utils.formatters import Formatters

class MenuOptions:
    """Contains all menu definitions"""
    
    @staticmethod
    def main_menu():
        """Display main menu"""
        Formatters.clear_screen()
        Formatters.print_header("🏦 BANK MANAGEMENT SYSTEM")
        print("1️⃣  Create New Account")
        print("2️⃣  Deposit Money")
        print("3️⃣  Withdraw Money")
        print("4️⃣  Transfer Funds")
        print("5️⃣  Check Balance")
        print("6️⃣  Transaction History")
        print("7️⃣  View All Accounts")
        print("8️⃣  Apply Interest (Savings)")
        print("0️⃣  Exit")
        Formatters.print_separator()
        return input("Select an option: ")
    
    @staticmethod
    def account_type_menu():
        """Display account type menu"""
        print("\n📋 Account Type:")
        print("1️⃣  Savings Account")
        print("2️⃣  Current Account")
        return input("Select account type: ")
    
    @staticmethod
    def authentication_menu():
        """Display authentication options"""
        print("\n🔐 Account Authentication:")
        print("Enter your account number and password to proceed")
