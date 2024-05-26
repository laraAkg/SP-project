"""This script creates the tables in the SQLite database for the user project.
It also contains functions to interact with the 'Users' table in the user database."""
import sqlite3
from user import User

def create_tables_for_user_db(connection):
    """
    Creates the 'Users' table in the user database if it doesn't exist.

    Args:
        connection (sqlite3.Connection): The connection to the user database.

    Returns:
        None
    """
    try:
        c = connection.cursor()
        query = '''CREATE TABLE IF NOT EXISTS Users (
                            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            score INTEGER DEFAULT 0)'''
        c.execute(query)
    except sqlite3.Error as e:
        print("SQLite Error:", e)


def check_username_exists(connection, username):
    """
    Checks if a username exists in the 'Users' table.

    Args:
        connection (sqlite3.Connection): The connection to the user database.
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


def set_user_score(connection, username, score):
    """
    Sets the score for a user in the 'Users' table.

    Args:
        connection (sqlite3.Connection): The connection to the user database.
        username (str): The username of the user.
        score (int): The score to set.

    Returns:
        None
    """
    try:
        c = connection.cursor()
        c.execute("INSERT INTO Users (name, score) VALUES (?, ?)",
                  (username, score))
        connection.commit()
        print("Score updated successfully!")
    except sqlite3.Error as e:
        print("SQLite Error:", e)


def get_score_by_username(connection, username):
    """
    Retrieves the score and rank for a user from the 'Users' table.

    Args:
        connection (sqlite3.Connection): The connection to the user database.
        username (str): The username of the user.

    Returns:
        User or None: The User object containing the score and rank if the user exists
        None otherwise.
    """
    try:
        c = connection.cursor()
        c.execute("SELECT score FROM Users WHERE name = ?", (username,))
        result = c.fetchone()
        if result is not None:
            score = result[0]
            rank = 0
            user = User(rank, username, score)
            return user
        return None
    except sqlite3.Error as e:
        print("SQLite Error:", e)
        return None


def get_top_ten_score(connection):
    """
    Retrieves the top ten scores from the 'Users' table.

    Args:
        connection (sqlite3.Connection): The connection to the user database.

    Returns:
        list: A list of User objects representing the top ten scores.
    """
    try:
        c = connection.cursor()
        c.execute("SELECT name, score FROM Users ORDER BY score DESC LIMIT 10")
        results = c.fetchall()
        top_scores = []
        for result in results:
            username = result[0]
            score = result[1]
            rank = 0
            user = User(rank, username, score)
            top_scores.append(user)
        return top_scores
    except sqlite3.Error as e:
        print("SQLite Error:", e)
        return []


def get_rank_for_username(connection, username):
    """
    Retrieves the rank of a user based on their score from the 'Users' table.

    Args:
        connection (sqlite3.Connection): The connection to the user database.
        username (str): The username of the user.

    Returns:
        int or None: The rank of the user if they exist, None otherwise.
    """
    try:
        c = connection.cursor()
        c.execute(
            "SELECT COUNT(*) FROM Users WHERE score > (SELECT score FROM Users WHERE name = ?)",
            (username,
             ))
        result = c.fetchone()
        if result is not None:
            rank = result[0] + 1
            return rank
        return None
    except sqlite3.Error as e:
        print("SQLite Error:", e)
        return None
