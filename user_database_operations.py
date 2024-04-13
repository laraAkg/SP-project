"This module contains functions to interact with the SQLite database."
import sqlite3

def insert_user(database_name, name, email):
    """
    Inserts a new user into the 'user' table of the SQLite database.

    Args:
        database_name (str): The name of the SQLite database.
        name (str): The name of the user.
        email (str): The email address of the user.
    """
    try:
        with sqlite3.connect("database/"+database_name) as conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO Users (name, email) VALUES (?, ?)", (name, email))
            conn.commit()
    except sqlite3.Error as e:
        print("SQLite Error:", e)

def print_users(database_name):
    """
    Prints all the users in the 'user' table of the SQLite database.

    Args:
        database_name (str): The name of the SQLite database.
    """
    try:
        with sqlite3.connect("database/"+database_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Users")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
    except sqlite3.Error as e:
        print("SQLite Error:", e)


def check_email_exists(database_name, email):
    """
    Checks if the email exists in the Users table of the specified database.

    Args:
        database_name (str): The name of the SQLite database.
        email (str): The email address to check.

    Returns:
        bool: True if the email exists, False otherwise.
    """
    try:
        with sqlite3.connect("database/"+database_name) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM Users WHERE email = ?", (email,))
            result = c.fetchone()
            return result is not None
    except sqlite3.Error as e:
        print("SQLite Error:", e)
        return False
