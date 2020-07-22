#  Copyright (c) 2020 Aaron Beetstra
#  All rights reserved.
from pokemon_dex_entries.bulbapedia.pokedex_entry_parser_strategy_bulbapedia import \
    PokedexEntryParserPokemonStrategyBulbapedia
from pokemon_dex_entries.bulbapedia.pokedex_entry_parser_strategy_form_bulbapedia import \
    PokedexEntryParserPokemonStrategyFormBulbapedia
from pokemon_dex_entries.bulbapedia.pokedex_entry_scraper_bulbapedia import PokedexEntryScraperPokemonBulbapedia


class PokedexEntryBulbapedia:

    def __init__(self, url: str):

        # Setup scraper:
        scraper = PokedexEntryScraperPokemonBulbapedia(url)

        # Scrape the data
        infobox_dict, ndex_dict, evolines, forms = scraper.generate_usable_data()

        # Generate the base form:
        parser_base = PokedexEntryParserPokemonStrategyBulbapedia(infobox_dict, ndex_dict, evolines)
        dex_entry = parser_base.build_pokedex_entry()

        # Generate seperate forms if applicable:

        if forms:
            parsed_forms = []
            for form_id in forms:
                parser_form = PokedexEntryParserPokemonStrategyFormBulbapedia(infobox_dict, form_id)
                parsed_forms.append(parser_form.build_pokedex_form_entry())

            # Add the forms to the Pokedex Entry:
            dex_entry.add_forms(parsed_forms)

        # Generate the output for Fandom
        output = dex_entry.create_dutch_wiki_entry()

        print(output)
