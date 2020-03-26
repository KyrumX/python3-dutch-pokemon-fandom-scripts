import argparse

import importlib

from pokemon_lists.list_scraper_factory import ListScraperFactory


def main():

    parser = argparse.ArgumentParser(description='Scrape a website and convert the data to a pokedex entry format '
                                                 'usable by the Dutch Pokémon fandom/.')

    parser.add_argument('-url', action="store", help='Target url', required=True)
    parser.add_argument('-type', action="store", help='Source type of website being scraped, options', type=str, choices=["pokemondb"], default="pokemondb")

    args = parser.parse_args()

    scraper_class = ListScraperFactory().create(source_type=args.type, url=args.url)

    try:
        formatted_fandom_list = scraper_class.scrape()

        text_file = open("output.txt", "w")
        text_file.write(formatted_fandom_list)
        text_file.close()

        print("Done! Dutch Fandom formatted text can be found in output.txt")

    except Exception as e:
        print("Something went wrong during scraping, the source site may have changed its format.")

if __name__ == "__main__":
   main()
