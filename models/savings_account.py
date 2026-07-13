"""
Savings Account Model
"""
from .base_account import BaseAccount
from config import SAVINGS_INTEREST_RATE

class SavingsAccount(BaseAccount):
    """Savings account with interest earning capability"""
    
    def __init__(self, holder_name, password, initial_deposit=0.0):
        super().__init__(holder_name, 'Savings', password, initial_deposit)
        self.minimum_balance = 0.0
        self.interest_rate = SAVINGS_INTEREST_RATE
        self.total_interest_earned = 0.0
    
    def deposit(self, amount):
        """Deposit money to savings account"""
        if amount <= 0:
            return False, "Deposit amount must be positive"
        
        self.balance += amount
        return True, f"Deposited ₹{amount:.2f}. New balance: ₹{self.balance:.2f}"
    
    def withdraw(self, amount):
        """Withdraw money from savings account"""
        if amount <= 0:
            return False, "Withdrawal amount must be positive"
        
        if amount > self.balance:
            return False, f"Insufficient balance. Current balance: ₹{self.balance:.2f}"
        
        self.balance -= amount
        return True, f"Withdrawn ₹{amount:.2f}. New balance: ₹{self.balance:.2f}"
    
    def calculate_interest(self):
        """Calculate monthly interest for savings account"""
        monthly_interest = self.balance * self.interest_rate / 12
        if monthly_interest > 0:
            self.balance += monthly_interest
            self.total_interest_earned += monthly_interest
            return True, f"Interest ₹{monthly_interest:.2f} added. New balance: ₹{self.balance:.2f}"
        return False, "No interest added (balance is zero or negative)"
    
    def get_account_details(self):
        """Get savings account details with additional fields"""
        details = super().get_account_details()
        details['total_interest_earned'] = self.total_interest_earned
        return details
