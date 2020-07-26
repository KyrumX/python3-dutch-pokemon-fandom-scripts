#  Copyright (c) 2020 Aaron Beetstra
#  All rights reserved.
from pokemon_dex_entries.bulbapedia.pokedex_entry_parser_strategy_bulbapedia_base import \
    PokedexEntryParserPokemonStrategyBulbapediaBase


class PokedexEntryParserPokemonStrategyBulbapediaForm(PokedexEntryParserPokemonStrategyBulbapediaBase):

    def __init__(self, infobox_dict: dict, form_id: int):
        super().__init__(infobox_dict)
        self.form_id = form_id

    def parse_pokemon_form_name(self):
        """"
        Grab the form name
        key: "form{form_id}"
        :return form_name
        """
        key = "form{form_id}".format(form_id=self.form_id.__str__())

        # Not using super().parse_pokemon_form_name here since the base value actually has 2 options depending
        #   if the base form has a different name to begin with
        return self.infobox_dict[key]

    def parse_pokemon_types(self):
        # Grab the Pokémon type(s), found inside the infobox dict
        # keys: "form{form_id}type1" and optionally "form{form_id}type2"
        # Returns [] with type1(str) and type2(str) or None
        # Returns [] with the base values (str type1, type2) through super() if the form has no different typing
        #   from the base form
        form_primary_type_key = "form{}type1".format(self.form_id.__str__())
        form_secondary_type_key = "form{}type2".format(self.form_id.__str__())

        form_types = super().parse_pokemon_types(primary_key=form_primary_type_key,
                                                 secondary_key=form_secondary_type_key)

        if form_types:
            return form_types
        return super().parse_pokemon_types()

    def parse_pokemon_abilities(self):
        # Grab the Pokémon abilities, found inside the infobox dict
        # Key: "ability{form_id}-{n}"
        # Returns [] of abilities
        # Returns [] of base form abilities through super() if no abilities different from the base form

        ability_key = "ability{}".format(self.form_id.__str__())
        form_ability_key = ability_key + "-{}"

        form_abilities = super().parse_pokemon_abilities(ability_key=form_ability_key)

        return form_abilities if form_abilities else super().parse_pokemon_abilities()

    def parse_pokemon_hidden_ability(self):
        # Grab the Pokémon hidden ability (if it has one), found inside the infobox dict
        # key: "abilityd{form_id}"
        # Returns hidden ability: str or None if the form has no hidden ability

        form_hidden_ability_key = "abilityd{form_id}".format(form_id=self.form_id.__str__())

        return super().parse_pokemon_hidden_ability(hidden_ability_key=form_hidden_ability_key)

    def parse_pokemon_met_height(self):
        # Grab the Pokémon height in meters
        # key: "height-m{form_id}"
        # Returns height(str) if found, else returns None

        form_metric_height_key = "height-m{form_id}".format(form_id=self.form_id.__str__())

        height = super().parse_pokemon_met_height(metric_height_key=form_metric_height_key)

        return height if height else super().parse_pokemon_met_height()

    def parse_pokemon_met_weight(self):
        # Grab the Pokémon height in meters
        # key: "weight-kg{form_id}"
        # Returns weight(str) if found, else returns None

        form_metric_weight_key = "weight-kg{form_id}".format(form_id=self.form_id.__str__())

        weight = super().parse_pokemon_met_weight(metric_weight_key=form_metric_weight_key)

        return weight if weight else super().parse_pokemon_met_weight()

    def parse_pokemon_imp_height(self):
        # Grab the Pokémon height in meters
        # key: "height-ftin{form_id}"
        # Returns height(str) if found, else returns None

        form_imperial_height_key = "height-ftin{form_id}".format(form_id=self.form_id.__str__())

        height = super().parse_pokemon_imp_height(imperial_height_key=form_imperial_height_key)

        return height if height else super().parse_pokemon_imp_height()

    def parse_pokemon_imp_weight(self):
        # Grab the Pokémon height in meters
        # key: "weight-lbs{form_id}"
        # Returns weight(str) if found, else returns None

        form_imperial_height_key = "weight-lbs{form_id}".format(form_id=self.form_id.__str__())

        weight = super().parse_pokemon_imp_weight(imperial_weight_key=form_imperial_height_key)

        return weight if weight else super().parse_pokemon_imp_weight()
