"""
Transfer Service - Manages fund transfers between accounts
"""
from database.database_manager import DatabaseManager
from config import DATABASE_PATH
from datetime import datetime

class TransferService:
    """Service class for fund transfers"""
    
    def __init__(self):
        self.database = DatabaseManager(DATABASE_PATH)
    
    def transfer_funds(self, sender_account, receiver_account, amount, description='Fund Transfer'):
        """Transfer funds between accounts"""
        if amount <= 0:
            return False, "Amount must be positive"
        
        if sender_account == receiver_account:
            return False, "Cannot transfer to the same account"
        
        try:
            self.database.connect()
            
            # Get both accounts
            sender = self.database.get_account_by_number(sender_account)
            receiver = self.database.get_account_by_number(receiver_account)
            
            if not sender:
                self.database.disconnect()
                return False, "Sender account not found"
            
            if not receiver:
                self.database.disconnect()
                return False, "Receiver account not found"
            
            # Check sender's available balance
            available_balance = sender['balance']
            if sender['account_type'] == 'Current':
                from config import CURRENT_OVERDRAFT_LIMIT
                available_balance += CURRENT_OVERDRAFT_LIMIT
            
            if amount > available_balance:
                self.database.disconnect()
                return False, f"Insufficient balance in sender account. Available: ₹{available_balance:.2f}"
            
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Update sender's balance
            sender_new_balance = sender['balance'] - amount
            self.database.update_account_balance(sender_account, sender_new_balance)
            
            # Update receiver's balance
            receiver_new_balance = receiver['balance'] + amount
            self.database.update_account_balance(receiver_account, receiver_new_balance)
            
            # Record sender's transaction
            sender_transaction = (
                sender_account,
                'Transfer',
                amount,
                current_time,
                f"Transfer to {receiver_account}: {description}",
                sender_new_balance,
                receiver_account
            )
            self.database.insert_transaction(sender_transaction)
            
            # Record receiver's transaction
            receiver_transaction = (
                receiver_account,
                'Transfer',
                amount,
                current_time,
                f"Transfer from {sender_account}: {description}",
                receiver_new_balance,
                sender_account
            )
            self.database.insert_transaction(receiver_transaction)
            
            self.database.disconnect()
            return True, f"Transfer successful! ₹{amount:.2f} transferred to {receiver['holder_name']}"
        
        except Exception as error:
            self.database.disconnect()
            return False, f"Error processing transfer: {str(error)}"
