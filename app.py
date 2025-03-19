import streamlit as st
import pandas as pd
from data_manager import FinanceDataManager
from analytics import create_monthly_trend_chart, create_expense_category_chart

# Initialize session state
if 'data_manager' not in st.session_state:
    st.session_state.data_manager = FinanceDataManager()

def main():
    st.title("Personal Finance Tracker")
    
    # Sidebar for adding transactions
    with st.sidebar:
        st.header("Add Transaction")
        transaction_type = st.selectbox("Transaction Type", ["Income", "Expense"])
        amount = st.number_input("Amount", min_value=0.01, step=0.01)
        categories = st.session_state.data_manager.categories
        category = st.selectbox("Category", categories)
        description = st.text_input("Description")
        
        if st.button("Add Transaction"):
            st.session_state.data_manager.save_transaction(
                transaction_type, amount, category, description
            )
            st.success("Transaction added successfully!")
            st.rerun()

    # Main content area
    col1, col2 = st.columns(2)
    
    # Current Balance
    with col1:
        st.metric("Current Balance", f"${st.session_state.data_manager.get_balance():.2f}")
    
    # Monthly Summary
    st.header("Monthly Summary")
    monthly_summary = st.session_state.data_manager.get_monthly_summary()
    st.plotly_chart(create_monthly_trend_chart(monthly_summary), use_container_width=True)
    
    # Expense Categories
    st.header("Expense Categories")
    category_summary = st.session_state.data_manager.get_category_summary()
    st.plotly_chart(create_expense_category_chart(category_summary), use_container_width=True)
    
    # Transaction History
    st.header("Transaction History")
    df = st.session_state.data_manager.df.sort_values('date', ascending=False)
    st.dataframe(df, use_container_width=True)
    
    # Export Data
    st.download_button(
        label="Export Data",
        data=st.session_state.data_manager.export_data(),
        file_name="finance_data.csv",
        mime="text/csv"
    )

if __name__ == "__main__":
    main()
