#  Copyright (c) 2020 Aaron Beetstra
#  All rights reserved.


class EvolutionStep(object):
    """An step in an evolution line"""

    def __init__(self,
                 pokemon_name: str,
                 evo_stage: int):
        self.pokemon_name = pokemon_name
        self.next = []
        self.evo_stage = evo_stage

    def add_next(self, evolution_step):
        self.next.append(evolution_step)


class EvolutionLine:
    """An evolution line object"""

    def __init__(self, first: EvolutionStep):
        self.first = first

    @staticmethod
    def _find_evolution_step(evolution_step: EvolutionStep,
                    pokemon_name: str) -> EvolutionStep:
        if evolution_step.pokemon_name == pokemon_name:
            return evolution_step
        for next_evultion in evolution_step.next:
            result = EvolutionLine._find_evolution_step(next_evultion, pokemon_name)
            if result:
                return result

    @staticmethod
    def is_part_of_evo_line(evolution_step: EvolutionStep,
                            pokemon_name: str) -> bool:

        if evolution_step.pokemon_name == pokemon_name:
            return True
        for next_evolution in evolution_step.next:
            result = EvolutionLine.is_part_of_evo_line(next_evolution, pokemon_name)
            if result:
                return result
        return False

    def combine_evo_lines(self, second_evo_first_step: EvolutionStep):
        """Combine a secondary evolution line with this one.

        Keyword arguments:
        second_evo_first_step: EvolutionStep -- The secondary evolution line
        """
        if self.first.pokemon_name != second_evo_first_step.pokemon_name:
            raise Exception("UNEQUAL PARENTS")
        else:
            self._combine_evo_lines([self.first.pokemon_name], second_evo_first_step.next)

    def _combine_evo_lines(self, path: list, secondary: list):
        """Combine a secondary evolution line with this one recursively

        Keyword arguments:
        path: list -- The path (where we are), e.g. ['Shinx', 'Luxio']
        secondary: list -- the .next() of the secondary EvolutionLine, contains the next EvolutionStep(s)
        """
        for pkmn in secondary:
            if not EvolutionLine.is_part_of_evo_line(self.first, pkmn.pokemon_name):
                self._insert(path.copy(), pkmn.pokemon_name, pkmn.evo_stage)
            new_path = path.copy()
            new_path.append(pkmn.pokemon_name)
            self._combine_evo_lines(new_path, pkmn.next)

    def _insert(self, path: list, pkmn_name: str, evo_stage: int):
        """Insert a new EvolutionStep into the EvolutionLine object

        Keyword arguments:
        path: list -- The path (where we are), e.g. ['Shinx', 'Luxio']
        pkmn_name: str -- The Pokémon name
        evo_stage: int -- The evolution stage
        """
        current = self.first
        path.pop(0)

        while path:
            next = path.pop(0)
            print(next)
            for evo in current.next:
                if evo.pokemon_name == next:
                    current = evo
        current.add_next(
            EvolutionStep(
                pkmn_name,
                evo_stage
            )
        )