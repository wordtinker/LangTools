import unittest
import json
import os
from lang.lexer import Lexer


class BaseTestCase:

    class Word(unittest.TestCase):

        def setUp(self):
            self.lexer = Lexer()
            plugin_name = os.path.join(os.getcwd(), 'plugins', 'Hebrew.json')
            with open(plugin_name, "r") as file:
                plugin = json.loads(file.read())
            self.lexer.load_plugin(plugin)
            self.lexer.dic[self.word] = 'original'
            self.lexer.expand_dic()

        def tearDown(self):
            self.word = ''
            self.stem = ''
            self.lexer = None
            self.checksum = 0

        def test_checksum(self):
            self.assertEqual(self.checksum, len(self.lexer.dic))

    class Hifil(Word):

        def test_past_1s(self):
            self.assertIn(self.stem + 'תי', self.lexer.dic)

        def test_past_2s(self):
            self.assertIn(self.stem + 'ת', self.lexer.dic)

        def test_past_1p(self):
            self.assertIn(self.stem + 'נו', self.lexer.dic)

        def test_past_2pm(self):
            self.assertIn(self.stem + 'תם', self.lexer.dic)

        def test_past_2pf(self):
            self.assertIn(self.stem + 'תן', self.lexer.dic)

    class Ephol(Word):

        def test_fut_1s(self):
            self.assertIn('א' + self.stem, self.lexer.dic)

        def test_fut_1p(self):
            self.assertIn('נ' + self.stem, self.lexer.dic)

        def test_fut_2sm(self):
            self.assertIn('ת' + self.stem, self.lexer.dic)

    class EpholReduced(Word):

        def test_fut_2sf(self):
            self.assertIn('ת' + self.stem + 'י', self.lexer.dic)

        def test_fut_2p(self):
            self.assertIn('ת' + self.stem + 'ו', self.lexer.dic)

        def test_fut_3p(self):
            self.assertIn('י' + self.stem + 'ו', self.lexer.dic)

    class Noun(Word):

        def test_with_it(self):
            self.assertIn(self.stem + 'ית', self.lexer.dic)

        def test_with_im(self):
            self.assertIn(self.stem + 'ים', self.lexer.dic)

        def test_with_t(self):
            self.assertIn(self.stem + 'ת', self.lexer.dic)

        def test_with_ot(self):
            self.assertIn(self.stem + 'ות', self.lexer.dic)

        def test_with_hey(self):
            self.assertIn(self.stem + 'ה', self.lexer.dic)

        def test_with_ti(self):
            self.assertIn(self.stem + 'תי', self.lexer.dic)

        def test_with_nu(self):
            self.assertIn(self.stem + 'נו', self.lexer.dic)

        def test_with_o(self):
            self.assertIn(self.stem + 'ו', self.lexer.dic)

        def test_with_tm(self):
            self.assertIn(self.stem + 'תם', self.lexer.dic)

        def test_with_tn(self):
            self.assertIn(self.stem + 'תן', self.lexer.dic)

        def test_with_i(self):
            self.assertIn(self.stem + 'י', self.lexer.dic)

        def test_with_h(self):
            self.assertIn(self.stem + 'ך', self.lexer.dic)

        def test_with_hm(self):
            self.assertIn(self.stem + 'כם', self.lexer.dic)

        def test_with_hn(self):
            self.assertIn(self.stem + 'כן', self.lexer.dic)

        def test_with_m(self):
            self.assertIn(self.stem + 'ם', self.lexer.dic)

        def test_with_n(self):
            self.assertIn(self.stem + 'ן', self.lexer.dic)

        def test_with_ii(self):
            self.assertIn(self.stem + 'יי', self.lexer.dic)

        def test_with_ih(self):
            self.assertIn(self.stem + 'יך', self.lexer.dic)

        def test_with_iih(self):
            self.assertIn(self.stem + 'ייך', self.lexer.dic)

        def test_with_av(self):
            self.assertIn(self.stem + 'יו', self.lexer.dic)

        def test_with_ihey(self):
            self.assertIn(self.stem + 'יה', self.lexer.dic)

        def test_with_einu(self):
            self.assertIn(self.stem + 'ינו', self.lexer.dic)

        def test_with_eihem(self):
            self.assertIn(self.stem + 'יכם', self.lexer.dic)

        def test_with_eihen(self):
            self.assertIn(self.stem + 'יכן', self.lexer.dic)

        def test_with_eihhem(self):
            self.assertIn(self.stem + 'יהם', self.lexer.dic)

        def test_with_eihhen(self):
            self.assertIn(self.stem + 'יהן', self.lexer.dic)

        def test_with_oti(self):
            self.assertIn(self.stem + 'ותי', self.lexer.dic)

        def test_with_oteiha(self):
            self.assertIn(self.stem + 'ותיך', self.lexer.dic)

        def test_with_otaiih(self):
            self.assertIn(self.stem + 'ותייך', self.lexer.dic)

        def test_with_otav(self):
            self.assertIn(self.stem + 'ותיו', self.lexer.dic)

        def test_with_oteihha(self):
            self.assertIn(self.stem + 'ותיה', self.lexer.dic)

        def test_with_oteinu(self):
            self.assertIn(self.stem + 'ותינו', self.lexer.dic)

        def test_with_oteihm(self):
            self.assertIn(self.stem + 'ותיכם', self.lexer.dic)

        def test_with_oteihn(self):
            self.assertIn(self.stem + 'ותיכן', self.lexer.dic)

        def test_with_oteihem(self):
            self.assertIn(self.stem + 'ותיהם', self.lexer.dic)

        def test_with_oteihen(self):
            self.assertIn(self.stem + 'ותיהן', self.lexer.dic)


