"""Main entry point for the BudgetBuddy application"""
from auth import launch

def main():
    """
    Starts the BudgetBuddy application.

    This function prints a startup message, launches the authentication UI,
    and prints an exit message after the authentication window is closed.
    """
    print('Program started')
    launch()
    print('program exited')

if __name__ == "__main__":
    main()