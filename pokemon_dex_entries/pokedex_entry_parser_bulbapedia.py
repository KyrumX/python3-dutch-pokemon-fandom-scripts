#  Copyright (c) 2020 Aaron Beetstra
#  All rights reserved.
import re

from pokemon_dex_entries.pokedex_entry_parser import PokedexEntryParser
from utils.color_translation import ENGLISH_TO_DUTCH_COLOR
from utils.egg_groups_translation import ENGLISH_TO_DUTCH_EGG_GROUP
from utils.evolution_line import EvolutionLine, EvolutionStep
from utils.gen_translation import ENGLISH_TO_DUTCH_GEN
from utils.gender_conversion import GENDER_DECIMAL_TO_MALE_PERCENTAGE
from utils.list_to_dict import str_list_to_dict
from utils.type_translation import ENGLISH_TO_DUTCH_TYPE


class PokedexEntryParserPokemonBulbapedia(PokedexEntryParser):
    """On the edit pages, Bulbapedia provides a structure we can use.
    Almost all data we need can be found inside the infobox, which uses the following structure:
        {{Pokémon Infobox
        |name=Dragapult
        |jname=ドラパルト
        |jtranslit=Doraparuto
        ...
        }}
    We grab this and convert it to a dict for our usage.

    Other information we need: prev, next from the national dex, evolution
    """

    def __init__(self, url: str):
        super().__init__(url)

        text_area_text = self.structured_object.find("textarea", class_="mw-editfont-default").text

        # Grab the Pokémon info box and convert to a list
        info_box_raw = text_area_text.partition("{{Pokémon Infobox")[2].partition("\'\'\'")[0].replace("\n", "")[:-2]
        info_box = re.split(r'\|+(?![^{{]*}})', info_box_raw)

        # Grab the Pokémon PrevNext box and convert to a list
        prev_next_box = text_area_text.partition("{{PokémonPrevNext/Pokémon")[2].partition("}}")[0].split("|")

        # To get the evolution line we need to get another part of the page.
        #   This is found between ===Evolution=== and ===Forms=== or ===Sprites===

        if "===Forms===" in text_area_text:
            evolution_box = text_area_text.partition("===Evolution===")[2].partition("===Forms===")[0]
        else:
            evolution_box = text_area_text.partition("===Evolution===")[2].partition("===Sprites===")[0]

        # So I couldn't get regex to work with dotall and \n\n (it would always see the entire object as one,
        #   rather than finding multiple occurrences...), so dirty workaround I guess
        evolution_box = evolution_box.replace("\n\n", "ENDHERE")
        evolution_box = evolution_box.replace("\n", "")
        evolution_box = evolution_box.replace("ENDHERE", "\n")

        # For Gen VIII Sprites are commented out, replace it with a newline to make it match all previous gens (regex)
        evolution_box = evolution_box.replace("<!--", "\n")

        # Pattern to grab all evo boxes if there are multiple
        regex_pattern_individual_evo_boxes = r"{{Evobox(.*)}}\n"

        self.raw_pokemon_evolution_lines = re.findall(regex_pattern_individual_evo_boxes, evolution_box, re.IGNORECASE)

        # Bulbapedia uses "=" to split between the key and value
        self.infobox_dict = str_list_to_dict(info_box, "=")
        self.prev_next_dict = str_list_to_dict(prev_next_box, "=")

    def parse_pokemon_name(self):
        # Grab the Pokémon name, found inside the infobox dict
        # key: "name"
        return self.infobox_dict["name"]

    def parse_pokemon_japanese_name(self):
        # Grab the Japanese name, found inside the infobox dict
        # keys: "jname" and "tmname"
        return self.infobox_dict["jname"] + " " + self.infobox_dict["tmname"]

    def parse_pokemon_generation(self):
        # Grab the Pokémon generation, found inside the infobox dict
        # key: "generation"
        return ENGLISH_TO_DUTCH_GEN[self.infobox_dict["generation"]]

    def parse_pokemon_types(self):
        # Grab the Pokémon type(s), found inside the infobox dict
        # keys: "type1" and optionally "type2"
        primary_type = self.infobox_dict["type1"]

        if "type2" in self.infobox_dict:
            secondary_type = self.infobox_dict["type2"]
            return [ENGLISH_TO_DUTCH_TYPE[primary_type.lower()], ENGLISH_TO_DUTCH_TYPE[secondary_type.lower()]]
        else:
            return [ENGLISH_TO_DUTCH_TYPE[primary_type.lower()], None]

    def parse_pokemon_species(self):
        # Grab the Pokémon species, found inside the infobox dict
        # key: "category"

        return self.translator.translate(self.infobox_dict["category"], src="en", dest="nl").text.capitalize()

    def parse_pokemon_abilities(self):
        # Grab the Pokémon abilities, found inside the infobox dict
        # All keys that contain "ability" except "abilityd", "abilitycold", "abilityn" and "abilitylayout"

        abilities = []
        excluded_keys = ["abilityd", "abilitycold", "abilitylayout", "abilityn"]

        for key, value in self.infobox_dict.items():
            if "ability" in key and key not in excluded_keys:
                abilities.append(value)

        return abilities

    def parse_pokemon_hidden_ability(self):
        # Grab the Pokémon hidden ability (if it has one), found inside the infobox dict
        # key: "abilityd"

        if "abilityd" in self.infobox_dict:
            return self.infobox_dict["abilityd"]

    def parse_pokemon_national_dex_number(self):
        # Grab the Pokémon national dex number, found inside the infobox dict
        # key: "ndex"
        return self.infobox_dict["ndex"]

    def parse_pokemon_national_dex_next(self):
        # Grab the Pokémon national dex next, found inside the prev_next box dict
        # key: "next" and check if "nextnum" isn't 001 (since Bulbapedia loops from last to first)
        if "next" in self.prev_next_dict and self.prev_next_dict["nextnum"] != "001":
            return self.prev_next_dict["next"]

    def parse_pokemon_national_dex_previous(self):
        # Grab the Pokémon national dex next, found inside the prev_next box dict
        # key: "prev" and check if "nextnum" isn't 002 (since Bulbapedia loops from last to first)
        if "prev" in self.prev_next_dict and self.prev_next_dict["nextnum"] != "002":
            return self.prev_next_dict["prev"]

    @staticmethod
    def _create_evo_line(evo_dict: dict) -> EvolutionLine:
        # normal_path:
        #   any path that follows a basic succession: a --> b --> c OR a --> b OR a
        normal_path = ["name1", "name2", "name3"]

        # one_split_two_path:
        #   a --> b
        #    \--> c
        one_split_two_path = ["name1", "name2a", "name2b"]

        # one_one_split_two_path:
        #   a --> b --> c
        #          \--> d
        one_one_split_two_path = ["name1", "name2", "name3", "name3a"]

        # one_split_two_two_path:
        #   a --> b --> d
        #    \--> c --> e
        one_split_two_two_path = ["name1", "name2", "name2a", "name3", "name3a"]

        paths = []
        evo_keys = ["name{}", "name{}a", "name{}b"]

        # Detect which path type we are dealing with
        list_of_keys = list(evo_dict.keys())

        type = "normal"

        # one_split_two_two_path?
        if set(one_split_two_two_path).issubset(list_of_keys):
            type = "one_split_two_two_path"
        elif set(one_one_split_two_path).issubset(list_of_keys):
            type = "one_one_split_two_path"
        elif set(one_split_two_path).issubset(list_of_keys):
            type = "one_split_two_path"

        if type == "normal":
            evo_steps = []
            for i in range(1, 5):
                name_key = "name{}".format(i.__str__())
                ndex_key = "no{}".format(i.__str__())
                if name_key in evo_dict:
                    evo_steps.append(EvolutionStep(evo_dict[name_key], evo_dict[ndex_key], evo_stage=i))
            parent = evo_steps.pop(0)
            current_parent = parent
            while evo_steps:
                temp = evo_steps.pop(0)
                current_parent.add_next(temp)
                current_parent = temp
            return EvolutionLine(parent)
        elif type == "one_split_two_path":
            child_a = EvolutionStep(pokemon_name=evo_dict["name2a"],
                                    ndex=evo_dict["no2a"],
                                    evo_stage=2)
            child_b = EvolutionStep(pokemon_name=evo_dict["name2b"],
                                    ndex=evo_dict["no2b"],
                                    evo_stage=2)
            parent = EvolutionStep(pokemon_name=evo_dict["name1"],
                                   ndex=evo_dict["no1"],
                                   evo_stage=1)
            parent.add_next(child_a)
            if not child_b.pokemon_name == child_a.pokemon_name:
                parent.add_next(child_b)
            return EvolutionLine(parent)
        elif type == "one_one_split_two_path":
            # TODO: Remove some duplicated code between one_one_split_two and one_two_two.
            parent = EvolutionStep(pokemon_name=evo_dict["name1"],
                                   ndex=re.findall(r'\d+', evo_dict["sprite1"])[0],  # Extract the ndex: 703Name
                                   evo_stage=1)
            child = EvolutionStep(pokemon_name=evo_dict["name2"],
                                  ndex=re.findall(r'\d+', evo_dict["sprite2"])[0],  # Extract the ndex: 703Name
                                  evo_stage=2)
            child_child_a = EvolutionStep(pokemon_name=evo_dict["name3"],
                                          ndex=re.findall(r'\d+', evo_dict["sprite3"])[0],  # Extract the ndex: 703Name
                                          evo_stage=3)
            child_child_b = EvolutionStep(pokemon_name=evo_dict["name3a"],
                                          ndex=re.findall(r'\d+', evo_dict["sprite3a"])[0],  # Extract the ndex: 703Name
                                          evo_stage=3)
            child.add_next(child_child_a)
            child.add_next(child_child_b)
            parent.add_next(child)
            return EvolutionLine(parent)
        elif type == "one_split_two_two_path":
            parent = EvolutionStep(pokemon_name=evo_dict["name1"],
                                   ndex=re.findall(r'\d+', evo_dict["sprite1"])[0],  # Extract the ndex: 703Name
                                   evo_stage=1)
            child_a = EvolutionStep(pokemon_name=evo_dict["name2"],
                                    ndex=re.findall(r'\d+', evo_dict["sprite2"])[0],  # Extract the ndex: 703Name
                                    evo_stage=2)
            child_b = EvolutionStep(pokemon_name=evo_dict["name2a"],
                                    ndex=re.findall(r'\d+', evo_dict["sprite2a"])[0],  # Extract the ndex: 703Name
                                    evo_stage=2)
            child_child_a = EvolutionStep(pokemon_name=evo_dict["name3"],
                                          ndex=re.findall(r'\d+', evo_dict["sprite3"])[0],  # Extract the ndex: 703Name
                                          evo_stage=3)
            child_child_b = EvolutionStep(pokemon_name=evo_dict["name3a"],
                                          ndex=re.findall(r'\d+', evo_dict["sprite3a"])[0],  # Extract the ndex: 703Name
                                          evo_stage=3)

            child_a.add_next(child_child_a)
            child_b.add_next(child_child_b)
            parent.add_next(child_a)
            parent.add_next(child_b)
            return EvolutionLine(parent)

    def parse_pokemon_evo_line(self) -> EvolutionLine:
        # Create an evolution line for this Pokémon

        # Some Pokémon cannot be done. Bulbapedia writers deemed these too complex, their evo logic is not
        #   present in the data we have, rather this data is found somewhere else on their site.
        skip = ["Eevee", "Tyrogue", "Feebas", "Milotic", "Nincada"]
        if self.parse_pokemon_name() in skip:
            return EvolutionLine(first=EvolutionStep(pokemon_name=self.parse_pokemon_name(), ndex="???", evo_stage=1))

        # First create a usable format, we only need the names from the infobox, put them in a dict:
        raw_evo_lines = []
        needed_keys = ["name{}", "name{}a", "name{}b", "sprite{}", "sprite{}a", "sprite{}b", "no{}", "no{}a", "no{}b"]
        for raw_pokemon_evolution_line in self.raw_pokemon_evolution_lines:
            temp = raw_pokemon_evolution_line.split("|", 1)[1]
            dict = {}
            for i in range(1, 5):
                for key in needed_keys:
                    formatted_key = key.format(str(i))
                    pattern = r"\b" + re.escape(formatted_key) + r"\b"
                    if re.search(pattern, temp):
                        index = temp.index(formatted_key)
                        index += len(formatted_key) + 1
                        key_value = ""
                        while temp[index] != "|":
                            key_value += temp[index]
                            index += 1
                        dict[formatted_key] = key_value
            raw_evo_lines.append(dict)

        # Some Pokémon have multiple evo lines on their pages (need to fix forms here!), call the first on our
        #   main line:
        main_line = self._create_evo_line(raw_evo_lines[0])
        # If we have more than one line, combine them together into one (again, need to fix forms, since different
        #   forms do not need to be combined!)
        if len(raw_evo_lines) > 1:
            for line in raw_evo_lines[1:]:
                secondary_line = self._create_evo_line(line)
                main_line.combine_evo_lines(secondary_line.first)

        return main_line

    def parse_pokemon_gender(self):
        # Grab the Pokémon decimal gender code, found inside the infobox dict, convert to male%
        # key: "gendercode"
        return GENDER_DECIMAL_TO_MALE_PERCENTAGE[int(self.infobox_dict["gendercode"])]

    def parse_pokemon_met_height(self) -> str:
        # Grab the Pokémon height in meters
        # key: "height-m"
        return self.infobox_dict["height-m"]

    def parse_pokemon_met_weight(self) -> str:
        # Grab the Pokémon height in kilograms
        # key: "weight-kg"
        return self.infobox_dict["weight-kg"]

    def parse_pokemon_imp_height(self) -> str:
        # Grab the Pokémon height in float inch
        # key: "height-ftin"
        return self.infobox_dict["height-ftin"]

    def parse_pokemon_imp_weight(self) -> str:
        # Grab the Pokémon height in float inch
        # key: "weight-lbs"
        return self.infobox_dict["weight-lbs"]

    def parse_pokemon_dex_color(self):
        # Grab the Pokémon dex color
        # key: "color"
        return ENGLISH_TO_DUTCH_COLOR[self.infobox_dict["color"].lower()]

    def parse_pokemon_egg_groups(self):
        # Grab the Pokémon egg group(s)
        # key: "egggroupn" for the amount, "egggroup1" and "egggroup2" (if n == 2)
        egg_groups_n = int(self.infobox_dict["egggroupn"])

        if egg_groups_n == 0:
            return ENGLISH_TO_DUTCH_EGG_GROUP["Undiscovered"]
        elif egg_groups_n == 1:
            return [ENGLISH_TO_DUTCH_EGG_GROUP[self.infobox_dict["egggroup1"].lower()]]
        else:
            return [ENGLISH_TO_DUTCH_EGG_GROUP[self.infobox_dict["egggroup1"].lower()],
                    ENGLISH_TO_DUTCH_EGG_GROUP[self.infobox_dict["egggroup2"].lower()]]