class SimpleWord(BaseTestCase.Noun):

    def setUp(self):
        self.checksum = 37
        self.word = 'כלב'
        self.stem = 'כלב'
        super().setUp()

    def test_unmodified(self):
        self.assertIn(self.stem, self.lexer.dic)


class MemWord(BaseTestCase.Noun):

    def setUp(self):
        self.checksum = 40
        self.word = 'יום'
        self.stem = 'יומ'
        super().setUp()

    def test_unmodified(self):
        self.assertNotIn(self.stem, self.lexer.dic)


class NunWord(BaseTestCase.Noun):

    def setUp(self):
        self.checksum = 37
        self.word = 'ענן'
        self.stem = 'עננ'
        super().setUp()

    def test_unmodified(self):
        self.assertNotIn(self.stem, self.lexer.dic)


class PeiWord(BaseTestCase.Noun):

    def setUp(self):
        self.checksum = 37
        self.word = 'שרף'
        self.stem = 'שרפ'
        super().setUp()

    def test_unmodified(self):
        self.assertNotIn(self.stem, self.lexer.dic)


class KafWord(BaseTestCase.Noun):

    def setUp(self):
        self.checksum = 37
        self.word = 'דרך'
        self.stem = 'דרכ'
        super().setUp()

    def test_unmodified(self):
        self.assertNotIn(self.stem, self.lexer.dic)


class TsadiWord(BaseTestCase.Noun):

    def setUp(self):
        self.checksum = 37
        self.word = 'קיץ'
        self.stem = 'קיצ'
        super().setUp()

    def test_unmodified(self):
        self.assertNotIn(self.stem, self.lexer.dic)


class HeyWord(BaseTestCase.Noun):

    def setUp(self):
        self.checksum = 45
        self.word = 'שכונה'
        self.stem = 'שכונ'
        super().setUp()

    def test_unmodified(self):
        self.assertNotIn(self.stem, self.lexer.dic)

    def test_with_it(self):
        self.assertIn(self.stem + "ית", self.lexer.dic)

    def test_with_iti(self):
        self.assertIn(self.stem + "יתי", self.lexer.dic)

    def test_with_ta(self):
        self.assertIn(self.stem + "תה", self.lexer.dic)

    def test_with_inu(self):
        self.assertIn(self.stem + "ינו", self.lexer.dic)

    def test_with_itn(self):
        self.assertIn(self.stem + "יתן", self.lexer.dic)

    def test_with_itm(self):
        self.assertIn(self.stem + "יתם", self.lexer.dic)

    def test_with_th(self):
        self.assertIn(self.stem + "תך", self.lexer.dic)

    def test_with_to(self):
        self.assertIn(self.stem + "תו", self.lexer.dic)

    def test_with_tnu(self):
        self.assertIn(self.stem + "תנו", self.lexer.dic)

    def test_with_thm(self):
        self.assertIn(self.stem + "תכם", self.lexer.dic)

    def test_with_thn(self):
        self.assertIn(self.stem + "תכן", self.lexer.dic)


class EpholSimple(BaseTestCase.Ephol):

    def setUp(self):
        self.checksum = 43
        self.word = 'יכתוב'
        self.stem = 'כתוב'
        super().setUp()


