#  Copyright (c) 2020 Aaron Beetstra
#  All rights reserved.

class PokedexEntry:

    def __init__(self,
                 name:  str,
                 japanse_name: str,
                 generation: str,
                 type: str,
                 type2: str,
                 abilities: list,
                 hidden_ability: list,
                 ndex_num: int,
                 ndex_next: str,
                 ndex_prev: str,
                 evo_in: str,
                 evo_from: str,
                 percent_male: int,
                 met_height: float,
                 met_weight: float,
                 imp_height: float,
                 imp_weight: float,
                 egg_groups: list):
        self.name = name
        self.japanese_name = japanse_name
        self.generation = generation
        self.type = type
        self.type2 = type2
        self.abilities = abilities
        self.hidden_ability = hidden_ability
        self.ndex_num = ndex_num
        self.evo_in = evo_in
        self.evo_from = evo_from
        self.percent_male = percent_male
        self.met_height = met_height
        self.met_weight = met_weight
        self.imp_height = imp_height
        self.imp_weight = imp_weight
        self.egg_groups = egg_groups
