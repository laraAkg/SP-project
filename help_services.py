"""
This module contains helper functions for the quiz services.
"""
import random
from database_operations.countries_database_operations import (
    get_random_countries,
    return_three_different_continents,
    get_country_by_continent_id)


def get_shuffled_country(
        first_option_country,
        second_option_country,
        third_option_country):
    """
    Returns a randomly shuffled country from the given options.

    Parameters:
    first_option_country (str): The first option country.
    second_option_country (str): The second option country.
    third_option_country (str): The third option country.

    Returns:
    str: A randomly shuffled country from the given options.
    """
    countries = [
        first_option_country,
        second_option_country,
        third_option_country]
    random.shuffle(countries)
    return countries[0]


def get_random_quiz_data(country_connection, quiz_type):
    """
    Generate random quiz data based on the specified quiz type.

    Args:
        country_connection: The connection to the country database.
        quiz_type (str): The type of quiz to generate. Possible values are 'capital', 'population',
        'area', 'currency', or any other value for a general quiz.

    Returns:
        tuple: A tuple containing the first option country, second option country,
        third option country, and the correct country for the quiz.
    """
    random_countries = get_random_countries(country_connection)

    while True:
        first_option_country, second_option_country, third_option_country = random.sample(
            random_countries, 3)

        # Quiz-specific conditions
        if quiz_type == 'capital':
            condition_met = (first_option_country.capital != second_option_country.capital
                             and second_option_country.capital != third_option_country.capital
                             and first_option_country.capital != third_option_country.capital)
        elif quiz_type == 'population':
            condition_met = (first_option_country.population != second_option_country.population
                             and second_option_country.population != third_option_country.population
                             and first_option_country.population != third_option_country.population)
        elif quiz_type == 'area':
            condition_met = (first_option_country.area != second_option_country.area
                             and second_option_country.area != third_option_country.area
                             and first_option_country.area != third_option_country.area)
        elif quiz_type == 'currency':
            condition_met = (first_option_country.currency != second_option_country.currency
                             and second_option_country.currency != third_option_country.currency
                             and first_option_country.currency != third_option_country.currency
                             and first_option_country.currency != 'None'
                             and second_option_country.currency != 'None'
                             and third_option_country.currency != 'None')
        else:
            condition_met = first_option_country != second_option_country != third_option_country

        if condition_met:
            break

    correct_country = get_shuffled_country(
        first_option_country,
        second_option_country,
        third_option_country)
    return first_option_country, second_option_country, third_option_country, correct_country


def return_options_for_continents(country_connection):
    """
    Returns a tuple of three random country options and the correct country for a given continent.

    Parameters:
    country_connection (Connection): The connection to the country database.

    Returns:
    tuple: A tuple containing three random country options and the correct country.
    """

    continents = return_three_different_continents(country_connection)
    countries = list(map(lambda x: get_country_by_continent_id(
        country_connection, x), continents))
    correct_country = countries[0]
    first_option, second_option, third_option = random.sample(countries, 3)
    get_country_by_continent_id(country_connection, first_option)
    return (first_option,
            second_option,
            third_option,
            correct_country)
