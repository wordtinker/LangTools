# -*- coding: utf-8 -*-

import regex


class Tokenizer:
    """ Takes a string and returns iterator of tokens. """

    def __init__(self, string):
        self.string = string

    def __iter__(self):
        # Calculating string bounds
        self.pos = 0
        self.length = len(self.string)
        self.word = regex.compile(
            r"""(
            \p{L}+   # any character of: UTF macro 'Letter' 1 or more times
            ([״'׳"]      # \' or ׳(0x5f3) symbol exactly once
            \p{L}+   # any character of: UTF macro 'Letter' 1 or more times
            )?       # optionally
            )""", regex.VERBOSE)
        return self

    def __next__(self):
        if self.pos >= self.length:  # Reached the end of string
            raise StopIteration
        else:
            match = self.word.search(self.string, self.pos)
            if not match:  # No words left, will return some trailing characters
                old_start = self.pos
                self.pos = self.length
                return self.string[old_start:], {"type": "non_word"}
            start = match.start()
            end = match.end()
            if self.pos != start:  # Some non-letters are left before word
                old_start = self.pos
                self.pos = start
                return self.string[old_start:start], {"type": "non_word"}
            else:
                self.pos = end
                return self.string[start:end], {"type": "word"}