import argparse

import importlib

from pokemon_dex_entries.pokedex_entry_factory import PokedexEntryFactory


def main():

    print("???")

    parser = argparse.ArgumentParser(description='Scrape a website and convert the data to a pokedex entry format '
                                                 'usable by the Dutch Pokémon fandom/.')

    parser.add_argument('-url', action="store", help='Target url', required=True)
    parser.add_argument('-type', action="store", help='Source type of website being scraped, options', type=str, choices=["pokemondb"], default="pokemondb")

    args = parser.parse_args()

    scraper_class = PokedexEntryFactory().create(source_type=args.type, url=args.url)

    try:
        pokedex_entry = scraper_class.build_pokedex_entry()

        print(pokedex_entry.convert_to_dutch_wiki_template())

        print("Done! Dutch Fandom formatted text can be found in output.txt")

    except Exception as e:
        print(e)
        print("Something went wrong during scraping, the source site may have changed its format.")

if __name__ == "__main__":
   main()