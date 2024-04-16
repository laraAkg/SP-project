"This module contains functions to interact with the SQLite database."
import sqlite3

def insert_user(name):
    """
    Inserts a new user into the 'user' table of the SQLite database.

    Args:
        database_name (str): The name of the SQLite database.
        name (str): The name of the user.
    """
    try:
        with sqlite3.connect("database/users.db") as conn:
            c = conn.cursor()
            c.execute("INSERT INTO Users (name) VALUES (?)", (name,))
            conn.commit()
            print("User inserted successfully!")
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


def check_username_exists(username):
    """
    Checks if the username exists in the Users table of the specified database.

    Args:
        database_name (str): The name of the SQLite database.
        username (str): The username to check.

    Returns:
        bool: True if the username exists, False otherwise.
    """
    try:
        with sqlite3.connect("database/users.db") as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM Users WHERE name = ?", (username,))
            result = c.fetchone()
            return result is not None
    except sqlite3.Error as e:
        print("SQLite Error:", e)
        return False