class EpholSimpleShort(BaseTestCase.EpholReduced):

    def setUp(self):
        self.checksum = 43
        self.word = 'יכתוב'
        self.stem = 'כתב'
        super().setUp()


class EpholMem(BaseTestCase.Ephol):

    def setUp(self):
        self.checksum = 43
        self.word = 'יהלום'
        self.stem = 'הלום'
        super().setUp()


class EpholMemShort(BaseTestCase.EpholReduced):

    def setUp(self):
        self.checksum = 43
        self.word = 'יהלום'
        self.stem = 'הלמ'
        super().setUp()


class EpholNun(BaseTestCase.Ephol):

    def setUp(self):
        self.checksum = 43
        self.word = 'יקרון'
        self.stem = 'קרון'  # synthetic
        super().setUp()


class EpholNunShort(BaseTestCase.EpholReduced):

    def setUp(self):
        self.checksum = 43
        self.word = 'יקרון'
        self.stem = 'קרנ'  # synthetic
        super().setUp()


class EpholKaf(BaseTestCase.Ephol):

    def setUp(self):
        self.checksum = 43
        self.word = 'יהפוך'
        self.stem = 'הפוך'
        super().setUp()


class EpholkafShort(BaseTestCase.EpholReduced):

    def setUp(self):
        self.checksum = 43
        self.word = 'יהפוך'
        self.stem = 'הפכ'
        super().setUp()


class EpholPei(BaseTestCase.Ephol):

    def setUp(self):
        self.checksum = 43
        self.word = 'ישרוף'
        self.stem = 'שרוף'
        super().setUp()


class EpholPeiShort(BaseTestCase.EpholReduced):

    def setUp(self):
        self.checksum = 43
        self.word = 'ישרוף'
        self.stem = 'שרפ'
        super().setUp()


class EpholTsadi(BaseTestCase.Ephol):

    def setUp(self):
        self.checksum = 43
        self.word = 'יקפוץ'
        self.stem = 'קפוץ'
        super().setUp()


class EpholTsadiShort(BaseTestCase.EpholReduced):

    def setUp(self):
        self.checksum = 43
        self.word = 'יקפוץ'
        self.stem = 'קפצ'
        super().setUp()


class EphalSimple(BaseTestCase.Ephol, BaseTestCase.EpholReduced):

    def setUp(self):
        self.checksum = 42
        self.word = 'יגדל'
        self.stem = 'גדל'
        super().setUp()


class EphalMem(BaseTestCase.Ephol):

    def setUp(self):
        self.checksum = 42
        self.word = 'יממם'
        self.stem = 'ממם'  # Synthetic
        super().setUp()


class EphalMemShort(BaseTestCase.EpholReduced):

    def setUp(self):
        self.checksum = 42
        self.word = 'יממם'
        self.stem = 'מממ'  # Synthetic
        super().setUp()


class EphalNun(BaseTestCase.Ephol):

    def setUp(self):
        self.checksum = 42
        self.word = 'יננן'
        self.stem = 'ננן'  # Synthetic
        super().setUp()


class EphalNunShort(BaseTestCase.EpholReduced):

    def setUp(self):
        self.checksum = 42
        self.word = 'יננן'
        self.stem = 'נננ'  # Synthetic
        super().setUp()


class EphalKaf(BaseTestCase.Ephol):

    def setUp(self):
        self.checksum = 42
        self.word = 'יככך'
        self.stem = 'ככך'  # Synthetic
        super().setUp()


class EphalKafShort(BaseTestCase.EpholReduced):

    def setUp(self):
        self.checksum = 42
        self.word = 'יככך'
        self.stem = 'כככ'  # Synthetic
        super().setUp()


class EphalPei(BaseTestCase.Ephol):

    def setUp(self):
        self.checksum = 42
        self.word = 'יפפף'
        self.stem = 'פפף'  # Synthetic
        super().setUp()


class EphalPeiShort(BaseTestCase.EpholReduced):

    def setUp(self):
        self.checksum = 42
        self.word = 'יפפף'
        self.stem = 'פפפ'  # Synthetic
        super().setUp()


class EphalTsadi(BaseTestCase.Ephol):

    def setUp(self):
        self.checksum = 42
        self.word = 'יצצץ'
        self.stem = 'צצץ'  # Synthetic
        super().setUp()


