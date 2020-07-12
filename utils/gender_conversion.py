# Gender Decimal values based on Gen 8
# E.g. Decimal value of 63 means 75% chance of being male.
# source: https://bulbapedia.bulbagarden.net/wiki/Personality_value#Gender

GENDER_DECIMAL_TO_MALE_PERCENTAGE = {
    0: 100,
    31: 88,
    63: 75,
    127: 50,
    191: 25,
    225: 12,
    254: 0,
    255: None,
}