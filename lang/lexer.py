# -*- coding: utf-8 -*-

import regex
from lang.tokenizer import Tokenizer


class Lexer:

    def __init__(self):
        self.patterns = {}
        self.prefixes = []
        self.re_prefixes = []
        self.dic = {}

        # Current text counters
        self.c_dic_unknown = {}
        self.c_known = 0
        self.c_text_size = 0
        self.c_might_know = 0

    def __build_cleaner(self, pattern):
        def apply_pattern(word):
            cleared_word = ''
            # stem group of any unicode letter with specified prefix
            expression = regex.compile(
                r'(?P<prefix>\b' + pattern + r')(?P<stem>\p{L}+)')
            matched = expression.match(word)
            if matched:
                cleared_word = matched.group("stem")
            return cleared_word

        return apply_pattern

    def __put_to_dic(self, word, source):
        if word not in self.dic:
            self.dic[word] = source

    def __update_dic(self, word):
        if word not in self.c_dic_unknown:
            self.c_dic_unknown[word] = 1
        else:
            self.c_dic_unknown[word] += 1

    def __is_expandable(self, token_word):
        for clearance_function in self.re_prefixes:
            cleared_word = clearance_function(token_word)
            if cleared_word and cleared_word in self.dic:
                return True

        return False

    def __analyze_token(self, token):
        word, description = token
        word = word.lower()
        if description["type"] == "word":
            self.c_text_size += 1
            if word in self.dic:
                if self.dic[word] == "original":
                    self.c_known += 1
                    description["class"] = "known"
                else:
                    self.c_might_know += 1
                    description["class"] = "maybe"
            elif self.__is_expandable(word):
                self.c_might_know += 1
                description["class"] = "maybe"
            else:
                description["class"] = "unknown"
                self.__update_dic(word)
        return token

    def analyze(self, content):
        content = content.read()
        tokens = Tokenizer(content)
        # Reset Current text counters.
        self.c_dic_unknown = {}
        self.c_known = 0
        self.c_text_size = 0
        self.c_might_know = 0

        new_tokens = [self.__analyze_token(token) for token in tokens]
        return new_tokens, self.c_dic_unknown,\
            self.c_text_size, self.c_known, self.c_might_know

    def load_dictionary(self, content):
        content = content.read().lower()
        words = Tokenizer(content)
        for word in words:
            self.__put_to_dic(word[0], "original")

    def load_plugin(self, plugin):
        if "pattern" in plugin:
            for level in plugin["pattern"]:
                self.patterns[level] = []
                for pattern, subs in plugin["pattern"][level]:
                    p = regex.compile(pattern)
                    for sub in subs:
                        self.patterns[level].append((p, sub))
        if "prefix" in plugin:
            self.prefixes = plugin["prefix"]

    def expand_dic(self):
        # Expand for every layer of tranfsormations
        for level in sorted(self.patterns.keys()):
            keys = list(self.dic.keys())
            for word in keys:
                for p, sub in self.patterns[level]:
                    new_word = p.sub(sub, word)
                    if word != new_word:
                        self.__put_to_dic(new_word, "expanded")

        self.re_prefixes = [self.__build_cleaner(prefix)
                            for prefix in self.prefixes]