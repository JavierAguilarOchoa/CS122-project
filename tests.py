import unittest
from backend.database import Base, User, Transaction, get_transactions, add_user, add_transaction, get_transactions, get_users
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import date

class TestBudgetBuddy(unittest.TestCase):
    def setUp(self):
        """
              Set up an in-memory SQLite database and a test session before each test.
              """
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        # Helps us use this session instead of global DB
        import backend.database as db
        db.Session = self.Session  # override session factory

    def test_add_user(self):
        """
        Test that a new user can be successfully added to the database.
        """
        success, msg = add_user("testuser", 0, "pw")
        self.assertTrue(success)
        self.assertIn("testuser", msg)

        # Check directly using session
        fetched_user = self.session.query(User).filter_by(name="testuser").first()
        self.assertIsNotNone(fetched_user)
        self.assertEqual(fetched_user.name, "testuser")

    def test_add_transaction(self):
        """
        Test that a transaction can be successfully added to the database.
        """
        success, _ = add_user("testy", 1000, "pass")
        self.assertTrue(success)
        user = self.session.query(User).filter_by(name="testy").first()
        self.assertIsNotNone(user)

        success, msg = add_transaction(user.id, 50.0, "Expense", date.today(), "Food")
        self.assertTrue(success)
        self.assertIn("added", msg)

if __name__ == '__main__':
    unittest.main()