"""
Configuration file for the Bank Management System
"""
import os

# Database Configuration
DATABASE_NAME = 'bank.db'
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'database', DATABASE_NAME)

# Account Types
ACCOUNT_TYPES = {
    'SAVINGS': 'Savings',
    'CURRENT': 'Current'
}

# Interest Rates and Limits
SAVINGS_INTEREST_RATE = 0.04  # 4% per annum
CURRENT_OVERDRAFT_LIMIT = 10000.0
CURRENT_MINIMUM_BALANCE = 5000.0

# Transaction Types
TRANSACTION_TYPES = {
    'DEPOSIT': 'Deposit',
    'WITHDRAWAL': 'Withdrawal',
    'TRANSFER': 'Transfer',
    'INTEREST': 'Interest'
}

# Validation Constants
MINIMUM_AMOUNT = 1.0
MAXIMUM_AMOUNT = 10000000.0
MINIMUM_INITIAL_DEPOSIT = 100.0
MINIMUM_PASSWORD_LENGTH = 6

# Account Status
ACCOUNT_STATUS = {
    'ACTIVE': 'Active',
    'INACTIVE': 'Inactive',
    'BLOCKED': 'Blocked'
}
