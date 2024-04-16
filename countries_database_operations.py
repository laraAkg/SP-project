"""
This module provides functions to interact with a SQLite database. 
It includes functions to create a new database and table, 
and to insert a new user into the 'user' table.
"""

import sqlite3


DATABASE_COUNTRY_FILE_NAME = "database/countries.db"

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
        with sqlite3.connect(DATABASE_COUNTRY_FILE_NAME) as conn:
            c = conn.cursor()
            c.execute(insert_query, (
            index,
            country_data['name'],
            country_data['code'],
            country_data['area'],
            country_data['population']
            ))
            conn.commit()
    except sqlite3.Error as e:
        print("SQLite Error:", e)


def get_countries_count():
    """
    Retrieves the number of countries in the specified database.

    Returns:
        The number of countries in the database.
    """
    conn = sqlite3.connect(DATABASE_COUNTRY_FILE_NAME)
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
    conn = sqlite3.connect(DATABASE_COUNTRY_FILE_NAME)
    cursor = conn.cursor()
    try:
        for sec_id in second_id:
            cursor.execute(query, (country_id, sec_id))
            conn.commit()
    except sqlite3.Error as e:
        print("SQLite Error: ", e)
    finally:
        conn.close()

########################################################################################
# The following functions are used to insert data into the database.

def insert_country_data_language(data):
    """
    Inserts language data into the 'Languages' table in the 'countries.db' database.
    
    Args:
        data (dict): A dictionary containing language data.
        
    Returns:
        list: A list of language IDs that were inserted or already existed in the database.
    """
    conn = sqlite3.connect(DATABASE_COUNTRY_FILE_NAME)
    c = conn.cursor()
    list_id = []
    try:
        for _, language in data.items():
            language_query = "SELECT id_language FROM Languages WHERE language = ?"
            c.execute(language_query, (language,))
            result = c.fetchone()
            if result is not None:
                language_id = result[0]
            else:
                insert_query = "INSERT OR IGNORE INTO Languages (language) VALUES (?)"
                c.execute(insert_query, (language,))
                language_id = c.lastrowid
            list_id.append(language_id)
        conn.commit()
    except sqlite3.Error as e:
        print("SQLite Error:", e)
    finally:
        conn.close()
    return list_id

def insert_country_data_capital(capitals):
    """
    Inserts country data into the database and returns a list of capital IDs.

    Args:
        data (dict): A dictionary containing country data with capital names as values.

    Returns:
        list: A list of capital IDs corresponding to the inserted data.

    Raises:
        sqlite3.Error: If there is an error executing the SQLite queries.

    """
    conn = sqlite3.connect("database/countries.db")
    c = conn.cursor()
    list_id = []
    try:
        for capital in capitals:
            capital_query = "SELECT id_capital FROM Capitals WHERE capital = ?"
            c.execute(capital_query, (capital,))
            result = c.fetchone()
            if result is not None:
                capital_id = result[0]
            else:
                insert_query = "INSERT OR IGNORE INTO Capitals (capital) VALUES (?)"
                c.execute(insert_query, (capital,))
                capital_id = c.lastrowid
            list_id.append(capital_id)
        conn.commit()
    except sqlite3.Error as e:
        print("SQLite Error:", e)
    finally:
        conn.close()
    return list_id

def insert_country_data_continent(data):
    """
    Inserts continent data into the 'Continents' table in the 'countries.db' database.

    Args:
        data (dict): A dictionary containing continent data.

    Returns:
        list: A list of continent IDs that were inserted or already existed in the database.
    """
    conn = sqlite3.connect("database/countries.db")
    c = conn.cursor()
    list_id = []
    try:
        for continent in data:
            continent_query = "SELECT id_continent FROM Continents WHERE continent = ?"
            c.execute(continent_query, (continent,))
            result = c.fetchone()
            if result is not None:
                continent_id = result[0]
            else:
                insert_query = "INSERT OR IGNORE INTO Continents (continent) VALUES (?)"
                c.execute(insert_query, (continent,))
                continent_id = c.lastrowid
            list_id.append(continent_id)
        conn.commit()
    except sqlite3.Error as e:
        print("SQLite Error:", e)
    finally:
        conn.close()
    return list_id

def insert_country_data_borders(borders):
    """
    Inserts border data into the 'Borders' table in the 'countries.db' database.

    Args:
        data (list): A list of border data.

    Returns:
        list: A list of border IDs that were inserted or already existed in the database.
    """
    conn = sqlite3.connect(DATABASE_COUNTRY_FILE_NAME)
    c = conn.cursor()
    list_id = []
    try:
        for border in borders:
            border_query = "SELECT id_border FROM Borders WHERE country_code_short = ?"
            c.execute(border_query, (border,))
            result = c.fetchone()
            if result is not None:
                border_id = result[0]
            else:
                insert_query = "INSERT OR IGNORE INTO Borders (country_code_short) VALUES (?)"
                c.execute(insert_query, (border,))
                border_id = c.lastrowid
            list_id.append(border_id)
        conn.commit()
    except sqlite3.Error as e:
        print("SQLite Error:", e)
    finally:
        conn.close()
    return list_id


