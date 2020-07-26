#  Copyright (c) 2020 Aaron Beetstra
#  All rights reserved.
from pokemon_dex_entries.abstract_pokedex_entry_parser_strategy import AbstractPokedexEntryParserStrategy
from utils.type_translation import ENGLISH_TO_DUTCH_TYPE


class PokedexEntryParserPokemonStrategyBulbapediaBase(AbstractPokedexEntryParserStrategy):

    def __init__(self, infobox_dict: dict):
        self.infobox_dict = infobox_dict

    def parse_pokemon_form_name(self):
        # Grab the Pokémon form1 name, found inside the infobox dict
        # key: "form1" (or name if form1 doesn't exist)
        return self.infobox_dict['form1'] if 'form1' in self.infobox_dict else None

    def parse_pokemon_types(self, **kwargs):
        # Grab the Pokémon type(s), found inside the infobox dict
        # keys: "type1" and optionally "type2" (or grab keys from kwargs through primary_key and secondary_key)

        primary_type_key = kwargs.get("primary_key", "type1")

        if primary_type_key in self.infobox_dict:
            primary_type = self.infobox_dict[primary_type_key]
        else:
            return None

        secondary_key = kwargs.get("secondary_key", "type2")

        if secondary_key in self.infobox_dict:
            secondary_type = self.infobox_dict[secondary_key]
            return [ENGLISH_TO_DUTCH_TYPE[primary_type.lower()], ENGLISH_TO_DUTCH_TYPE[secondary_type.lower()]]
        else:
            return [ENGLISH_TO_DUTCH_TYPE[primary_type.lower()], None]

    def parse_pokemon_abilities(self, **kwargs):
        # Grab the Pokémon abilities, found inside the infobox dict
        # Key: "ability-{n}" (for base form, ability{form_id}-{n} for forms, used as kwarg
        # Returns [] of abilities

        abilities = []

        searching = True
        n = 1

        ability_key = kwargs.get("ability_key", "ability{}")

        while searching:
            key = ability_key.format(n.__str__())
            if key in self.infobox_dict:
                abilities.append(self.infobox_dict[key])
                n += 1
            else:
                searching = False
        return abilities

    def parse_pokemon_hidden_ability(self, **kwargs):
        # Grab the Pokémon hidden ability (if it has one), found inside the infobox dict
        # key: "abilityd"

        hidden_ability_key = kwargs.get("hidden_ability_key", "abilityd")

        if hidden_ability_key in self.infobox_dict:
            return self.infobox_dict[hidden_ability_key]

    def parse_pokemon_met_height(self, **kwargs) -> str:
        # Grab the Pokémon height in meters
        # default key: "height-m"

        metric_height_key = kwargs.get("metric_height_key", "height-m")

        if metric_height_key in self.infobox_dict:
            return self.infobox_dict[metric_height_key]

    def parse_pokemon_met_weight(self, **kwargs) -> str:
        # Grab the Pokémon height in kilograms
        # default key: "weight-kg"

        metric_weight_key = kwargs.get("metric_weight_key", "weight-kg")

        if metric_weight_key in self.infobox_dict:
            return self.infobox_dict[metric_weight_key]

    def parse_pokemon_imp_height(self, **kwargs) -> str:
        # Grab the Pokémon height in float inch
        # default key: "height-ftin"

        imperial_height_key = kwargs.get("imperial_height_key", "height-ftin")

        if imperial_height_key in self.infobox_dict:
            return self.infobox_dict[imperial_height_key]

    def parse_pokemon_imp_weight(self, **kwargs) -> str:
        # Grab the Pokémon height in float inch
        # default key: "weight-lbs"
        imperial_weight_key = kwargs.get("imperial_weight_key", "weight-lbs")

        if imperial_weight_key in self.infobox_dict:
            return self.infobox_dict[imperial_weight_key]