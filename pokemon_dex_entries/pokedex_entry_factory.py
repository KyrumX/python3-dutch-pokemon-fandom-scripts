from pokemon_dex_entries.pokemondb.pokedex_entry_parser_pokemondb import PokedexEntryParserPokemonDB


class PokedexEntryFactory():
    @classmethod
    def create(cls, source_type: str, url: str):
        SOURCE_TYPE_TO_CLASS_MAP = {
            'pokemondb': PokedexEntryParserPokemonDB,
        }

        if source_type not in SOURCE_TYPE_TO_CLASS_MAP:
            raise ValueError('Invalid source type {}'.format(source_type))

        return SOURCE_TYPE_TO_CLASS_MAP[source_type](url)