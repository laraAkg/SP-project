import random
from countries_database_operations import (get_countries_count, return_country_data_capital,
                                           return_country_data_continent,
                                           return_country_data_borders,
                                           return_country_data_population,
                                           return_country_data_area, return_country_data_languages,
                                           return_country_data_official_name)


random_int = random.randint(0, get_countries_count())
print(random_int)

official_name = return_country_data_official_name(random_int)
capitals = return_country_data_capital(random_int)
continents = return_country_data_continent(random_int)
borders = return_country_data_borders(random_int)
population = return_country_data_population(random_int)
area = return_country_data_area(random_int)
languages = return_country_data_languages(random_int)

if "island" == borders[0]:
    story = f"""In a distant land, the official name of which is {official_name}, lies a capital city called {', '.join(capitals)} perched on the continent of {', '.join(continents)}. The population is {population}, and the land area spans {area}. This country is an island in the vast ocean."""
else:
    story = f"""In a distant land, the official name of which is {official_name}, lies a capital city called {', '.join(capitals)} perched on the continent of {', '.join(continents)}. The population is {population}, and the land area spans {area}. This country shares borders with {', '.join(borders)} and the official language spoken here is {', '.join(languages)}."""
print(story)
