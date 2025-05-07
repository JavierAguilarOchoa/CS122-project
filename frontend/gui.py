import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
from backend.database import add_transaction, get_transactions
from plots import plot_expenses
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from plots import plot_expenses
from backend.database import get_transactions

class BudgetApp:
    """
    A GUI application for personal budget management using Tkinter.

    This class provides the main interface for users to add transactions,
    view summaries, and interact with the underlying budget data.

    Attributes:
        root (tk.Tk): The root Tkinter window.
        user (User): The currently logged-in user object.
    """
    def __init__(self, root, logged_in_user):
        """
          Initialize the BudgetApp with a root window and a logged-in user.

          Args:
              root (tk.Tk): The main Tkinter window.
              logged_in_user (User): The user object of the logged-in user.
          """
        self.root = root
        self.root.title("BudgetBuddy")
        self.root.geometry("1100x700")
        self.user = logged_in_user
        self.set_background("../utils/bg_with_title_text.png")
        self.create_welcome()

    def set_background(self, image_path):
        """
          Sets the background image of the application window.

          Args:
              image_path (str): Path to the image file to be used as background.
          """
        self.bg_image = Image.open(image_path)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def clear(self):
        """
          Clears all widgets from the window and resets the background image.
          """
        for widget in self.root.winfo_children():
            widget.destroy()
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def create_welcome(self):
        """
        Displays the welcome screen with a 'Get Started' button.
        """
        self.clear()
        start_button = tk.Button(
            self.root,
            text="Get Started",
            font=("Times New Roman", 30, "bold"),
            bg="white",
            fg="black",
            width=15,
            height=1,
            borderwidth=0,
            relief="ridge",
            highlightbackground="#ccc",
            highlightthickness=0,
            command=self.create_home
        )
        start_button.place(x=425, y=500)

    def create_home(self):
        """
         Displays the main home screen with options to add a transaction or view a summary.
         """
        self.set_background("../utils/bg_add_transaction.jpg")
        self.clear()
        tk.Label(self.root, text="Add Transaction or View Summary", font=("Times New Roman", 30, "bold"), background="white", foreground="black").place(x=330, y=180)
        add_button = tk.Button(self.root, text="Add New Transaction",
                               font=("Times New Roman", 20, "bold"),
                               bg="white", fg="black",
                               width=20, height=2,
                               borderwidth=0, relief="ridge",
                               highlightbackground="#ccc", highlightthickness=0,
                               command=self.create_add_transaction)
        add_button.place(x=450, y=300)
        summary_button = tk.Button(self.root, text="View Summary",
                                   font=("Times New Roman", 20, "bold"),
                                   bg="white", fg="black",
                                   width=20, height=2,
                                   borderwidth=0, relief="ridge",
                                   highlightbackground="#ccc", highlightthickness=0,
                                   command=self.create_summary)
        summary_button.place(x=450, y=450)

    def create_add_transaction(self):
        """
          Displays the form for adding a new transaction with fields for date, amount,
          category, and type (Income/Expense).
          """
        self.set_background("../utils/bg_add_transaction.jpg")
        self.clear()
        tk.Label(self.root, text="Add New Transaction", font=("Times New Roman", 30, "bold"), background="white", foreground="black").place(x=400, y=160)

        labels_font = ("Times New Roman", 20, "bold")
        entry_font = ("Times New Roman", 20)

        tk.Label(self.root,
            text="Date (YYYY-MM-DD):",
            font=labels_font,
            background="white",
            foreground="black"
        ).place(x=300, y=250)
        # Entry (input box)
        self.date_entry = tk.Entry(
        self.root,
        font=entry_font,
        width=25,
        bg="white",
        fg="black",
        relief="ridge",
        borderwidth=3,
        highlightbackground="#ccc",
        highlightthickness=0
        )
        self.date_entry.place(x=620, y=250)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        tk.Label(self.root, text="Amount:", font=labels_font, background="white", foreground="black").place(x=300, y=320)
        self.amount_entry = tk.Entry(self.root, font=entry_font, background="white", foreground="black", width=25)
        self.amount_entry.place(x=620, y=320)

        tk.Label(self.root, text="Category:", font=labels_font, background="white", foreground="black").place(x=300, y=390)
        self.category_entry = tk.Entry(self.root, font=entry_font, background="white", foreground="black", width=25)
        self.category_entry.place(x=620, y=390)

        tk.Label(self.root, text="Type (Expense/Income):", font=labels_font, background="white", foreground="black").place(x=300, y=460)
        self.type_entry = tk.Entry(self.root, font=entry_font, background="white", foreground="black", width=25)
        self.type_entry.place(x=620, y=460)
        save_button = tk.Button(self.root, text="Save",
                                font=("Times New Roman", 20, "bold"),
                                bg="white", fg="black",
                                width=10, height=2,
                                borderwidth=0, relief="ridge",
                                highlightbackground="#ccc", highlightthickness=0,
                                command=self.save_transaction)
        save_button.place(x=620, y=560)

        back_button = tk.Button(self.root, text="Back",
                                font=("Times New Roman", 20, "bold"),
                                bg="white", fg="black",
                                width=10, height=2,
                                borderwidth=0, relief="ridge",
                                highlightbackground="#ccc", highlightthickness=0,
                                command=self.create_home)
        back_button.place(x=360, y=560)

    def save_transaction(self):
        """
           Saves a transaction after validating input fields. Ensures amount is a float,
           date is in YYYY-MM-DD format, and type is either 'Income' or 'Expense'.

           Shows appropriate message boxes for success or failure.
           """
        # TODO Come back and handle exceptions like invalid input and Valueerror for the amount.
        amount = self.amount_entry.get()
        type_ = self.type_entry.get().strip().capitalize()
        date = self.date_entry.get().strip()
        category = self.category_entry.get().strip().capitalize()

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be a positive number")
            date = datetime.strptime(date, "%Y-%m-%d").date()

            if type_ not in ["Expense", "Income"]:
                raise ValueError("Invalid Type entered, transaction type must be 'Income' or 'Expense'.")

            success, msg = add_transaction(self.user.id, amount, type_, date, category)
            if success:
                messagebox.showinfo("Success", msg)
                self.create_home()
            else:
                messagebox.showerror("Error", msg)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def create_summary(self):
        """
        Displays a summary of expenses in a chart using Matplotlib.

        If transactions are available, a chart is displayed. If there's an error,
        a fallback message is shown.
        """
        self.clear()
        self.set_background("../utils/bg_add_transaction.jpg")

        try:
            for widget in self.root.winfo_children():
                if isinstance(widget, FigureCanvasTkAgg):
                    widget.get_tk_widget().destroy()

            transactions = [
                [txn.id, txn.user_id, txn.amount, txn.type, txn.date, txn.category]
                for txn in get_transactions(self.user.id)
            ]

            fig = plot_expenses(transactions)
            canvas = FigureCanvasTkAgg(fig, master=self.root)
            canvas.draw()
            canvas.get_tk_widget().place(x=100, y=107)

        except Exception as e:
            print("Error in summary screen:", e)
            tk.Label(self.root, text="No transactions have been registered yet", font=("Times New Roman", 30, "bold"),
                     background="white", foreground="light blue").place(relx=0.5, rely=0.5, anchor="center")

        back_button = tk.Button(self.root, text="Back",
                                font=("Times New Roman", 14, "bold"),
                                bg="white", fg="black",
                                width=12, height=3,
                                borderwidth=0, relief="ridge",
                                highlightbackground="#ccc", highlightthickness=2,
                                command=self.create_home)
        back_button.place(x=500, y=620)

