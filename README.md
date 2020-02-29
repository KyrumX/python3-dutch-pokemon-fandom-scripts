# python3-dutch-pokemon-fandom-scripts
Some scripts which are useful to generate data/templates for the Dutch Pokémon Fandom

## Scripts:

Be sure to install the requirements.txt !

The `nl_pkmn_fandom_list_generator` script can be used to generate a generation [Pokémon lists](https://pokemon.fandom.com/nl/wiki/Lijst_van_Pok%C3%A9mon), possible types (sources): Serebii 

`python3 nl_pkmn_fandom_list_generator.py -url {the url}

Sample output for `python3 nl_pkmn_fandom_list_generator.py -url https://www.serebii.net/pokemon/gen7pokemon.shtml`:
```
{| class="wikitable sortable"  style="text-align: center; font-size: 90%"
!
! Engels
! Type (1)
! Type (2)
!  Afbeelding
 |-
| 722
| [[Rowlet]]
| {{Type|Gras}}
| {{Type|Vliegend}}
| [[Bestand:722.png]]
|-
| 723
| [[Dartrix]]
| {{Type|Gras}}
| {{Type|Vliegend}}
| [[Bestand:723.png]]
|-
| 724
| [[Decidueye]]
| {{Type|Gras}}
| {{Type|Geest}}
| [[Bestand:724.png]]
|-
| 725
| [[Litten]]
| {{Type|Vuur}}
| Geen
| [[Bestand:725.png]]
|-
| 726
| [[Torracat]]
| {{Type|Vuur}}
| Geen
| [[Bestand:726.png]]
|-
| 727
| [[Incineroar]]
| {{Type|Vuur}}
| {{Type|Duister}}
| [[Bestand:727.png]]
|-
| 728
| [[Popplio]]
| {{Type|Water}}
| Geen
| [[Bestand:728.png]]
|-
| 729
| [[Brionne]]
| {{Type|Water}}
| Geen
| [[Bestand:729.png]]
|-
|}
```
