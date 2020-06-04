#  Copyright (c) 2020 Aaron Beetstra
#  All rights reserved.
import re

from pokemon_dex_entries.pokedex_entry_parser import PokedexEntryParser
from utils.color_translation import ENGLISH_TO_DUTCH_COLOR
from utils.egg_groups_translation import ENGLISH_TO_DUTCH_EGG_GROUP
from utils.evolution_line import EvolutionLine, EvolutionStep
from utils.gen_translation import ENGLISH_TO_DUTCH_GEN
from utils.gender_conversion import GENDER_DECIMAL_TO_MALE_PERCENTAGE
from utils.list_to_dict import str_list_to_dict
from utils.type_translation import ENGLISH_TO_DUTCH_TYPE


class PokedexEntryParserPokemonBulbapedia(PokedexEntryParser):
    """On the edit pages, Bulbapedia provides a structure we can use.
    Almost all data we need can be found inside the infobox, which uses the following structure:
        {{Pokémon Infobox
        |name=Dragapult
        |jname=ドラパルト
        |jtranslit=Doraparuto
        ...
        }}
    We grab this and convert it to a dict for our usage.

    Other information we need: prev, next from the national dex, evolution
    """

    def __init__(self, url: str):
        super().__init__(url)

        text_area_text = self.structured_object.find("textarea", class_="mw-editfont-default").text

        # Grab the Pokémon info box and convert to a list (the string contains newlines, so every newline --> list item)
        info_box = text_area_text.partition("{{Pokémon Infobox")[2].partition("}}")[0].replace("\n", "").split("|")

        # Grab the Pokémon PrevNext box and convert to a list
        prev_next_box = text_area_text.partition("{{PokémonPrevNext/Pokémon")[2].partition("}}")[0].split("|")

        # To get the evolution line we need to get another part of the page.
        #   This is found between ===Evolution=== and ===Forms=== or ===Sprites===

        if "===Forms===" in text_area_text:
            evolution_box = text_area_text.partition("===Evolution===")[2].partition("===Forms===")[0]
        else:
            evolution_box = text_area_text.partition("===Evolution===")[2].partition("===Sprites===")[0]

        # So I couldn't get regex to work with dotall and \n\n (it would always see the entire object as one,
        #   rather than finding multiple occurrences...), so dirty workaround I guess
        evolution_box = evolution_box.replace("\n\n", "ENDHERE")
        evolution_box = evolution_box.replace("\n", "")
        evolution_box = evolution_box.replace("ENDHERE", "\n")

        # Pattern to grab all evo boxes if there are multiple
        regex_pattern_individual_evo_boxes = r"{{Evobox(.*)}}\n"

        self.raw_pokemon_evolution_lines = re.findall(regex_pattern_individual_evo_boxes, evolution_box, re.IGNORECASE)

        # Bulbapedia uses "=" to split between the key and value
        self.infobox_dict = str_list_to_dict(info_box, "=")
        self.prev_next_dict = str_list_to_dict(prev_next_box, "=")

    def parse_pokemon_name(self):
        # Grab the Pokémon name, found inside the infobox dict
        # key: "name"
        return self.infobox_dict["name"]

    def parse_pokemon_japanese_name(self):
        # Grab the Japanese name, found inside the infobox dict
        # keys: "jname" and "tmname"
        return self.infobox_dict["jname"] + " " + self.infobox_dict["tmname"]

    def parse_pokemon_generation(self):
        # Grab the Pokémon generation, found inside the infobox dict
        # key: "generation"
        return "Generatie " + self.infobox_dict["generation"]

    def parse_pokemon_types(self):
        # Grab the Pokémon type(s), found inside the infobox dict
        # keys: "type1" and optionally "type2"
        primary_type = self.infobox_dict["type1"]

        if "type2" in self.infobox_dict:
            secondary_type = self.infobox_dict["type2"]
            return [ENGLISH_TO_DUTCH_TYPE[primary_type.lower()], ENGLISH_TO_DUTCH_TYPE[secondary_type.lower()]]
        else:
            return [ENGLISH_TO_DUTCH_TYPE[primary_type.lower()], None]

    def parse_pokemon_species(self):
        # Grab the Pokémon species, found inside the infobox dict
        # key: "category"

        return self.translator.translate(self.infobox_dict["category"], src="en", dest="nl").text

    def parse_pokemon_abilities(self):
        # Grab the Pokémon abilities, found inside the infobox dict
        # All keys that contain "ability" except "abilityd", "abilitycold", "abilityn" and "abilitylayout"

        abilities = []
        excluded_keys = ["abilityd", "abilitycold", "abilitylayout", "abilityn"]

        for key, value in self.infobox_dict.items():
            if "ability" in key and key not in excluded_keys:
                abilities.append(value)

        return abilities

    def parse_pokemon_hidden_ability(self):
        # Grab the Pokémon hidden ability (if it has one), found inside the infobox dict
        # key: "abilityd"

        if "abilityd" in self.infobox_dict:
            return self.infobox_dict["abilityd"]

    def parse_pokemon_national_dex_number(self):
        # Grab the Pokémon national dex number, found inside the infobox dict
        # key: "ndex"
        return self.infobox_dict["ndex"]

    def parse_pokemon_national_dex_next(self):
        # Grab the Pokémon national dex next, found inside the prev_next box dict
        # key: "next" and check if "nextnum" isn't 001 (since Bulbapedia loops from last to first)
        if "next" in self.prev_next_dict and self.prev_next_dict["nextnum"] != "001":
            return self.prev_next_dict["next"]

    def parse_pokemon_national_dex_previous(self):
        # Grab the Pokémon national dex next, found inside the prev_next box dict
        # key: "prev" and check if "nextnum" isn't 002 (since Bulbapedia loops from last to first)
        if "prev" in self.prev_next_dict and self.prev_next_dict["nextnum"] != "002":
            return self.prev_next_dict["prev"]

    def parse_pokemon_evo_line(self) -> EvolutionLine:
        # The evolution line is a bit of work: the format changes sometimes (probably depending on the writers preference)
        # Some Pokémon dont have code for their evo lines present because bulbapedia deemed it too complex, so they
        #   have special cases, these are: Eevee, Tyrogue, (these special case aren't implemented yet here)
        # Like stated above, the format changes sometimes, e.g. sometimes name2 is first, other times name2a
        #   name1 --> name2 --> name3
        #   name1 --> name2 / name2a
        #   name1 --> name2 --> name3 / name3a
        #   name1 --> name2a / name2b
        # Notice how the 2nd and 4th are basically the same, but one uses [name2 / name2a] VS [name2a / name2b]
        skip = ["Eevee", "Tyrogue", "Wurmple"]

        base = None
        evo_lines = []

        raw_evo_lines = []
        evo_keys = ["name{}", "name{}a", "name{}b"]

        for raw_pokemon_evolution_line in self.raw_pokemon_evolution_lines:
            temp = raw_pokemon_evolution_line.split("|", 1)[1]
            dict = {}
            for i in range(1, 5):
                for key in evo_keys:
                    formatted_key = key.format(str(i))
                    pattern = r"\b" + re.escape(formatted_key) + r"\b"
                    if re.search(pattern, temp):
                        index = temp.index(formatted_key)
                        index += len(formatted_key) + 1
                        key_value = ""
                        while temp[index] != "|":
                            key_value += temp[index]
                            index += 1
                        dict[formatted_key] = key_value
            raw_evo_lines.append(dict)

        if not self.parse_pokemon_name() in skip:
            for evo_line in raw_evo_lines:
                print(evo_line)
                current = None
                current_base = None
                for index_step in range(1, 5):
                    if base is None:
                        base = EvolutionStep(
                            pokemon_name=evo_line["name1"]
                        )
                        current = base
                        current_base = current
                    elif index_step == 1:
                        current = EvolutionStep(
                            pokemon_name=evo_line["name1"]
                        )
                        current_base = current
                    else:
                        latest = None
                        for key in evo_keys:
                            formatted_key = key.format(str(index_step))
                            print(formatted_key)
                            if formatted_key in evo_line:
                                print("adding!")

                                # First check if it isn't the same Pokémon we are adding, since Bulbapedia adds
                                #   new evo steps for different forms, even though the Pokémon name doesn't change
                                duplicate = False
                                for pkmn in current.next:
                                    if evo_line[formatted_key] == pkmn.pokemon_name:
                                        duplicate = True

                                if not duplicate:
                                    new_step = EvolutionStep(
                                        pokemon_name=evo_line[formatted_key]
                                    )
                                    current.add_next(new_step)
                                    latest = new_step
                        if latest:
                            current = latest
                evo_lines.append(current_base)
        else:
            return None

        # Create the evolution line object
        #   Main evolution line is the first one
        main_evo_line = EvolutionLine(evo_lines[0])
        evo_lines.pop(0)

        # Now compare them, sometimes they are exactly the same since bulbapedia will add a new one for every form
        for evo_line in evo_lines:
            pass

        return main_evo_line

    def parse_pokemon_gender(self):
        # Grab the Pokémon decimal gender code, found inside the infobox dict, convert to male%
        # key: "gendercode"
        return GENDER_DECIMAL_TO_MALE_PERCENTAGE[int(self.infobox_dict["gendercode"])]

    def parse_pokemon_met_height(self) -> str:
        # Grab the Pokémon height in meters
        # key: "height-m"
        return self.infobox_dict["height-m"]

    def parse_pokemon_met_weight(self) -> str:
        # Grab the Pokémon height in kilograms
        # key: "weight-kg"
        return self.infobox_dict["weight-kg"]

    def parse_pokemon_imp_height(self) -> str:
        # Grab the Pokémon height in float inch
        # key: "height-ftin"
        return self.infobox_dict["height-ftin"]

    def parse_pokemon_imp_weight(self) -> str:
        # Grab the Pokémon height in float inch
        # key: "weight-lbs"
        return self.infobox_dict["weight-lbs"]

    def parse_pokemon_dex_color(self):
        # Grab the Pokémon dex color
        # key: "color"
        return ENGLISH_TO_DUTCH_COLOR[self.infobox_dict["color"].lower()]

    def parse_pokemon_egg_groups(self):

        egg_groups_n = int(self.infobox_dict["egggroupn"])

        if egg_groups_n == 0:
            return ENGLISH_TO_DUTCH_EGG_GROUP["Undiscovered"]
        elif egg_groups_n == 1:
            return [ENGLISH_TO_DUTCH_EGG_GROUP[self.infobox_dict["egggroup1"].lower()]]
        else:
            return [ENGLISH_TO_DUTCH_EGG_GROUP[self.infobox_dict["egggroup1"].lower()],
                    ENGLISH_TO_DUTCH_EGG_GROUP[self.infobox_dict["egggroup2"].lower()]]

