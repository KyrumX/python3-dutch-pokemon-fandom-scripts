#  Copyright (c) 2020 Aaron Beetstra
#  All rights reserved.
from pokemon_dex_entries.pokedex_entry_parser_strategy_form import PokedexEntryParserStrategyForm
from utils.type_translation import ENGLISH_TO_DUTCH_TYPE


class PokedexEntryParserPokemonStrategyFormBulbapedia(PokedexEntryParserStrategyForm):

    def __init__(self, infobox_dict: dict, form_id: int):
        self.infobox_dict = infobox_dict
        self.form_id = form_id

    def parse_pokemon_types(self):
        # Grab the Pokémon type(s), found inside the infobox dict
        # keys: "form{form_id}type1" and optionally "form{form_id}type2"
        # Returns None if the form has no type difference with it's primary form
        # Returns [] with type1(str) and type2(str) or None
        form_primary_type_key = "form{}type1".format(self.form_id.__str__())
        form_secondary_type_key = "form{}type2".format(self.form_id.__str__())

        if form_primary_type_key in self.infobox_dict:
            form_primary_type = ENGLISH_TO_DUTCH_TYPE[self.infobox_dict["form_primary_type_key"].lower()]
            if form_secondary_type_key in self.infobox_dict:
                form_secondary_type = ENGLISH_TO_DUTCH_TYPE[self.infobox_dict["form_secondary_type_key"].lower()]
                return [form_primary_type, form_secondary_type]
            else:
                return [form_primary_type, None]
        else:
            return None

    def parse_pokemon_abilities(self):
        # Grab the Pokémon abilities, found inside the infobox dict
        # Key(s): "ability{form_id}-{n}"
        # Returns None if no abilities different from the primary form
        # Returns list of abilities otherwise

        form_abilities = []

        searching = True
        n = 1

        while searching:
            key = "ability{form_id}-{n}".format(form_id=self.form_id.__str__(), n=n.__str__())
            if key in self.infobox_dict:
                form_abilities.append(self.infobox_dict[key])
                n += 1
            else:
                searching = False
        if form_abilities:
            return form_abilities
        else:
            return None

    def parse_pokemon_met_height(self):
        # Grab the Pokémon height in meters
        # key: "height-m{form_id}"
        # Returns height(str) if found, else returns None

        key = "height-m{form_id}".format(form_id=self.form_id.__str__())

        return self._if_key_found_return_else_none(key)

    def parse_pokemon_met_weight(self):
        # Grab the Pokémon height in meters
        # key: "weight-kg{form_id}"
        # Returns weight(str) if found, else returns None

        key = "weight-kg{form_id}".format(form_id=self.form_id.__str__())

        return self._if_key_found_return_else_none(key)

    def parse_pokemon_imp_height(self):
        # Grab the Pokémon height in meters
        # key: "height-ftin{form_id}"
        # Returns height(str) if found, else returns None

        key = "height-ftin{form_id}".format(form_id=self.form_id.__str__())

        return self._if_key_found_return_else_none(key)

    def parse_pokemon_imp_weight(self):
        # Grab the Pokémon height in meters
        # key: "weight-lbs{form_id}"
        # Returns weight(str) if found, else returns None

        key = "weight-lbs{form_id}".format(form_id=self.form_id.__str__())

        return self._if_key_found_return_else_none(key)

    def _if_key_found_return_else_none(self, key):
        if key in self.infobox_dict:
            return self.infobox_dict[key]
        return None