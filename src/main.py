import json
import csv
import os
from datetime import datetime

# Define the path to the data files
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
EXPENSES_FILE = os.path.join(DATA_DIR, 'expenses.json')
CSV_FILE = os.path.join(DATA_DIR, 'expenses.csv')

# Ensure the data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Load expenses from the JSON file
def load_expenses():
    try:
        with open(EXPENSES_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Error: expenses.json is corrupted. Initializing with an empty list.")
        return []

# Save expenses to the JSON file
def save_expenses(expenses):
    with open(EXPENSES_FILE, 'w') as file:
        json.dump(expenses, file, indent=4)

# Add a new expense
def add_expense(description, amount, category):
    expenses = load_expenses()
    expense = {
        'description': description,
        'amount': float(amount),
        'category': category,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"\n✅ Added expense: {description}, Amount: {amount}, Category: {category}\n")

# Update an existing expense by index
def update_expense(index, description=None, amount=None, category=None):
    expenses = load_expenses()
    if 0 <= index < len(expenses):
        if description:
            expenses[index]['description'] = description
        if amount:
            try:
                expenses[index]['amount'] = float(amount)
            except ValueError:
                print("❌ Invalid amount. Update aborted.")
                return
        if category:
            expenses[index]['category'] = category
        save_expenses(expenses)
        print(f"\n✅ Expense at index {index + 1} updated.\n")
    else:
        print("\n❌ Invalid index. Please try again.\n")

# Delete an expense by index
def delete_expense(index):
    expenses = load_expenses()
    if 0 <= index < len(expenses):
        removed = expenses.pop(index)
        save_expenses(expenses)
        print(f"\n✅ Deleted expense: {removed['description']} - {removed['amount']} - {removed['category']}\n")
    else:
        print("\n❌ Invalid index. Please try again.\n")

# View all expenses
def view_expenses():
    expenses = load_expenses()
    if expenses:
        print("\n📋 All Expenses:")
        print("-" * 60)
        print(f"{'Index':<6}{'Description':<20}{'Amount':<10}{'Category':<15}{'Date'}")
        print("-" * 60)
        for i, expense in enumerate(expenses, 1):
            date_str = datetime.strptime(expense['date'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
            print(f"{i:<6}{expense['description']:<20}{expense['amount']:<10.2f}{expense['category']:<15}{date_str}")
        print("-" * 60 + "\n")
    else:
        print("\n❌ No expenses found.\n")

# View summary of all expenses
def view_summary():
    expenses = load_expenses()
    if expenses:
        total = sum(expense['amount'] for expense in expenses)
        print(f"\n📊 Total Expenses: ${total:.2f}\n")
    else:
        print("\n❌ No expenses to summarize.\n")

# View summary for a specific month (of current year)
def view_summary_by_month(month):
    expenses = load_expenses()
    current_year = datetime.now().year
    try:
        month = int(month)
        if not 1 <= month <= 12:
            raise ValueError
    except ValueError:
        print("\n❌ Invalid month. Please enter a number between 1 and 12.\n")
        return

    filtered_expenses = [
        expense for expense in expenses
        if datetime.strptime(expense['date'], '%Y-%m-%d %H:%M:%S').year == current_year and
           datetime.strptime(expense['date'], '%Y-%m-%d %H:%M:%S').month == month
    ]
    if filtered_expenses:
        total = sum(expense['amount'] for expense in filtered_expenses)
        month_name = datetime(current_year, month, 1).strftime('%B')
        print(f"\n📊 Total Expenses for {month_name} {current_year}: ${total:.2f}\n")
        print(f"{'Description':<20}{'Amount':<10}{'Category':<15}{'Date'}")
        print("-" * 60)
        for expense in filtered_expenses:
            date_str = datetime.strptime(expense['date'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
            print(f"{expense['description']:<20}{expense['amount']:<10.2f}{expense['category']:<15}{date_str}")
        print("-" * 60 + "\n")
    else:
        print(f"\n❌ No expenses found for month {month}.\n")

# Set a monthly budget and check if it's exceeded
def check_budget(budget, month):
    expenses = load_expenses()
    current_year = datetime.now().year
    try:
        month = int(month)
        budget = float(budget)
        if not 1 <= month <= 12:
            raise ValueError
    except ValueError:
        print("\n❌ Invalid input. Please ensure month is between 1-12 and budget is a number.\n")
        return

    filtered_expenses = [
        expense for expense in expenses
        if datetime.strptime(expense['date'], '%Y-%m-%d %H:%M:%S').year == current_year and
           datetime.strptime(expense['date'], '%Y-%m-%d %H:%M:%S').month == month
    ]
    total = sum(expense['amount'] for expense in filtered_expenses)
    month_name = datetime(current_year, month, 1).strftime('%B')

    if total > budget:
        print(f"\n⚠️ Warning: You've exceeded your budget for {month_name} {current_year}!")
        print(f"   Budget: ${budget:.2f}")
        print(f"   Total Spent: ${total:.2f}\n")
    else:
        print(f"\n✅ You are within your budget for {month_name} {current_year}.")
        print(f"   Budget: ${budget:.2f}")
        print(f"   Total Spent: ${total:.2f}\n")

# Export expenses to a CSV file
def export_to_csv():
    expenses = load_expenses()
    if expenses:
        try:
            with open(CSV_FILE, 'w', newline='') as csvfile:
                fieldnames = ['description', 'amount', 'category', 'date']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for expense in expenses:
                    writer.writerow(expense)
            print(f"\n✅ Expenses exported to {CSV_FILE}\n")
        except Exception as e:
            print(f"\n❌ Failed to export expenses to CSV. Error: {e}\n")
    else:
        print("\n❌ No expenses to export.\n")

# Main command-line interface
def main():
    while True:
        print("\n📂 Expense Tracker")
        print("1. Add Expense")
        print("2. Update Expense")
        print("3. Delete Expense")
        print("4. View All Expenses")
        print("5. View Summary of Expenses")
        print("6. View Summary by Month")
        print("7. Set Monthly Budget and Check")
        print("8. Export Expenses to CSV")
        print("9. Exit")
        choice = input("Enter your choice (1-9): ").strip()

        if choice == '1':
            print("\n📝 Add a New Expense")
            desc = input("Enter description: ").strip()
            amt = input("Enter amount: ").strip()
            cat = input("Enter category: ").strip()
            if desc and amt and cat:
                try:
                    float(amt)
                    add_expense(desc, amt, cat)
                except ValueError:
                    print("\n❌ Invalid amount. Please enter a numerical value.\n")
            else:
                print("\n❌ All fields are required. Please try again.\n")

        elif choice == '2':
            print("\n✏️ Update an Expense")
            view_expenses()
            if load_expenses():
                index = input("Enter the index of the expense to update: ").strip()
                if index.isdigit():
                    index = int(index) - 1
                    desc = input("Enter new description (leave blank to keep current): ").strip()
                    amt = input("Enter new amount (leave blank to keep current): ").strip()
                    cat = input("Enter new category (leave blank to keep current): ").strip()
                    update_expense(index, desc if desc else None, amt if amt else None, cat if cat else None)
                else:
                    print("\n❌ Invalid input. Please enter a numerical index.\n")
            else:
                print("\n❌ No expenses available to update.\n")

        elif choice == '3':
            print("\n🗑️ Delete an Expense")
            view_expenses()
            if load_expenses():
                index = input("Enter the index of the expense to delete: ").strip()
                if index.isdigit():
                    index = int(index) - 1
                    confirm = input(f"Are you sure you want to delete expense #{index + 1}? (y/n): ").strip().lower()
                    if confirm == 'y':
                        delete_expense(index)
                    else:
                        print("\n❌ Deletion cancelled.\n")
                else:
                    print("\n❌ Invalid input. Please enter a numerical index.\n")
            else:
                print("\n❌ No expenses available to delete.\n")

        elif choice == '4':
            view_expenses()

        elif choice == '5':
            view_summary()

        elif choice == '6':
            print("\n📅 View Summary by Month")
            month = input("Enter month (1-12): ").strip()
            view_summary_by_month(month)

        elif choice == '7':
            print("\n💰 Set Monthly Budget and Check")
            month = input("Enter month (1-12): ").strip()
            budget = input("Enter your budget for the month: ").strip()
            check_budget(budget, month)

        elif choice == '8':
            export_to_csv()

        elif choice == '9':
            print("\n👋 Goodbye! Thank you for using Expense Tracker.\n")
            break

        else:
            print("\n❌ Invalid choice. Please enter a number between 1 and 9.\n")

if __name__ == "__main__":
    main()
