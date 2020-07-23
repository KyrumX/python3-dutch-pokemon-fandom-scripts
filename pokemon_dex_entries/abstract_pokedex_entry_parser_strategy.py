#  Copyright (c) 2020 Aaron Beetstra
#  All rights reserved.

import abc
from abc import abstractmethod


class AbstractPokedexEntryParserStrategy(abc.ABC):
    """
    A class used to build parsers for FORM depending characteristics
    """

    # TODO: Replace DICT with class
    def build_pokedex_form_entry(self):
        return {
            "form": self.parse_pokemon_form_name(),
            "type": self.parse_pokemon_types(),
            "ability": self.parse_pokemon_abilities(),
            "met_height": self.parse_pokemon_met_height(),
            "met_weight": self.parse_pokemon_met_weight(),
            "imp_height": self.parse_pokemon_imp_height(),
            "imp_weight": self.parse_pokemon_imp_weight()
        }

    @abstractmethod
    def parse_pokemon_form_name(self):
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
