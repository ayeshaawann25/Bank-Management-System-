"""
Current Account Model
"""
from .base_account import BaseAccount
from config import CURRENT_MINIMUM_BALANCE, CURRENT_OVERDRAFT_LIMIT

class CurrentAccount(BaseAccount):
    """Current account with overdraft facility"""
    
    def __init__(self, holder_name, password, initial_deposit=0.0):
        super().__init__(holder_name, 'Current', password, initial_deposit)
        self.minimum_balance = CURRENT_MINIMUM_BALANCE
        self.interest_rate = 0.0
        self.overdraft_limit = CURRENT_OVERDRAFT_LIMIT
    
    def deposit(self, amount):
        """Deposit money to current account"""
        if amount <= 0:
            return False, "Deposit amount must be positive"
        
        self.balance += amount
        return True, f"Deposited ₹{amount:.2f}. New balance: ₹{self.balance:.2f}"
    
    def withdraw(self, amount):
        """Withdraw money from current account with overdraft facility"""
        if amount <= 0:
            return False, "Withdrawal amount must be positive"
        
        available_balance = self.balance + self.overdraft_limit
        if amount > available_balance:
            return False, f"Insufficient balance. Available: ₹{available_balance:.2f} (including ₹{self.overdraft_limit:.2f} overdraft)"
        
        self.balance -= amount
        return True, f"Withdrawn ₹{amount:.2f}. New balance: ₹{self.balance:.2f}"
    
    def calculate_interest(self):
        """No interest for current account"""
        return False, "Current accounts do not earn interest"
    
    def get_account_details(self):
        """Get current account details with additional fields"""
        details = super().get_account_details()
        details['overdraft_limit'] = self.overdraft_limit
        return details
