"""
Transaction Service - Handles financial transactions
"""
from database.database_manager import DatabaseManager
from config import DATABASE_PATH
from datetime import datetime

class TransactionService:
    """Service class for transaction operations"""
    
    def __init__(self):
        self.database = DatabaseManager(DATABASE_PATH)
    
    def process_deposit(self, account_number, amount, description='Deposit'):
        """Process deposit transaction"""
        if amount <= 0:
            return False, "Amount must be positive"
        
        try:
            self.database.connect()
            
            # Get current account
            account = self.database.get_account_by_number(account_number)
            if not account:
                self.database.disconnect()
                return False, "Account not found"
            
            # Update balance
            new_balance = account['balance'] + amount
            self.database.update_account_balance(account_number, new_balance)
            
            # Record transaction
            transaction_data = (
                account_number,
                'Deposit',
                amount,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                description,
                new_balance,
                None
            )
            self.database.insert_transaction(transaction_data)
            
            self.database.disconnect()
            return True, f"Deposited ₹{amount:.2f}. New balance: ₹{new_balance:.2f}"
        
        except Exception as error:
            self.database.disconnect()
            return False, f"Error processing deposit: {str(error)}"
    
    def process_withdrawal(self, account_number, amount, description='Withdrawal'):
        """Process withdrawal transaction"""
        if amount <= 0:
            return False, "Amount must be positive"
        
        try:
            self.database.connect()
            
            # Get current account
            account = self.database.get_account_by_number(account_number)
            if not account:
                self.database.disconnect()
                return False, "Account not found"
            
            # Check sufficient balance (including overdraft for current accounts)
            available_balance = account['balance']
            if account['account_type'] == 'Current':
                from config import CURRENT_OVERDRAFT_LIMIT
                available_balance += CURRENT_OVERDRAFT_LIMIT
            
            if amount > available_balance:
                self.database.disconnect()
                return False, f"Insufficient balance. Available: ₹{available_balance:.2f}"
            
            # Update balance
            new_balance = account['balance'] - amount
            self.database.update_account_balance(account_number, new_balance)
            
            # Record transaction
            transaction_data = (
                account_number,
                'Withdrawal',
                amount,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                description,
                new_balance,
                None
            )
            self.database.insert_transaction(transaction_data)
            
            self.database.disconnect()
            return True, f"Withdrawn ₹{amount:.2f}. New balance: ₹{new_balance:.2f}"
        
        except Exception as error:
            self.database.disconnect()
            return False, f"Error processing withdrawal: {str(error)}"
    
    def get_transaction_history(self, account_number, limit=50):
        """Get transaction history for an account"""
        try:
            self.database.connect()
            transactions = self.database.get_transactions_by_account(account_number, limit)
            self.database.disconnect()
            
            if transactions:
                return True, [dict(transaction) for transaction in transactions]
            return False, "No transactions found"
        
        except Exception as error:
            self.database.disconnect()
            return False, f"Error fetching transactions: {str(error)}"
    
    def get_account_balance(self, account_number):
        """Get account balance"""
        try:
            self.database.connect()
            account = self.database.get_account_by_number(account_number)
            self.database.disconnect()
            
            if account:
                return True, account['balance'], account['holder_name']
            return False, None, "Account not found"
        
        except Exception as error:
            self.database.disconnect()
            return False, None, f"Error fetching balance: {str(error)}"
