"""
This module contains helper functions for the country quiz game.
"""
import random
from countries_database_operations import get_random_countries


def get_shuffled_country(first_option_country, second_option_country, third_option_country):
    """
    Shuffle the countries so that the correct answer is not always in the same position.
    """
    countries = [first_option_country,
                 second_option_country, third_option_country]
    random.shuffle(countries)
    return countries[0]


def get_random_quiz_data(country_connection, quiz_type):
    """
    Generates random quiz data based on the specified quiz type.

    Args:
        country_connection (Connection): The connection to the country database.
        quiz_type (str): The type of quiz to generate. Possible values are 'capital',
        'continent', 'area', or any other value.

    Returns:
        tuple: A tuple containing the first option country, second option country,
        third option country, and the correct country.

    Raises:
        None

    """
    random_countries = get_random_countries(country_connection)

    # Ensure no duplicate countries
    while True:
        first_option_country, second_option_country, third_option_country = random.sample(
            random_countries, 3)
        if (quiz_type == 'capital'):
            if first_option_country.capital != second_option_country.capital != third_option_country.capital:
                break
        elif (quiz_type == 'continent'):
            if first_option_country.continent != second_option_country.continent and second_option_country.continent != third_option_country.continent and first_option_country.continent != third_option_country.continent:
                break
        elif (quiz_type == 'area'):
            if first_option_country.area != second_option_country.area != third_option_country.area:
                break
        else:
            if first_option_country != second_option_country != third_option_country:
                break

    correct_country = get_shuffled_country(
        first_option_country, second_option_country, third_option_country)
    return first_option_country, second_option_country, third_option_country, correct_country
