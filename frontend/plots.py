import matplotlib.pyplot as plt
import seaborn as sns

"""def plot_expenses(transactions):
    expenses = {}
    for t in transactions:
        # Defensive unpacking
        try:
            # Adjust the unpacking to match your actual tuple structure
            _, _, _, amount, category, type_ = t
            if type_ == "Expense":
                expenses[category] = expenses.get(category, 0) + amount
        except Exception as e:
            print("Skipping invalid transaction:", t, "Error:", e)
            continue

    fig, ax = plt.subplots()
    if expenses:
        ax.pie(expenses.values(), labels=expenses.keys(), autopct='%1.1f%%')
        ax.set_title("Expenses by Category")
    else:
        ax.text(0.5, 0.5, "No Data", ha='center', va='center', fontsize=12)
        ax.set_axis_off()

    return fig """
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime


def plot_expenses(transactions):
    df = pd.DataFrame(transactions, columns=["id", "user_id", "amount", "type", "date", "category"])
    df['type'] = df['type'].str.capitalize()
    df['category'] = df['category'].str.capitalize()
    df['date'] = pd.to_datetime(df['date'])

    # Group by category and type (Income vs Expense)
    grouped = df.groupby(['category', 'type'])['amount'].sum().unstack(fill_value=0)

    if grouped.empty:
        raise ValueError("No data to plot.")

    categories = grouped.index.tolist()
    x = np.arange(len(categories))
    width = 0.35

    # Fallback if type is missing
    expense_values = grouped['Expense'] if 'Expense' in grouped else pd.Series([0]*len(categories), index=categories)
    income_values = grouped['Income'] if 'Income' in grouped else pd.Series([0]*len(categories), index=categories)

    # Total per category for pie chart
    total_per_category = df.groupby('category')['amount'].sum().sort_values()

    # Create figure with two subplots: bar + pie
    fig, axs = plt.subplots(1, 2, figsize=(9, 5))

    # Bar plot: grouped by Income and Expense
    axs[0].bar(x - width/2, expense_values, width, label='Expense', color='skyblue')
    axs[0].bar(x + width/2, income_values, width, label='Income', color='lightgreen')

    axs[0].set_title("Income and Expense by Category")
    axs[0].set_xlabel("Category")
    axs[0].set_ylabel("Amount ($)")
    axs[0].set_xticks(x)
    axs[0].set_xticklabels(categories, rotation=45)
    axs[0].legend()

    # Pie chart: total amounts (Expense + Income)
    axs[1].pie(total_per_category.values, labels=total_per_category.index,
               autopct='%1.1f%%', startangle=140)
    axs[1].set_title("Overall Distribution by Category")

    fig.tight_layout()
    return fig

