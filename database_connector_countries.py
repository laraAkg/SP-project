"""
This module provides functions to interact with a SQLite database. 
It includes functions to create a new database and table, 
and to insert a new user into the 'user' table.
"""

import sqlite3
import random


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


def insert_countries_data_to_db(country_data,index):
    """
    Creates a table in the specified database and inserts country data into it.

    Args:
        database_name (str): The name of the database.
        country_data (dict): A dictionary containing the country data.

    Returns:
        None
    """

    try:
        insert_query = '''
        INSERT OR IGNORE INTO Countries (id_country,official_name, code, area, population)
        VALUES (?,?, ?, ?, ?)
        '''
        with sqlite3.connect("database/countries.db") as conn:
            c = conn.cursor()
            c.execute(insert_query, (
            index,
            country_data['name'],
            country_data['code'],
            country_data['area'],
            country_data['population']
            ))
            conn.commit()
            if c.rowcount > 0:
                print("Country data inserted successfully!")
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


def get_country_entry_by_random_number():
    """
    Retrieves a random country entry from the database.

    Returns:
        A tuple containing the country data.
    """
    conn = sqlite3.connect("database/countries.db")
    cursor = conn.cursor()
    try:
        select_query = '''SELECT * FROM Countries WHERE id = ?'''
        random_count = random.randint(0, get_countries_count())
        cursor.execute(select_query, (random_count,))
        row = cursor.fetchone()
        print("Random country entry:", row)
        return row
    finally:
        conn.close()


def insert_country_data_currencies(currencies):
    """
    Inserts the given currency data into the Currencies table in the currencies.db database.

    Args:
        currency (str): The name of the currency to be inserted.

    Returns:
        None
    """
    conn = sqlite3.connect("database/countries.db")
    c = conn.cursor()
    list_id = []
    try:
        query = '''INSERT OR IGNORE INTO Currencies (name, symbol) VALUES (?, ?)'''
        for _, symbol in currencies.items():
            name = symbol['name']
            symbol = symbol['symbol']
            c.execute(query, (name, symbol,))
            list_id.append( c.lastrowid)
        conn.commit()
        print("Currency data inserted successfully!")
    except sqlite3.Error as e:
        print("SQLite Error:", e)

    except AttributeError as e:
        print("Symbol has a problem:", e)
    finally:
        conn.close()
    return list_id


def insert_country_data_one_param(data, query):
    """
    Insert country data into the database using a single parameterized query.

    Args:
        data (list): A list of data to be inserted into the database.
        query (str): The parameterized query to insert the data.

    Returns:
        None

    Raises:
        sqlite3.Error: If there is an error executing the query.

    """
    conn = sqlite3.connect("database/countries.db")
    c = conn.cursor()
    list_id = []
    try:
        for d in data:
            c.execute(query, (d,))
            list_id.append(c.lastrowid)
        conn.commit()
        print("Data inserted successfully!")
    except sqlite3.Error as e:
        print("SQLite Error:", e)
    finally:
        conn.close()
    return list_id

def insert_country_data_language(data):
    """
    Insert country data into the database using a single parameterized query.

    Args:
        data (list): A list of data to be inserted into the database.

    Returns:
        list: A list of inserted language IDs.

    Raises:
        sqlite3.Error: If there is an error executing the query.

    """
    conn = sqlite3.connect("database/countries.db")
    c = conn.cursor()
    list_id = []
    try:
        for _,language in data.items():
            language_query = "SELECT id_language FROM Languages WHERE language = ?"
            c.execute(language_query, (language,))
            result = c.fetchone()
            if result is not None:
                language_id = result[0]
            else:
                insert_query = "INSERT OR IGNORE INTO Languages (language) VALUES (?)"
                c.execute(insert_query, (language,))
                language_id = c.lastrowid
                print("Data inserted successfully!")
            list_id.append(language_id)
        conn.commit()
    except sqlite3.Error as e:
        print("SQLite Error:", e)
    finally:
        conn.close()
    return list_id


def get_countries_count():
    """
    Retrieves the number of countries in the specified database.

    Returns:
        The number of countries in the database.
    """
    conn = sqlite3.connect("database/countries.db")
    cursor = conn.cursor()
    try:
        select_query = '''SELECT COUNT(*) FROM Countries'''
        cursor.execute(select_query)
        count = cursor.fetchone()[0]
        print("Number of countries in the database:", count)
        return count
    finally:
        conn.close()

def insert_into_zwischentabelle(country_id,second_id,query):
    """
    Inserts data into the Zwischentabelle table in the countries.db database.
    """
    conn = sqlite3.connect("database/countries.db")
    cursor = conn.cursor()
    try:
        for sec_id in second_id:
            cursor.execute(query, (country_id, sec_id))
            conn.commit()
    except sqlite3.Error as e:
        print("SQLite Error:", e)
    finally:
        conn.close()


def print_country_data_language():
    """
    Prints all the country data in the 'Countries' table of the SQLite database.
    """
    conn = sqlite3.connect("database/countries.db")
    cursor = conn.cursor()
    try:
        select_query = '''
        SELECT Countries.official_name, GROUP_CONCAT(Languages.language, ', ') 
        FROM Countries 
        JOIN Countries_Languages ON Countries.id_country = Countries_Languages.id_country 
        JOIN Languages ON Countries_Languages.id_language = Languages.id_language 
        GROUP BY Countries.official_name
        '''
        cursor.execute(select_query)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    finally:
        conn.close()

def print_countries():
    """
    Prints all the country data in the 'Countries' table of the SQLite database.
    """
    conn = sqlite3.connect("database/countries.db")
    cursor = conn.cursor()
    try:
        select_query = '''SELECT * FROM Countries'''
        cursor.execute(select_query)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    finally:
        conn.close()

def print_languages():
    """
    Prints all the language data in the 'Languages' table of the SQLite database.
    """
    conn = sqlite3.connect("database/countries.db")
    cursor = conn.cursor()
    try:
        select_query = '''SELECT * FROM Languages'''
        cursor.execute(select_query)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    finally:
        conn.close()
# TODO - improve insert func to one big
