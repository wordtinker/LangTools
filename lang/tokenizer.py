# -*- coding: utf-8 -*-

import regex


class Tokenizer:
    """ Takes a string and returns iterator of tokens. """

    def __init__(self, string):
        self.string = string

    def __iter__(self):
        # Calculating string bounds
        position = 0
        self.length = len(self.string)
        self.word = regex.compile(
            r"""(
            \p{L}+   # any character of: UTF macro 'Letter' 1 or more times
            ([״'׳"]      # \' or ׳(0x5f3) symbol exactly once
            \p{L}+   # any character of: UTF macro 'Letter' 1 or more times
            )?       # optionally
            )""", regex.VERBOSE)
        while position < self.length:
            match = self.word.search(self.string, position)
            if not match:  # No words left, will return some trailing characters
                yield self.string[position:], {"type": "non_word"}
                position = self.length
            else:
                start = match.start()
                end = match.end()
                if position != start:  # Some non-letters are left before word
                    yield self.string[position:start], {"type": "non_word"}
                yield self.string[start:end], {"type": "word"}
                position = end
