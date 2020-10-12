#  Copyright (c) 2020 Aaron Beetstra
#  All rights reserved.
from string import ascii_uppercase

from utils.evolution_line import EvolutionLine


class PokedexEntry:
    prefix = "{{PokémonInfobox\n"
    suffix = "}}"

    prefix_multi_forms = """<div align="right"><tabber>\n"""
    delimiter_multi_forms = "|-|\n"
    suffix_multi_forms = "</tabber></div>"

    def __init__(self,
                 name: str,
                 form_name: str,
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
                 egg_groups: list,
                 color: str,
                 body: str,
                 kanto_num: str,
                 johto_num: str,
                 hoenn_num: str,
                 sinnoh_num: str,
                 unova_num: str,
                 kalos_num: str,
                 alola_num: str,
                 galar_num: str):
        self.name = name
        self.form_name = form_name
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
        self.color = color
        self.body = body
        self.kanto_num = kanto_num
        self.johto_num = johto_num
        self.hoenn_num = hoenn_num
        self.sinnoh_num = sinnoh_num
        self.unova_num = unova_num
        self.kalos_num = kalos_num
        self.alola_num = alola_num
        self.galar_num = galar_num

    def add_forms(self, forms: list):
        self.forms = self.forms + forms

    def _build_name(self):
        # Key: naam
        # Value: provided: str - Required: str
        name_entry = "| naam        = {}\n".format(self.name)
        return name_entry

    def build_form_name(self):
        # Format: {form_name}=\n
        # Value: provided: str - Required: str
        f_name = self.form_name
        if f_name is None:
            f_name = self.name
        form_name_entry = "{}=\n".format(f_name)
        return form_name_entry

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

    def _build_color(self):
        # Key: kleur
        # Value: provided: str - Required: str
        color_entry = "| kleur       = {}\n".format(self.color)
        return color_entry

    def _build_body(self):
        # Key: lichaam
        # Value: provided: str - Required: str
        body_entry = "| lichaam     = {}\n".format(self.body)
        return body_entry

    def _build_kanto_dex(self):
        # Key: dexkanto
        # Value: provided: str - Required: str
        kanto_dex_num_entry = "| dexkanto    = {}\n".format(self.kanto_num)
        return kanto_dex_num_entry

    def _build_johto_dex(self):
        # Key: dexjohto
        # Value: provided: str - Required: str
        johto_dex_num_entry = "| dexjohto    = {}\n".format(self.johto_num)
        return johto_dex_num_entry

    def _build_hoenn_dex(self):
        # Key: dexhoenn
        # Value: provided: str - Required: str
        hoenn_dex_num_entry = "| dexhoenn    = {}\n".format(self.hoenn_num)
        return hoenn_dex_num_entry

    def _build_sinnoh_dex(self):
        # Key: dexsinnoh
        # Value: provided: str - Required: str
        sinnoh_dex_num_entry = "| dexsinnoh   = {}\n".format(self.sinnoh_num)
        return sinnoh_dex_num_entry

    def _build_unova_dex(self):
        # Key: dexunova
        # Value: provided: str - Required: str
        unova_dex_num_entry = "| dexunova    = {}\n".format(self.unova_num)
        return unova_dex_num_entry

    def _build_kalos_dex(self):
        # The Kalos dex is divided into smaller parts, e.g. Central, Mountain, etc.
        # TODO: ADD THIS
        raise NotImplementedError()

    def _build_alola_dex(self):
        # Key: dexalola
        # Value: provided: str - Required: str
        alola_dex_num_entry = "| dexalola    = {}\n".format(self.alola_num)
        return alola_dex_num_entry

    def _build_galar_dex(self):
        # Key: dexgalar
        # Value: provided: str - Required: str
        galar_dex_num_entry = "| dexgalar    = {}\n".format(self.galar_num)
        return galar_dex_num_entry

    def create_dutch_wiki_entry(self):

        if self.forms:
            return self._create_dutch_wiki_entry_forms()
        return self._create_dutch_wiki_entry()

    def _create_dutch_wiki_entry(self):

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

        # Add regional dex numbers, when applicable
        if self.kanto_num:
            wiki_entry += self._build_kanto_dex()
        if self.johto_num:
            wiki_entry += self._build_johto_dex()
        if self.hoenn_num:
            wiki_entry += self._build_hoenn_dex()
        if self.sinnoh_num:
            wiki_entry += self._build_sinnoh_dex()
        if self.unova_num:
            wiki_entry += self._build_unova_dex()
        if self.alola_num:
            wiki_entry += self._build_alola_dex()
        if self.galar_num:
            wiki_entry += self._build_galar_dex()

        # Add metric weight
        wiki_entry += self._build_metric_weight()
        # Add metric height
        wiki_entry += self._build_metric_length()
        # Add imperial weight
        wiki_entry += self._build_imperial_weight()
        # Add imperial height
        wiki_entry += self._build_imperial_length()

        # Add body
        wiki_entry += self._build_body()

        # Add color
        wiki_entry += self._build_color()

        # Abilities
        wiki_entry += self._build_abilities()

        # Hidden ability (if applicable)
        if self.hidden_ability:
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

    def _create_dutch_wiki_entry_forms(self):

        wiki_entry = ""

        # Add the tabber
        wiki_entry += self.prefix_multi_forms

        # Add the form name
        wiki_entry += self.build_form_name()

        # Add the base form
        wiki_entry += self._create_dutch_wiki_entry()

        # Add forms

        # Forms cannot have the same ndex on the Dutch Fandom, we append a letter to the ndex string starting with
        #   the letter B for the first form, e.g. Giratina (altered form/base) is 487, Giratina (Origin Form) is
        #   487B.
        n_ndex_suffix = 1

        for form in self.forms:

            # Add delimiter
            wiki_entry += self.delimiter_multi_forms
            form_entry = PokedexEntry(
                self.name,
                form["form"],
                self.japanese_name,
                self.generation,
                self.species,
                form["type"][0],
                form["type"][1],
                form["ability"],
                form["h_ability"],
                self.ndex_num + ascii_uppercase[n_ndex_suffix],
                self.ndex_next,
                self.ndex_prev,
                self.evo_line,
                self.percent_male,
                form["met_height"],
                form["met_weight"],
                form["imp_height"],
                form["imp_weight"],
                self.egg_groups,
                self.color,
                self.body,
                self.kanto_num,
                self.johto_num,
                self.hoenn_num,
                self.sinnoh_num,
                self.unova_num,
                self.kalos_num,
                self.alola_num,
                self.galar_num
            )

            # Add next form name
            wiki_entry += form_entry.build_form_name()

            # Build the form data
            wiki_entry += form_entry.create_dutch_wiki_entry()

            # Go to the next letter (no need to check bounds, since no Pokémon has more than 25 forms)
            n_ndex_suffix += 1

        # Add suffix
        wiki_entry += self.suffix_multi_forms

        return wiki_entry
