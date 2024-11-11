import streamlit as st
from datetime import datetime
from database import Database  # Import the Database class from database.py
from auth_handler import AuthHandler
from pymongo import MongoClient
import os

# Initialize database and auth handler
db = Database()
auth_handler = AuthHandler()

def initialize_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None

def login_page():
    st.title("Login")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            success, result = auth_handler.login_user(email, password)
            if success:
                st.session_state.logged_in = True
                st.session_state.user_id = result['_id']
                st.session_state.user_email = result['email']
                st.success("Logged in successfully!")
                st.experimental_rerun()
            else:
                st.error(result)

def register_page():
    st.title("Register")
    with st.form("register_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submitted = st.form_submit_button("Register")
        
        if submitted:
            success, message = auth_handler.register_user(email, password, confirm_password)
            if success:
                st.success(message)
            else:
                st.error(message)

def expense_tracker():
    st.title(f"Expense Tracker - {st.session_state.user_email}")
    
    # Add new expense
    with st.form("add_expense"):
        st.subheader("Add New Expense")
        description = st.text_input("Description")
        amount = st.number_input("Amount", min_value=0.0, step=0.01)
        category = st.selectbox("Category", [
            "Food & Dining",
            "Transportation",
            "Shopping",
            "Bills & Utilities",
            "Entertainment",
            "Health & Fitness",
            "Travel",
            "Other"
        ])
        date = st.date_input("Date", datetime.now())
        
        if st.form_submit_button("Add Expense"):
            db.add_expense(st.session_state.user_id, description, amount, category, date)
            st.success("Expense added successfully!")
            st.experimental_rerun()
    
    # View expenses
    st.subheader("Your Expenses")
    expenses = db.get_expenses(st.session_state.user_id)
    
    # Summary statistics
    if expenses:
        total_expenses = sum(expense['amount'] for expense in expenses)
        st.metric("Total Expenses", f"Rs.{total_expenses:.2f}")
        
        # Category-wise breakdown
        st.subheader("Expenses by Category")
        categories = {}
        for expense in expenses:
            categories[expense['category']] = categories.get(expense['category'], 0) + expense['amount']
        
        for category, amount in categories.items():
            st.write(f"{category}: Rs{amount:.2f}")
    
    # Expense list
    for expense in expenses:
        with st.expander(f"{expense['description']} - Rs.{expense['amount']:.2f}"):

            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.write(f"Category: {expense['category']}")
            with col2:
                st.write(f"Date: {expense['date'].strftime('%Y-%m-%d')}")
            with col3:
                if st.button("Delete", key=f"delete_{str(expense['_id'])}"):
                    db.delete_expense(expense['_id'], st.session_state.user_id)
                    st.success("Expense deleted!")
                    st.experimental_rerun()

def main():
    initialize_session_state()
    
    if not st.session_state.logged_in:
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            login_page()
        with tab2:
            register_page()
    else:
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.user_email = None
            st.experimental_rerun()
        
        expense_tracker()

if __name__ == "__main__":
    main()