class EphalTsadiShort(BaseTestCase.EpholReduced):

    def setUp(self):
        self.checksum = 42
        self.word = 'יצצץ'
        self.stem = 'צצצ'  # Synthetic
        super().setUp()


class PaalAyinVav(BaseTestCase.Ephol, BaseTestCase.EpholReduced):

    def setUp(self):
        self.checksum = 42
        self.word = 'יבוא'
        self.stem = 'בוא'
        super().setUp()


class PaalAyinVavMem(BaseTestCase.Ephol):

    def setUp(self):
        self.checksum = 42
        self.word = 'יקום'
        self.stem = 'קום'
        super().setUp()


class PaalAyinVavMemShort(BaseTestCase.EpholReduced):

    def setUp(self):
        self.checksum = 42
        self.word = 'יקום'
        self.stem = 'קומ'
        super().setUp()


class PaalAyinVavNun(BaseTestCase.Ephol):

    def setUp(self):
        self.checksum = 42
        self.word = 'ירון'
        self.stem = 'רון'
        super().setUp()


class PaalAyinVavNunShort(BaseTestCase.EpholReduced):

    def setUp(self):
        self.checksum = 42
        self.word = 'ירון'
        self.stem = 'רונ'
        super().setUp()


class PaalAyinVavKaf(BaseTestCase.Ephol):

    def setUp(self):
        self.checksum = 42
        self.word = 'יכוך'  # Synthetic
        self.stem = 'כוך'
        super().setUp()


class PaalAyinVavKafShort(BaseTestCase.EpholReduced):

    def setUp(self):
        self.checksum = 42
        self.word = 'יכוך'  # Synthetic
        self.stem = 'כוכ'
        super().setUp()


class PaalAyinVavPei(BaseTestCase.Ephol):

    def setUp(self):
        self.checksum = 42
        self.word = 'יעוף'
        self.stem = 'עוף'
        super().setUp()


class PaalAyinVavPeiShort(BaseTestCase.EpholReduced):

    def setUp(self):
        self.checksum = 42
        self.word = 'יעוף'
        self.stem = 'עופ'
        super().setUp()


class PaalAyinVavTsadi(BaseTestCase.Ephol):

    def setUp(self):
        self.checksum = 42
        self.word = 'ירוץ'
        self.stem = 'רוץ'
        super().setUp()


class PaalAyinVavTsadiShort(BaseTestCase.EpholReduced):

    def setUp(self):
        self.checksum = 42
        self.word = 'ירוץ'
        self.stem = 'רוצ'
        super().setUp()


class PaalAyinIudSimple(BaseTestCase.Ephol, BaseTestCase.EpholReduced):

    def setUp(self):
        self.checksum = 42
        self.word = 'ישיר'
        self.stem = 'שיר'
        super().setUp()


class PaalLamedHei(BaseTestCase.Ephol):

    def setUp(self):
        self.checksum = 50
        self.word = 'ירצה'
        self.stem = 'רצה'
        super().setUp()


class PaalLamedHeiShort(BaseTestCase.EpholReduced):

    def setUp(self):
        self.checksum = 50
        self.word = 'ירצה'
        self.stem = 'רצ'
        super().setUp()


class HifilSimple(BaseTestCase.Hifil):

    def setUp(self):
        self.checksum = 42
        self.word = 'הפעיל'
        self.stem = 'הפעל'
        super().setUp()


class HifilKaf(BaseTestCase.Hifil):

    def setUp(self):
        self.checksum = 42
        self.word = 'הפעיך'  # Synthetic
        self.stem = 'הפעכ'
        super().setUp()


class HifilMem(BaseTestCase.Hifil):

    def setUp(self):
        self.checksum = 42
        self.word = 'הפעים'  # Synthetic
        self.stem = 'הפעמ'
        super().setUp()


class HifilNun(BaseTestCase.Hifil):

    def setUp(self):
        self.checksum = 43
        self.word = 'הפעין'  # Synthetic
        self.stem = 'הפענ'
        super().setUp()

    def test_past_1p(self):
        self.assertIn(self.stem + 'ו', self.lexer.dic)


class HifilPei(BaseTestCase.Hifil):

    def setUp(self):
        self.checksum = 42
        self.word = 'הפעיף'  # Synthetic
        self.stem = 'הפעפ'
        super().setUp()


class HifilTsadi(BaseTestCase.Hifil):

    def setUp(self):
        self.checksum = 42
        self.word = 'הפעיץ'  # Synthetic
        self.stem = 'הפעצ'
        super().setUp()


