#  Copyright (c) 2020 Aaron Beetstra
#  All rights reserved.


def str_list_to_dict(l: list, split_str: str) -> dict:
    # Function to convert a list to a dict
    # Example: func(["", "name=Giratina"], "=") -> {"name": "Giratina"}

    dict = {}

    for x in l:
        if not len(x) == 0 and not x is None:
            splitted = x.split(split_str)
            dict[splitted[0]] = splitted[1]

    return dict