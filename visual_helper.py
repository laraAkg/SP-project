"""
This module contains visual helper functions for the quiz services.
"""
import matplotlib.pyplot as plt
import matplotlib.style
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import pearsonr
from database_operations.countries_database_operations import (
    get_all_areas,
    get_all_population,
    get_top_five_largest_countries,
    get_top_five_population_countries,
)


def plot_top_five_largest_countries(country_connection):
    """
    Plots a pie chart showing the top 5 largest countries by area.

    Parameters:
    - country_connection: The connection to the country database.

    Returns:
    None
    """

    top_area = get_top_five_largest_countries(country_connection)
    countries, areas = zip(*top_area)
    df = pd.DataFrame({'Country': countries, 'Area': areas})
    plt.figure(figsize=(8, 6))
    plt.pie(df['Area'], labels=df['Country'], autopct='%1.1f%%')
    plt.title('Top 5 Largest Countries by Area')
    plt.savefig('static/diagrams/topfiveareacountry.png')
    plt.close()


def plot_top_five_population_countries(country_connection):
    """
    Plots a pie chart showing the top 5 largest countries by population.

    Parameters:
    - country_connection: The connection to the country database.

    Returns:
    None
    """
    top_population = get_top_five_population_countries(country_connection)
    countries, populations = zip(*top_population)
    df = pd.DataFrame({'Country': countries, 'Population': populations})
    plt.figure(figsize=(8, 6))
    plt.pie(df['Population'], labels=df['Country'], autopct='%1.1f%%')
    plt.title('Top 5 Largest Countries by Population')
    plt.savefig('static/diagrams/topfivepopulationcountry.png')
    plt.close()


def hypothesis_test(country_connection):
    """
    Perform a hypothesis test to determine the correlation between area and population.

    Parameters:
    - country_connection: The connection to the country data.

    Returns:
    - A string indicating whether the null hypothesis is rejected or not.
    """

    areas = get_all_areas(country_connection)
    population = get_all_population(country_connection)
    correlation, p_value = stats.pearsonr(areas, population)

    print(f"Correlation coefficient: {correlation}")
    print(f"P-Value: {p_value}")

    significance_level = 0.05
    if p_value < significance_level:
        return "The null hypothesis is rejected. There is a significant correlation between area and population."
    else:
        return "The null hypothesis cannot be rejected. There is no significant correlation between area and population."

def get_correlation_coefficient(connection):
    """
    Calculate the correlation coefficient between the area and population of a given connection.

    Parameters:
    connection (object): The connection object used to retrieve data.

    Returns:
    tuple: A tuple containing the correlation coefficient and the p-value.

    """
    area = get_all_areas(connection)
    population = get_all_population(connection)
    print(np.corrcoef(area, population))
    matplotlib.style.use("ggplot")
    plt.scatter(area, population)
    plt.title("Correlation between Area and Population")
    plt.savefig('static/diagrams/CorrelationAreaPopulation.png')
    corr_coeff = pearsonr(area, population)
    return corr_coeff
