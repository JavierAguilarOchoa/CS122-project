import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import add_transaction, get_transactions
from plots import plot_expenses
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

class BudgetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BudgetBuddy")
        self.root.geometry("1100x700")
        self.user = "default"

        self.set_background("bg_with_title_text.png")
        self.create_welcome()

    def set_background(self, image_path):
        self.bg_image = Image.open(image_path)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def restart_app(self):
        self.__init__(self.root)

    def create_welcome(self):
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
            command=self.create_add_transaction
        )
        start_button.place(x=425, y=500)

    def create_home(self):
        self.clear()
        ttk.Label(self.root, text="Transaction Successfully Saved!!!", font=("Times New Roman", 30, "bold"), background="white").place(x=320, y=180)

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
        self.set_background("bg_add_transaction.jpg")
        self.clear()
        ttk.Label(self.root, text="Add New Transaction", font=("Times New Roman", 30, "bold"), background="white").place(x=400, y=160)

        labels_font = ("Times New Roman", 20, "bold")
        entry_font = ("Times New Roman", 20)

        ttk.Label(self.root,
            text="Date (YYYY-MM-DD):",
            font=labels_font,
            background="white",
            #foreground="black"  # Make sure text is black
        ).place(x=300, y=250)

        # Entry (input box)
        self.date_entry = tk.Entry(
        self.root,
        font=entry_font,
        width=25,
        bg="white",     # Input box background color
        fg="black",     # Input text color
        relief="ridge",
        borderwidth=3,
        highlightbackground="#ccc",
        highlightthickness=0
        )
        self.date_entry.place(x=620, y=250)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        ttk.Label(self.root, text="Amount:", font=labels_font, background="white").place(x=300, y=320)
        self.amount_entry = ttk.Entry(self.root, font=entry_font, width=25)
        self.amount_entry.place(x=620, y=320)

        ttk.Label(self.root, text="Category:", font=labels_font, background="white").place(x=300, y=390)
        self.category_entry = ttk.Entry(self.root, font=entry_font, width=25)
        self.category_entry.place(x=620, y=390)

        ttk.Label(self.root, text="Type (Expense/Income):", font=labels_font, background="white").place(x=300, y=460)
        self.type_entry = ttk.Entry(self.root, font=entry_font, width=25)
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
                                command=self.restart_app)
        back_button.place(x=360, y=560)

    def save_transaction(self):
        date = self.date_entry.get()
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        type_ = self.type_entry.get().capitalize()

        try:
            amount = float(amount)
            datetime.strptime(date, "%Y-%m-%d")
            if type_ not in ["Expense", "Income"]:
                raise ValueError("Invalid Type")
            add_transaction(self.user, date, amount, category, type_)
            messagebox.showinfo("Success", "Transaction added!")
            self.create_home()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def create_summary(self):
        self.clear()
        transactions = get_transactions(self.user)
        fig = plot_expenses(transactions)

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().place(x=300, y=120)

        back_button = tk.Button(self.root, text="Back",
                                font=("Times New Roman", 20, "bold"),
                                bg="white", fg="black",
                                width=15, height=2,
                                borderwidth=0, relief="ridge",
                                highlightbackground="#ccc", highlightthickness=2,
                                command=self.create_home)
        back_button.place(x=500, y=600)
