#  Copyright (c) 2020 Aaron Beetstra
#  All rights reserved.

import abc
from abc import abstractmethod

from googletrans import Translator

from pokemon_dex_entries.pokedex_entry import PokedexEntry
from pokemon_dex_entries.pokedex_entry_parser_strategy_form import PokedexEntryParserStrategyForm
from utils.evolution_line import EvolutionLine


class PokedexEntryParserStrategy(PokedexEntryParserStrategyForm, abc.ABC):
    """
    A class used to build parsers for all characteristics (form depending, and general characteristics)

    Inherits from PokedexEntryParserStrategyForm as this parser needs all characteristics, thus
        form depending characteristics are required as well as general characteristics.
    """

    def __init__(self):
        self.translator = Translator()

    def build_pokedex_entry(self):
        return PokedexEntry(
            self.parse_pokemon_name(),
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

    @abstractmethod
    def parse_pokemon_japanese_name(self):
        pass

    @abstractmethod
    def parse_pokemon_generation(self):
        pass

    @abstractmethod
    def parse_pokemon_species(self):
        pass

    @abstractmethod
    def parse_pokemon_hidden_ability(self):
        pass

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

    @abstractmethod
    def parse_pokemon_dex_color(self):
        pass

    @abstractmethod
    def parse_pokemon_egg_groups(self):
        pass