def insert_country_data_currencies(currencies):
    """
    Inserts the given currency data into the Currencies table in the currencies.db database.

    Args:
        currency (str): The name of the currency to be inserted.

    Returns:
        None
    """
    conn = sqlite3.connect(DATABASE_COUNTRY_FILE_NAME)
    c = conn.cursor()
    list_id = []
    try:
        for _,currency in currencies.items():
            currency_query = "SELECT id_currency FROM Currencies WHERE name = ?"
            c.execute(currency_query, (currency.get('name'),))
            result = c.fetchone()
            if result is not None:
                currency_id = result[0]
            else:
                insert_query = "INSERT OR IGNORE INTO Currencies (name, symbol) VALUES (?, ?)"
                c.execute(insert_query, (currency.get('name'),currency.get('symbol')))
                currency_id = c.lastrowid
            list_id.append(currency_id)
        conn.commit()
    except sqlite3.Error as e:
        print("SQLite Error:", e)
    finally:
        conn.close()
    return list_id  

########################################################################################
# The following functions are used to retrieve data from the database.

def return_country_data_official_name(country_id):
    """
    Returns the official name of a specific country ID in the 'Countries' table of the SQLite database.

    Args:
        country_id (int): The ID of the country.

    Returns:
        str: The official name of the country.
    """
    conn = sqlite3.connect(DATABASE_COUNTRY_FILE_NAME)
    cursor = conn.cursor()
    try:
        select_query = '''
        SELECT official_name
        FROM Countries 
        WHERE id_country = ?
        '''
        cursor.execute(select_query, (country_id,))
    finally:
        conn.close()


def return_country_data_capital(country_id):
    """
    Returns the capital data for a specific country ID in the 'Countries' table of the SQLite database.

    Args:
        country_id (int): The ID of the country.

    Returns:
        list: A list of capital names.
    """
    conn = sqlite3.connect(DATABASE_COUNTRY_FILE_NAME)
    cursor = conn.cursor()
    try:
        select_query = '''
        SELECT Capitals.capital
        FROM Countries 
        JOIN Countries_Capitals ON Countries.id_country = Countries_Capitals.id_country 
        JOIN Capitals ON Countries_Capitals.id_capital = Capitals.id_capital 
        WHERE Countries.id_country = ?
        '''
        cursor.execute(select_query, (country_id,))
        rows = cursor.fetchall()
        capitals = [row[0] for row in rows]
        return capitals
    finally:
        conn.close()

def return_country_data_continent(country_id):
    """
    Returns the continent data for a specific country ID in the 'Countries' table of the SQLite database.

    Args:
        country_id (int): The ID of the country.

    Returns:
        list: A list of continent names.
    """
    conn = sqlite3.connect(DATABASE_COUNTRY_FILE_NAME)
    cursor = conn.cursor()
    try:
        select_query = '''
        SELECT Continents.continent
        FROM Countries 
        JOIN Countries_Continents ON Countries.id_country = Countries_Continents.id_country 
        JOIN Continents ON Countries_Continents.id_continent = Continents.id_continent 
        WHERE Countries.id_country = ?
        '''
        cursor.execute(select_query, (country_id,))
        rows = cursor.fetchall()
        continents = [row[0] for row in rows]
        return continents
    finally:
        conn.close()

def return_country_data_borders(country_id):
    """
    Returns the border data for a specific country ID in the 'Countries' table of the SQLite database.

    Args:
        country_id (int): The ID of the country.

    Returns:
        list: A list of border names.
    """
    conn = sqlite3.connect(DATABASE_COUNTRY_FILE_NAME)
    cursor = conn.cursor()
    try:
        select_query = '''
        SELECT Borders.country_code_short
        FROM Countries 
        JOIN Countries_Borders ON Countries.id_country = Countries_Borders.id_country 
        JOIN Borders ON Countries_Borders.id_border = Borders.id_border 
        WHERE Countries.id_country = ?
        '''
        cursor.execute(select_query, (country_id,))
        rows = cursor.fetchall()
        borders = [row[0] for row in rows]
        return borders
    except sqlite3.Error as e:
        print("SQLite Error:", e)
    finally:
        conn.close()

def return_country_data_population(country_id):
    """
    Returns the population data for a specific country ID in the 'Countries' table of the SQLite database.

    Args:
        country_id (int): The ID of the country.

    Returns:
        int: The population of the country.
    """
    conn = sqlite3.connect(DATABASE_COUNTRY_FILE_NAME)
    cursor = conn.cursor()
    try:
        select_query = '''
        SELECT population
        FROM Countries 
        WHERE id_country = ?
        '''
        cursor.execute(select_query, (country_id,))
        population = cursor.fetchone()[0]
        return population
    finally:
        conn.close()

def return_country_data_area(country_id):
    """
    Returns the area data for a specific country ID in the 'Countries' table of the SQLite database.

    Args:
        country_id (int): The ID of the country.

    Returns:
        int: The area of the country.
    """
    conn = sqlite3.connect(DATABASE_COUNTRY_FILE_NAME)
    cursor = conn.cursor()
    try:
        select_query = '''
        SELECT area
        FROM Countries 
        WHERE id_country = ?
        '''
        cursor.execute(select_query, (country_id,))
        area = cursor.fetchone()[0]
        return area
    finally:
        conn.close()

def return_country_data_languages(country_id):
    """
    Returns the language data for a specific country ID in the 'Countries' table of the SQLite database.

    Args:
        country_id (int): The ID of the country.

    Returns:
        list: A list of language names.
    """
    conn = sqlite3.connect(DATABASE_COUNTRY_FILE_NAME)
    cursor = conn.cursor()
    try:
        select_query = '''
        SELECT Languages.language
        FROM Countries 
        JOIN Countries_Languages ON Countries.id_country = Countries_Languages.id_country 
        JOIN Languages ON Countries_Languages.id_language = Languages.id_language 
        WHERE Countries.id_country = ?
        '''
        cursor.execute(select_query, (country_id,))
        rows = cursor.fetchall()
        languages = [row[0] for row in rows]
        return languages
    finally:
        conn.close()

########################################################################################
