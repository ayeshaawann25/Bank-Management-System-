"""
Database Manager - Handles all database operations
"""
import sqlite3
from datetime import datetime
import os

class DatabaseManager:
    """Manages database connections and operations"""
    
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize database with required tables"""
        self.connect()
        self._create_tables()
        self.disconnect()
    
    def connect(self):
        """Establish database connection"""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
    
    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
    
    def _create_tables(self):
        """Create necessary tables if they don't exist"""
        # Accounts table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                account_number TEXT PRIMARY KEY,
                account_type TEXT NOT NULL,
                holder_name TEXT NOT NULL,
                balance REAL DEFAULT 0.0,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL,
                minimum_balance REAL DEFAULT 0.0,
                interest_rate REAL DEFAULT 0.0,
                account_status TEXT DEFAULT 'Active'
            )
        ''')
        
        # Transactions table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_number TEXT NOT NULL,
                transaction_type TEXT NOT NULL,
                amount REAL NOT NULL,
                transaction_date TEXT NOT NULL,
                description TEXT,
                balance_after REAL NOT NULL,
                related_account TEXT,
                FOREIGN KEY (account_number) REFERENCES accounts(account_number)
            )
        ''')
        
        self.connection.commit()
    
    def execute_query(self, query, params=()):
        """Execute a query and return results"""
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return self.cursor
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
    
    def fetch_one(self, query, params=()):
        """Fetch one record"""
        self.cursor.execute(query, params)
        return self.cursor.fetchone()
    
    def fetch_all(self, query, params=()):
        """Fetch all records"""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def insert_account(self, account_data):
        """Insert a new account"""
        query = '''
            INSERT INTO accounts 
            (account_number, account_type, holder_name, balance, password_hash, 
             created_at, minimum_balance, interest_rate, account_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        return self.execute_query(query, account_data)
    
    def update_account_balance(self, account_number, new_balance):
        """Update account balance"""
        query = 'UPDATE accounts SET balance = ? WHERE account_number = ?'
        return self.execute_query(query, (new_balance, account_number))
    
    def insert_transaction(self, transaction_data):
        """Insert a new transaction"""
        query = '''
            INSERT INTO transactions 
            (account_number, transaction_type, amount, transaction_date, 
             description, balance_after, related_account)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        return self.execute_query(query, transaction_data)
    
    def get_account_by_number(self, account_number):
        """Get account by account number"""
        query = 'SELECT * FROM accounts WHERE account_number = ?'
        return self.fetch_one(query, (account_number,))
    
    def get_transactions_by_account(self, account_number, limit=50):
        """Get transactions for an account"""
        query = '''
            SELECT * FROM transactions 
            WHERE account_number = ? 
            ORDER BY transaction_date DESC 
            LIMIT ?
        '''
        return self.fetch_all(query, (account_number, limit))
    
    def get_all_accounts(self):
        """Get all accounts"""
        query = 'SELECT * FROM accounts ORDER BY created_at DESC'
        return self.fetch_all(query)
    
    def update_account_status(self, account_number, status):
        """Update account status"""
        query = 'UPDATE accounts SET account_status = ? WHERE account_number = ?'
        return self.execute_query(query, (status, account_number))
