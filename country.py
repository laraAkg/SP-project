import random
from countries_database_operations import (get_countries_count, return_country_data_capital,
                                           return_country_data_continent,
                                           return_country_data_borders,
                                           return_country_data_population,
                                           return_country_data_area, return_country_data_languages)

class Country:
    def __init__(self, official_name, capital, continent, borders, population, area, languages):
        self.official_name = official_name
        self.capital = capital
        self.continent = continent
        self.borders = borders
        self.population = population
        self.area = area
        self.languages = languages



def get_random_countries():
    """
    Returns a list of randomly generated Country objects.
    
    This function generates a list of Country objects with random attributes such as capital, continent,
    borders, population, area, and languages. The number of countries generated is determined by the range
    specified in the for loop.
    
    Returns:
        list: A list of Country objects.
    """
    countries = []
    for _ in range(3):
        while True:
            random_int = random.randint(0, get_countries_count())
            capital = return_country_data_capital(random_int)
            continent = return_country_data_continent(random_int)
            borders = return_country_data_borders(random_int)
            population = return_country_data_population(random_int)
            area = return_country_data_area(random_int)
            languages = return_country_data_languages(random_int)
            country = Country("Cuba", capital, continent, borders, population, area, languages)
            if capital not in [c.capital for c in countries]:
                break
        countries.append(country)
    
    return countries
