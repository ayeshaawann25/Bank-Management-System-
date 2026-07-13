"""
Transaction Model
"""
from datetime import datetime

class Transaction:
    """Represents a financial transaction"""
    
    def __init__(self, account_number, transaction_type, amount, description=''):
        self.account_number = account_number
        self.transaction_type = transaction_type
        self.amount = amount
        self.description = description
        self.transaction_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.balance_after = 0.0
        self.related_account = None
    
    def to_dictionary(self):
        """Convert transaction to dictionary"""
        return {
            'account_number': self.account_number,
            'transaction_type': self.transaction_type,
            'amount': self.amount,
            'transaction_date': self.transaction_date,
            'description': self.description,
            'balance_after': self.balance_after,
            'related_account': self.related_account
        }
    
    def __str__(self):
        return f"{self.transaction_date} | {self.transaction_type} | ₹{self.amount:.2f} | {self.description}"
