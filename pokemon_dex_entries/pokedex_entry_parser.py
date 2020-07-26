#  Copyright (c) 2020 Aaron Beetstra
#  All rights reserved.

import abc
from abc import abstractmethod

from utils.evolution_line import EvolutionLine


class PokedexEntryParser(abc.ABC):

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
    def parse_pokemon_types(self):
        pass

    @abstractmethod
    def parse_pokemon_species(self):
        pass

    @abstractmethod
    def parse_pokemon_abilities(self):
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

    @abstractmethod
    def parse_pokemon_dex_color(self):
        pass

    @abstractmethod
    def parse_pokemon_egg_groups(self):
        pass
