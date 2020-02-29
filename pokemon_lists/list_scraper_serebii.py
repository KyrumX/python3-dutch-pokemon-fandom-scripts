import re

from pokemon_lists.nl_pkmn_fandom_list import DutchPokemonFandomPokemonList
from utils.pokemon import Pokemon
from utils.pokemon_type import PokemonType
from pokemon_lists.list_scraper import ListScraper


class ListScraperSerebii(ListScraper):
    def scrape(self):
        table = self.structured_object.find('table', class_="dextable")
        mons = []
        for row in table.find_all("tr", recursive=False)[2:]:  # skipping header rows
            cells = row.find_all("td", recursive=False)

            pkmn_types = []
            for a in cells[3].find_all('a', href=True):
                pkmn_type = a['href'].split("/")[-1]
                pkmn_types.append(pkmn_type)

            pkmn = Pokemon(
                name=cells[2].text.strip(),
                ndex=int(re.sub('\D', '', cells[0].text.strip())),
                type=PokemonType(pkmn_types)
            )

            mons.append(pkmn)

        fandom_list = DutchPokemonFandomPokemonList()
        for mon in mons:
            fandom_list.add_pokemon(mon)

        return fandom_list.generate_fandom_list()

