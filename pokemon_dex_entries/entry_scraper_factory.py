#  Copyright (c) 2020 Aaron Beetstra
#  All rights reserved.
from pokemon_dex_entries.bulbapedia.pokedex_entry_scraper_bulbapedia import PokedexEntryParserPokemonBulbapedia

# TODO: FIX THIS, REMOVE PARSER SWITCH TO POKEDEX_ENTRY_{WEBSITE}
class EntryScraperFactory():
    @classmethod
    def create(cls, source_type: str, url: str):
        SOURCE_TYPE_TO_CLASS_MAP = {
            'bulbapedia': PokedexEntryParserPokemonBulbapedia,
        }

        if source_type not in SOURCE_TYPE_TO_CLASS_MAP:
            raise ValueError('Invalid source type {}'.format(source_type))

        return SOURCE_TYPE_TO_CLASS_MAP[source_type](url)