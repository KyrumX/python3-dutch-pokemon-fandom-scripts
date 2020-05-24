#  Copyright (c) 2020 Aaron Beetstra
#  All rights reserved.
import re

from pokemon_dex_entries.pokedex_entry_parser import PokedexEntryParser
from utils.egg_groups_translation import ENGLISH_TO_DUTCH_EGG_GROUP
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

    Other information we need: prev, next from the national dex
    """

    def __init__(self, url: str):
        super().__init__(url)

        text_area_text = self.structured_object.find("textarea", class_="mw-editfont-default").text

        # Grab the Pokémon info box and convert to a list (the string contains newlines, so every newline --> list item)
        info_box = text_area_text.partition("{{Pokémon Infobox")[2].partition("}}")[0].replace("\n", "").split("|")

        # Grab the Pokémon PrevNext box and convert to a list
        prev_next_box = text_area_text.partition("{{PokémonPrevNext/Pokémon")[2].partition("}}")[0].split("|")

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