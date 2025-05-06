import matplotlib.pyplot as plt
import seaborn as sns

def plot_expenses(transactions):
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

    return fig

