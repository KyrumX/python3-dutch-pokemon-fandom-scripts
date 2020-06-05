#  Copyright (c) 2020 Aaron Beetstra
#  All rights reserved.

from utils.evolution_line import EvolutionLine, EvolutionStep


beautifly = EvolutionStep("Beautifly", 3)
silcoon = EvolutionStep("Silcoon", 2)
wurmple = EvolutionStep("Wurmple", 1)

silcoon.add_next(beautifly)
wurmple.add_next(silcoon)
evo_line_1 = EvolutionLine(wurmple)

dustox_mega = EvolutionStep("Mega Dustox", 3)
dustox2 = EvolutionStep("Dustox", 3)
cascoon2 = EvolutionStep("Cascoon", 2)
wurmple2 = EvolutionStep("Wurmple", 1)

cascoon2.add_next(dustox2)
cascoon2.add_next(dustox_mega)
wurmple2.add_next(cascoon2)
evo_line_2 = EvolutionLine(wurmple2)

evo_line_1.combine_evo_lines(evo_line_2.first)
print("!!!")
