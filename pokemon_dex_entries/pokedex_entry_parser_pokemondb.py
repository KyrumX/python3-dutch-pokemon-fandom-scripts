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

    def _parse_pokemon_evo_line(self):
        # Evolution data can be found in a chart form, we need to import it fully
        # We also need to consider that some Pokémon can evolve into 2 different Pokémon depending on conditions
        # TODO: Now, Eevee is a real pain since it can evolve into MANY MANY different Pokémon

        splits = self.structured_object.find_all('span', class_="infocard-evo-split")
        if len(splits) == 1:
            pass
        elif len(splits) > 1:
            # CHECK FOR DUPLICATES, MON WTIH DIFFERENT FORMS
            print("EEVEE/Burmy")
        else:
            # Normal evolution line
            evo_line = []
            info_card_list = self.structured_object.find('div', class_="infocard-list-evo")

            # Check if this Pokémon even has an evolution line
            if info_card_list is None:
                return [None, None]
            evo_steps = info_card_list.find_all('div', class_="infocard")
            for evo_step in evo_steps:
                evo_line.append(evo_step.find('span', class_='infocard-lg-data text-muted').find('a', class_="ent-name").text)
            evo_position = evo_line.index(self.parse_pokemon_name())
            if evo_position == 0:
                return [None, evo_line[1]]
            elif 0 < evo_position < len(evo_line) - 1:
                return [evo_line[evo_position - 1], evo_line[evo_position + 1]]
            else:
                return [evo_line[evo_position - 1], None]

    def parse_pokemon_evo_in(self):
        return self._parse_pokemon_evo_line()[1]

    def parse_pokemon_evo_from(self):
        return self._parse_pokemon_evo_line()[0]

    def parse_pokemon_gender(self):
        # Returns the % of male or 'Geslachtloos'

        # Grab the gender value from the td under the 'Gender' th
        gender = self.structured_object.find("th", text="Gender").find_next_sibling("td").text

        if gender == "Genderless":
            return "Geslachtloos"
        else:
            # We only need to return the male value in string representation, split after first '%' and return
            return gender.split("%", 1)[0]

    def parse_pokemon_met_height(self):
        # Grab the height value from the td under the 'Height' th
        height = self.structured_object.find("th", text="Height").find_next_sibling("td").text

        # Height contains both met and imp, so we need to extract the metric value
        return height.split()[0]

    def parse_pokemon_met_weight(self):
        # Grab the height value from the td under the 'Height' th
        height = self.structured_object.find("th", text="Weight").find_next_sibling("td").text

        # Weight contains both met and imp, so we need to extract the metric value
        return height.split()[0]

    def parse_pokemon_imp_height(self):
        # Grab the height value from the td under the 'Height' th
        height = self.structured_object.find("th", text="Height").find_next_sibling("td").text

        # Height contains both met and imp, so we need to extract the imperial value
        return height.split("(")[1].replace(")", "")

    def parse_pokemon_imp_weight(self):
        # Grab the weight value from the td under the 'Weight' th
        weight = self.structured_object.find("th", text="Height").find_next_sibling("td").text

        # Weight contains both met and imp, so we need to extract the imperial value
        return weight.split("(")[1].replace(")", "")

    def parse_pokemon_dex_color(self):
        # Color is not stored on PokémonDB
        return ""

    def parse_pokemon_egg_groups(self):
        # Grab the ergg groups value from the td under the 'Egg Groups' th
        egg_groups = self.structured_object.find("th", text="Egg Groups").find_next_sibling("td")

        groups = egg_groups.find_all('a', recursive=False)
        if len(groups) == 1:
            return [groups[0].text]
        else:
            return [groups[0].text, groups[1].text]

