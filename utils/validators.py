"""
Validation utilities for input validation
"""
import re
from config import MINIMUM_AMOUNT, MAXIMUM_AMOUNT, MINIMUM_INITIAL_DEPOSIT, MINIMUM_PASSWORD_LENGTH

class Validators:
    """Collection of validation methods"""
    
    @staticmethod
    def validate_holder_name(name):
        """Validate account holder name"""
        if not name or len(name.strip()) < 2:
            return False, "Name must be at least 2 characters"
        if not re.match(r'^[a-zA-Z\s]+$', name):
            return False, "Name can only contain letters and spaces"
        return True, "Valid name"
    
    @staticmethod
    def validate_password(password):
        """Validate password strength"""
        if len(password) < MINIMUM_PASSWORD_LENGTH:
            return False, f"Password must be at least {MINIMUM_PASSWORD_LENGTH} characters"
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        if not re.search(r'\d', password):
            return False, "Password must contain at least one number"
        return True, "Valid password"
    
    @staticmethod
    def validate_amount(amount, min_amount=MINIMUM_AMOUNT, max_amount=MAXIMUM_AMOUNT):
        """Validate transaction amount"""
        try:
            amount = float(amount)
            if amount < min_amount:
                return False, f"Amount must be at least ₹{min_amount:.2f}"
            if amount > max_amount:
                return False, f"Amount cannot exceed ₹{max_amount:.2f}"
            return True, "Valid amount"
        except ValueError:
            return False, "Invalid amount format"
    
    @staticmethod
    def validate_initial_deposit(amount):
        """Validate initial deposit amount"""
        return Validators.validate_amount(amount, MINIMUM_INITIAL_DEPOSIT)
    
    @staticmethod
    def validate_account_number(account_number):
        """Validate account number format"""
        if not account_number or not re.match(r'^ACC\d{6}$', account_number):
            return False, "Invalid account number format (should be ACC followed by 6 digits)"
        return True, "Valid account number"
