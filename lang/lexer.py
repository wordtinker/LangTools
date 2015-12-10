# -*- coding: utf-8 -*-

import regex
from collections import defaultdict
from lang.tokenizer import Tokenizer


class Lexer:

    def __init__(self):
        self.patterns = {}
        self.prefixes = []
        self.dic = {}

        # Current text counters
        self.c_dic_unknown = defaultdict(int)
        self.c_known = 0
        self.c_text_size = 0
        self.c_might_know = 0

    def __put_to_dic(self, word, source):
        if word not in self.dic:
            self.dic[word] = source

    def __is_expandable(self, token_word):
        for prefix in self.prefixes:
            if (token_word.startswith(prefix) and
                    token_word[len(prefix):] in self.dic):
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
                self.c_dic_unknown[word] += 1
        return token

    def analyze(self, content):
        content = content.read()
        tokens = Tokenizer(content)
        # Reset Current text counters.
        self.c_dic_unknown.clear()
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
        last_level = len(self.patterns) - 1
        before_state = set()
        for i, level in enumerate(sorted(self.patterns.keys())):
            after_state = set()
            if i == 0:
                # On the lowest level copy initial list from Dictionary
                keys = self.dic.keys()
            else:
                # On subsequent calls copy from previous level
                keys = before_state

            for word in keys:
                # Transform the word into new form
                for p, sub in self.patterns[level]:
                    if p.search(word):
                        # Add the word only if it could be transformed
                        new_word = p.sub(sub, word)
                        after_state.add(new_word)

            if i == last_level:
                # Copy the final state to Dictionary
                for word in after_state:
                    self.__put_to_dic(word, "expanded")
            else:
                # Push it to the next level
                before_state = after_state
