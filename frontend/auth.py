# Handles login, registration, user selection
import tkinter as tk
from tkinter import simpledialog, messagebox
from backend.database import add_user, get_users, Session, User, verify_login
from gui import BudgetApp
from PIL import Image, ImageTk

# --------------------Login or create account--------------------

#-----------Launches authorization and opens app once user logs in or creates account-----------
def launch():
    root = tk.Tk()
    root.withdraw()

    def on_login():
        login_window.destroy()
        show_login_form(root)

    def on_register():
        login_window.destroy()
        show_register_form(root)

    login_window = tk.Toplevel(root)
    login_window.title("Welcome to BudgetBuddy")
    login_window.geometry("400x300")
    login_window.resizable(False, False)

    # ----------- Background Image -----------
    bg_image = Image.open("../utils/login_background.jpg")
    bg_image = bg_image.resize((400, 300))
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(login_window, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # ----------- Foreground Frame with Buttons -----------
    content_frame = tk.Frame(login_window, bg="white", bd=0)
    content_frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(content_frame, text="Welcome to BudgetBuddy", font=("Times New Roman", 16, "bold"), fg="black", bg="white").pack(pady=10)
    tk.Button(content_frame, text="Login", font=("Times New Roman", 14), width=20, command=on_login).pack(pady=5)
    tk.Button(content_frame, text="Create New User", font=("Times New Roman", 14), width=20, command=on_register).pack(pady=5)

    login_window.protocol("WM_DELETE_WINDOW", root.destroy)
    login_window.mainloop()

def get_user_by_id(user_id):
    with Session() as session:
        return session.query(User).filter(User.id == user_id).first()

def prompt(root):
    return messagebox.askquestion("Welcome", "Do you want to log in?\n(Click 'No' to create a new user)", parent=root)

def show_login_form(root):
    login_form = tk.Toplevel(root)
    login_form.title("Login")
    login_form.geometry("400x250")
    login_form.resizable(False, False)

    window_background(login_form)
    login_form.resizable(True, True)

    tk.Label(login_form, text="User ID:", font=("Times New Roman", 12)).pack(pady=5)
    user_id_entry = tk.Entry(login_form, font=("Times New Roman", 12))
    user_id_entry.pack(pady=5)

    tk.Label(login_form, text="Password:", font=("Times New Roman", 12)).pack(pady=5)
    password_entry = tk.Entry(login_form, show='*', font=("Times New Roman", 12))
    password_entry.pack(pady=5)

    def attempt_login():
        user_id = user_id_entry.get()
        password = password_entry.get()

        try:
            user_id = int(user_id)
            success, msg = verify_login(user_id, password)
            if success:
                user = get_user_by_id(user_id)
                login_form.destroy()
                root.deiconify()
                BudgetApp(root, logged_in_user=user)
            else:
                messagebox.showerror("Login Failed", msg, parent=login_form)
        except ValueError:
            messagebox.showerror("Invalid Input", "User ID must be a number.", parent=login_form)

    tk.Button(login_form, text="Login", font=("Times New Roman", 12), command=attempt_login).pack(pady=15)

def show_register_form(root):
    register_form = tk.Toplevel(root)
    register_form.title("Create Account")
    register_form.geometry("400x300")
    register_form.resizable(False, False)

    window_background(register_form)
    register_form.resizable(True, True)

    tk.Label(register_form, text="Name:", font=("Times New Roman", 12)).pack(pady=5)
    name_entry = tk.Entry(register_form, font=("Times New Roman", 12))
    name_entry.pack(pady=5)

    tk.Label(register_form, text="Password:", font=("Times New Roman", 12)).pack(pady=5)
    password_entry = tk.Entry(register_form, show='*', font=("Times New Roman", 12))
    password_entry.pack(pady=5)

    def attempt_register():
        name = name_entry.get()
        password = password_entry.get()
        if not name or not password:
            messagebox.showerror("Error", "All fields are required.", parent=register_form)
            return

        success, msg = add_user(name, 0, password)
        if success:
            users = get_users()
            for user in users:
                if user.name == name:
                    register_form.destroy()
                    root.deiconify()
                    BudgetApp(root, logged_in_user=user)
                    return
        else:
            messagebox.showerror("Error", msg, parent=register_form)

    tk.Button(register_form, text="Register", font=("Times New Roman", 12), command=attempt_register).pack(pady=15)



def window_background(form):
    bg_image = Image.open("../utils/login_background.jpg")
    bg_photo = ImageTk.PhotoImage(bg_image)
    form.bg_photo = bg_photo
    bg_label = tk.Label(form, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
