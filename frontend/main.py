# Launches the app
# TODO Include proper documentation in the form of docstrings for classes, functions, and methods.
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from auth import launch

def main():
    print('Program started')
    launch()
    print('program exited')

if __name__ == "__main__":
    main()