from utils.pokemon import Pokemon


class DutchPokemonFandomPokemonList:

    prefix = "{| class=\"wikitable sortable\"  style=\"text-align: center; font-size: 90%\"\n!\n! Engels\n! Type (" \
             "1)\n! Type (2)\n!  Afbeelding\n"
    suffix = "|-\n|}"

    def __init__(self):
        self.body = ""

    def add_pokemon(self, pokemon: Pokemon):
        self.body += "|-\n"

        self.body += pokemon.convert_to_fandom_list_entry()

    def generate_fandom_list(self):
        return self.prefix + self.body + self.suffix
