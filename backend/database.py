from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import datetime
from sqlalchemy.sql.functions import user

# ----------Database tables----------
Base = declarative_base()

class User(Base):
    """Represents user in our budgetBuddy application.

    Attributes:
        id: Unique identifier for user.
        name: Name of the user
        money: Current balance or budget the user has.
        password: Password used for logging into account.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    money = Column(Float, nullable=False)
    password = Column(String, nullable=False)

    def __repr__(self):
        """Return string representation of user."""
        return f"<User(id='{self.id}', ' name='{self.name}', ' money={self.money}')>"

class Transaction(Base):
    """Represents a financial transaction in our budgetBuddy application and splits them based on category of purchase.

    Attributes:
        id: Unique identifier for transaction.
        user_id: Unique identifier for user.
        amount: Amount of the transaction.
        type: Type of transaction(Expense or Income).
        date: Date of transaction.
        category: Category of purchase.
    """
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True) # Transaction id
    user_id = Column(Integer, ForeignKey('users.id')) # This is the transactions user id(The id of who made the transaction)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False) # 'income' or 'expense'
    date = Column(Date, default=datetime.date.today(), nullable=False)
    category = Column(String, nullable=False)

    user = relationship("User", back_populates="transactions")

    def __repr__(self):
        """Return string representation of transaction."""
        return f"<Transaction(id='{self.id}', ' amount={self.amount}, type={self.type})>"

User.transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")

engine = create_engine('sqlite:///budgetBuddy_data.db')
Base.metadata.create_all(engine) # Creating the tables
Session = sessionmaker(bind=engine)


# ----------Database functions for user----------
def add_user(user_name, user_money, login_password):
    """Adds a new user to the database.
    Args:
        user_name: Name of the user.
        user_money: Current balance or budget the user has.
        login_password: Password for the user account.
    """
    # INSERT INTO
    with Session() as session:
        try:
            new_user = User(name=user_name, money=user_money, password = login_password)
            session.add(new_user)
            session.commit()
            return True, f"User ({new_user.name},{new_user.id}) added Successfully!"
        except Exception as e:
            return False, f"Add user failed, due to {e}"

def get_users():
    """
      Retrieves and prints all users from the database.

      Returns:
          list: A list of all User objects in the database.
      """
    with Session() as session:
        users = session.query(User).all()
        for user in users:
            print(user)
        return users

def verify_login(user_id, password):
    """
        Verifies a user's login credentials.

        Args:
            user_id (int): The ID of the user attempting to log in.
            password (str): The password provided by the user.

        Returns:
            tuple: (bool, str) - True and success message if login is valid,
                                 otherwise False and error message.
        """
    with Session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if user and user.password == password:
            return True, f"Login successful, welcome back {user.name}!"
        return False, f"Invalid user ID or password."


# ----------Database functions for transactions----------
def add_transaction(trans_user_id, new_amount, trans_type, trans_date, trans_category):
    """
        Adds a transaction to the database and updates the user's balance.

        Deducts money from the user's balance if it's an 'Expense',
        or adds money if it's an 'Income'.

        Args:
            trans_user_id (int): The ID of the user making the transaction.
            new_amount (float): The amount of the transaction.
            trans_type (str): The type of transaction - 'Income' or 'Expense'.
            trans_date (datetime.date): The date of the transaction.
            trans_category (str): The category of the transaction.

        Returns:
            tuple: (bool, str) - Success flag and a message.
        """
    # INSERT INTO
    with Session() as session:
        try:
            user = session.query(User).filter(User.id == trans_user_id).first()
            if not user:
                return False, f"User:{trans_user_id} does NOT exist!"

            if trans_type == "Expense":
                if user.money < new_amount:
                    return False, "Insufficient money."
                user.money -= new_amount
            elif trans_type == "Income":
                user.money += new_amount
            else:
                return False, "Incorrect trans_type."
            new_trans = Transaction(
                user_id=trans_user_id,
                amount = new_amount,
                type = trans_type,
                date = trans_date,
                category = trans_category
            )
            session.add(new_trans)
            session.commit()
            return True, f"Transaction added Successfully! ID:  {new_trans.id}"
        except Exception as e:
            return False, f"Transaction failed due to {e}"

# Gets a users transactions
def get_transactions(user_id):
    """
        Retrieves all transactions associated with a specific user.

        Args:
            user_id (int): The ID of the user whose transactions to fetch.

        Returns:
            list: A list of Transaction objects, or an empty list if none found.
        """
    with Session() as session:
        transactions = session.query(Transaction).filter(Transaction.user_id == user_id).all()
        return transactions