"""
This module provides functions for generating random numbers.
"""

import random

import pycountry
import requests
from flask import Flask, render_template

# Specify the templates folder
app = Flask(__name__, template_folder='templates')


def get_all_countries():
    """
    Retrieves a list of all countries using pagination.

    Returns:
            list: A list of all countries.

    Raises:
            requests.exceptions.RequestException: If there is an error while making the API request.

    """
    url = "https://wft-geo-db.p.rapidapi.com/v1/geo/countries"
    headers = {
        "X-RapidAPI-Key": "bcb6679012msh169f4edcd407c6dp17800bjsnb43444ccba7a",
        "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
    }
    countries = []
    page = 1
    while True:
        params = {
            "page": page,
            "limit": 50  # Adjust the limit as per your requirement
        }
        response = requests.get(url, headers=headers, params=params, timeout=5)
        data = response.json()
        countries.extend(data['data'])
        if page >= data['metadata']['total_pages']:
            break
        page += 1
    return countries


def generate_random_country_code():
    """
    Generates a random country code using the pycountry library.

    Returns:
            str: A random country code in ISO 3166-1 alpha-2 format.
    """
    countries = list(pycountry.countries)
    random_country = random.choice(countries)
    return random_country.alpha_2


def get_country_details(country_code):
    """
    Retrieves details of a country based on the provided country code.

    Args:
            country_code (str): The country code of the country to retrieve details for.

    Returns:
            dict: A dictionary containing the details of the country.

    Raises:
            requests.exceptions.RequestException: If there is an error while making the API request.

    """
    url = f"https://wft-geo-db.p.rapidapi.com/v1/geo/countries/{country_code}"
    headers = {
        "X-RapidAPI-Key": "bcb6679012msh169f4edcd407c6dp17800bjsnb43444ccba7a",
        "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, timeout=5)
    data = response.json()
    return data['data']


def get_places_in_country(country_code):
    """
    Retrieves a list of places in a specific country using the country code.

    Args:
            country_code (str): The country code of the desired country.

    Returns:
            list: A list of places in the specified country.

    Raises:
            requests.exceptions.RequestException: If there is an error making the API request.

    """
    url = f"https://wft-geo-db.p.rapidapi.com/v1/geo/countries/{country_code}/places"
    headers = {
        "X-RapidAPI-Key": "bcb6679012msh169f4edcd407c6dp17800bjsnb43444ccba7a",
        "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, timeout=5)
    data = response.json()
    return data['data']


@app.route('/')
def index():
    """
    Renders the index.html template with random country details.

    Returns:
            A rendered HTML template with the following variables:
            - country_code: A randomly generated country code.
            - country_details: Details of the randomly generated country.
            - places_in_country: Places within the randomly generated country.
    """
    random_country_code = generate_random_country_code()
    country_details = get_country_details(random_country_code)
    places_in_country = get_places_in_country(random_country_code)
    print(random_country_code)
    print(country_details)
    print(places_in_country)
    return render_template('index.html', country_code=random_country_code, country_details=country_details,	places_in_country=places_in_country)


if __name__ == '__main__':
    app.run(debug=True, port=20302)
