import pandas as pd
from datetime import datetime
import os

class FinanceDataManager:
    def __init__(self):
        self.file_path = "transactions.csv"
        self.categories = [
            "Salary", "Investments", "Food", "Transportation", 
            "Housing", "Utilities", "Entertainment", "Healthcare",
            "Shopping", "Other"
        ]
        self.df = self._load_data()

    def _load_data(self):
        if os.path.exists(self.file_path):
            return pd.read_csv(self.file_path)
        return pd.DataFrame({
            'date': [],
            'type': [],
            'amount': [],
            'category': [],
            'description': []
        })

    def save_transaction(self, transaction_type, amount, category, description):
        new_transaction = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'type': transaction_type,
            'amount': float(amount),
            'category': category,
            'description': description
        }
        self.df = pd.concat([self.df, pd.DataFrame([new_transaction])], ignore_index=True)
        self.df.to_csv(self.file_path, index=False)

    def get_balance(self):
        income = self.df[self.df['type'] == 'Income']['amount'].sum()
        expenses = self.df[self.df['type'] == 'Expense']['amount'].sum()
        return income - expenses

    def get_monthly_summary(self):
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df['month'] = self.df['date'].dt.strftime('%Y-%m')
        monthly = self.df.groupby(['month', 'type'])['amount'].sum().unstack(fill_value=0)
        if 'Income' not in monthly.columns:
            monthly['Income'] = 0
        if 'Expense' not in monthly.columns:
            monthly['Expense'] = 0
        monthly['Balance'] = monthly['Income'] - monthly['Expense']
        return monthly

    def get_category_summary(self):
        return self.df[self.df['type'] == 'Expense'].groupby('category')['amount'].sum()

    def export_data(self):
        return self.df.to_csv(index=False).encode('utf-8')
