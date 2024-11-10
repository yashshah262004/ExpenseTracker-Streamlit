# database.py
import os
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGO_URI'))
        self.db = self.client.expense_tracker
        
    def add_user(self, email, password_hash):
        return self.db.users.insert_one({
            'email': email,
            'password': password_hash,
            'created_at': datetime.now()
        })
    
    def get_user(self, email):
        return self.db.users.find_one({'email': email})
    
    def add_expense(self, user_id, description, amount, category, date):
        # Convert date to datetime
        if isinstance(date, datetime):
            expense_date = date
        else:
            # Convert the date to datetime at midnight
            expense_date = datetime.combine(date, datetime.min.time())
        
        return self.db.expenses.insert_one({
            'user_id': str(user_id),
            'description': description,
            'amount': float(amount),
            'category': category,
            'date': expense_date,  # Store as datetime
            'created_at': datetime.now()
        })
    
    def get_expenses(self, user_id):
        expenses = list(self.db.expenses.find(
            {'user_id': str(user_id)},
            {'_id': 1, 'description': 1, 'amount': 1, 'category': 1, 'date': 1}
        ).sort('date', -1))
        
        # Convert datetime back to date for display
        for expense in expenses:
            if expense['date']:
                expense['date'] = expense['date'].date()
        
        return expenses
    
    def delete_expense(self, expense_id, user_id):
        return self.db.expenses.delete_one({
            '_id': expense_id,
            'user_id': str(user_id)
        })
    
    def update_expense(self, expense_id, user_id, description, amount, category, date):
        # Convert date to datetime
        if isinstance(date, datetime):
            expense_date = date
        else:
            # Convert the date to datetime at midnight
            expense_date = datetime.combine(date, datetime.min.time())
            
        return self.db.expenses.update_one(
            {'_id': expense_id, 'user_id': str(user_id)},
            {
                '$set': {
                    'description': description,
                    'amount': float(amount),
                    'category': category,
                    'date': expense_date,
                    'updated_at': datetime.now()
                }
            }
        )