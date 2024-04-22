"""
Th
"""

class Country:
    """
    Represents a country with its official name, capital, continent, borders, 
    population, area, and languages.
    """

    def __init__(self, official_name, capital, continent, borders, population, area, languages, currency):
        """
        Initializes a new instance of the Country class.

        Parameters:
        - official_name (str): The official name of the country.
        - capital (str): The capital city of the country.
        - continent (str): The continent where the country is located.
        - borders (list): A list of countries that share borders with the country.
        - population (int): The population of the country.
        - area (float): The area of the country in square kilometers.
        - languages (list): A list of languages spoken in the country.
        """
        self.official_name = official_name
        self.capital = capital
        self.continent = continent
        self.borders = borders
        self.population = population
        self.area = area
        self.languages = languages
        self.currency = currency
