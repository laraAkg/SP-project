"This script creates the tables in the SQLite database for the countries project."
import sqlite3
import requests
from countries_database_operations import (
    insert_countries_data_to_db,
    insert_country_data_capital,
    insert_country_data_continent,
    insert_country_data_language,
    insert_country_data_borders,
    insert_country_data_currencies,
    insert_into_zwischentabelle
)


def fetch_and_insert_data(connection):
    """
    Fetches data from a REST API and inserts it into a database.

    Args:
        connection: The database connection object.

    Returns:
        None
    """

    response = requests.get("https://restcountries.com/v3.1/all", timeout=10)

    index = 1
    if response.status_code == 200:
        countries = response.json()
        for country in countries:
            try:
                country_data = {
                    'name': country['name']['official'],
                    'code': country['cca2'],
                    'area': country['area'],
                    'population': country['population'],
                }
                insert_countries_data_to_db(connection, country_data, index)

                capital = country.get(
                    'capital', {'noCapital': 'No Capital Found'})
                id_capital = insert_country_data_capital(connection, capital)

                continents = country.get(
                    'continents', {'noContinent': 'No Continent Found'})
                id_continent = insert_country_data_continent(
                    connection, continents)

                languages = country.get(
                    'languages', {'noLang': 'No Language Found'})
                id_language = insert_country_data_language(
                    connection, languages)

                borders = country.get('borders', {'island': 'Island'})
                id_border = insert_country_data_borders(connection, borders)

                currencies = country.get(
                    'currencies', {'NoCurr': {'name': 'No currency', 'symbol': 'No symbol'}})
                id_currency = insert_country_data_currencies(
                    connection, currencies)

                insert_into_zwischentabelle(connection,
                                            index, id_border,
                                            '''INSERT INTO Countries_Borders (id_country,id_border) VALUES (?,?)'''
                                            )
                insert_into_zwischentabelle(connection,
                                            index, id_capital,
                                            '''INSERT INTO Countries_Capitals (id_country,id_capital) VALUES (?,?)'''
                                            )
                insert_into_zwischentabelle(connection,
                                            index, id_currency,
                                            '''INSERT INTO Countries_Currencies (id_country,id_currency) VALUES (?,?)'''
                                            )
                insert_into_zwischentabelle(connection,
                                            index, id_language,
                                            '''INSERT INTO Countries_Languages (id_country,id_language) VALUES (?,?)'''
                                            )
                insert_into_zwischentabelle(connection,
                                            index, id_continent,
                                            '''INSERT INTO Countries_Continents (id_country,id_continent) VALUES (?,?)'''
                                            )
                index += 1
            except requests.exceptions.RequestException as e:
                print("Error in loading:", str(e))
                continue
    else:
        print("Error in fetching data!")


def create_tables_for_country_db(connection):
    """
    Create tables for the country database.

    Args:
        connection: The database connection object.

    Returns:
        None
    """
    queries = [
        """
        CREATE TABLE IF NOT EXISTS Countries (
            id_country INTEGER PRIMARY KEY,
            official_name TEXT UNIQUE,
            code TEXT,
            area REAL,
            population INTEGER
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Capitals (
            id_capital INTEGER PRIMARY KEY,
            capital TEXT UNIQUE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Continents (
            id_continent INTEGER PRIMARY KEY AUTOINCREMENT,
            continent TEXT UNIQUE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Borders (
            id_border INTEGER PRIMARY KEY AUTOINCREMENT,
            country_code_short TEXT UNIQUE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Currencies (
            id_currency INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            symbol TEXT UNIQUE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Languages (
            id_language INTEGER PRIMARY KEY AUTOINCREMENT,
            language TEXT UNIQUE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Countries_Capitals (
            id_capital INTEGER,
            id_country INTEGER,
            UNIQUE(id_capital, id_country) ON CONFLICT REPLACE,
            FOREIGN KEY (id_capital) REFERENCES Capitals(id_capital),
            FOREIGN KEY (id_country) REFERENCES Countries(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Countries_Currencies (
            id_currency INTEGER,
            id_country INTEGER,
            UNIQUE(id_currency, id_country) ON CONFLICT REPLACE,
            FOREIGN KEY (id_currency) REFERENCES Currencies(id_currency),
            FOREIGN KEY (id_country) REFERENCES Countries(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Countries_Languages (
            id_language INTEGER,
            id_country INTEGER,
            UNIQUE(id_language, id_country) ON CONFLICT REPLACE,
            FOREIGN KEY (id_language) REFERENCES Languages(id_language),
            FOREIGN KEY (id_country) REFERENCES Countries(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Countries_Continents (
            id_continent INTEGER,
            id_country INTEGER,
            UNIQUE(id_continent, id_country) ON CONFLICT REPLACE,
            FOREIGN KEY (id_continent) REFERENCES Continents(id_continent),
            FOREIGN KEY (id_country) REFERENCES Countries(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Countries_Borders (
            id_border INTEGER,
            id_country INTEGER,
            UNIQUE(id_border, id_country) ON CONFLICT REPLACE,
            FOREIGN KEY (id_border) REFERENCES Borders(id_border),
            FOREIGN KEY (id_country) REFERENCES Countries(id)
        )
        """
    ]
    for query in queries:
        c = connection.cursor()
        try:
            c.execute(query)
            connection.commit()
        except sqlite3.Error as e:
            print("Error executing query:", e)
