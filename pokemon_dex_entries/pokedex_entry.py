#  Copyright (c) 2020 Aaron Beetstra
#  All rights reserved.
from utils.evolution_line import EvolutionLine


class PokedexEntry:
    prefix = "{{PokémonInfobox\n"
    suffix = "}}"

    def __init__(self,
                 name: str,
                 japanse_name: str,
                 generation: str,
                 species: str,
                 type: str,
                 type2: str,
                 abilities: list,
                 hidden_ability: list,
                 ndex_num: str,
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
        self.evo_line = evo_line
        self.percent_male = percent_male
        self.met_height = met_height
        self.met_weight = met_weight
        self.imp_height = imp_height
        self.imp_weight = imp_weight
        self.egg_groups = egg_groups
        self.forms = []

    def add_forms(self, forms: list):
        self.forms = self.forms + forms

    def _build_name(self):
        # Key: naam
        # Value: provided: str - Required: str
        name_entry = "| naam        = {}\n".format(self.name)
        return name_entry

    def _build_japanese_name(self):
        # Key: jnaam
        # Value: provided: str - Required: str
        japanese_name_entry = "| jnaam       = {}\n".format(self.japanese_name)
        return japanese_name_entry

    def _build_national_dex_number(self):
        # Key: ndex
        # Value: provided: str - Required: str
        national_dex_entry = "| ndex        = {}\n".format(self.ndex_num)
        return national_dex_entry

    def _build_prev_national_dex_number(self):
        # Key: ndexvorig
        # Value: provided: str - Required: str
        prev_national_dex_entry = "| ndexvorig   = {}\n".format(self.ndex_prev)
        return prev_national_dex_entry

    def _build_next_national_dex_number(self):
        # Key: ndexvolgend
        # Value: provided: str - Required: str
        next_national_dex_entry = "| ndexvolgend = {}\n".format(self.ndex_next)
        return next_national_dex_entry

    def _build_generation(self):
        # Key: gen
        # Value: provided: str - Required: str
        generation_dex_entry = "| gen         = {}\n".format(self.generation)
        return generation_dex_entry

    def _build_species(self):
        # Key: soort
        # Value: provided: str (species only) - Required: str ('Species' Pokémon), so add ' Pokémon'
        species_dex_entry = "| soort       = {} Pokémon\n".format(self.species)
        return species_dex_entry

    def _build_primary_type(self):
        # Key: type
        # Value: provided: str - Required: str
        primary_type_dex_entry = "| type        = {}\n".format(self.type)
        return primary_type_dex_entry

    def _build_secondary_type(self):
        # Key: type2
        # Value: provided: str - Required: str
        secondary_type_dex_entry = "| type2       = {}\n".format(self.type2)
        return secondary_type_dex_entry

    def _build_metric_weight(self):
        # Key: metgewicht
        # Value: provided: str - Required: str ('weight' kg), so add ' kg'
        metric_weight_dex_entry = "| metgewicht  = {} kg\n".format(self.met_weight)
        return metric_weight_dex_entry

    def _build_metric_length(self):
        # Key: metlengte
        # Value: provided: str - Required: str ('length' m), so add ' m'
        metric_length_dex_entry = "| metlengte   = {} m\n".format(self.met_height)
        return metric_length_dex_entry

    def _build_imperial_weight(self):
        # Key: imgewicht
        # Value: provided: str - Required: str ('length' lbs.), so add ' lbs.'
        imperial_weight_dex_entry = "| imgewicht   = {} lbs.\n".format(self.imp_weight)
        return imperial_weight_dex_entry

    def _build_imperial_length(self):
        # Key: imlengte
        # Value: provided: str - Required: str
        imperial_length_dex_entry = "| imlengte    = {}\n".format(self.imp_height)
        return imperial_length_dex_entry

    def _build_abilities(self):
        # Key: gave
        # Value: provided: List - Required: str
        abilities_dex_entry = "| gave        = "
        for i in range(len(self.abilities)):
            abilities_dex_entry += "[[{}]]".format(self.abilities[i])

            if i + 1 < len(self.abilities):
                abilities_dex_entry += "<br />"
        abilities_dex_entry += "\n"
        return abilities_dex_entry

    def _build_hidden_ability(self):
        # Key: dw
        # Value: provided: str - Required: str
        hidden_ability_dex_entry = "| dw          = {}\n".format(self.hidden_ability)
        return hidden_ability_dex_entry

    def _build_male_percentage(self):
        # Key: mannelijk
        # Value: provided: str - Required: str
        male_percentage_dex_entry = "| mannelijk   = {}\n".format(self.percent_male)
        return male_percentage_dex_entry

    def _build_egg1(self):
        # Key: ei1
        # Value: provided: str - Required: str
        egg1_dex_entry = "| ei1         = {}\n".format(self.egg_groups[0])
        return egg1_dex_entry

    def _build_egg2(self):
        # Key: ei2
        # Value: provided: str - Required: str
        egg2_dex_entry = "| ei2         = {}\n".format(self.egg_groups[1])
        return egg2_dex_entry

    def _build_evo_in(self):
        # Key: evoin
        # Value: provided: str - Required: str
        current_step = EvolutionLine.find_evolution_step(self.evo_line.first, self.name)
        evo_in = current_step.next

        if evo_in:
            evo_in_dex_entry = "| evoin       = "
            if type(evo_in) is list:
                for i in range(len(evo_in)):
                    evo_in_dex_entry += "{}".format(evo_in[i].pokemon_name)

                    if i + 1 < len(evo_in):
                        evo_in_dex_entry += "<br />"
            else:
                evo_in_dex_entry += "{}".format(evo_in.pokemon_name)
            evo_in_dex_entry += "\n"
            return evo_in_dex_entry
        return ""

    def _build_evo_from(self):
        # Key: evovan
        # Value: provided: str - Required: str
        evo_from = EvolutionLine.previous_step(self.evo_line.first, self.name)

        if evo_from:
            evo_from_dex_entry = "| evovan      = {}\n".format(evo_from.pokemon_name)
            return evo_from_dex_entry
        return ""

    def _build_evo_line(self):
        # Key: evo
        # Value: provided: tuple(name, ndex) -
        #   Required: [[Bestand:729.png|link=Brionne]][[Bestand:730.png|link=Primarina]]

        evo_line_dex_entry = "| evo         = "

        link_frame = "[[Bestand:{ndex_number}.png|link={pkmn_name}]]"

        for name, ndex_number in self.evo_line.yield_all_name_ndex():
            link = link_frame.format(ndex_number=ndex_number, pkmn_name=name)
            evo_line_dex_entry += link

        evo_line_dex_entry += "\n"
        return evo_line_dex_entry

    def create_dutch_wiki_entry(self):

        wiki_entry = ""

        # Add the prefix
        wiki_entry += self.prefix

        # Add the name
        wiki_entry += self._build_name()

        # Add japanese name
        wiki_entry += self._build_japanese_name()

        # Add ndex number
        wiki_entry += self._build_national_dex_number()

        # Check if we need to add ndex prev
        if self.ndex_prev:
            wiki_entry += self._build_prev_national_dex_number()

        # Check if we need to add ndex next
        if self.ndex_next:
            wiki_entry += self._build_next_national_dex_number()

        # Add generation
        wiki_entry += self._build_generation()

        # Add species
        wiki_entry += self._build_species()

        # Add type
        wiki_entry += self._build_primary_type()

        # Add type2 if applicable
        if self.type2:
            wiki_entry += self._build_secondary_type()

        # Add metric weight
        wiki_entry += self._build_metric_weight()
        # Add metric height
        wiki_entry += self._build_metric_length()
        # Add imperial weight
        wiki_entry += self._build_imperial_weight()
        # Add imperial height
        wiki_entry += self._build_imperial_length()

        # Abilities
        wiki_entry += self._build_abilities()

        # Hidden ability
        wiki_entry += self._build_hidden_ability()

        # Gender (if applicable)
        if self.percent_male:
            wiki_entry += self._build_male_percentage()

        # Egg groups (if applicable)
        if self.egg_groups:
            wiki_entry += self._build_egg1()
            if self.egg_groups.__len__() > 1:
                wiki_entry += self._build_egg2()

        # Evolutions
        wiki_entry += self._build_evo_in()
        wiki_entry += self._build_evo_from()
        wiki_entry += self._build_evo_line()

        # And add the suffix
        wiki_entry += self.suffix

        return wiki_entry
