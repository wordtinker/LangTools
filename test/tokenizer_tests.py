import unittest
from lang import tokenizer


class TokenizerTests(unittest.TestCase):
 
    def test_a_simple_hebrew_word(self):
        content = "אבא"
        tknzr = tokenizer.Tokenizer(content)
        result = [w for w in tknzr]
        self.assertEqual(result, [('אבא', {'type': 'word'})])

    def test_two_hebrew_words_and_a_space(self):
        content = "אבא אמא"
        tknzr = tokenizer.Tokenizer(content)
        result = [w for w in tknzr]
        self.assertEqual(result, [
            ('אבא', {'type': 'word'}),
            (' ', {'type': 'non_word'}),
            ('אמא', {'type': 'word'})])

    def test_a_hebrew_word_and_a_dot(self):
        content = "אבא."
        tknzr = tokenizer.Tokenizer(content)
        result = [w for w in tknzr]
        self.assertEqual(result, [
            ('אבא', {'type': 'word'}),
            ('.', {'type': 'non_word'})])

    def test_a_hebrew_word_in_single_quotes(self):
        content = "'אבא'"
        tknzr = tokenizer.Tokenizer(content)
        result = [w for w in tknzr]
        self.assertEqual(result, [
            ("'", {'type': 'non_word'}),
            ('אבא', {'type': 'word'}),
            ("'", {'type': 'non_word'})])

    def test_a_hebrew_word_in_single_quotes_with_quote_in_the_middle(self):
        content = "'א'בא'"
        tknzr = tokenizer.Tokenizer(content)
        result = [w for w in tknzr]
        self.assertEqual(result, [
            ("'", {'type': 'non_word'}),
            ("א'בא", {'type': 'word'}),
            ("'", {'type': 'non_word'})])

    def test_a_hebrew_word_in_double_quotes(self):
        content = '"אבא"'
        tknzr = tokenizer.Tokenizer(content)
        result = [w for w in tknzr]
        self.assertEqual(result, [
            ('"', {'type': 'non_word'}),
            ("אבא", {'type': 'word'}),
            ('"', {'type': 'non_word'})])

    def test_a_hebrew_word_in_double_quotes_with_quote_in_the_middle(self):
        content = '"אב"א"'
        tknzr = tokenizer.Tokenizer(content)
        result = [w for w in tknzr]
        self.assertEqual(result, [
            ('"', {'type': 'non_word'}),
            ('אב"א', {'type': 'word'}),
            ('"', {'type': 'non_word'})])

    def test_a_hebrew_word_with_geresh(self):
        # print(hex(ord("׳")))
        content = 'צ׳ק'
        tknzr = tokenizer.Tokenizer(content)
        result = [w for w in tknzr]
        self.assertEqual(result, [
            ('צ׳ק', {'type': 'word'})])

    def test_a_hebrew_word_with_gershaim(self):
        # print(hex(ord("״")))
        content = 'צ״ק'
        tknzr = tokenizer.Tokenizer(content)
        result = [w for w in tknzr]
        self.assertEqual(result, [
            ('צ״ק', {'type': 'word'})])