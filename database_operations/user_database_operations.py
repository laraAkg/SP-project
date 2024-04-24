"This module contains functions to interact with the SQLite database."
import sqlite3


def create_tables_for_user_db(connection):
    """
    Creates a new SQLite database and executes the given query.

    Parameters:
    - connection: The database connection object.
    - query (str): The SQL query to be executed.

    Returns:
    None
    """
    try:
        c = connection.cursor()
        query = '''CREATE TABLE IF NOT EXISTS Users (
                            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT UNIQUE NOT NULL,
                            score INTEGER DEFAULT 0)'''
        c.execute(query)
    except sqlite3.Error as e:
        print("SQLite Error:", e)


def insert_user(connection, name):
    """
    Inserts a new user into the 'user' table of the SQLite database.

    Args:
        database_name (str): The name of the SQLite database.
        name (str): The name of the user.
    """
    try:
        c = connection.cursor()
        c.execute("INSERT INTO Users (name) VALUES (?)", (name,))
        connection.commit()
        print("User inserted successfully!")
    except sqlite3.Error as e:
        print("SQLite Error:", e)

def check_username_exists(connection, username):
    """
    Checks if the username exists in the Users table of the specified database.

    Args:
        database_name (str): The name of the SQLite database.
        username (str): The username to check.

    Returns:
        bool: True if the username exists, False otherwise.
    """
    try:
        c = connection.cursor()
        c.execute("SELECT * FROM Users WHERE name = ?", (username,))
        result = c.fetchone()
        return result is not None
    except sqlite3.Error as e:
        print("SQLite Error:", e)
        return False


def get_user_score(connection, username):
    """
    Retrieves the score of the specified user from the Users table.

    Args:
        database_name (str): The name of the SQLite database.
        username (str): The username to retrieve the score for.

    Returns:
        int: The score of the user.
    """
    try:
        c = connection.cursor()
        c.execute("SELECT score FROM Users WHERE name = ?", (username,))
        result = c.fetchone()
        return result
    except sqlite3.Error as e:
        print("SQLite Error:", e)
        return None

def set_user_score(connection, username, score ):
    """
    Sets the score of the specified user in the Users table.

    Args:
        database_name (str): The name of the SQLite database.
        username (str): The username to set the score for.
        score (int): The score to set for the user.
    """
    try:
        c = connection.cursor()
        c.execute("INSERT INTO Users (name, score) VALUES (?, ?)", (username, score))
        connection.commit()
        print("Score updated successfully!")
    except sqlite3.Error as e:
        print("SQLite Error:", e)
