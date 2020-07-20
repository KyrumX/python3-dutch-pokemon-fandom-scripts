#  Copyright (c) 2020 Aaron Beetstra
#  All rights reserved.

import abc
from abc import abstractmethod


class PokedexEntryParserStrategyForm(abc.ABC):
    """
    A class used to build parsers for FORM depending characteristics
    """

    def build_pokedex_form_entry(self):
        pass

    @abstractmethod
    def parse_pokemon_types(self):
        pass

    @abstractmethod
    def parse_pokemon_abilities(self):
        pass

    @abstractmethod
    def parse_pokemon_met_height(self):
        pass

    @abstractmethod
    def parse_pokemon_met_weight(self):
        pass

    @abstractmethod
    def parse_pokemon_imp_height(self):
        pass

    @abstractmethod
    def parse_pokemon_imp_weight(self):
        pass
