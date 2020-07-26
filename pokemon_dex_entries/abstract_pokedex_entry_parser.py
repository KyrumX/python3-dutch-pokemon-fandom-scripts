#  Copyright (c) 2020 Aaron Beetstra
#  All rights reserved.

import abc
from abc import abstractmethod

from googletrans import Translator

from pokemon_dex_entries.pokedex_entry import PokedexEntry
from pokemon_dex_entries.abstract_pokedex_entry_parser_strategy import AbstractPokedexEntryParserStrategy
from utils.evolution_line import EvolutionLine


class AbstractPokedexEntryParser(abc.ABC):
    """
    A class used to build parsers for all characteristics (form depending, and general characteristics)

    Inherits from PokedexEntryParserStrategyForm as this parser needs all characteristics, thus
        form depending characteristics are required as well as general characteristics.
    """

    def __init__(self, strategy: AbstractPokedexEntryParserStrategy):
        self.translator = Translator()

        self._form_strategy = strategy
        self.default_strategy = strategy

    @property
    def form_strategy(self) -> AbstractPokedexEntryParserStrategy:
        return self._form_strategy

    @form_strategy.setter
    def form_strategy(self, strategy: AbstractPokedexEntryParserStrategy):
        self._form_strategy = strategy

    def build_pokedex_entry(self):
        return PokedexEntry(
            self.parse_pokemon_name(),
            self.parse_pokemon_form_name(),
            self.parse_pokemon_japanese_name(),
            self.parse_pokemon_generation(),
            self.parse_pokemon_species(),
            self.parse_pokemon_types()[0],
            self.parse_pokemon_types()[1],
            self.parse_pokemon_abilities(),
            self.parse_pokemon_hidden_ability(),
            self.parse_pokemon_national_dex_number(),
            self.parse_pokemon_national_dex_next(),
            self.parse_pokemon_national_dex_previous(),
            self.parse_pokemon_evo_line(),
            self.parse_pokemon_gender(),
            self.parse_pokemon_met_height(),
            self.parse_pokemon_met_weight(),
            self.parse_pokemon_imp_height(),
            self.parse_pokemon_imp_weight(),
            self.parse_pokemon_egg_groups()
        )

    @abstractmethod
    def parse_pokemon_name(self):
        pass

    def parse_pokemon_form_name(self):
        return self._form_strategy.parse_pokemon_form_name()

    @abstractmethod
    def parse_pokemon_japanese_name(self):
        pass

    @abstractmethod
    def parse_pokemon_generation(self):
        pass

    @abstractmethod
    def parse_pokemon_species(self):
        pass

    def parse_pokemon_types(self):
        return self._form_strategy.parse_pokemon_types()

    def parse_pokemon_abilities(self):
        return self._form_strategy.parse_pokemon_abilities()

    def parse_pokemon_hidden_ability(self):
        return self._form_strategy.parse_pokemon_hidden_ability()

    @abstractmethod
    def parse_pokemon_national_dex_number(self):
        pass

    @abstractmethod
    def parse_pokemon_national_dex_next(self):
        pass

    @abstractmethod
    def parse_pokemon_national_dex_previous(self):
        pass

    @abstractmethod
    def parse_pokemon_evo_line(self) -> EvolutionLine:
        pass

    @abstractmethod
    def parse_pokemon_gender(self):
        pass

    def parse_pokemon_met_height(self):
        return self._form_strategy.parse_pokemon_met_height()

    def parse_pokemon_met_weight(self):
        return self._form_strategy.parse_pokemon_met_weight()

    def parse_pokemon_imp_height(self):
        return self._form_strategy.parse_pokemon_imp_height()

    def parse_pokemon_imp_weight(self):
        return self._form_strategy.parse_pokemon_imp_weight()

    @abstractmethod
    def parse_pokemon_dex_color(self):
        pass

    @abstractmethod
    def parse_pokemon_egg_groups(self):
        pass
