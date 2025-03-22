# ----------------------------------------------------------------------
# Tests: NLP - Syllable tokenization
# Copyright (C) 2018-2025  Ye Lei (叶磊)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

import pytest

from tests import wl_test_init, wl_test_lang_examples
from wordless.wl_nlp import wl_syl_tokenization, wl_texts, wl_word_tokenization

main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'fast')

test_syl_tokenizers = []

for lang, syl_tokenizers in main.settings_global['syl_tokenizers'].items():
    for syl_tokenizer in syl_tokenizers:
        test_syl_tokenizers.append((lang, syl_tokenizer))

@pytest.mark.parametrize('lang, syl_tokenizer', test_syl_tokenizers)
def test_syl_tokenize(lang, syl_tokenizer):
    tests_lang_util_skipped = False
    test_sentence = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}')

    # Untokenized
    tokens_untokenized = wl_syl_tokenization.wl_syl_tokenize(
        main,
        inputs = test_sentence,
        lang = lang,
        syl_tokenizer = syl_tokenizer
    )
    syls_tokens = [token.syls for token in tokens_untokenized]

    # Tokenized
    tokens = wl_word_tokenization.wl_word_tokenize_flat(
        main,
        text = test_sentence,
        lang = lang
    )
    tokens_tokenized = wl_syl_tokenization.wl_syl_tokenize(
        main,
        inputs = tokens,
        lang = lang,
        syl_tokenizer = syl_tokenizer
    )
    syls_tokens_tokenized = [token.syls for token in tokens_tokenized]

    print(f'{lang} / {syl_tokenizer}:')
    print(f'{syls_tokens}\n')

    # Check for empty syllables
    assert all(all(syls_token) for syls_token in syls_tokens)
    assert all(all(syls_token) for syls_token in syls_tokens_tokenized)

    # The count of syllables should be more than the count of tokens
    assert sum((len(syls_token) for syls_token in syls_tokens)) > len(tokens)
    assert sum((len(syls_token) for syls_token in syls_tokens_tokenized)) > len(tokens)

    # Tokenization should not be modified
    assert len(syls_tokens_tokenized) == len(tokens)

    # Tagged
    main.settings_custom['files']['tags']['body_tag_settings'] = [['Embedded', 'Part of speech', '_*', 'N/A']]

    tokens_tagged = wl_syl_tokenization.wl_syl_tokenize(
        main,
        inputs = [wl_texts.Wl_Token(token, tag = '_TEST') for token in tokens],
        lang = lang,
        syl_tokenizer = syl_tokenizer
    )
    syls_tokens_tagged = [token.syls for token in tokens_tagged]

    assert syls_tokens_tagged == syls_tokens_tokenized

    # Long
    tokens_long = wl_syl_tokenization.wl_syl_tokenize(
        main,
        inputs = wl_texts.to_tokens(wl_test_lang_examples.TOKENS_LONG, lang = lang),
        lang = lang,
        syl_tokenizer = syl_tokenizer
    )
    syls_tokens_long = [token.syls for token in tokens_long]

    assert syls_tokens_long == [(token,) for token in wl_test_lang_examples.TOKENS_LONG]

    # Syllabified
    syls_tokens_orig = [('te', 'st')]
    tokens_syllabified = wl_syl_tokenization.wl_syl_tokenize(
        main,
        inputs = wl_texts.to_tokens(['test'], lang = lang, syls_tokens = syls_tokens_orig),
        lang = lang,
        syl_tokenizer = syl_tokenizer
    )
    syls_tokens_syllabified = [token.syls for token in tokens_syllabified]

    assert syls_tokens_syllabified == syls_tokens_orig

    match lang:
        case 'afr':
            assert syls_tokens == [('Afri', 'kaans'), ('is',), ('ti', 'po', 'lo', 'gies'), ('be', 'skou'), ("'n",), ('In', 'do', 'Eu', 'ro', 'pe', 'se'), (',',), ('Wes', 'Ger', 'maan', 'se'), (',',), ('Ne', 'derfran', 'kie', 'se'), ('taal',), (',',), ('[',), ('2',), (']',), ('wat',), ('aan',), ('die',), ('suid', 'punt'), ('van',), ('Afri', 'ka'), ('on', 'der'), ('in', 'vloed'), ('van',), ('ver', 'skeie'), ('an', 'der'), ('ta', 'le'), ('en',), ('taal', 'groe', 'pe'), ('ont', 'staan'), ('het',), ('.',)]
        case 'sqi':
            assert syls_tokens == [('Ke', 'to'), ('gju', 'he'), ('kry', 'esisht'), ('pe', 'r', 'do', 'ret'), ('në',), ('Shqi', 'pë', 'ri'), (',',), ('Ko', 'so', 'vë'), ('dhe',), ('Ma', 'qe', 'do', 'ni', 'në'), ('e',), ('Ve', 'ri', 'ut'), (',',), ('por',), ('edhe',), ('në',), ('zo', 'na'), ('të',), ('tje', 'ra'), ('të',), ('Ev', 'ro', 'pës'), ('Ju', 'g', 'li', 'n', 'do', 're'), ('ku',), ('ka',), ('një',), ('po', 'pu', 'll', 'si'), ('shqi', 'p', 'ta', 're'), (',',), ('du', 'ke'), ('pë', 'r', 'f', 'shi', 'rë'), ('Ma', 'lin'), ('e',), ('Zi',), ('dhe',), ('Lu', 'gi', 'nën'), ('e',), ('Pre', 'she', 'vës'), ('.',)]
        case 'eus':
            assert syls_tokens == [('Eus', 'ka', 'ra'), ('Eus', 'kal'), ('He', 'rri', 'ko'), ('hiz', 'kun', 'tza'), ('da.',), ('[',), ('8',), (']',)]
        case 'bel':
            assert syls_tokens == [('Бе', 'ла', 'ру́с', 'кая'), ('мо́', 'ва'), ('—',), ('на', 'цы', 'я', 'на', 'ль', 'ная'), ('мо', 'ва'), ('бе', 'ла', 'ру', 'саў'), (',',), ('ува', 'хо', 'дзіць'), ('у',), ('ін', 'да', 'еў', 'ра', 'пей', 'с', 'кую'), ('моў', 'ную'), ('сям',), ('’',), ('ю',), (',',), ('сла', 'вя', 'н', 'с', 'кую'), ('гру', 'пу'), (',',), ('ус', 'хо', 'д', 'не', 'с', 'ла', 'вя', 'н', 'с', 'кую'), ('па', 'д', 'г', 'ру', 'пу'), ('.',)]
        case 'bul':
            assert syls_tokens == [('Бъ', '̀л', 'гар', 'с', 'ки', 'ят'), ('ез', 'ѝк'), ('е',), ('ин', 'до', 'ев', 'ро', 'пейс', 'ки'), ('език',), ('от',), ('гру', 'па', 'та'), ('на',), ('юж', 'нос', 'ла', 'вян', 'с', 'ки', 'те'), ('ези', 'ци'), (',',), ('ка', 'то'), ('об', 'ра', 'зу', 'ва'), ('не', 'го', 'ва', 'та'), ('из', 'точ', 'на'), ('под', 'г', 'ру', 'па'), ('.',)]
        case 'cat':
            assert syls_tokens == [('Hi',), ('ha',), ('al', 'tres'), ('glo', 'tò', 'nims'), ('tra', 'di', 'ci', 'o', 'nals'), ('que',), ('es',), ('fan',), ('ser', 'vir'), ('com',), ('a',), ('si', 'nò', 'nim'), ('de',), ('``',), ('ca', 'ta', 'là'), ("''",), ('al',), ('llarg',), ('del',), ('do', 'mi', 'ni'), ('lin', 'güís', 'tic'), ('.',)]
        case 'hrv':
            assert syls_tokens == [('Hr', 'vat', 'ski'), ('je', 'zik'), ('obu', 'hva', 'ća'), ('go', 'vo', 're', 'ni'), ('i',), ('pi', 'sa', 'ni'), ('hr', 'vat', 'ski'), ('stan', 'dard', 'ni'), ('je', 'zik'), ('i',), ('sve',), ('na', 'rod', 'ne'), ('go', 'vo', 're'), ('ko', 'ji', 'ma'), ('go', 'vo', 're'), ('i',), ('pi', 'šu'), ('Hr', 'va', 'ti.'), ('[',), ('4',), (']',)]
        case 'ces':
            assert syls_tokens == [('Češ', 'ti', 'na'), ('ne', 'bo', 'li'), ('čes', 'ký'), ('ja', 'zyk'), ('je',), ('zá', 'pa', 'doslo', 'van', 'ský'), ('ja', 'zyk'), (',',), ('nej', 'bliž', 'ší'), ('slo', 'ven', 'šti', 'ně'), (',',), ('po', 'té'), ('lužic', 'ké'), ('srbšti', 'ně'), ('a',), ('pol', 'šti', 'ně'), ('.',)]
        case 'dan':
            assert syls_tokens == [('Dansk',), ('er',), ('et',), ('øst', 'n', 'or', 'disk'), ('sprog',), ('in', 'den', 'for'), ('den',), ('ger', 'man', 'ske'), ('gren',), ('af',), ('den',), ('in', 'do', 'eu', 'ro', 'pæ', 'i', 'ske'), ('sprog', 'fa', 'mi', 'lie'), ('.',)]
        case 'nld':
            assert syls_tokens == [('Het',), ('Ne', 'der', 'lands'), ('is',), ('een',), ('Wes', 't', 'Ger', 'maan', 'se'), ('taal',), (',',), ('de',), ('meest',), ('ge', 'bruik', 'te'), ('taal',), ('in',), ('Ne', 'der', 'land'), ('en',), ('Bel', 'gië'), (',',), ('de',), ('of', 'fi', 'ci', 'ë', 'le'), ('taal',), ('van',), ('Su', 'ri', 'na', 'me'), ('en',), ('een',), ('van',), ('de',), ('drie',), ('of', 'fi', 'ci', 'ë', 'le'), ('ta', 'len'), ('van',), ('Bel', 'gië'), ('.',)]
        case 'eng_gb' | 'eng_us':
            match syl_tokenizer:
                case 'nltk_legality':
                    assert syls_tokens == [('En', 'glish'), ('is',), ('a',), ('West',), ('Ger', 'ma', 'nic'), ('lan', 'gu', 'a', 'ge'), ('in',), ('the',), ('In', 'do-', 'E', 'u', 'rop', 'ean'), ('lan', 'gu', 'a', 'ge'), ('fa', 'mi', 'ly'), (',',), ('who', 'se'), ('spe', 'a', 'kers'), (',',), ('cal', 'led'), ('An', 'glo', 'pho', 'nes'), (',',), ('o', 'ri', 'gi', 'na', 'ted'), ('in',), ('e', 'ar', 'ly'), ('me', 'di', 'e', 'val'), ('En', 'gland'), ('on',), ('the',), ('i', 'sland'), ('of',), ('Gr', 'eat'), ('Brit', 'ain.'), ('[',), ('4',), (']',), ('[',), ('5',), (']',), ('[',), ('6',), (']',)]
                case 'nltk_sonority_sequencing':
                    assert syls_tokens == [('English',), ('is',), ('a',), ('West',), ('Ger', 'ma', 'nic'), ('lan', 'gua', 'ge'), ('in',), ('the',), ('Indo', '-', 'Eu', 'ro', 'pean'), ('lan', 'gua', 'ge'), ('fa', 'mi', 'ly'), (',',), ('who', 'se'), ('spea', 'kers'), (',',), ('cal', 'led'), ('Anglop', 'ho', 'nes'), (',',), ('o', 'ri', 'gi', 'na', 'ted'), ('in',), ('ear', 'ly'), ('me', 'die', 'val'), ('England',), ('on',), ('the',), ('i', 'sland'), ('of',), ('Great',), ('Bri', 'tain.'), ('[',), ('4',), (']',), ('[',), ('5',), (']',), ('[',), ('6',), (']',)]
                case 'pyphen_eng_gb':
                    assert syls_tokens == [('Eng', 'lish'), ('is',), ('a',), ('West',), ('Ger', 'man', 'ic'), ('lan', 'guage'), ('in',), ('the',), ('In', 'do', 'European'), ('lan', 'guage'), ('fam', 'ily'), (',',), ('whose',), ('speak', 'ers'), (',',), ('called',), ('Anglo', 'phones'), (',',), ('ori', 'gin', 'ated'), ('in',), ('early',), ('me', 'di', 'ev', 'al'), ('Eng', 'land'), ('on',), ('the',), ('is', 'land'), ('of',), ('Great',), ('Bri', 'tain.'), ('[',), ('4',), (']',), ('[',), ('5',), (']',), ('[',), ('6',), (']',)]
                case 'pyphen_eng_us':
                    assert syls_tokens == [('Eng', 'lish'), ('is',), ('a',), ('West',), ('Ger', 'man', 'ic'), ('lan', 'guage'), ('in',), ('the',), ('In', 'do', 'Eu', 'ro', 'pean'), ('lan', 'guage'), ('fam', 'i', 'ly'), (',',), ('whose',), ('speak', 'ers'), (',',), ('called',), ('An', 'glo', 'phones'), (',',), ('orig', 'i', 'nat', 'ed'), ('in',), ('ear', 'ly'), ('me', 'dieval'), ('Eng', 'land'), ('on',), ('the',), ('is', 'land'), ('of',), ('Great',), ('Britain.',), ('[',), ('4',), (']',), ('[',), ('5',), (']',), ('[',), ('6',), (']',)]
                case _:
                    tests_lang_util_skipped = True
        case 'epo':
            assert syls_tokens == [('Es', 'pe', 'r', 'anto'), (',',), ('ori', 'gi', 'ne'), ('la',), ('Lin', 'g', 'vo'), ('In', 'ter', 'na', 'cia'), ('[',), ('4',), (']',), (',',), ('es', 'tas'), ('la',), ('plej',), ('dis', 'vas', 't', 'iĝ', 'inta'), ('in', 'ter', 'na', 'cia'), ('plan', 'lin', 'g', 'vo'), ('[',), ('5',), (']',), ('.',)]
        case 'est':
            assert syls_tokens == [('Ees', 'ti'), ('keel',), ('(',), ('vara', 'sem'), ('ni', 'me', 'tus'), ('maa', 'keel'), (')',), ('on',), ('lää', 'ne', 'me', 're', 'soo', 'me'), ('lõu', 'na', 'rüh', 'ma'), ('kuu', 'luv'), ('keel',), ('.',)]
        case 'fra':
            assert syls_tokens == [('Le',), ('fran', 'çais'), ('est',), ('une',), ('langue',), ('in', 'do', 'eu', 'ro', 'péenne'), ('de',), ('la',), ('fa', 'mille'), ('des',), ('langues',), ('ro', 'manes'), ('dont',), ('les',), ('lo', 'cu', 'teurs'), ('sont',), ('ap', 'pe', 'lés'), ('«',), ('fran', 'co', 'phones'), ('»',), ('.',)]
        case 'glg':
            assert syls_tokens == [('O',), ('ga', 'le', 'go'), ('(',), ('[',), ('ɡaˈleɣo̝',), (']',), ('[',), ('1',), (']',), (')',), ('é',), ('unha',), ('lin', 'gua'), ('in', 'do', 'eu', 'ro', 'pea'), ('que',), ('per', 'ten', 'ce'), ('á',), ('póla',), ('de',), ('lin', 'guas'), ('ro', 'má', 'ni', 'cas'), ('.',)]
        case 'deu_at' | 'deu_de' | 'deu_ch':
            assert syls_tokens == [('Die',), ('deut', 'sche'), ('Spra', 'che'), ('oder',), ('Deutsch',), ('[',), ('dɔɪ̯tʃ',), (']',), ('[',), ('24',), (']',), ('ist',), ('ei', 'ne'), ('west', 'ger', 'ma', 'ni', 'sche'), ('Spra', 'che'), (',',), ('die',), ('welt', 'weit'), ('et', 'wa'), ('90',), ('bis',), ('105',), ('Mil', 'li', 'o', 'nen'), ('Men', 'schen'), ('als',), ('Mut', 'ter', 'spra', 'che'), ('und',), ('wei', 'te', 'ren'), ('rund',), ('80',), ('Mil', 'li', 'o', 'nen'), ('als',), ('Zweit',), ('oder',), ('Fremd', 'spra', 'che'), ('dient',), ('.',)]
        case 'ell':
            assert syls_tokens == [('Η',), ('ελ', 'λη', 'νι', 'κή'), ('γλώσ', 'σα'), ('ανή', 'κει'), ('στην',), ('ιν', 'δο', 'ευ', 'ρω', 'παϊκή'), ('οι', 'κο', 'γένεια'), ('[',), ('9',), (']',), ('secε', 'πί', 'σης'), ('στο',), ('βαλ', 'κα', 'νι', 'κό'), ('γλωσ', 'σι', 'κό'), ('δε', 'σμό'), ('.',)]
        case 'hun':
            assert syls_tokens == [('A',), ('ma', 'gyar'), ('nyelv',), ('az',), ('urá', 'li'), ('nyelv', 'csa', 'lád'), ('tag', 'ja'), (',',), ('azon',), ('be', 'lül'), ('a',), ('finn', 'ugor'), ('nyel', 'vek'), ('kö', 'zé'), ('tar', 'to', 'zó'), ('ugor',), ('nyel', 'vek'), ('egyi', 'ke'), ('.',)]
        case 'isl':
            assert syls_tokens == [('Ís', 'lenska'), ('er',), ('vest', 'ur', 'nor', 'rænt'), (',',), ('germ', 'anskt'), ('og',), ('indó', 'evr', 'ópskt'), ('tungu', 'mál'), ('sem',), ('er',), ('eink', 'um'), ('tal', 'að'), ('og',), ('rit', 'að'), ('á',), ('Ís', 'landi'), ('og',), ('er',), ('móð', 'ur', 'mál'), ('lang', 'flestra'), ('Ís', 'lend', 'inga.'), ('[',), ('6',), (']',)]
        case 'ind':
            assert syls_tokens == [('Ba', 'ha', 'sa'), ('In', 'do', 'ne', 'sia'), ('(',), ('[',), ('baˈha', 'sa'), ('in', 'doˈne', 'si', 'ja'), (']',), (')',), ('me', 'ru', 'pa', 'kan'), ('ba', 'ha', 'sa'), ('res', 'mi'), ('se', 'ka', 'li', 'gus'), ('ba', 'ha', 'sa'), ('na', 'si', 'o', 'nal'), ('di',), ('In', 'do', 'ne', 'si', 'a.'), ('[',), ('16',), (']',)]
        case 'ita':
            assert syls_tokens == [("L'i", 'ta', 'lia', 'no'), ('è',), ('una',), ('lin', 'gua'), ('ro', 'man', 'za'), ('par', 'la', 'ta'), ('prin', 'ci', 'pal', 'men', 'te'), ('in',), ('Ita', 'lia'), ('.',)]
        case 'lav':
            assert syls_tokens == [('Lat', 'vie', 'šu'), ('va', 'lo', 'da'), ('ir',), ('dzim', 'tā'), ('va', 'lo', 'da'), ('ap', 'mē', 'ram'), ('1,5',), ('mil', 'jo', 'niem'), ('cil', 'vē', 'ku'), (',',), ('gal', 've', 'no', 'kārt'), ('Lat', 'vi', 'jā'), (',',), ('kur',), ('tā',), ('ir',), ('vien', 'ī', 'gā'), ('valsts',), ('va', 'lo', 'da.'), ('[',), ('1',), (']',), ('[',), ('3',), (']',)]
        case 'lit':
            assert syls_tokens == [('Lie', 'tu', 'vių'), ('kal', 'ba'), ('–',), ('iš',), ('bal', 'tų'), ('pro', 'kal', 'bės'), ('ki', 'lu', 'si'), ('lie', 'tu', 'vių'), ('tau', 'tos'), ('kal', 'ba'), (',',), ('ku', 'ri'), ('Lie', 'tu', 'vo', 'je'), ('yra',), ('vals', 'ty', 'bi', 'nė'), (',',), ('o',), ('Eu', 'ro', 'pos'), ('Są', 'jun', 'go', 'je'), ('–',), ('vie', 'na'), ('iš',), ('ofi', 'cia', 'lių', 'jų'), ('kal', 'bų'), ('.',)]
        case 'mon_cyrl':
            assert syls_tokens == [('Мон', 'гол'), ('хэл',), ('нь',), ('Мон', 'гол'), ('ул', 'сын'), ('ал', 'бан'), ('ёс', 'ны'), ('хэл',), ('юм',), ('.',)]
        case 'nob':
            assert syls_tokens == [('Bok', 'mål'), ('er',), ('en',), ('av',), ('to',), ('of', 'fi', 'si', 'el', 'le'), ('mål', 'for', 'mer'), ('av',), ('norsk',), ('skrift', 'språk'), (',',), ('hvor', 'av'), ('den',), ('and', 're'), ('er',), ('ny', 'norsk'), ('.',)]
        case 'nno':
            assert syls_tokens == [('Ny', 'norsk'), (',',), ('før',), ('1929',), ('of', 'fi', 'si', 'elt'), ('kal', 'la'), ('lands', 'mål'), (',',), ('er',), ('si', 'dan'), ('jam', 'stil', 'lings', 'ved', 'ta', 'ket'), ('av',), ('12',), ('.',), ('mai',), ('1885',), ('ei',), ('av',), ('dei',), ('to',), ('of', 'fi', 'si', 'el', 'le'), ('mål', 'for', 'me', 'ne'), ('av',), ('norsk',), (';',), ('den',), ('and', 're'), ('for', 'ma'), ('er',), ('bok', 'mål'), ('.',)]
        case 'pol':
            assert syls_tokens == [('Ję', 'zyk'), ('pol', 'ski'), (',',), ('pol', 'sz', 'czy', 'zna'), ('–',), ('ję', 'zyk'), ('le', 'chic', 'ki'), ('z',), ('gru', 'py'), ('za', 'chod', 'nio', 'sło', 'wiań', 'skiej'), ('(',), ('do',), ('któ', 'rej'), ('na', 'le', 'żą'), ('rów', 'nież'), ('cze', 'ski'), (',',), ('ka', 'szub', 'ski'), (',',), ('sło', 'wac', 'ki'), (',',), ('ję', 'zy', 'ki'), ('łu', 'życ', 'kie'), ('czy',), ('wy', 'mar', 'ły'), ('ję', 'zyk'), ('drze', 'wiań', 'ski'), (')',), (',',), ('sta', 'no', 'wią', 'cej'), ('część',), ('ro', 'dzi', 'ny'), ('in', 'do', 'eu', 'ro', 'pej', 'skiej'), ('.',)]
        case 'por_br' | 'por_pt':
            assert syls_tokens == [('A',), ('lín', 'gua'), ('por', 'tu', 'gue', 'sa'), (',',), ('tam', 'bém'), ('de', 'sig', 'na', 'da'), ('por', 'tu', 'guês'), (',',), ('é',), ('uma',), ('lín', 'gua'), ('in', 'do', 'eu', 'ro', 'peia'), ('ro', 'mâ', 'ni', 'ca'), ('fle', 'xi', 'va'), ('oci', 'den', 'tal'), ('ori', 'gi', 'na', 'da'), ('no',), ('ga', 'le', 'go', 'por', 'tu', 'guês'), ('fa', 'la', 'do'), ('no',), ('Rei', 'no'), ('da',), ('Ga', 'li', 'za'), ('e',), ('no',), ('nor', 'te'), ('de',), ('Por', 'tu', 'gal'), ('.',)]
        case 'ron':
            assert syls_tokens == [('Lim', 'ba'), ('ro', 'mâ', 'nă'), ('(',), ('[',), ('ˈlim', 'ba'), ('roˈ', 'mɨnə'), (']',), ('(',), ('au', 'dio'), (')',), ('sau',), ('ro', 'mâ', 'neș', 'te'), ('[',), ('ro', 'mɨˈ', 'neʃ', 'te'), (']',), (')',), ('es', 'te'), ('lim', 'ba'), ('ofi', 'ci', 'a', 'lă'), ('și',), ('prin', 'ci', 'pa', 'lă'), ('a',), ('Ro', 'mâ', 'ni', 'ei'), ('și',), ('a',), ('Re', 'pu', 'bli', 'cii'), ('Mol', 'do', 'va'), ('.',)]
        case 'rus':
            assert syls_tokens == [('Рус', 'ский'), ('язык',), ('(',), ('МФА',), (':',), ('[',), ('ˈruskʲɪɪ̯',), ('ɪ̯ɪˈzɨk',), (']',), ('о',), ('фай', 'ле'), (')',), ('[',), ('~',), ('3',), (']',), ('—',), ('язык',), ('вос', 'точ', 'но', 'сла', 'вян', 'ской'), ('груп', 'пы'), ('сла', 'вян', 'ской'), ('вет', 'ви'), ('ин', 'до', 'ев', 'ро', 'пей', 'ской'), ('язы', 'ко', 'вой'), ('се', 'мьи'), (',',), ('на', 'ци', 'о', 'наль', 'ный'), ('язык',), ('рус', 'ско', 'го'), ('на', 'ро', 'да'), ('.',)]
        case 'srp_cyrl':
            assert syls_tokens == [('Срп', 'ски'), ('је', 'зик'), ('при', 'па', 'да'), ('сло', 'вен', 'ској'), ('гру', 'пи'), ('је', 'зи', 'ка'), ('по', 'ро', 'ди', 'це'), ('ин', 'до', 'е', 'вроп', 'ских'), ('је', 'зи', 'ка.'), ('[',), ('12',), (']',)]
        case 'srp_latn':
            assert syls_tokens == [('Srp', 'ski'), ('je', 'zik'), ('pri', 'pa', 'da'), ('slo', 'ven', 'skoj'), ('gru', 'pi'), ('je', 'zi', 'ka'), ('po', 'ro', 'di', 'ce'), ('in', 'do', 'e', 'vrop', 'skih'), ('je', 'zi', 'ka.'), ('[',), ('12',), (']',)]
        case 'slk':
            assert syls_tokens == [('Slo', 'ven', 'či', 'na'), ('pat', 'rí'), ('do',), ('sku', 'pi', 'ny'), ('zá', 'pa', 'do', 'slo', 'van', 'ských'), ('ja', 'zy', 'kov'), ('(',), ('spo', 'lu'), ('s',), ('češ', 'ti', 'nou'), (',',), ('poľš', 'ti', 'nou'), (',',), ('hor', 'nou'), ('a',), ('dol', 'nou'), ('lu', 'žic', 'kou'), ('srb', 'či', 'nou'), ('a',), ('ka', 'šub', 'či', 'nou'), (')',), ('.',)]
        case 'slv':
            assert syls_tokens == [('Slo', 'ven', 'šči', 'na'), ('[',), ('slo', 'ˈʋe', 'nʃtʃi', 'na'), (']',), ('je',), ('zdru', 'že', 'ni'), ('na', 'ziv'), ('za',), ('ura', 'dni'), ('knji', 'žni'), ('je', 'zik'), ('Slo', 'ven', 'cev'), ('in',), ('sku', 'pno'), ('ime',), ('za',), ('na', 're', 'čja'), ('in',), ('go', 'vo', 're'), (',',), ('ki',), ('jih',), ('go', 'vo', 'ri', 'jo'), ('ali',), ('so',), ('jih',), ('ne', 'koč'), ('go', 'vo', 'ri', 'li'), ('Slo', 'ven', 'ci'), ('.',)]
        case 'spa':
            assert syls_tokens == [('El',), ('es', 'pa', 'ñol'), ('o',), ('cas', 'te', 'llano'), ('es',), ('una',), ('len', 'gua'), ('ro', 'man', 'ce'), ('pro', 'ce', 'den', 'te'), ('del',), ('la', 'tín'), ('ha', 'bla', 'do'), (',',), ('per', 'te', 'ne', 'cien', 'te'), ('a',), ('la',), ('fa', 'mi', 'lia'), ('de',), ('len', 'guas'), ('in', 'doeu', 'ro', 'peas'), ('.',)]
        case 'swe':
            assert syls_tokens == [('Svens', 'ka'), ('(',), ('svens', 'ka'), ('(',), ('fil',), (')',), (')',), ('är',), ('ett',), ('öst', 'nor', 'diskt'), ('språk',), ('som',), ('ta', 'las'), ('av',), ('un', 'ge', 'fär'), ('tio',), ('mil', 'jo', 'ner'), ('per', 'so', 'ner'), (',',), ('främst',), ('i',), ('Sve', 'ri', 'ge'), ('där',), ('språ', 'ket'), ('har',), ('en',), ('do', 'mi', 'nant'), ('ställ', 'ning'), ('som',), ('hu', 'vud', 'språk'), (',',), ('men',), ('även',), ('som',), ('det',), ('ena',), ('na', 'tio', 'nal', 'språ', 'ket'), ('i',), ('Fin', 'land'), ('och',), ('som',), ('en', 'da'), ('of', 'fi', 'ci', 'el', 'la'), ('språk',), ('på',), ('Åland',), ('.',)]
        case 'tel':
            assert syls_tokens == [('తె', 'లు', 'గు'), ('ఆం', 'ధ్ర'), (',',), ('తె', 'లం', 'గాణ'), ('రా', 'ష్ట్రా', 'ల', 'లో'), ('ము', 'న్న', 'ధి', 'కా', 'రిక'), ('ను', 'డి'), ('.',)]
        case 'tha':
            match syl_tokenizer:
                case 'pyphen_tha' | 'pythainlp_syl_dict':
                    assert syls_tokens == [('ภา', 'ษา', 'ไทย'), ('หรือ',), ('ภา', 'ษา', 'ไทย'), ('กลาง',), ('เป็น',), ('ภา', 'ษา'), ('ใน',), ('กลุ่ม',), ('ภา', 'ษา'), ('ไท',), ('สา', 'ขา'), ('ย่อย',), ('เชียง', 'แสน'), ('ซึ่ง',), ('เป็น',), ('กลุ่ม', 'ย่อย'), ('ของ',), ('ตระ', 'กูล'), ('ภา', 'ษา'), ('ข',), ('ร้า',), ('-',), ('ไท',), ('และ',), ('เป็น',), ('ภา', 'ษา', 'ราช', 'การ'), ('และ',), ('ภา', 'ษา', 'ประ', 'จำ', 'ชาติ'), ('ของ',), ('ประ', 'เทศ'), ('ไทย',), ('[3][4]',)]
                case 'pythainlp_han_solo':
                    assert syls_tokens == [('ภา', 'ษา', 'ไทย'), ('หรือ',), ('ภา', 'ษา', 'ไทย'), ('กลาง',), ('เป็น',), ('ภา', 'ษา'), ('ใน',), ('กลุ่ม',), ('ภา', 'ษา'), ('ไท',), ('สา', 'ขา'), ('ย่อย',), ('เชียง', 'แสน'), ('ซึ่ง',), ('เป็น',), ('กลุ่ม', 'ย่อย'), ('ของ',), ('ตระ', 'กูล'), ('ภา', 'ษา'), ('ข',), ('ร้า',), ('-',), ('ไท',), ('และ',), ('เป็น',), ('ภา', 'ษา', 'ราช', 'การ'), ('และ',), ('ภา', 'ษา', 'ประ', 'จำ', 'ชาติ'), ('ของ',), ('ประ', 'เทศ'), ('ไทย',), ('[3', '][4', ']')]
                case _:
                    tests_lang_util_skipped = True
        case 'ukr':
            assert syls_tokens == [('Укра', 'ї', '́', 'н', 'сь', 'ка'), ('мо', '́', 'ва'), ('(',), ('МФА',), (':',), ('[',), ('ʊkrɐˈjinʲsʲkɐ',), ('ˈmɔʋɐ',), (']',), (',',), ('іс', 'то', 'ри', 'ч', 'на'), ('на', 'зва'), ('—',), ('ру', '́', 'сь', 'ка'), ('[',), ('10',), (']',), ('[',), ('11',), (']',), ('[',), ('12',), (']',), ('[',), ('*',), ('1',), (']',), (')',), ('—',), ('на', 'ціо', 'на', 'ль', 'на'), ('мо', 'ва'), ('укра', 'ї', 'н', 'ців'), ('.',)]
        case 'zul':
            assert syls_tokens == [('Zu', 'lu'), ('/ˈzu', 'ːlu', 'ː/'), (',',), ('no', 'ma'), ('isi', 'Zu', 'lu'), ('wu', 'li', 'mi'), ('lwa', 'ba', 'ntu'), ('ba', 'se'), ('Ni', 'ngi', 'zi', 'mu'), ('neA', 'fri', 'ka'), ('aba', 'yi', 'ngxe', 'nye'), ('ya', 'ma', 'Ngu', 'ni'), ('.',)]
        case _:
            raise wl_test_init.Wl_Exc_Tests_Lang_Skipped(lang)

    if tests_lang_util_skipped:
        raise wl_test_init.Wl_Exc_Tests_Lang_Util_Skipped(syl_tokenizer)

def test_syl_tokenize_misc():
    # Unsupported languages
    wl_syl_tokenization.wl_syl_tokenize(
        main,
        inputs = 'test',
        lang = 'other'
    )

    wl_syl_tokenization.wl_syl_tokenize(
        main,
        inputs = [wl_texts.Wl_Token('test', lang = 'other')],
        lang = 'other'
    )

if __name__ == '__main__':
    for lang, syl_tokenizer in test_syl_tokenizers:
        test_syl_tokenize(lang, syl_tokenizer)

    test_syl_tokenize_misc()
