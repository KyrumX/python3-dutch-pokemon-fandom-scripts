#  Copyright (c) 2020 Aaron Beetstra
#  All rights reserved.
import re
import regex

from pokemon_dex_entries.pokedex_entry_parser import PokedexEntryParser
from utils.egg_groups_translation import ENGLISH_TO_DUTCH_EGG_GROUP
from utils.evolution_line import EvolutionLine
from utils.gen_translation import ENGLISH_TO_DUTCH_GEN
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

        # We further want to split at every | (because it indicates a new dict pair), however: sometimes the dict pair
        #   value has a nested |, always used between {{ and }}, example: |evo1:{{...|...}}, we dont want to split at
        #   the 2nd | char, since its part of a value rather than a new key/value.
        #   Luckily Matthew Barnett's Regex library supports infinite lookbehinds, which is what is needed!
        #   \| --> matches the character | literally
        #   (?<!{{.*|) --> Negative lookbehind, so exclude any | character when preceded by: {{ and infinite chars .*
        #   (?!\|.*}}) --> Negative Lookahead, so exclude any | char if it is followed by infinite chars and }}
        #   Note that the the infinite chars in the lookbehind is not possible in a lot of regex engines, including
        #   the built in Python one, that is why I use the one made my Matthew Barnett.
        split_at_vertical_bar_except_when_between_brackets = r'\|(?<!{{.*\|)(?!\|.*}})'

        raw_pokemon_evolution_lines = re.findall(regex_pattern_individual_evo_boxes, evolution_box, re.IGNORECASE)
        self.pokemon_evolution_lines = []
        for raw_pokemon_evolution_line in raw_pokemon_evolution_lines:
            temp = raw_pokemon_evolution_line.split("|", 1)[1]
            splitted = regex.split(split_at_vertical_bar_except_when_between_brackets, temp)
            splitted_to_dict = str_list_to_dict(splitted, "=")
            self.pokemon_evolution_lines.append(splitted_to_dict)

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
        #   have special cases, these are: Eevee, Tyrogue, (these special case arent implemented yet here)
        # Like stated above, no strict format, but the basic formats are:
        #   name1 --> name2 --> name3
        #   name1 --> name2 / name2a
        #   name1 --> name2 --> name3 / name3a
        #   name1 --> name2a / name2b
        # Notice how the 2nd and 4th are basically the same, but one uses name2 / name2a VS name2a / name2b
        skip = ["Eevee", "Tyrogue"]
        key = ["name"]
        sub_keys = ["a", "b"]

        if not self.parse_pokemon_name() in skip:
            for evo_line in self.pokemon_evolution_lines:
                for evo_step in range(1, 5):
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