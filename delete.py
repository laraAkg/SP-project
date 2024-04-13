"""
This module fetches data from a REST API and inserts it into a SQLite database.
"""

import requests
from database_connector_countries import *

response = requests.get("https://restcountries.com/v3.1/all", timeout=10)


def fetch_and_insert_data():
    """
    Fetches data from a response object and inserts it into a database.

    This function takes no arguments and assumes that the `response` object is defined and contains the data to be fetched.
    It iterates over the countries in the response, extracts relevant information, and inserts it into the database using the `insert_countries_data_to_db` function.

    If an error occurs during the loading process, the error message is printed and the loop continues to the next country.

    If the response status code is not 200, an error message is printed.

    Note: Make sure to define the `response` object before calling this function.

    Returns:
        None
    """
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
                insert_countries_data_to_db(country_data, index)

                capital = country.get('capital', {'noCapital': 'No Capital Found'})
                id_capital = insert_country_data_capital(capital)

               # capitals = country.get('capital', [])
                #id_capital = insert_country_data_one_param(capitals, '''INSERT INTO Capitals (capital) VALUES (?)''')

                languages = country.get('languages', {'noLang': 'No Language Found'})
                id_language = insert_country_data_language(languages)

                #borders = country.get('borders', [])
                #id_border = insert_country_data_one_param(borders, '''INSERT OR IGNORE INTO Borders (country_code_short) VALUES (?)''')

                #currencies = country.get('currencies', [])
                #id_currency = insert_country_data_currencies(currencies)
                #insert_into_zwischentabelle(index,id_border, '''INSERT INTO Countries_Borders (id_boarder,id_country) VALUES (?,?)''')
                insert_into_zwischentabelle(index, id_capital,'''INSERT INTO Countries_Capitals (id_country,id_capital) VALUES (?,?)''')
                #insert_into_zwischentabelle(index, id_currency,'''INSERT INTO Countries_Currencies (id_currency,id_country) VALUES (?,?)''')
                insert_into_zwischentabelle(index, id_language,'''INSERT INTO Countries_Languages (id_country,id_language) VALUES (?,?)''')
                #insert_into_zwischentabelle(index, id_capital,'''INSERT INTO Countries_Continents (id_country,id_continent) VALUES (?,?)''')
                index += 1
            except Exception as e:
                print("Error in loading:", str(e),)
                continue
    else:
        print("Error in fetching data!")

fetch_and_insert_data()

print_country_data_capital()
