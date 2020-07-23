#  Copyright (c) 2020 Aaron Beetstra
#  All rights reserved.
from pokemon_dex_entries.abstract_pokedex_entry_parser_strategy_base import AbstractPokedexEntryParserStrategyBase
from utils.type_translation import ENGLISH_TO_DUTCH_TYPE


class PokedexEntryParserPokemonStrategyBulbapediaBase(AbstractPokedexEntryParserStrategyBase):

    def __init__(self, infobox_dict: dict):
        self.infobox_dict = infobox_dict

    def parse_pokemon_form_name(self):
        # Grab the Pokémon form1 name, found inside the infobox dict
        # key: "form1" (or name if form1 doesn't exist)
        return self.infobox_dict['form1'] if 'form1' in self.infobox_dict else None

    def parse_pokemon_types(self):
        # Grab the Pokémon type(s), found inside the infobox dict
        # keys: "type1" and optionally "type2"
        primary_type = self.infobox_dict["type1"]

        if "type2" in self.infobox_dict:
            secondary_type = self.infobox_dict["type2"]
            return [ENGLISH_TO_DUTCH_TYPE[primary_type.lower()], ENGLISH_TO_DUTCH_TYPE[secondary_type.lower()]]
        else:
            return [ENGLISH_TO_DUTCH_TYPE[primary_type.lower()], None]

    def parse_pokemon_abilities(self):
        # TODO: FIX WITH FORMS
        # Grab the Pokémon abilities, found inside the infobox dict
        # All keys that contain "ability" except "abilityd", "abilitycold", "abilityn" and "abilitylayout"

        abilities = []
        excluded_keys = ["abilityd", "abilitycold", "abilitylayout", "abilityn"]

        for key, value in self.infobox_dict.items():
            if "ability" in key and key not in excluded_keys:
                abilities.append(value)

        return abilities

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