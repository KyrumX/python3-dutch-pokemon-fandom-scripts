from utils.type_translation import ENGLISH_TO_DUTCH_TYPE


class PokemonType:

    def __init__(self, types: list):
        self.type1 = ENGLISH_TO_DUTCH_TYPE[types[0]]
        self.type2 = ENGLISH_TO_DUTCH_TYPE[types[1]] if len(types) > 1 else "Geen"
