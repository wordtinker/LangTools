# -*- coding: utf-8 -*-
from json import *

patterns = {"pattern":
            {
                0: [["$",  # end of the word
                     ["s", "'", "'s", "es", "ed","ing"]],
                    ["y$", ["ies","ied"]],
                    ["e$", ["ed", "ing"]]
                    ]
            },
            "prefix": []}


with open("English.json", mode='w', encoding='utf-8') as file:
            file.write(dumps(patterns))
