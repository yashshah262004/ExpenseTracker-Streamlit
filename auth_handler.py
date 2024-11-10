# auth_handler.py
import bcrypt
import streamlit as st
from database import Database

class AuthHandler:
    def __init__(self):
        self.db = Database()
    
    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    def verify_password(self, password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    
    def register_user(self, email, password, confirm_password):
        if password != confirm_password:
            return False, "Passwords do not match"
        
        if self.db.get_user(email):
            return False, "Email already exists"
        
        hashed_password = self.hash_password(password)
        self.db.add_user(email, hashed_password)
        return True, "Registration successful!"
    
    def login_user(self, email, password):
        user = self.db.get_user(email)
        if not user or not self.verify_password(password, user['password']):
            return False, "Invalid email or password"
        return True, user