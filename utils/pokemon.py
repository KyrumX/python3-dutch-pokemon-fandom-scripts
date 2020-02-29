from utils.pokemon_type import PokemonType

class Pokemon:

    def __init__(self, name: str, ndex: int, type: PokemonType):
        self.pkmn_name = name
        self.ndex_no = ndex
        self.pkmn_type = type

    def convert_to_fandom_list_entry(self):
        body = ""

        # Add the Pokémon national dex no.
        body += "| " + self.ndex_no.__str__() + "\n"

        # Add the Pokémon name
        body += "| [[" + self.pkmn_name + "]]\n"

        # Add the Pokémon type1
        body += "| {{Type|" + self.pkmn_type.type1 + "}}\n"

        # Add the Pokémon type2
        body += "| {{Type|" + self.pkmn_type.type2 + "}}\n" if self.pkmn_type.type2 != "Geen" else "| Geen\n"

        # Add the Pokémon icon
        body += "| [[Bestand:" + self.ndex_no.__str__() + ".png]]\n"

        return body
