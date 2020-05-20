#  Copyright (c) 2020 Aaron Beetstra
#  All rights reserved.


class EvolutionStep(object):
    """An step in an evolution line"""
    # TODO: EVO_STAGE CAN BE REMOVED AND REPLACED BY A FUNCTION

    def __init__(self,
                 pokemon_name: str):
        self.pokemon_name = pokemon_name
        self.next = []

    def _add_next(self, evolution_step):
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

    def _create_pretty_evolution_line(self):
        raise NotImplementedError()