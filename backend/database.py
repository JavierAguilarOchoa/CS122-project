# TODO Include proper documentation in the form of docstrings for classes, functions, and methods.

from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import datetime

# ----------Database tables----------
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    money = Column(Float, nullable=False)
    password = Column(String, nullable=False)

    def __repr__(self):
        return f"<User(id='{self.id}', ' name='{self.name}', ' money={self.money}')>"

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True) # Transaction id
    user_id = Column(Integer, ForeignKey('users.id')) # This is the transactions user id(The id of who made the transaction)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False) # 'income' or 'expense'
    date = Column(Date, default=datetime.date.today(), nullable=False)

    user = relationship("User", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction(id='{self.id}', ' amount={self.amount}, type={self.type})>"

User.transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")

engine = create_engine('sqlite:///budgetBuddy_data.db')
Base.metadata.create_all(engine) # Creating the tables
Session = sessionmaker(bind=engine)


# ----------Database functions for user----------
def add_user(user_name, user_money, login_password):
    # INSERT INTO
    with Session() as session:
        try:
            new_user = User(name=user_name, money=user_money, password = login_password) # Money might start from 0 or user_money
            session.add(new_user)
            session.commit()
            return True, f"User ({new_user.name},{new_user.id}) added Successfully!"
        except Exception as e:
            return False, f"Add user failed, due to {e}"

def update_user(user_id, user_name, user_money): # Maybe we just want to use this to update the money
    # UPDATE
    with Session() as session:
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                return False, "User not found!"
            user.name = user_name
            user.money = user_money
            session.commit()
            return True, f"User ({user.name},{user.id}) updated successfully!"
        except Exception as e:
            return False, f"Update user failed, due to {e}"

def delete_user(user_id):
    # DELETE
    with Session() as session:
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                return False, f"User:{user_id} does NOT exist!"
            session.delete(user)
            session.commit()
            return True, f"User ({user.name},{user.id}) deleted successfully!"
        except Exception as e:
            return False, f"Delete user failed, due to {e}"

def get_users():
    with Session() as session:
        users = session.query(User).all()
        for user in users:
            print(user)
        return users

def verify_login(user_id, password):
    with Session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if user and user.password == password:
            return True, f"Login successful, welcome back {user.name}!"
        return False, f"Invalid user ID or password."


# ----------Database functions for transactions----------(Might just want the add/look over this as project implementation continues)
def add_transaction(trans_user_id, new_amount, trans_type, trans_date): #TODO make sure that trans_user_id does not have to be inputted from a user's pov(Under the hood)
    # INSERT INTO
    with Session() as session:
        try:
            new_trans = Transaction(
                user_id=trans_user_id,
                amount = new_amount,
                type = trans_type,
                date = trans_date
            )
            session.add(new_trans)
            session.commit()
            return True, f"Transaction added Successfully! ID:  {new_trans.id}"
        except Exception as e:
            return False, f"Transaction failed due to {e}"

def delete_transaction(trans_id, trans_user_id): #TODO make sure that trans_user_id does not have to be inputted from a user's pov(Under the hood) Might not need this method
    # DELETE
    with Session() as session:
        try:
            transaction = session.query(Transaction).filter(Transaction.id == trans_id, Transaction.user_id == trans_user_id).first()
            if not transaction:
                return False, "Transaction does NOT exist!"
            session.delete(transaction)
            session.commit()
            return True, f"Transaction {trans_id} deleted successfully!"
        except Exception as e:
            return False, f"Delete transaction failed, due to {e}"

# Gets a users transactions
def get_transactions(user_id):
    with Session() as session:
        transactions = session.query(Transaction).filter(Transaction.user_id == user_id).all()
        return transactions