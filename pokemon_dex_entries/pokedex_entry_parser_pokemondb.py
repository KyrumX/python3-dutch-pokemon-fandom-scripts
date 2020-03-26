#  Copyright (c) 2020 Aaron Beetstra
#  All rights reserved.

from pokemon_dex_entries.pokedex_entry_parser import PokedexEntryParser
from utils.gen_translation import ENGLISH_TO_DUTCH_GEN
from utils.type_translation import ENGLISH_TO_DUTCH_TYPE


class PokedexEntryParserPokemonDB(PokedexEntryParser):
    def parse_pokemon_name(self):
        # The names table is the last vitals-table class table on the page
        name_table = self.structured_object.find_all('table', class_="vitals-table")[-1]
        tbody = name_table.find("tbody")
        # The English name can be found in the first row in the first table data
        tr = tbody.find_all("tr", recursive=False)[0]
        return tr.find_all("td", recursive=False)[0].text

    def parse_pokemon_japanese_name(self):
        # The names table is the last vitals-table class table on the page
        name_table = self.structured_object.find_all('table', class_="vitals-table")[-1]
        tbody = name_table.find("tbody")
        # The Japanese name can be found in the second row in the first table data
        tr = tbody.find_all("tr", recursive=False)[1]
        return tr.find_all("td", recursive=False)[0].text

    def parse_pokemon_generation(self):
        # The generation number can be found in the first abbr element
        return ENGLISH_TO_DUTCH_GEN[self.structured_object.find('abbr').text]

    def parse_pokemon_types(self):
        # The general info table, which includes the types, is the first virtals-table class table on the page
        general_info_table = self.structured_object.find_all('table', class_="vitals-table")[0]
        tbody = general_info_table.find("tbody")
        # The types can be found in the second row
        tr = tbody.find_all("tr", recursive=False)[1]
        data = tr.find("td", recursive=False).find_all('a')
        if len(data) == 1:
            return [ENGLISH_TO_DUTCH_TYPE[data[0].text.lower()], None]
        else:
            return [ENGLISH_TO_DUTCH_TYPE[data[0].text.lower()], ENGLISH_TO_DUTCH_TYPE[data[1].text.lower()]]

    def parse_pokemon_species(self):
        # The general info table, which includes the species, is the first virtals-table class table on the page
        general_info_table = self.structured_object.find_all('table', class_="vitals-table")[0]
        tbody = general_info_table.find("tbody")
        # The species can be found in the third row
        tr = tbody.find_all("tr", recursive=False)[2]
        # Extract the species, remove spaces and the word 'Pokémon' from the string
        species = tr.find("td").text.replace('Pokémon', '').replace(' ', '')
        # Translate it to Dutch and re-add the 'Pokémon' word
        return self.translator.translate(species, src="en", dest="nl").text + " Pokémon"

    def parse_pokemon_abilities(self):
        abilities = []
        # The general info table, which includes the abilities, is the first virtals-table class table on the page
        general_info_table = self.structured_object.find_all('table', class_="vitals-table")[0]
        tbody = general_info_table.find("tbody")
        # The abilities can be found in the sixth row
        tr = tbody.find_all("tr", recursive=False)[5]
        td = tr.find("td")
        # Normal abilities are found inside 'span' attributes
        for ability in td.find_all('span', recursive=False):
            abilities.append(ability.find('a').text)
        return abilities

    def parse_pokemon_hidden_ability(self):
        # The general info table, which includes the abilities, is the first virtals-table class table on the page
        general_info_table = self.structured_object.find_all('table', class_="vitals-table")[0]
        tbody = general_info_table.find("tbody")
        # The abilities can be found in the sixth row
        tr = tbody.find_all("tr", recursive=False)[5]
        td = tr.find("td")
        # The hidden ability is found inside 'small' attributes, strip '(hidden ability)' and spaces
        return td.find('small').text.replace('(hidden ability)', '').replace(' ', '')

    def parse_pokemon_national_dex_number(self):
        # The general info table, which includes the ndex number, is the first virtals-table class table on the page
        general_info_table = self.structured_object.find_all('table', class_="vitals-table")[0]
        tbody = general_info_table.find("tbody")
        # The species can be found in the first row
        tr = tbody.find_all("tr", recursive=False)[0]
        # Extract the ndex number
        return int(tr.find("td").text)

    def parse_pokemon_evo_in(self):
        pass

    def parse_pokemon_evo_from(self):
        pass

    def parse_pokemon_gender(self):
        pass

    def parse_pokemon_met_height(self):
        pass

    def parse_pokemon_met_weight(self):
        pass

    def parse_pokemon_imp_height(self):
        pass

    def parse_pokemon_imp_weight(self):
        pass

    def parse_pokemon_dex_color(self):
        pass

    def parse_pokemon_egg_groups(self):
        pass

