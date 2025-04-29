#Todo implement test cases & Include proper documentation in the form of docstrings for classes, functions, and methods.
import unittest
from backend.database import add_transaction, get_transactions, add_user, add_transaction, get_transactions, delete_user, get_users
from datetime import datetime

class TestBudgetBuddy(unittest.TestCase):
    def setUp(self):
        success, _ = add_user("TestUser",0)
        self.test_user = [user for user in get_users() if user.name == "TestUser"][-1]

    def tearDown(self):
        delete_user(self.test_user.id)

    def test_add_user(self):
        return

    def test_add_transaction(self):
        return

    def test_add_and_get_transaction(self):
        add_transaction(self.test_user.id, 25, "Income", datetime.today().date())
        transactions = get_transactions(self.test_user.id)
        self.assertTrue(any(t.amount == 25 and t.type == "Income" for t in transactions))


if __name__ == '__main__':
    unittest.main()