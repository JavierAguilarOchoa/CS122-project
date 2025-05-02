# Handles login, registration, user selection
#TODO add password functionalities.(Might have to update user table to include a password field)

import tkinter as tk
from tkinter import simpledialog, messagebox
from backend.database import add_user, get_users, Session, User
from gui import BudgetApp

# --------------------Login or create account--------------------

#-----------Launches authorization and opens app once user logs in or creates account-----------
def launch(): # TODO make it nice and add interface to this. Add a main page with buttons to either log or create new user.
    try:
        root = tk.Tk()
        root.withdraw()

        choice = prompt(root) # Prompt for login or register
        if choice == "yes":
            user = user_login(root)
        else:
            user = prompt_new_user(root)

        if not user:
            messagebox.showerror("Error", "Could not log in or create user.", parent=root)
            return

        root.deiconify()
        app = BudgetApp(root, logged_in_user=user)
        root.mainloop()
    except Exception as e:
        return f"Error {e}"


def get_user_by_id(user_id):
    with Session() as session:
        return session.query(User).filter(User.id == user_id).first()

def prompt(root):
    return messagebox.askquestion("Welcome", "Do you want to log in?\n(Click 'No' to create a new user)", parent=root)

def user_login(root): #TODO might want to add password here and make sure it is right.
    user_id = simpledialog.askinteger("Login", "Enter your user ID: ", parent=root)
    return get_user_by_id(user_id)

def prompt_new_user(root):
    name = simpledialog.askstring("New User", "Enter your name", parent=root)
    if name is None:
        return None
    success, msg = add_user(name, 0)
    if not success:
        messagebox.showerror("Error", msg, parent=root)
        return None
    users = get_users()
    for user in users:
        if user.name == name:
            return user
    return None

