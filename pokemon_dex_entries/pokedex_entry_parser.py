#  Copyright (c) 2020 Aaron Beetstra
#  All rights reserved.

import abc
from abc import abstractmethod

import requests
from bs4 import BeautifulSoup
from googletrans import Translator

from pokemon_dex_entries.pokedex_entry import PokedexEntry


class PokedexEntryParser(abc.ABC):

    def __init__(self, url: str):
        request = requests.get(url)
        self.structured_object = BeautifulSoup(request.text, 'html.parser')
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
            self.parse_pokemon_evo_in(),
            self.parse_pokemon_evo_from(),
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
    def parse_pokemon_evo_in(self):
        pass

    @abstractmethod
    def parse_pokemon_evo_from(self):
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
