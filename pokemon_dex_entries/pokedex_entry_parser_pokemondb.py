#  Copyright (c) 2020 Aaron Beetstra
#  All rights reserved.

from pokemon_dex_entries.pokedex_entry_parser import PokedexEntryParser
from utils.egg_groups_translation import ENGLISH_TO_DUTCH_EGG_GROUP
from utils.gen_translation import ENGLISH_TO_DUTCH_GEN
from utils.type_translation import ENGLISH_TO_DUTCH_TYPE


class PokedexEntryParserPokemonDB(PokedexEntryParser):
    def parse_pokemon_name(self):
        # Some pages aren't updated yet with a names table, so if the names table isn't present we
        # need to grab h1 for name

        # Check if name table
        english_name_th = self.structured_object.find("th", text="English")

        if english_name_th:
            # Grab the Name value from the td under the 'English' th
            return english_name_th.find_next_sibling("td").text
        else:
            return self.structured_object.find("h1").text

    def parse_pokemon_japanese_name(self):
        # Some pages aren't updated yet with a names table, so if the names table isn't present we
        # need to skip the japanese name, unfortunately

        # Grab the Japanese Name value from the td under the 'English' th
        japanese_name_th = self.structured_object.find("th", text="Japanese")
        if japanese_name_th:
            return japanese_name_th.find_next_sibling("td").text
        else:
            return None

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
        # Grab the Species value from the td under the 'English' th and remove the 'Pokémon' part
        species = self.structured_object.find("th", text="Species").find_next_sibling("td").text.replace('Pokémon', '').replace(' ', '')
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
        # Grab the Ndex value from the td under the 'National №' th
        return int(self.structured_object.find("th", text="National №").find_next_sibling("td").text)

    def parse_pokemon_national_dex_next(self):
        # First check if there is a next ndex Pokemon
        ndex_next = self.structured_object.find("a", class_="entity-nav-next")

        if ndex_next:
            # Remove the ndex number and keep only the name
            return ndex_next.text.split(" ", 1)[1]
        return None

    def parse_pokemon_national_dex_previous(self):
        # First check if there is a previous ndex Pokemon
        ndex_previous = self.structured_object.find("a", class_="entity-nav-prev")

        if ndex_previous:
            # Remove the ndex number and keep only the name
            return ndex_previous.text.split(" ", 1)[1]
        return None

    def _parse_pokemon_evo_line(self):
        # Evolution data can be found in a chart form, we need to import it fully
        # We also need to consider that some Pokémon can evolve into 2 different Pokémon depending on conditions
        # This whole function is a mess. But pokemondb doesn't seem to use solid logic rather what fits best at the
        # time, will look into it again (maybe)... For now it works.

        info_card_list = self.structured_object.find('div', class_="infocard-list-evo")

        # Check if this Pokémon even has an evolution line
        if info_card_list is None:
            # No evolution line
            return [None, None]

        splits = self.structured_object.find_all('span', class_="infocard-evo-split")

        # Get all evo lines, some Pokémon have been set up to have multiple evo lines for clarity reasons...
        evo_lines = self.structured_object.find('main').find_all('div', recursive=False, class_="infocard-list-evo")

        if len(splits) == 0 and len(evo_lines) == 1:
            # A simple straight evolution line, example: a --> b --> c
            evo_steps = info_card_list.find_all('div', class_="infocard")
            evo_line = []

            for evo_step in evo_steps:
                evo_line.append(
                    evo_step.find('span', class_='infocard-lg-data text-muted').find('a', class_="ent-name").text)

            return evo_line

        if len(splits) == 0 and len(evo_lines) == 2:
            # Mr.Mime and Koffing
            evo_line_one = []
            evo_line_two = []

            evo_steps_one = evo_lines[0].find_all('div', class_="infocard")
            evo_steps_two = evo_lines[1].find_all('div', class_="infocard")

            for evo_step in evo_steps_one:
                evo_line_one.append(
                    evo_step.find('span', class_='infocard-lg-data text-muted').find('a', class_="ent-name").text)
            for evo_step in evo_steps_two:
                evo_line_two.append(
                    evo_step.find('span', class_='infocard-lg-data text-muted').find('a', class_="ent-name").text)

            if evo_line_one == evo_line_two:
                return evo_line_one

            evo_line_two.pop(0)
            return evo_line_one + evo_line_two

        if len(splits) == 1 and len(evo_lines) == 1:
            # Relatively simple evolution line, example: a --> b --> c or d
            first_evo_steps = info_card_list.find_all('div', class_="infocard", recursive=False)
            evo_line = []

            for evo_step in first_evo_steps:
                evo_line.append(
                    evo_step.find('span', class_='infocard-lg-data text-muted').find('a', class_="ent-name").text)

            split_evo = []
            second_evo_steps = info_card_list.find('span', class_="infocard-evo-split").find_all('div', class_="infocard", recursive=True)
            for evo_step in second_evo_steps:
                pokemon = evo_step.find('span', class_='infocard-lg-data text-muted').find('a', class_="ent-name").text

                # Some Pokémon are shown as split evolution lines only because of form changes, like Pikachu --> Raichu
                if not pokemon in split_evo:
                    split_evo.append(
                        pokemon
                    )

            if len(split_evo) < 2:
                evo_line.append(split_evo[0])
            else:
                evo_line.append(split_evo)

            return evo_line

        else:
            # First check if there is a normal evo line present (should always be the first one on the bunch)
            evo_line = []
            i = 0
            for line in evo_lines:
                print(i)
                line_is_normal = len(line.find_all('span', class_="infocard-evo-split")) == 0
                evo_line_empty = len(evo_line) <= 0
                if line_is_normal:
                    print("Normal line")
                    # Generate the first evo line ('normal', e.g. a->b)
                    evo_steps = line.find_all('div', class_="infocard")

                    if evo_line_empty:
                        for evo_step in evo_steps:
                            evo_line.append(
                                evo_step.find('span', class_='infocard-lg-data text-muted').find('a',
                                                                                                 class_="ent-name").text)
                    else:
                        pokemon = evo_steps[1].find('span', class_='infocard-lg-data text-muted').find('a',
                                                                                                 class_="ent-name").text
                        if not pokemon in evo_line[1]:
                            evo_line[1].append(pokemon)

                else:
                    # Get normal info-cards first
                    info_cards = line.find_all('div', class_="infocard", recursive=False)

                    if i == 0:
                        for evo_step in info_cards:
                            evo_line.append(
                                evo_step.find('span', class_='infocard-lg-data text-muted').find('a',
                                                                                                 class_="ent-name").text)
                        split_info_cards = line.find('span', class_="infocard-evo-split").find_all('div', class_="infocard", recursive=True)
                        split_evo = []
                        for split_card in split_info_cards:
                            pokemon = split_card.find('span', class_='infocard-lg-data text-muted').find('a',
                                                                                                       class_="ent-name").text

                            # Some Pokémon are shown as split evolution lines only because of form changes, like Burmy --> Wormadam
                            if not pokemon in split_evo:
                                split_evo.append(
                                    pokemon
                                )
                        evo_line.append(split_evo)
                    elif i > 0:
                        print("Hier")
                        # basic line has been done, we only care about the splits now
                        if type(evo_line[1]) is not list:
                            evo_line[1] = [evo_line[1]]

                        split_info_cards = line.find('span', class_="infocard-evo-split").find_all('div',
                                                                                                    class_="infocard",
                                                                                                    recursive=True)
                        for split_card in split_info_cards:
                            pokemon = split_card.find('span', class_='infocard-lg-data text-muted').find('a',
                                                                                                             class_="ent-name").text
                            # Some Pokémon are shown as split evolution lines only because of form changes, like Burmy --> Wormadam
                            if not pokemon in evo_line[1]:
                                evo_line[1].append(
                                    pokemon
                                )
                i += 1

            return evo_line

    def parse_pokemon_evo_in(self):
        evo_line = self._parse_pokemon_evo_line()

        # Find the position of our Pokémon in the evolution chain
        evo_index = self.__find_evo_line_index(evo_line, self.parse_pokemon_name())

        if evo_index is not None and evo_index < len(evo_line) - 1:
            return evo_line[evo_index + 1]
        return None

    def parse_pokemon_evo_from(self):
        evo_line = self._parse_pokemon_evo_line()

        # Find the position of our Pokémon in the evolution chain
        evo_index = self.__find_evo_line_index(evo_line, self.parse_pokemon_name())

        if evo_index is not None and evo_index <= len(evo_line) - 1 and evo_index != 0:
            return evo_line[evo_index - 1]
        return None

    @staticmethod
    def __find_evo_line_index(evo_line: list, pokemon_name: str) -> int:
        index = 0
        for evo_step in evo_line:
            if type(evo_step) is list:
                if pokemon_name in evo_step:
                    return index
                else:
                    index+=1
            else:
                if evo_step == pokemon_name:
                    return index
                else:
                    index+=1

    def parse_pokemon_gender(self):
        # Returns the % of male or 'Geslachtloos'

        # Grab the gender value from the td under the 'Gender' th
        gender = self.structured_object.find("th", text="Gender").find_next_sibling("td").text

        if gender == "Genderless":
            return None
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
            return [ENGLISH_TO_DUTCH_EGG_GROUP[groups[0].text]]
        else:
            return [ENGLISH_TO_DUTCH_EGG_GROUP[groups[0].text], ENGLISH_TO_DUTCH_EGG_GROUP[groups[1].text]]\
