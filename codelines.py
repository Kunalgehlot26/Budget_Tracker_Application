import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

DATA_FILE = "budget_data.csv"

# Load existing transactions from CSV or create a new DataFrame
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Date", "Category", "Amount", "Type", "Description"])

# Save all transactions back to CSV
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Add a new transaction
def add_transaction(df):
    print("\n--- Add New Transaction ---")
    date = input("Date (YYYY-MM-DD): ").strip()
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("❌ Invalid date format.")
        return df

    category = input("Category (e.g., Food, Rent, Salary): ").strip()
    try:
        amount = float(input("Amount: ").strip())
    except ValueError:
        print("❌ Amount must be a number.")
        return df

    t_type = input("Type (income/expense): ").strip().lower()
    if t_type not in ["income", "expense"]:
        print("❌ Type must be 'income' or 'expense'.")
        return df

    description = input("Description (optional): ").strip()

    new_entry = {
        "Date": date,
        "Category": category,
        "Amount": amount,
        "Type": t_type,
        "Description": description
    }

    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    save_data(df)
    print("✅ Transaction added successfully.")
    return df

# Display summary chart of expenses vs income by category
def show_summary(df):
    print("\n--- Spending Summary ---")
    if df.empty:
        print("No transactions found.")
        return

    grouped = df.groupby(["Category", "Type"])["Amount"].sum().unstack().fillna(0)
    print(grouped)

    grouped.plot(kind="bar", stacked=True, figsize=(8, 4))
    plt.title("Income & Expenses by Category")
    plt.ylabel("Amount")
    plt.tight_layout()
    plt.show()

# Main CLI menu loop
def main():
    df = load_data()

    while True:
        print("\n==== Budget Tracker Menu ====")
        print("1. Add Transaction")
        print("2. Show Summary")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            df = add_transaction(df)
        elif choice == "2":
            show_summary(df)
        elif choice == "3":
            print("👋 Exiting. Stay financially sharp!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
