import matplotlib.pyplot as plt

def plot_expenses(transactions):
    expenses = {}
    for _, _, _, amount, category, type_ in transactions:
        if type_ == "Expense":
            expenses[category] = expenses.get(category, 0) + amount

    fig, ax = plt.subplots()
    if expenses:
        ax.pie(expenses.values(), labels=expenses.keys(), autopct='%1.1f%%')
        ax.set_title("Expenses by Category")
    else:
        ax.text(0.5, 0.5, "No Data", ha='center')

    return fig
