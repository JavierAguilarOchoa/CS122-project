# Handles login, registration, user selection
import tkinter as tk
from tkinter import simpledialog, messagebox
from backend.database import add_user, get_users, Session, User, verify_login
from gui import BudgetApp
from PIL import Image, ImageTk

# --------------------Login or create account--------------------

#-----------Launches authorization and opens app once user logs in or creates account-----------
def launch():
    """
     Launches the initial authentication window for the BudgetBuddy application.

     Presents users with options to either log in or register a new account.
     Upon successful authentication, launches the main application!
     """
    root = tk.Tk()
    root.withdraw()

    def on_login():
        """
        This is a callback function that is called when the user logs in

        Closes the login window and opens the login form to allow users to input their credentials.
        """
        login_window.destroy()
        show_login_form(root)

    def on_register():
        """
        This is a callback function that is called when the user wants to register (Creates new user)

        Closes the welcome/login window and opens the registration form to allow users to create a new account.
        """
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
    """
      Retrieves a user from the database by their user ID.

      Args:
          user_id (int): The ID of the user to retrieve.

      Returns:
          User: SQLAlchemy User object if found, else None.
      """
    with Session() as session:
        return session.query(User).filter(User.id == user_id).first()

def prompt(root):
    """
     Displays a dialog asking the user whether they want to log in or register.

     Args:
         root (tk.Tk): The parent Tkinter window.

     Returns:
         str: 'yes' if the user wants to log in, 'no' otherwise.
     """
    return messagebox.askquestion("Welcome", "Do you want to log in?\n(Click 'No' to create a new user)", parent=root)

def show_login_form(root):
    """
      Opens a login window where users enter their user ID and password.

      On successful login, launches the BudgetApp GUI for the logged-in user.

      Args:
          root (tk.Tk): The main Tkinter root window.
      """
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
        """
            Handles the login process when the "Login" button is clicked.

            Retrieves the user ID and password from the input fields, validates that the user ID is an integer,
            and verifies credentials using the `verify_login` function. If the login is successful,
            it retrieves the corresponding user object, closes the login form, and opens the BudgetApp interface.

            Displays appropriate error messages for invalid credentials or incorrect input types.
            """
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
    """
       Opens a registration window where users can create a new account.

       Prompts for name and password. On success, shows the user ID and launches BudgetApp.

       Args:
           root (tk.Tk): The main Tkinter root window.
       """
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
        """
            Handles user registration logic when the "Register" button is clicked.

            Validates the input fields (name and password), creates a new user with an initial balance of 0,
            and retrieves the user ID upon successful registration. If registration succeeds,
            it displays the user ID in a messagebox and launches the BudgetApp interface.

            Displays error messages for missing input fields or failed registration attempts.
            """
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
                    messagebox.showinfo("Registration Successful",
                                        f"Your account has been created.\nYour User ID is: {user.id}\nPlease remember this ID and your password to log in next time. Thank you!",
                                        parent=register_form)
                    register_form.destroy()
                    root.deiconify()
                    BudgetApp(root, logged_in_user=user)
                    return
        else:
            messagebox.showerror("Error", msg, parent=register_form)

    tk.Button(register_form, text="Register", font=("Times New Roman", 12), command=attempt_register).pack(pady=15)


def window_background(form):
    """
        Applies a background image to a given Tkinter form.

        Args:
            form (tk.Toplevel): The window to set the background for.

        Note:
            The image must exist at "../utils/login_background.jpg".
        """
    bg_image = Image.open("../utils/login_background.jpg")
    bg_photo = ImageTk.PhotoImage(bg_image)
    form.bg_photo = bg_photo
    bg_label = tk.Label(form, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
