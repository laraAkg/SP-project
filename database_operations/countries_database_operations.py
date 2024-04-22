"""
This module provides functions to interact with a SQLite database.
It includes functions to create a new database and table,
and to insert a new user into the 'user' table.
"""

import sqlite3
import random
from country import Country


def insert_countries_data_to_db(connection, country_data, index):
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
        c = connection.cursor()
        c.execute(insert_query, (
            index,
            country_data['name'],
            country_data['code'],
            country_data['area'],
            country_data['population']
        ))
        connection.commit()
    except sqlite3.Error as e:
        print("SQLite Error:", e)


def get_countries_count(connection):
    """
    Returns the number of countries in the 'Countries' table of the SQLite database.
    """
    cursor = connection.cursor()
    try:
        select_query = '''SELECT COUNT(*) FROM Countries'''
        cursor.execute(select_query)
        count = cursor.fetchone()[0]
        print("Number of countries in the database:", count)
        return count
    except sqlite3.Error as e:
        print("SQLite Error:", e)


def insert_into_zwischentabelle(connection, country_id, second_id, query):
    """
    Inserts data into the Zwischentabelle table in the countries.db database.
    """
    cursor = connection.cursor()
    try:
        for sec_id in second_id:
            cursor.execute(query, (country_id, sec_id))
            connection.commit()
    except sqlite3.Error as e:
        print("SQLite Error: ", e)


########################################################################################
# The following functions are used to insert data into the database.

def insert_country_data_language(connection, data):
    """
    Inserts language data into the database and returns a list of language IDs.

    Args:
        connection: The SQLite database connection object.
        data: A dictionary containing language data.

    Returns:
        A list of language IDs corresponding to the inserted data.

    Raises:
        sqlite3.Error: If there is an error executing the SQLite queries.
    """
    c = connection.cursor()
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
        connection.commit()
    except sqlite3.Error as e:
        print("SQLite Error:", e)
    return list_id


def insert_country_data_capital(connection, capitals):
    """
    Inserts capital data into the database and returns a list of capital IDs.

    Args:
        connection (sqlite3.Connection): The connection object to the SQLite database.
        capitals (list): A list of capital names to be inserted into the database.

    Returns:
        list: A list of capital IDs corresponding to the inserted capitals.
    """
    c = connection.cursor()
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
        connection.commit()
    except sqlite3.Error as e:
        print("SQLite Error:", e)
    return list_id


def insert_country_data_continent(connection, data):
    """
    Inserts country data into the Continents table in the database.

    Args:
        connection: The SQLite database connection object.
        data: A list of continents.

    Returns:
        A list of continent IDs that were inserted or already existed in the database.
    """
    c = connection.cursor()
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
        connection.commit()
    except sqlite3.Error as e:
        print("SQLite Error:", e)
    return list_id


def insert_country_data_borders(connection, borders):
    """
    Inserts country border data into the database.

    Args:
        connection (sqlite3.Connection): The connection object to the SQLite database.
        borders (list): A list of country codes representing the borders.

    Returns:
        list: A list of border IDs that were inserted or already existed in the database.
    """
    c = connection.cursor()
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
        connection.commit()
    except sqlite3.Error as e:
        print("SQLite Error:", e)
    return list_id


def insert_country_data_currencies(connection, currencies):
    """
    Inserts currency data into the Currencies table in the database.

    Args:
        connection (sqlite3.Connection): The connection object to the SQLite database.
        currencies (dict): A dictionary containing currency data.

    Returns:
        list: A list of currency IDs that were inserted or retrieved from the database.
    """
    list_id = []
    try:
        for _, currency in currencies.items():
            c = connection.cursor()
            currency_query = "SELECT id_currency FROM Currencies WHERE name = ?"
            c.execute(currency_query, (currency.get('name'),))
            result = c.fetchone()
            if result is not None:
                currency_id = result[0]
            else:
                insert_query = "INSERT INTO Currencies (name, symbol) VALUES (?, ?)"
                c.execute(insert_query, (currency.get(
                    'name'), currency.get('symbol')))
                currency_id = c.lastrowid
            list_id.append(currency_id)
        connection.commit()
    except sqlite3.Error as e:
        print("SQLite Error:", e)
    return list_id

########################################################################################
# The following functions are used to retrieve data from the database.


def return_country_data_official_name(connection, country_id):
    """
    Returns the official name of a specific country ID in
    the 'Countries' table of the SQLite database.

    Args:
        connection (sqlite3.Connection): The connection object to the SQLite database.
        country_id (int): The ID of the country.

    Returns:
        str: The official name of the country.
    """

    cursor = connection.cursor()
    try:
        select_query = '''
        SELECT official_name
        FROM Countries
        WHERE id_country = ?
        '''
        cursor.execute(select_query, (country_id,))
        official_name = cursor.fetchone()[0]
        if official_name:
            return official_name
        else:
            return "No official name"
    except sqlite3.Error as e:
        print("SQLite Error:", e)


def return_country_data_capital(connection, country_id):
    """
    Returns the capital data for a specific country ID
    in the 'Countries' table of the SQLite database.

    Args:
        connection (sqlite3.Connection): The connection object to the SQLite database.
        country_id (int): The ID of the country.

    Returns:
        list: A list of capital names.
    """
    cursor = connection.cursor()
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
    except sqlite3.Error as e:
        print("SQLite Error:", e)


def return_country_data_continent(connection, country_id):
    """
    Returns the continent data for a specific country ID
    in the 'Countries' table of the SQLite database.

    Args:
        connection (sqlite3.Connection): The connection object to the SQLite database.
        country_id (int): The ID of the country.

    Returns:
        list: A list of continent names.
    """
    cursor = connection.cursor()
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
    except sqlite3.Error as e:
        print("SQLite Error:", e)


