"This module contains functions for general database operations."
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


def execute_query(database_file, query):
    """
    Executes the given SQL query on the specified database file.

    Args:
        database_file (str): The path to the SQLite database file.
        query (str): The SQL query to execute.

    Returns:
        None

    Raises:
        sqlite3.Error: If there is an error executing the query.

    """
    conn = sqlite3.connect(database_file)
    c = conn.cursor()
    try:
        c.execute(query)
        conn.commit()
    except sqlite3.Error as e:
        print("Error executing query:", e)
    finally:
        conn.close()
        