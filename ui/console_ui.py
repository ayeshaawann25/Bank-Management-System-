"""
Console User Interface - Main UI handler
"""
from utils.formatters import Formatters
from utils.validators import Validators
from services.account_service import AccountService
from services.transaction_service import TransactionService
from services.transfer_service import TransferService
from .menu_options import MenuOptions

class ConsoleUI:
    """Main console user interface"""
    
    def __init__(self):
        self.account_service = AccountService()
        self.transaction_service = TransactionService()
        self.transfer_service = TransferService()
        self.current_account = None
    
    def run(self):
        """Run the main application loop"""
        while True:
            option = MenuOptions.main_menu()
            
            if option == '1':
                self.create_account_flow()
            elif option == '2':
                self.deposit_flow()
            elif option == '3':
                self.withdraw_flow()
            elif option == '4':
                self.transfer_flow()
            elif option == '5':
                self.balance_inquiry_flow()
            elif option == '6':
                self.transaction_history_flow()
            elif option == '7':
                self.view_all_accounts_flow()
            elif option == '8':
                self.apply_interest_flow()
            elif option == '0':
                self.exit_application()
                break
            else:
                Formatters.print_error("Invalid option. Please try again.")
                Formatters.pause()
    
    def create_account_flow(self):
        """Handle account creation flow"""
        Formatters.clear_screen()
        Formatters.print_header("📝 Create New Account")
        
        account_type = MenuOptions.account_type_menu()
        
        if account_type not in ['1', '2']:
            Formatters.print_error("Invalid account type selection")
            Formatters.pause()
            return
        
        # Get account holder name
        name = Formatters.get_input(
            "Enter account holder name: ",
            Validators.validate_holder_name
        )
        
        # Get password
        password = Formatters.get_input(
            "Enter password (min 6 chars with uppercase, lowercase, digit): ",
            Validators.validate_password
        )
        
        # Get initial deposit
        deposit = Formatters.get_input(
            f"Enter initial deposit (min ₹{Validators.MINIMUM_INITIAL_DEPOSIT:.2f}): ",
            Validators.validate_initial_deposit
        )
        
        # Create account based on type
        if account_type == '1':
            success, acc_number, message = self.account_service.create_savings_account(
                name, password, float(deposit)
            )
        else:
            success, acc_number, message = self.account_service.create_current_account(
                name, password, float(deposit)
            )
        
        if success:
            Formatters.print_success(message)
            Formatters.print_info(f"Account Number: {acc_number}")
            Formatters.print_warning("Please save your account number for future logins")
        else:
            Formatters.print_error(message)
        
        Formatters.pause()
    
    def authenticate_account(self):
        """Authenticate account access"""
        Formatters.clear_screen()
        Formatters.print_header("🔐 Account Authentication")
        
        account_number = Formatters.get_input(
            "Enter account number: ",
            Validators.validate_account_number
        )
        
        password = input("Enter password: ")
        
        success, message = self.account_service.verify_account_credentials(account_number, password)
        
        if success:
            Formatters.print_success("Authentication successful!")
            self.current_account = account_number
            return True, account_number
        else:
            Formatters.print_error(message)
            Formatters.pause()
            return False, None
    
    def deposit_flow(self):
        """Handle deposit operation flow"""
        Formatters.clear_screen()
        Formatters.print_header("💰 Deposit Money")
        
        success, account = self.authenticate_account()
        if not success:
            return
        
        amount = Formatters.get_input(
            "Enter amount to deposit: ",
            Validators.validate_amount
        )
        
        success, message = self.transaction_service.process_deposit(account, float(amount))
        
        if success:
            Formatters.print_success(message)
        else:
            Formatters.print_error(message)
        
        Formatters.pause()
    
    def withdraw_flow(self):
        """Handle withdrawal operation flow"""
        Formatters.clear_screen()
        Formatters.print_header("🏧 Withdraw Money")
        
        success, account = self.authenticate_account()
        if not success:
            return
        
        amount = Formatters.get_input(
            "Enter amount to withdraw: ",
            Validators.validate_amount
        )
        
        success, message = self.transaction_service.process_withdrawal(account, float(amount))
        
        if success:
            Formatters.print_success(message)
        else:
            Formatters.print_error(message)
        
        Formatters.pause()
    
    def transfer_flow(self):
        """Handle fund transfer flow"""
        Formatters.clear_screen()
        Formatters.print_header("💸 Fund Transfer")
        
        # Authenticate sender
        Formatters.print_info("Authenticate sender account")
        success, from_account = self.authenticate_account()
        if not success:
            return
        
        # Get receiver account
        to_account = Formatters.get_input(
            "Enter receiver account number: ",
            Validators.validate_account_number
        )
        
        # Get amount
        amount = Formatters.get_input(
            "Enter amount to transfer: ",
            Validators.validate_amount
        )
        
        # Confirm transfer
        print("\n📋 Transfer Details:")
        print(f"From Account: {from_account}")
        print(f"To Account: {to_account}")
        print(f"Amount: {Formatters.format_currency(float(amount))}")
        
        confirm = input("\nConfirm transfer? (y/n): ")
        
        if confirm.lower() != 'y':
            Formatters.print_info("Transfer cancelled")
            Formatters.pause()
            return
        
        success, message = self.transfer_service.transfer_funds(
            from_account, to_account, float(amount)
        )
        
        if success:
            Formatters.print_success(message)
        else:
            Formatters.print_error(message)
        
        Formatters.pause()
    
    def balance_inquiry_flow(self):
        """Handle balance inquiry flow"""
        Formatters.clear_screen()
        Formatters.print_header("📊 Balance Inquiry")
        
        success, account = self.authenticate_account()
        if not success:
            return
        
        success, balance, name = self.transaction_service.get_account_balance(account)
        
        if success:
            print("\n📋 Account Details:")
            print(f"👤 Account Holder: {name}")
            print(f"🔢 Account Number: {account}")
            print(f"💰 Balance: {Formatters.format_currency(balance)}")
        else:
            Formatters.print_error(name)
        
        Formatters.pause()
    
    def transaction_history_flow(self):
        """Handle transaction history flow"""
        Formatters.clear_screen()
        Formatters.print_header("📜 Transaction History")
        
        success, account = self.authenticate_account()
        if not success:
            return
        
        success, transactions = self.transaction_service.get_transaction_history(account)
        
        if success:
            if not transactions:
                Formatters.print_info("No transactions found")
            else:
                print("\n📋 Recent Transactions:")
                Formatters.print_separator()
                for transaction in transactions:
                    date = Formatters.format_date(transaction['transaction_date'])
                    print(f"📅 {date}")
                    print(f"   Type: {transaction['transaction_type']}")
                    print(f"   Amount: {Formatters.format_currency(transaction['amount'])}")
                    print(f"   Balance: {Formatters.format_currency(transaction['balance_after'])}")
                    if transaction['description']:
                        print(f"   Note: {transaction['description']}")
                    Formatters.print_separator()
        else:
            Formatters.print_error(transactions)
        
        Formatters.pause()
    
    def view_all_accounts_flow(self):
        """Handle view all accounts flow"""
        Formatters.clear_screen()
        Formatters.print_header("📋 All Accounts")
        
        success, accounts = self.account_service.get_all_accounts()
        
        if success:
            if not accounts:
                Formatters.print_info("No accounts found")
            else:
                print(f"\nTotal Accounts: {len(accounts)}")
                Formatters.print_separator()
                for account in accounts:
                    print(f"🔢 Account: {account['account_number']}")
                    print(f"👤 Holder: {account['holder_name']}")
                    print(f"📊 Type: {account['account_type']}")
                    print(f"💰 Balance: {Formatters.format_currency(account['balance'])}")
                    print(f"📌 Status: {account['account_status']}")
                    Formatters.print_separator()
        else:
            Formatters.print_error(accounts)
        
        Formatters.pause()
    
    def apply_interest_flow(self):
        """Handle interest application for savings accounts"""
        Formatters.clear_screen()
        Formatters.print_header("💰 Apply Interest (Savings Accounts)")
        
        print("⚠️  This will add monthly interest to all savings accounts")
        confirm = input("Continue? (y/n): ")
        
        if confirm.lower() != 'y':
            Formatters.print_info("Operation cancelled")
            Formatters.pause()
            return
        
        # Get all accounts
        success, accounts = self.account_service.get_all_accounts()
        
        if not success:
            Formatters.print_error(accounts)
            Formatters.pause()
            return
        
        interest_applied = 0
        
        for account in accounts:
            if account['account_type'] == 'Savings':
                # Create savings account object to calculate interest
                savings_acc = SavingsAccount(
                    account['holder_name'],
                    'dummy',  # dummy password, we just need the object for calculation
                    account['balance']
                )
                savings_acc.balance = account['balance']  # Set current balance
                
                success, message = savings_acc.calculate_interest()
                
                if success:
                    # Update balance in database
                    self.account_service.database.connect()
                    self.account_service.database.update_account_balance(
                        account['account_number'],
                        savings_acc.balance
                    )
                    # Record interest transaction
                    self.account_service.database.insert_transaction((
                        account['account_number'],
                        'Interest',
                        savings_acc.balance - account['balance'],
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'Monthly interest applied',
                        savings_acc.balance,
                        None
                    ))
                    self.account_service.database.disconnect()
                    interest_applied += 1
        
        Formatters.print_success(f"Interest applied to {interest_applied} savings accounts")
        Formatters.pause()
    
    def exit_application(self):
        """Exit the application"""
        Formatters.clear_screen()
        Formatters.print_header("👋 Thank You!")
        print("Thank you for using the Bank Management System.")
        print("Have a great day!")
