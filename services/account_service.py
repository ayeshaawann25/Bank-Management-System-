"""
Account Service - Manages account operations
"""
from database.database_manager import DatabaseManager
from models.savings_account import SavingsAccount
from models.current_account import CurrentAccount
from config import DATABASE_PATH

class AccountService:
    """Service class for account operations"""
    
    def __init__(self):
        self.database = DatabaseManager(DATABASE_PATH)
    
    def create_savings_account(self, holder_name, password, initial_deposit):
        """Create a new savings account"""
        account = SavingsAccount(holder_name, password, float(initial_deposit))
        return self._save_account(account)
    
    def create_current_account(self, holder_name, password, initial_deposit):
        """Create a new current account"""
        account = CurrentAccount(holder_name, password, float(initial_deposit))
        return self._save_account(account)
    
    def _save_account(self, account):
        """Save account to database"""
        account_data = (
            account.account_number,
            account.account_type,
            account.holder_name,
            account.balance,
            account.password_hash,
            account.created_at,
            account.minimum_balance,
            account.interest_rate,
            account.account_status
        )
        
        try:
            self.database.connect()
            self.database.insert_account(account_data)
            
            # Add initial deposit transaction if any
            if account.balance > 0:
                self.database.insert_transaction((
                    account.account_number,
                    'Deposit',
                    account.balance,
                    account.created_at,
                    'Initial deposit',
                    account.balance,
                    None
                ))
            
            self.database.disconnect()
            return True, account.account_number, f"Account created successfully! Account Number: {account.account_number}"
        except Exception as error:
            self.database.disconnect()
            return False, None, f"Error creating account: {str(error)}"
    
    def get_account(self, account_number):
        """Get account by account number"""
        try:
            self.database.connect()
            account_data = self.database.get_account_by_number(account_number)
            self.database.disconnect()
            
            if account_data:
                return True, dict(account_data)
            return False, "Account not found"
        except Exception as error:
            self.database.disconnect()
            return False, f"Error fetching account: {str(error)}"
    
    def verify_account_credentials(self, account_number, password):
        """Verify account credentials"""
        try:
            self.database.connect()
            account = self.database.get_account_by_number(account_number)
            self.database.disconnect()
            
            if not account:
                return False, "Account not found"
            
            # Hash the provided password and compare
            from models.base_account import BaseAccount
            hashed_password = BaseAccount._hash_password(password)
            
            if account['password_hash'] == hashed_password:
                return True, "Verification successful"
            return False, "Invalid password"
        except Exception as error:
            self.database.disconnect()
            return False, f"Error verifying account: {str(error)}"
    
    def get_all_accounts(self):
        """Get all accounts"""
        try:
            self.database.connect()
            accounts = self.database.get_all_accounts()
            self.database.disconnect()
            return True, [dict(account) for account in accounts]
        except Exception as error:
            self.database.disconnect()
            return False, f"Error fetching accounts: {str(error)}"
