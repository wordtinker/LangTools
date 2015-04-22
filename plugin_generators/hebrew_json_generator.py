# -*- coding: utf-8 -*-
from json import *
from collections import OrderedDict

patterns = OrderedDict()
patterns["pattern"] = {
    0: [
        ["[^ןםךףץה]$", ['\g<0>']],
        ["ם$", ['\g<0>', 'מ']],  # \g<0> -- use pattern unmodified on the next
        ["ן$", ['\g<0>', 'נ']],   # level
        ["ך$", ['\g<0>', 'כ']],
        ["ף$", ['\g<0>', 'פ']],
        ["ץ$", ['\g<0>', 'צ']],
        ["ה$", ['\g<0>', '']]  # strip to masculine form
    ],
    1: [["ה$",  # Special cases for hey
         ["תך", "תו", "תה", "ית", "יתי", "תכם", "תכן", "תנו", "יתם", "יתן"]],
        ["^.+[^ןםךףץה]$",  # sofits not preceding end of word
         ["\g<0>ים", "\g<0>ת", "\g<0>ות", "\g<0>ה", "\g<0>תי",
          "\g<0>נו", "\g<0>ו", "\g<0>תם", "\g<0>תן", "\g<0>י",
          "\g<0>ך", "\g<0>כם", "\g<0>כן", "\g<0>ם", "\g<0>ן",
          "\g<0>יי", "\g<0>יך", "\g<0>ייך", "\g<0>יו",
          "\g<0>יה", "\g<0>ינו", "\g<0>יכם", "\g<0>יכן",
          "\g<0>יהם", "\g<0>יהן", "\g<0>ותי", "\g<0>ותיך",
          "\g<0>ותייך", "\g<0>ותיו", "\g<0>ותיה", "\g<0>ותינו",
          "\g<0>ותיכם", "\g<0>ותיכן", "\g<0>ותיהם", "\g<0>ותיהן", "\g<0>ית"]],
        ["י(?P<beg>.+[^מנפכצ]$)",
         ["א\g<beg>", "נ\g<beg>", "ת\g<beg>"]],  # future
        ["י(?P<beg>.{2})ו(?P<end>[^ןםךףץה]$)",  # future ephol i(?P<beginning>.+)o(?P<ending>[^h])
         ["ת\g<beg>\g<end>י", "ת\g<beg>\g<end>ו", "י\g<beg>\g<end>ו"]],
        ["י(?P<beg>.*[^ו][^ןםךףץה]$)",  # future ephal i(?P<beginning>.+[^o][^h]$)
         ["ת\g<beg>י", "ת\g<beg>ו", "י\g<beg>ו"]],
        ["י(?P<beg>.ו[^ןםךףץה]$)",  # future aynvav
         ["ת\g<beg>י", "ת\g<beg>ו", "י\g<beg>ו"]],
        ["י(?P<beg>.+)ה$",
         ["ת\g<beg>י", "ת\g<beg>ו", "י\g<beg>ו"]],
        ["(?P<beg>^ה.+)י(?P<end>[^ןםךףץה]$)",
         ["\g<beg>\g<end>ת", "\g<beg>\g<end>תי", "\g<beg>\g<end>נו",
          "\g<beg>\g<end>תם", "\g<beg>\g<end>תן"]],  # hifil (?P<beginning>^h.+)i(?P<ending>[^a])
        ["(?P<beg>^ה.+)י(?P<end>נ$)", ["\g<beg>\g<end>ו"]]  # hifil double nun special case
    ]
}

patterns["prefix"] = ["ה", "ל", "ב", "לב", "מ", "מה", "כ", "כה", "כש",
                      "כשה", "ש", "שה", "ו", "וה", "וב", "ול", "ולב", "ומ",
                      "ומה", "וכ", "וכה", "וכש", "וכשה", "וש", "ושה", "ת'",
                      "שב", "ושב", "כשב", "שכש", "שכשה", "של"
                      ]

with open("Hebrew.json", mode='w', encoding='utf-8') as file:
    file.write(dumps(patterns))