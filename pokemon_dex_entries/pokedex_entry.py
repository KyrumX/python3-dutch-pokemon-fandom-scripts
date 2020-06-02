#  Copyright (c) 2020 Aaron Beetstra
#  All rights reserved.
from utils.evolution_line import EvolutionLine


class PokedexEntry:

    # TODO: FIX EVOLUTION LINE PARSING

    def __init__(self,
                 name:  str,
                 japanse_name: str,
                 generation: str,
                 species: str,
                 type: str,
                 type2: str,
                 abilities: list,
                 hidden_ability: list,
                 ndex_num: int,
                 ndex_next: str,
                 ndex_prev: str,
                 evo_line: EvolutionLine,
                 percent_male: int,
                 met_height: float,
                 met_weight: float,
                 imp_height: float,
                 imp_weight: float,
                 egg_groups: list):
        self.name = name
        self.japanese_name = japanse_name
        self.generation = generation
        self.species = species
        self.type = type
        self.type2 = type2
        self.abilities = abilities
        self.hidden_ability = hidden_ability
        self.ndex_num = ndex_num
        self.ndex_next = ndex_next
        self.ndex_prev = ndex_prev
        self.evo_line = EvolutionLine
        self.percent_male = percent_male
        self.met_height = met_height
        self.met_weight = met_weight
        self.imp_height = imp_height
        self.imp_weight = imp_weight
        self.egg_groups = egg_groups

    def convert_to_dutch_wiki_template(self):

        result = "{{PokémonInfobox\n"

        # Add name
        result += "| naam        = {}\n".format(self.name)
        # Add japanese name
        result += "| jnaam       = {}\n".format(self.japanese_name)
        # Add ndex number
        result += "| ndex        = {}\n".format(self.ndex_num.__str__())

        # Check if we need to add ndex prev
        if self.ndex_prev:
            result += "| ndexvorig   = {}\n".format(self.ndex_prev)

        # Check if we need to add ndex next
        if self.ndex_next:
            result += "| ndexvolgend = {}\n".format(self.ndex_next)

        # Add generation
        result += "| gen         = {}\n".format(self.generation)

        # Add species
        result += "| soort       = {}\n".format(self.species)

        # Add type
        result += "| type        = {}\n".format(self.type)

        # Add type2 if applicable
        if self.type2:
            result += "| type2       = {}\n".format(self.type2)

        # Add metric weight
        result += "| metgewicht  = {} kg\n".format(self.met_weight)
        # Add metric height
        result += "| metlengte   = {} m\n".format(self.met_height)
        # Add imperial weight
        result += "| imgewicht   = {} lbs.\n".format(self.imp_weight)
        # Add imperial height
        result += "| imlengte    = {}\n".format(self.imp_height)

        # Abilities
        result += "| gave        = "
        for i in range(len(self.abilities)):
            result += "[[{}]]".format(self.abilities[i])

            if i + 1 < len(self.abilities):
                result += "<br />"
        result += "\n"

        # Hidden ability
        result += "| dw          = {}\n".format(self.hidden_ability)

        # Gender
        if self.percent_male:
            result += "| mannelijk   = {}\n".format(self.percent_male)

        # Egg groups, if applicable
        if self.egg_groups:
            for i in range(len(self.egg_groups)):
                if i == 0:
                    result += "| ei1         = {}\n".format(self.egg_groups[i])
                else:
                    result += "| ei2         = {}\n".format(self.egg_groups[i])

        # Evolutions
        if self.evo_in:
            result += "| evoin       = "
            if type(self.evo_in) is list:
                for i in range(len(self.evo_in)):
                    result += "[[{}]]".format(self.evo_in[i])

                    if i + 1 < len(self.evo_in):
                        result += "<br />"
            else:
                result += "[[{}]]".format(self.evo_in)
            result += "\n"
        if self.evo_from:
            result += "| evovan      = {}\n".format(self.evo_from)

        result += "}}"

        return result
