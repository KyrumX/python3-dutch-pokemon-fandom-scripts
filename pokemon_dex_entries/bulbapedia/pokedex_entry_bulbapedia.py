#  Copyright (c) 2020 Aaron Beetstra
#  All rights reserved.
from pokemon_dex_entries.bulbapedia.pokedex_entry_parser_bulbapedia import \
    PokedexEntryParserPokemonStrategyBulbapedia
from pokemon_dex_entries.bulbapedia.pokedex_entry_parser_strategy_bulbapedia_form import \
    PokedexEntryParserPokemonStrategyBulbapediaForm
from pokemon_dex_entries.bulbapedia.pokedex_entry_scraper_bulbapedia import PokedexEntryScraperPokemonBulbapedia


class PokedexEntryBulbapedia:

    def __init__(self, url: str):

        # Setup scraper:
        scraper = PokedexEntryScraperPokemonBulbapedia(url)

        # Scrape the data
        infobox_dict, ndex_dict, evolines, forms, dex_data = scraper.generate_usable_data()

        # Generate the base form:
        parser_base = PokedexEntryParserPokemonStrategyBulbapedia(infobox_dict, ndex_dict, evolines, dex_data)
        dex_entry = parser_base.build_pokedex_entry()

        # Generate seperate forms if applicable:
        if forms:
            parsed_forms = []
            for form_id in forms:
                parser_base.form_strategy = PokedexEntryParserPokemonStrategyBulbapediaForm(
                    form_id=form_id,
                    infobox_dict=parser_base.infobox_dict
                )
                parsed_forms.append(parser_base.form_strategy.build_pokedex_form_entry())

            # Add the forms to the Pokedex Entry:
            dex_entry.add_forms(parsed_forms)

        self.dex_entry = dex_entry

    def build_template(self):
        # Generate the output for Fandom
        return self.dex_entry.create_dutch_wiki_entry()

