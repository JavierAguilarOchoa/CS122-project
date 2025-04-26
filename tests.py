import unittest
from database import add_transaction, get_transactions

class TestBudgetBuddy(unittest.TestCase):
    def test_add_and_get_transaction(self):
        user = "testuser"
        add_transaction(user, "2024-04-24", 100, "Food", "Expense")
        transactions = get_transactions(user)
        self.assertTrue(any(t[4] == "Food" for t in transactions))

if __name__ == "__main__":
    unittest.main()
