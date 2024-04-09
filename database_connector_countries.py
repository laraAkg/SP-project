"""
This module provides functions to interact with a SQLite database. 
It includes functions to create a new database and table, 
and to insert a new user into the 'user' table.
"""

import sqlite3


def create_database(database_name, query):
    """
    Creates a new SQLite database if it doesn't exist and creates a 'user' table in it.

    Args:
        database_name (str): The name of the SQLite database.
        query (str): The SQL query to create the 'user' table.
    """
    try:
        with sqlite3.connect("database/"+database_name) as conn:
            c = conn.cursor()
            c.execute(query)
    except sqlite3.Error as e:
        print("SQLite Error:", e)


def insert_user(database_name, name, email):
    """
    Inserts a new user into the 'user' table of the SQLite database.

    Args:
        database_name (str): The name of the SQLite database.
        name (str): The name of the user.
        email (str): The email address of the user.
    """
    try:
        with sqlite3.connect(database_name) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM user WHERE email=?", (email,))
            existing_user = c.fetchone()
            if existing_user:
                print(f"Email address '{email}' already exists.")
            else:
                c.execute(
                    "INSERT INTO user (name, email) VALUES (?, ?)", (name, email))
                print(
                    f"User '{name}' with email address '{email}' has been added.")
    except sqlite3.Error as e:
        print("SQLite Error:", e)


def print_users(database_name):
    """
    Prints all the users in the 'user' table of the SQLite database.

    Args:
        database_name (str): The name of the SQLite database.
    """
    try:
        with sqlite3.connect(database_name) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM user")
            users = c.fetchall()

            for user in users:
                print("Name:", user[0])
                print("Email:", user[1])
                print()
    except sqlite3.Error as e:
        print("SQLite Error:", e)


def insert_countries(database_name, country_map):
    """
    Inserts a list of countries into the 'countries' table of the SQLite database.

    Args:
        database_name (str): The name of the SQLite database.
        country_map (list): A list of country names.
    """
    conn = sqlite3.connect("database/"+database_name)
    c = conn.cursor()
    query = '''INSERT INTO Countries (code) VALUES (?)'''
    for country in country_map:
        c.execute(query, (country,))
    conn.commit()
    conn.close()


def show_countries(database_name):
    """
    Retrieves and prints all the countries from the specified database.

    Parameters:
    - database_name (str): The name of the database to connect to.

    Returns:
    None
    """
    conn = sqlite3.connect("database/"+database_name)
    cursor = conn.cursor()

    try:
        select_query = '''SELECT * FROM Countries'''
        cursor.execute(select_query)
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    finally:
        conn.close()


def drop_table(database_name, table_name):
    """
    Drops a table from the specified database.

    Args:
        database_name (str): The name of the database.
        table_name (str): The name of the table to be dropped.

    Returns:
        None
    """
    conn = sqlite3.connect("database/"+database_name)
    c = conn.cursor()
    query = f'''DROP TABLE {table_name}'''
    c.execute(query)
    conn.commit()
    conn.close()
