import unittest
import os
import json
from lang.lexer import Lexer


class PseudoFile:

    def __init__(self, word):
        self.word = word

    def read(self):
        return self.word


class Test:

    class PrefixTest(unittest.TestCase):

        def setUp(self):
            self.lexer = Lexer()
            plugin_name = os.path.join(os.getcwd(), 'plugins', 'Hebrew.json')
            with open(plugin_name, "r") as file:
                plugin = json.loads(file.read())
            self.lexer.load_plugin(plugin)
            self.lexer.dic[self.origin] = 'original'

        def tearDown(self):
            self.origin = ''
            self.exp = ''
            self.lexer = None

        def test_prefix(self):
            word = PseudoFile(self.exp)
            result, *_ = self.lexer.analyze(word)
            expected = [(self.exp, {'class': 'maybe', 'type': 'word'})]
            self.assertEqual(expected, result)


class TestL(Test.PrefixTest):

    def setUp(self):
        self.origin = 'כלב'
        self.exp = 'לכלב'
        super().setUp()


class TestHa(Test.PrefixTest):

    def setUp(self):
        self.origin = 'כלב'
        self.exp = 'הכלב'
        super().setUp()


class TestBa(Test.PrefixTest):

    def setUp(self):
        self.origin = 'כלב'
        self.exp = 'בכלב'
        super().setUp()


class TestLeBa(Test.PrefixTest):

    def setUp(self):
        self.origin = 'כלב'
        self.exp = 'לבכלב'
        super().setUp()


class TestMe(Test.PrefixTest):

    def setUp(self):
        self.origin = 'כלב'
        self.exp = 'מכלב'
        super().setUp()


class TestMeHa(Test.PrefixTest):

    def setUp(self):
        self.origin = 'כלב'
        self.exp = 'מהכלב'
        super().setUp()


class TestKe(Test.PrefixTest):

    def setUp(self):
        self.origin = 'כלב'
        self.exp = 'ככלב'
        super().setUp()


class TestKeHa(Test.PrefixTest):

    def setUp(self):
        self.origin = 'כלב'
        self.exp = 'כהכלב'
        super().setUp()


class TestKshe(Test.PrefixTest):

    def setUp(self):
        self.origin = 'כלב'
        self.exp = 'כשכלב'
        super().setUp()


class TestKsheHa(Test.PrefixTest):

    def setUp(self):
        self.origin = 'כלב'
        self.exp = 'כשהכלב'
        super().setUp()


class TestShe(Test.PrefixTest):

    def setUp(self):
        self.origin = 'כלב'
        self.exp = 'שכלב'
        super().setUp()


class TestSheHa(Test.PrefixTest):

    def setUp(self):
        self.origin = 'כלב'
        self.exp = 'שהכלב'
        super().setUp()


class TestVe(Test.PrefixTest):

    def setUp(self):
        self.origin = 'כלב'
        self.exp = 'וכלב'
        super().setUp()


class TestVeHa(Test.PrefixTest):

    def setUp(self):
        self.origin = 'כלב'
        self.exp = 'והכלב'
        super().setUp()


class TestUva(Test.PrefixTest):

    def setUp(self):
        self.origin = 'כלב'
        self.exp = 'ובכלב'
        super().setUp()


class TestVeLe(Test.PrefixTest):

    def setUp(self):
        self.origin = 'כלב'
        self.exp = 'ולכלב'
        super().setUp()


class TestULeVa(Test.PrefixTest):

    def setUp(self):
        self.origin = 'כלב'
        self.exp = 'ולבכלב'
        super().setUp()


class TestVeMa(Test.PrefixTest):

    def setUp(self):
        self.origin = 'כלב'
        self.exp = 'ומכלב'
        super().setUp()


class TestVeMeHa(Test.PrefixTest):

    def setUp(self):
        self.origin = 'כלב'
        self.exp = 'ומהכלב'
        super().setUp()


class TestVeKe(Test.PrefixTest):

    def setUp(self):
        self.origin = 'כלב'
        self.exp = 'וככלב'
        super().setUp()


class TestVeKeHa(Test.PrefixTest):

    def setUp(self):
        self.origin = 'כלב'
        self.exp = 'וכהכלב'
        super().setUp()


class TestVeKshe(Test.PrefixTest):

    def setUp(self):
        self.origin = 'כלב'
        self.exp = 'וכשכלב'
        super().setUp()


class TestVeKsheHa(Test.PrefixTest):

    def setUp(self):
        self.origin = 'כלב'
        self.exp = 'וכשהכלב'
        super().setUp()


class TestVeShe(Test.PrefixTest):

    def setUp(self):
        self.origin = 'כלב'
        self.exp = 'ושכלב'
        super().setUp()


class TestVeSheHa(Test.PrefixTest):

    def setUp(self):
        self.origin = 'כלב'
        self.exp = 'ושהכלב'
        super().setUp()


class TestTa(Test.PrefixTest):

    def setUp(self):
        self.origin = 'כלב'
        self.exp = "ת'כלב"
        super().setUp()


class TestSheBa(Test.PrefixTest):

    def setUp(self):
        self.origin = 'כלב'
        self.exp = 'שבכלב'
        super().setUp()


class TestVeSheBa(Test.PrefixTest):

    def setUp(self):
        self.origin = 'כלב'
        self.exp = 'ושבכלב'
        super().setUp()


class TestKsheBa(Test.PrefixTest):

    def setUp(self):
        self.origin = 'כלב'
        self.exp = 'כשבכלב'
        super().setUp()


class TestVeSheKshe(Test.PrefixTest):

    def setUp(self):
        self.origin = 'כלב'
        self.exp = 'שכשכלב'
        super().setUp()


class TestVeSheKsheHa(Test.PrefixTest):

    def setUp(self):
        self.origin = 'כלב'
        self.exp = 'שכשהכלב'
        super().setUp()


class TestVeSheLe(Test.PrefixTest):

    def setUp(self):
        self.origin = 'כל'
        self.exp = 'שלכל'
        super().setUp()
