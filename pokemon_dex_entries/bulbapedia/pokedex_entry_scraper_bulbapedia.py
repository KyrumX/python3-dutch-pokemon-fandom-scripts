#  Copyright (c) 2020 Aaron Beetstra
#  All rights reserved.
import re

from pokemon_dex_entries.pokedex_entry_scraper import PokedexEntryScraper
from utils.list_to_dict import str_list_to_dict


class PokedexEntryScraperPokemonBulbapedia(PokedexEntryScraper):
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

    # List of forms we can safely ignore:
    bulbapedia_ignored_forms = [
        "cosplay",
        "in a cap",
        "partner",
        "gigantamax",
        "spikey eared",
        "neutral mode",
        "busted form",
        "original color",
        "gulping form",
        "gorging form"
    ]

    def __init__(self, url: str):
        super().__init__(url)

    def generate_usable_data(self):
        """"
        Generate data based on the scaped HTML


        :returns infobox, the ndex prev/next box, and raw evolution lines
        :type dict, dict, list
        """
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

        raw_pokemon_evolution_lines = re.findall(regex_pattern_individual_evo_boxes, evolution_box, re.IGNORECASE)

        # Bulbapedia uses "=" to split between the key and value
        infobox_dict = str_list_to_dict(info_box, "=")
        prev_next_dict = str_list_to_dict(prev_next_box, "=")

        # Decide if we have multiple forms to deal with, key: 'forme'
        n_forms = None if 'forme' not in infobox_dict else int(infobox_dict['forme'])
        pokemon_forms = {}

        if n_forms:
            # Remove forms we don't care about:
            for i in range(1, n_forms + 1):
                key = "form{}".format(i.__str__())
                form_name = infobox_dict[key] if key in infobox_dict else None
                if form_name and not form_name.lower() in self.bulbapedia_ignored_forms:
                    pokemon_forms[i] = form_name

        n_forms = len(pokemon_forms)
        if 1 in pokemon_forms:
            # Form1 might be seen as a different form (due to name), but to us it's just the base form.
            #   So we need to verify whether there are actually more forms if we remove form1.
            del pokemon_forms[1]

        # There are multiple text partitions called 'Pokédex entries', we only care about the one in
        #   the 'Game data' partition, the dex data is then found in the 'Pokédex entries' partition
        #   Remove all newlines to make splitting more consistent (as bulbapedia sometimes uses \n followed by a space)
        game_data_partition = text_area_text.partition("==Game data==")[2].partition("==Trivia==")[0]
        dex_partition = game_data_partition.partition("===Pokédex entries===")[2].partition("{{Dex/Footer}}")[0] \
            .replace('\n', '') \
            .split("|}|}")

        local_dex = self._extract_local_dex_data(dex_partition)

        return infobox_dict, prev_next_dict, raw_pokemon_evolution_lines, pokemon_forms

    @staticmethod
    def _extract_local_dex_data(local_data_entries):
        # Their data works as follows:
        #   regN='region' numN='local dex number'
        #   Now sometimes regN is present without a numN to match it, meaning that the Pokémon did have a local dex
        #   description but not a local dex number. So skip those, since we only want the number.
        #   Sample: ...|reg1=Kalos|num1=025|...

        results = {}

        region_key = "reg{}"
        number_key = "num{}"
        for entry in local_data_entries:
            # Loop over all regN, take a maximum of 3 as there is yet to be a generation with more than 2 regions
            for i in range(1, 4):

                # Create the keys we are looking for, e.g. reg1 and num1
                reg_key = region_key.format(i.__str__())
                num_key = number_key.format(i.__str__())

                # Search for the reg key, and try to grab the value between the reg key and the delimiter '|',
                #   or the ending '}}'
                #   Sample: ...reg1=Kalos|...
                reg_regex = rf'{re.escape(reg_key)}=([\w]*)((\|)|(}}))'
                reg_regex_search = re.search(reg_regex, entry)

                # If reg_regex_search is not None, then it has been found
                if reg_regex_search:
                    region = reg_regex_search.group(1)

                    # Search for the num key, and try to grab the value between the num key and the delimiter ('|'),
                    #   or the ending '}}'
                    #   Sample: ...num1=023|... / ...num1=026}}
                    num_regex = rf'{re.escape(num_key)}=([\w]*)((\|)|(}}))'
                    num_regex_search = re.search(num_regex, entry)

                    # If num_regex_search is not None, then a local dex num has been found
                    if num_regex_search:
                        if region in results:
                            results[region].append(num_regex_search.group(1))
                        else:
                            results[region] = [num_regex_search.group(1)]

                i += 1

        # Remove duplicated numbers
        return results