def return_country_data_borders(connection, country_id):
    """
    Returns the border data for a specific country ID
    in the 'Countries' table of the SQLite database.

    Args:
        connection (sqlite3.Connection): The connection object to the SQLite database.
        country_id (int): The ID of the country.

    Returns:
        list: A list of border names.
    """
    cursor = connection.cursor()
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


def return_country_data_population(connection, country_id):
    """
    Returns the population data for a specific country ID
    in the 'Countries' table of the SQLite database.

    Args:
        connection (sqlite3.Connection): The connection object to the SQLite database.
        country_id (int): The ID of the country.

    Returns:
        int: The population of the country.
    """
    cursor = connection.cursor()
    try:
        select_query = '''
        SELECT population
        FROM Countries
        WHERE id_country = ?
        '''
        cursor.execute(select_query, (country_id,))
        population = cursor.fetchone()[0]
        return population
    except sqlite3.Error as e:
        print("SQLite Error:", e)


def return_country_data_area(connection, country_id):
    """
    Returns the area data for a specific country ID in the 'Countries' table of the SQLite database.

    Args:
        connection (sqlite3.Connection): The connection object to the SQLite database.
        country_id (int): The ID of the country.

    Returns:
        int: The area of the country.
    """
    cursor = connection.cursor()
    try:
        select_query = '''
        SELECT area
        FROM Countries
        WHERE id_country = ?
        '''
        cursor.execute(select_query, (country_id,))
        area = cursor.fetchone()[0]
        return int(area)
    except sqlite3.Error as e:
        print("SQLite Error:", e)


def return_country_data_languages(connection, country_id):
    """
    Returns the language data for a specific country ID
    in the 'Countries' table of the SQLite database.

    Args:
        connection (sqlite3.Connection): The connection object to the SQLite database.
        country_id (int): The ID of the country.

    Returns:
        list: A list of language names.
    """
    cursor = connection.cursor()
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
    except sqlite3.Error as e:
        print("SQLite Error:", e)


def return_country_data_currency(connection, country_id):
    """
    Returns the currency data for a specific country ID
    in the 'Countries' table of the SQLite database.

    Args:
        connection (sqlite3.Connection): The connection object to the SQLite database.
        country_id (int): The ID of the country.

    Returns:
        list: A list of currency names.
    """
    cursor = connection.cursor()
    try:
        select_query = '''
        SELECT Currencies.name, Currencies.symbol
        FROM Countries
        JOIN Countries_Currencies ON Countries.id_country = Countries_Currencies.id_country
        JOIN Currencies ON Countries_Currencies.id_currency = Currencies.id_currency
        WHERE Countries.id_country = ?
        '''
        cursor.execute(select_query, (country_id,))
        rows = cursor.fetchall()
        currencies = [{'name': row[0], 'symbol': row[1]} for row in rows]
        currencies_string = ', '.join(
            [f"{currency['name']} ({currency['symbol']})" for currency in currencies])
        return currencies_string
    except sqlite3.Error as e:
        print("SQLite Error:", e)


def return_three_different_continents(connection):
    """
    Returns a list of three different continents from the Continents table in the database.

    Args:
        connection (sqlite3.Connection): The connection object to the SQLite database.

    Returns:
        list: A list of three different continent names.
    """
    cursor = connection.cursor()
    try:
        select_query = '''
        SELECT id_continent
        FROM Continents
        ORDER BY RANDOM()
        LIMIT 3
        '''
        cursor.execute(select_query)
        rows = cursor.fetchall()
        continents = [row[0] for row in rows]
        return continents
    except sqlite3.Error as e:
        print("SQLite Error:", e)

########################################################################################


def get_random_countries(connection):
    """
    Returns a list of randomly generated Country objects.

    Parameters:
    - connection: The database connection object.

    Returns:
    - countries: A list of Country objects.

    """
    countries = []
    for _ in range(3):
        while True:
            random_int = random.randint(0, get_countries_count(connection))
            official_name = return_country_data_official_name(
                connection, random_int)
            capital = return_country_data_capital(connection, random_int)
            continent = return_country_data_continent(
                connection, random_int)
            borders = return_country_data_borders(connection, random_int)
            population = return_country_data_population(
                connection, random_int)
            area = return_country_data_area(connection, random_int)
            languages = return_country_data_languages(
                connection, random_int)
            currency = return_country_data_currency(
                connection, random_int)
            country = Country(official_name, capital, continent,
                              borders, population, area, languages, currency)
            if capital not in [c.capital for c in countries]:
                break
        countries.append(country)
    return countries


def get_country_by_continent_id(connection, continent_id):
    """
    Returns a list of countries that belong to a specific continent.

    Parameters:
    - continent_id: The ID of the continent.

    Returns:
    - countries: A list of countries that belong to the specified continent.

    """
    try:
        select_query = '''
        SELECT Countries.id_country, Countries.official_name, Countries.code, Countries.area, Countries.population, Continents.continent
        FROM Countries
        JOIN Countries_Continents ON Countries.id_country = Countries_Continents.id_country
        JOIN Continents ON Countries_Continents.id_continent = Continents.id_continent
        WHERE Countries_Continents.id_continent = ?
        ORDER BY RANDOM()
        '''
        cursor = connection.cursor()
        cursor.execute(select_query, (continent_id,))
        result = cursor.fetchone()

        borders = return_country_data_borders(connection, result[0])
        capital = return_country_data_capital(connection, result[0])
        languages = return_country_data_languages(connection, result[0])
        currency = return_country_data_currency(connection, result[0])

        return Country(result[1], capital, result[5], borders, result[4], result[3], languages, currency)
    except sqlite3.Error as e:
        print("SQLite Error:", e)
