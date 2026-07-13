"""
Base Account Model - Abstract class for all account types
"""
from abc import ABC, abstractmethod
from datetime import datetime
import random
import hashlib

class BaseAccount(ABC):
    """Abstract base class for bank accounts"""
    
    def __init__(self, holder_name, account_type, password, initial_balance=0.0):
        self.account_number = self._generate_account_number()
        self.holder_name = holder_name
        self.account_type = account_type
        self.balance = initial_balance
        self.password_hash = self._hash_password(password)
        self.created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.account_status = 'Active'
        self.minimum_balance = 0.0
        self.interest_rate = 0.0
    
    @staticmethod
    def _hash_password(password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def _generate_account_number():
        """Generate a unique account number"""
        return f"ACC{random.randint(100000, 999999)}"
    
    def verify_password(self, password):
        """Verify account password"""
        return self.password_hash == self._hash_password(password)
    
    @abstractmethod
    def deposit(self, amount):
        """Deposit money into account"""
        pass
    
    @abstractmethod
    def withdraw(self, amount):
        """Withdraw money from account"""
        pass
    
    @abstractmethod
    def calculate_interest(self):
        """Calculate interest for the account"""
        pass
    
    def get_account_details(self):
        """Get account details as dictionary"""
        return {
            'account_number': self.account_number,
            'account_type': self.account_type,
            'holder_name': self.holder_name,
            'balance': self.balance,
            'password_hash': self.password_hash,
            'created_at': self.created_at,
            'account_status': self.account_status,
            'minimum_balance': self.minimum_balance,
            'interest_rate': self.interest_rate
        }
    
    def __str__(self):
        return f"Account: {self.account_number} | Type: {self.account_type} | Balance: ₹{self.balance:.2f}"
