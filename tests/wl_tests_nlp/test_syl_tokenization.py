# ----------------------------------------------------------------------
# Wordless: Tests - NLP - Syllable Tokenization
# Copyright (C) 2018-2023  Ye Lei (叶磊)
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

import pytest

from tests import wl_test_init, wl_test_lang_examples
from wordless.wl_checks import wl_checks_tokens
from wordless.wl_nlp import wl_syl_tokenization, wl_word_tokenization

main = wl_test_init.Wl_Test_Main()

test_syl_tokenizers = []

for lang, syl_tokenizers in main.settings_global['syl_tokenizers'].items():
    for syl_tokenizer in syl_tokenizers:
        test_syl_tokenizers.append((lang, syl_tokenizer))

@pytest.mark.parametrize('lang, syl_tokenizer', test_syl_tokenizers)
def test_syl_tokenize(lang, syl_tokenizer):
    # Untokenized
    syls = wl_syl_tokenization.wl_syl_tokenize(
        main,
        inputs = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}'),
        lang = lang,
        syl_tokenizer = syl_tokenizer
    )

    # Tokenized
    tokens = wl_word_tokenization.wl_word_tokenize_flat(
        main,
        text = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}'),
        lang = lang
    )
    syls_tokenized = wl_syl_tokenization.wl_syl_tokenize(
        main,
        inputs = tokens,
        lang = lang,
        syl_tokenizer = syl_tokenizer
    )
    syls_long_text_tokenized = wl_syl_tokenization.wl_syl_tokenize(
        main,
        inputs = [str(i) for i in range(101) for j in range(50)],
        lang = lang,
        syl_tokenizer = syl_tokenizer
    )

    print(f'{lang} / {syl_tokenizer}:')
    print(f'{syls}\n')

    # Check for empty syllables
    assert all(all(syls_token) for syls_token in syls)
    assert all(all(syls_token) for syls_token in syls_tokenized)

    # The count of syllables should be more than the count of tokens
    assert sum((len(syls_token) for syls_token in syls)) > len(tokens)
    assert sum((len(syls_token) for syls_token in syls_tokenized)) > len(tokens)

    # Tokenization should not be modified
    assert len(syls_tokenized) == len(tokens)

    # Test long texts
    if syl_tokenizer != 'nltk_sonority_sequencing':
        assert syls_long_text_tokenized == [[str(i)] for i in range(101) for j in range(50)]

    syl_tokenizer_skipped = False

    if lang == 'afr':
        assert syls == [['Afri', 'kaans'], ['is'], ['ti', 'po', 'lo', 'gies'], ['be', 'skou'], ["'"], ['n'], ['In', 'do'], ['-'], ['Eu', 'ro', 'pe', 'se'], [','], ['Wes'], ['-'], ['Ger', 'maan', 'se'], [','], ['Ne', 'derfran', 'kie', 'se'], ['taal', ',[2'], [']'], ['wat'], ['aan'], ['die'], ['suid', 'punt'], ['van'], ['Afri', 'ka'], ['on', 'der'], ['in', 'vloed'], ['van'], ['ver', 'skeie'], ['an', 'der'], ['ta', 'le'], ['en'], ['taal', 'groe', 'pe'], ['ont', 'staan'], ['het'], ['.']]
    elif lang == 'sqi':
        assert syls == [['Gju', 'ha'], ['shqi', 'pe'], ['('], ['ose'], ['thjesht'], ['shqi', 'p', 'ja'], [')'], ['ësh', 'të'], ['gju', 'hë'], ['dhe'], ['de', 'gë'], ['e'], ['ve', 'ça', 'n', 'të'], ['e'], ['fa', 'mi', 'l', 'jes'], ['in', 'do'], ['-'], ['ev', 'ro', 'pi', 'ane'], ['që'], ['fli', 'tet'], ['nga'], ['rreth'], ['7'], ['-'], ['10'], ['mi', 'li', 'onë'], ['nje', 'rëz'], ['në'], ['bo', 'të,[1'], [']'], ['kry', 'esisht'], ['në'], ['Shqi', 'pë', 'ri'], [','], ['Ko', 'so', 'vë'], ['dhe'], ['Ma', 'qe', 'do', 'ni', 'në'], ['e'], ['Ve', 'ri', 'ut'], [','], ['por'], ['edhe'], ['në'], ['zo', 'na'], ['të'], ['tje', 'ra'], ['të'], ['Ev', 'ro', 'pës'], ['Ju', 'g', 'li', 'n', 'do', 're'], ['ku'], ['ka'], ['një'], ['po', 'pu', 'll', 'si'], ['shqi', 'p', 'ta', 're'], [','], ['du', 'ke'], ['pë', 'r', 'f', 'shi', 'rë'], ['Ma', 'lin'], ['e'], ['Zi'], ['dhe'], ['Lu', 'gi', 'nën'], ['e'], ['Pre', 'she', 'vës'], ['.']]
    elif lang == 'bel':
        assert syls == [['Бе', 'ла', 'ру́с', 'кая'], ['мо́', 'ва'], ['—'], ['на', 'цы', 'я', 'на', 'ль', 'ная'], ['мо', 'ва'], ['бе', 'ла', 'ру', 'саў'], [','], ['ува', 'хо', 'дзіць'], ['у'], ['ін', 'да', 'еў', 'ра', 'пей', 'с', 'кую'], ['моў', 'ную'], ['ся', "м'ю"], [','], ['сла', 'вя', 'н', 'с', 'кую'], ['гру', 'пу'], [','], ['ус', 'хо', 'д', 'не', 'с', 'ла', 'вя', 'н', 'с', 'кую'], ['па', 'д', 'г', 'ру', 'пу'], ['.']]
    elif lang == 'bul':
        assert syls == [['Бъ', '̀л', 'гар', 'с', 'ки', 'ят'], ['ез', 'ѝк'], ['е'], ['ин', 'до', 'ев', 'ро', 'пейс', 'ки'], ['език'], ['от'], ['гру', 'па', 'та'], ['на'], ['юж', 'нос', 'ла', 'вян', 'с', 'ки', 'те'], ['ези', 'ци'], ['.']]
    elif lang == 'cat':
        assert syls == [['El'], ['ca', 'ta', 'là'], ['('], ['de', 'no', 'mi', 'na', 'ció'], ['ofi', 'ci', 'al'], ['a'], ['Ca', 'ta', 'lu', 'nya'], [','], ['a'], ['les'], ['Illes'], ['Ba', 'le', 'ars'], [','], ['a'], ['An', 'dor', 'ra'], [','], ['a'], ['la'], ['ciu', 'tat'], ['de'], ["l'"], ['Al', 'guer'], ['i'], ['tra', 'di', 'ci', 'o', 'nal'], ['a'], ['Ca', 'ta', 'lu', 'nya'], ['d'], ['el'], ['Nord'], [')'], ['o'], ['va', 'len', 'cià'], ['('], ['de', 'no', 'mi', 'na', 'ció'], ['ofi', 'ci', 'al'], ['a'], ['l'], ['Pa', 'ís'], ['Va', 'len', 'cià'], ['i'], ['tra', 'di', 'ci', 'o', 'nal'], ['a'], ['l'], ['Car', 'xe'], [')'], ['és'], ['una'], ['llen', 'gua'], ['ro', 'mà', 'ni', 'ca'], ['par', 'la', 'da'], ['a'], ['Ca', 'ta', 'lu', 'nya'], [','], ['el'], ['Pa', 'ís'], ['Va', 'len', 'cià'], ['('], ['tret'], ["d'"], ['al', 'gu', 'nes'], ['co', 'mar', 'ques'], ['i'], ['lo', 'ca', 'li', 'tats'], ['de'], ["l'"], ['in', 'te', 'ri', 'or'], [')'], [','], ['les'], ['Illes'], ['Ba', 'le', 'ars'], [','], ['An', 'dor', 'ra'], [','], ['la'], ['Fran', 'ja'], ['de'], ['Po', 'nent'], ['('], ['a'], ["l'"], ['Ara', 'gó'], [')'], [','], ['la'], ['ciu', 'tat'], ['de'], ["l'"], ['Al', 'guer'], ['('], ['a'], ["l'"], ['illa'], ['de'], ['Sar', 'de', 'nya'], [')'], [','], ['la'], ['Ca', 'ta', 'lu', 'nya'], ['d'], ['el'], ['Nord,[8'], [']'], ['el'], ['Car', 'xe'], ['('], ['un'], ['pe', 'tit'], ['ter', 'ri', 'to', 'ri'], ['de'], ['Múr', 'cia'], ['po', 'blat'], ['per'], ['po', 'bla', 'dors'], ['va', 'len', 'ci', 'ans),[9][10'], [']'], ['i'], ['en'], ['co', 'mu', 'ni', 'tats'], ['ar', 'reu'], ['d'], ['el'], ['món'], ['('], ['en', 'tre'], ['les'], ['quals'], ['des', 'ta', 'ca'], ['la'], ['de'], ["l'"], ['Ar', 'gen', 'ti', 'na'], [','], ['amb'], ['200.000'], ['par', 'lants).[11'], [']']]
    elif lang == 'hrv':
        assert syls == [['Hr', 'vat', 'ski'], ['je', 'zik'], ['('], ['ISO'], ['639'], ['-'], ['3'], [':'], ['hrv'], ['Ina', 'či', 'ca'], ['iz', 'vor', 'ne'], ['stra', 'ni', 'ce'], ['ar', 'hi', 'vi', 'ra', 'na'], ['18'], ['.'], ['ruj', 'na'], ['2012'], ['.'], [')'], ['skup', 'ni'], ['je'], ['na', 'ziv'], ['za'], ['na', 'ci', 'onal', 'ni'], ['stan', 'dard', 'ni'], ['je', 'zik'], ['Hr', 'va', 'ta'], [','], ['te'], ['za'], ['skup'], ['na', 'rje', 'čja'], ['i'], ['go', 'vo', 'ra'], ['ko', 'ji', 'ma'], ['go', 'vo', 're'], ['ili'], ['su'], ['ne', 'ka', 'da'], ['go', 'vo', 'ri', 'li'], ['Hr', 'va', 'ti'], ['.']]
    elif lang == 'ces':
        assert syls == [['Češ', 'ti', 'na'], ['ne', 'bo', 'li'], ['čes', 'ký'], ['ja', 'zyk'], ['je'], ['zá', 'pa', 'doslo', 'van', 'ský'], ['ja', 'zyk'], [','], ['nej', 'bliž', 'ší'], ['slo', 'ven', 'šti', 'ně'], [','], ['po', 'té'], ['lužic', 'ké'], ['srbšti', 'ně'], ['a'], ['pol', 'šti', 'ně'], ['.']]
    elif lang == 'dan':
        assert syls == [['Dansk'], ['er'], ['et'], ['øst', 'n', 'or', 'disk'], ['sprog'], ['in', 'den', 'for'], ['den'], ['ger', 'man', 'ske'], ['gren'], ['af'], ['den'], ['in', 'do', 'eu', 'ro', 'pæ', 'i', 'ske'], ['sprog', 'fa', 'mi', 'lie'], ['.']]
    elif lang == 'nld':
        assert syls == [['Het'], ['Ne', 'der', 'lands'], ['is'], ['een'], ['Wes', 't', 'Ger', 'maan', 'se'], ['taal'], ['en'], ['de'], ['of', 'fi', 'ci', 'ë', 'le'], ['taal'], ['van'], ['Ne', 'der', 'land'], [','], ['Su', 'ri', 'na', 'me'], ['en'], ['een'], ['van'], ['de'], ['drie'], ['of', 'fi', 'ci', 'ë', 'le'], ['ta', 'len'], ['van'], ['Bel', 'gië'], ['.']]
    elif lang.startswith('eng_'):
        if syl_tokenizer == 'nltk_legality':
            assert syls == [['En', 'glish'], ['is'], ['a'], ['West'], ['Ger', 'ma', 'nic'], ['lan', 'gu', 'a', 'ge'], ['of'], ['the'], ['In', 'do'], ['-'], ['E', 'u', 'rop', 'ean'], ['lan', 'gu', 'a', 'ge'], ['fa', 'mi', 'ly'], [','], ['o', 'ri', 'gi', 'nal', 'ly'], ['spo', 'ken'], ['by'], ['the'], ['in', 'ha', 'bi', 'tants'], ['of'], ['e', 'ar', 'ly'], ['me', 'di', 'e', 'val'], ['En', 'gland.[3][4][5'], [']']]
        elif syl_tokenizer == 'nltk_sonority_sequencing':
            assert syls == [['English'], ['is'], ['a'], ['West'], ['Ger', 'ma', 'nic'], ['lan', 'gua', 'ge'], ['of'], ['the'], ['Indo'], ['-'], ['Eu', 'ro', 'pean'], ['lan', 'gua', 'ge'], ['fa', 'mi', 'ly'], [','], ['o', 'ri', 'gi', 'nal', 'ly'], ['spo', 'ken'], ['by'], ['the'], ['in', 'ha', 'bi', 'tants'], ['of'], ['ear', 'ly'], ['me', 'die', 'val'], ['England.[3][4][5'], [']']]
        elif syl_tokenizer == 'pyphen_eng_gb':
            assert syls == [['Eng', 'lish'], ['is'], ['a'], ['West'], ['Ger', 'man', 'ic'], ['lan', 'guage'], ['of'], ['the'], ['Indo'], ['-'], ['European'], ['lan', 'guage'], ['fam', 'ily'], [','], ['ori', 'gin', 'ally'], ['spoken'], ['by'], ['the'], ['in', 'hab', 'it', 'ants'], ['of'], ['early'], ['me', 'di', 'ev', 'al'], ['Eng', 'land.[3][4][5'], [']']]
        elif syl_tokenizer == 'pyphen_eng_us':
            assert syls == [['Eng', 'lish'], ['is'], ['a'], ['West'], ['Ger', 'man', 'ic'], ['lan', 'guage'], ['of'], ['the'], ['In', 'do'], ['-'], ['Eu', 'ro', 'pean'], ['lan', 'guage'], ['fam', 'i', 'ly'], [','], ['orig', 'i', 'nal', 'ly'], ['spo', 'ken'], ['by'], ['the'], ['in', 'hab', 'i', 'tants'], ['of'], ['ear', 'ly'], ['me', 'dieval'], ['Eng', 'land.[3][4][5'], [']']]
        else:
            syl_tokenizer_skipped = True
    elif lang == 'epo':
        assert syls == [['Es', 'pe', 'r', 'anto'], [','], ['ori', 'gi', 'ne'], ['la'], ['Lin', 'g', 'vo'], ['In', 'ter', 'na', 'ci', 'a', ',[4'], [']'], ['es', 'tas'], ['la'], ['plej'], ['dis', 'vas', 't', 'iĝ', 'inta'], ['in', 'ter', 'na', 'cia'], ['plan', 'lin', 'g', 'vo', '.[5'], [']']]
    elif lang == 'est':
        assert syls == [['Ees', 'ti'], ['keel'], ['('], ['vara', 'sem'], ['ni', 'me', 'tus'], ['maa', 'keel'], [')'], ['on'], ['lää', 'ne', 'me', 're', 'soo', 'me'], ['lõu', 'na', 'rüh', 'ma'], ['kuu', 'luv'], ['keel'], ['.']]
    elif lang == 'fra':
        assert syls == [['Le'], ['fran', 'çais'], ['est'], ['une'], ['langue'], ['in', 'do', 'eu', 'ro', 'péenne'], ['de'], ['la'], ['fa', 'mille'], ['des'], ['langues'], ['ro', 'manes'], ['dont'], ['les'], ['lo', 'cu', 'teurs'], ['sont'], ['ap', 'pe', 'lés'], ['fran', 'co', 'phones'], [','], ['éga', 'le', 'ment'], ['sur', 'nom', 'mé'], ['la'], ['langue'], ['de'], ['Mo', 'lière'], ['.']]
    elif lang == 'glg':
        assert syls == [['O'], ['ga', 'le', 'go'], ['('], ['['], ['ɡaˈleɣo̝'], [']'], [')'], ['é'], ['unha'], ['lin', 'gua'], ['in', 'do', 'eu', 'ro', 'pea'], ['que'], ['per', 'ten', 'ce'], ['á'], ['póla'], ['de'], ['lin', 'guas'], ['ro', 'má', 'ni', 'cas'], ['.']]
    elif lang.startswith('deu_'):
        assert syls == [['Die'], ['deut', 'sche'], ['Spra', 'che'], ['bzw.'], ['Deutsch'], ['('], ['['], ['dɔɪ̯tʃ];[26'], [']'], ['ab', 'ge', 'kürzt'], ['dt'], ['.'], ['oder'], ['dtsch'], ['.'], [')'], ['ist'], ['ei', 'ne'], ['west', 'ger', 'ma', 'ni', 'sche'], ['Spra', 'che'], [','], ['die'], ['welt', 'weit'], ['et', 'wa'], ['90'], ['bis'], ['105'], ['Mil', 'li', 'o', 'nen'], ['Men', 'schen'], ['als'], ['Mut', 'ter', 'spra', 'che'], ['und'], ['wei', 'te', 'ren'], ['rund'], ['80'], ['Mil', 'li', 'o', 'nen'], ['als'], ['Zweit'], ['oder'], ['Fremd', 'spra', 'che'], ['dient'], ['.']]
    elif lang == 'ell':
        assert syls == [['Η'], ['ελ', 'λη', 'νι', 'κή'], ['γλώσ', 'σα'], ['ανή', 'κει'], ['στην'], ['ιν', 'δο', 'ευ', 'ρω', 'παϊκή'], ['οι', 'κο', 'γένεια', '[9'], [']'], ['και'], ['απο', 'τε', 'λεί'], ['το'], ['μο', 'να', 'δι', 'κό'], ['μέλος'], ['του'], ['ελ', 'λη', 'νι', 'κού'], ['κλάδου'], [','], ['ενώ'], ['εί', 'ναι'], ['η'], ['επί', 'ση', 'μη'], ['γλώσ', 'σα'], ['της'], ['Ελ', 'λάδας'], ['και'], ['της'], ['Κύ', 'πρου'], ['.']]
    elif lang == 'hun':
        assert syls == [['A'], ['ma', 'gyar'], ['nyelv'], ['az'], ['urá', 'li'], ['nyelv', 'csa', 'lád'], ['tag', 'ja'], [','], ['a'], ['finn', 'ugor'], ['nyel', 'vek'], ['kö', 'zé'], ['tar', 'to', 'zó'], ['ugor'], ['nyel', 'vek'], ['egyi', 'ke'], ['.']]
    elif lang == 'isl':
        assert syls == [['Ís', 'lenska'], ['er'], ['vest', 'ur', 'nor', 'rænt'], [','], ['germ', 'anskt'], ['og'], ['indó', 'evr', 'ópskt'], ['tungu', 'mál'], ['sem'], ['er'], ['eink', 'um'], ['tal', 'að'], ['og'], ['rit', 'að'], ['á'], ['Ís', 'landi'], ['og'], ['er'], ['móð', 'ur', 'mál'], ['lang', 'flestra'], ['Ís', 'lend', 'inga'], ['.'], ['['], ['4'], [']']]
    elif lang == 'ind':
        assert syls == [['Ba', 'ha', 'sa'], ['In', 'do', 'ne', 'sia'], ['ada', 'lah'], ['ba', 'ha', 'sa'], ['na', 'si', 'o', 'nal'], ['dan'], ['res', 'mi'], ['di'], ['se', 'lu', 'r', 'uh'], ['In', 'do', 'ne', 'sia'], ['.']]
    elif lang == 'ita':
        assert syls == [["L'"], ['ita', 'lia', 'no'], ['('], ['['], ['itaˈ', 'l', 'jaː', 'no][', 'No', 'ta'], ['1'], [']'], ['ascol', 'ta[?·in', 'fo'], [']'], [')'], ['è'], ['una'], ['lin', 'gua'], ['ro', 'man', 'za'], ['par', 'la', 'ta'], ['prin', 'ci', 'pal', 'men', 'te'], ['in'], ['Ita', 'lia'], ['.']]
    elif lang == 'lit':
        assert syls == [['Lie', 'tu', 'vių'], ['kal', 'ba'], ['–'], ['iš'], ['bal', 'tų'], ['pro', 'kal', 'bės'], ['ki', 'lu', 'si'], ['lie', 'tu', 'vių'], ['tau', 'tos'], ['kal', 'ba'], [','], ['ku', 'ri'], ['Lie', 'tu', 'vo', 'je'], ['yra'], ['vals', 'ty', 'bi', 'nė'], [','], ['o'], ['Eu', 'ro', 'pos'], ['Są', 'jun', 'go', 'je'], ['–'], ['vie', 'na'], ['iš'], ['ofi', 'cia', 'lių', 'jų'], ['kal', 'bų'], ['.']]
    elif lang == 'lav':
        assert syls == [['Lat', 'vie', 'šu'], ['va', 'lo', 'da'], ['ir'], ['dzim', 'tā'], ['va', 'lo', 'da'], ['ap', 'mē', 'ram'], ['1,7'], ['mil', 'jo', 'niem'], ['cil', 'vē', 'ku'], [','], ['gal', 've', 'no', 'kārt'], ['Lat', 'vi', 'jā'], [','], ['kur'], ['tā'], ['ir'], ['vien', 'ī', 'gā'], ['valsts'], ['va', 'lo', 'da'], ['.'], ['['], ['3'], [']']]
    elif lang == 'mon':
        assert syls == [['Мон', 'гол'], ['хэл'], ['нь'], ['Мон', 'гол'], ['ул', 'сын'], ['ал', 'бан'], ['ёс', 'ны'], ['хэл'], ['юм'], ['.']]
    elif lang == 'nob':
        assert syls == [['Bok', 'mål'], ['er'], ['en'], ['va', 'rie', 'tet'], ['av'], ['norsk'], ['språk'], ['.']]
    elif lang == 'nno':
        assert syls == [['Ny', 'norsk'], [','], ['før'], ['1929'], ['of', 'fi', 'si', 'elt'], ['kal', 'la'], ['lands', 'mål'], [','], ['er'], ['si', 'dan'], ['jam', 'stil', 'lings', 'ved', 'ta', 'ket'], ['av'], ['12'], ['.'], ['mai'], ['1885'], ['ei'], ['av'], ['dei'], ['to'], ['of', 'fi', 'si', 'el', 'le'], ['mål', 'for', 'me', 'ne'], ['av'], ['norsk'], [';'], ['den'], ['and', 're'], ['for', 'ma'], ['er'], ['bok', 'mål'], ['.']]
    elif lang == 'pol':
        assert syls == [['Ję', 'zyk'], ['pol', 'ski'], [','], ['pol', 'sz', 'czy', 'zna'], ['–'], ['ję', 'zyk'], ['le', 'chic', 'ki'], ['z'], ['gru', 'py'], ['za', 'chod', 'nio', 'sło', 'wiań', 'skiej'], ['('], ['do'], ['któ', 'rej'], ['na', 'le', 'żą'], ['rów', 'nież'], ['cze', 'ski'], [','], ['ka', 'szub', 'ski'], [','], ['sło', 'wac', 'ki'], ['i'], ['ję', 'zy', 'ki'], ['łu', 'życ', 'kie'], [')'], [','], ['sta', 'no', 'wią', 'cej'], ['część'], ['ro', 'dzi', 'ny'], ['in', 'do', 'eu', 'ro', 'pej', 'skiej'], ['.']]
    elif lang.startswith('por_'):
        assert syls == [['A'], ['lín', 'gua'], ['por', 'tu', 'gue', 'sa'], [','], ['tam', 'bém'], ['de', 'sig', 'na', 'da'], ['por', 'tu', 'guês'], [','], ['é'], ['uma'], ['lín', 'gua'], ['in', 'do', 'eu', 'ro', 'peia'], ['ro', 'mâ', 'ni', 'ca'], ['fle', 'xi', 'va'], ['oci', 'den', 'tal'], ['ori', 'gi', 'na', 'da'], ['no'], ['ga', 'le', 'go', 'por', 'tu', 'guês'], ['fa', 'la', 'do'], ['no'], ['Rei', 'no'], ['da'], ['Ga', 'li', 'za'], ['e'], ['no'], ['nor', 'te'], ['de'], ['Por', 'tu', 'gal'], ['.']]
    elif lang == 'ron':
        assert syls == [['Lim', 'ba'], ['ro', 'mâ', 'nă'], ['es', 'te'], ['o'], ['lim', 'bă'], ['in', 'do', 'e', 'u', 'ro', 'pe', 'a', 'nă'], [','], ['din'], ['gru', 'pul'], ['ita', 'lic'], ['și'], ['din'], ['sub', 'gru', 'pul'], ['orien', 'tal'], ['al'], ['lim', 'bi', 'lor'], ['ro', 'ma', 'ni', 'ce'], ['.']]
    elif lang == 'rus':
        assert syls == [['Ру́с', 'ский'], ['язы́к'], ['('], ['['], ['ˈruskʲɪi̯'], ['jɪˈzɨk'], [']'], ['Ин', 'фор', 'ма', 'ция'], ['о'], ['фай', 'ле'], ['слу', 'шать)[~'], ['3'], [']'], ['['], ['⇨'], [']'], ['—'], ['один'], ['из'], ['вос', 'точ', 'но', 'сла', 'вян', 'ских'], ['язы', 'ков'], [','], ['на', 'ци', 'о', 'наль', 'ный'], ['язык'], ['рус', 'ско', 'го'], ['на', 'ро', 'да'], ['.']]
    elif lang == 'srp_cyrl':
        assert syls == [['Срп', 'ски'], ['је', 'зик'], ['при', 'па', 'да'], ['сло', 'вен', 'ској'], ['гру', 'пи'], ['је', 'зи', 'ка'], ['по', 'ро', 'ди', 'це'], ['ин', 'до', 'е', 'вроп', 'ских'], ['је', 'зи', 'ка', '.[12'], [']']]
    elif lang == 'srp_latn':
        assert syls == [['Srp', 'ski'], ['je', 'zik'], ['pri', 'pa', 'da'], ['slo', 'ven', 'skoj'], ['gru', 'pi'], ['je', 'zi', 'ka'], ['po', 'ro', 'di', 'ce'], ['in', 'do', 'e', 'vrop', 'skih'], ['je', 'zi', 'ka', '.[12'], [']']]
    elif lang == 'slk':
        assert syls == [['Slo', 'ven', 'či', 'na'], ['pat', 'rí'], ['do'], ['sku', 'pi', 'ny'], ['zá', 'pa', 'do', 'slo', 'van', 'ských'], ['ja', 'zy', 'kov'], ['('], ['spo', 'lu'], ['s'], ['češ', 'ti', 'nou'], [','], ['poľš', 'ti', 'nou'], [','], ['hor', 'nou'], ['a'], ['dol', 'nou'], ['lu', 'žic', 'kou'], ['srb', 'či', 'nou'], ['a'], ['ka', 'šub', 'či', 'nou'], [')'], ['.']]
    elif lang == 'slv':
        assert syls == [['Slo', 'ven', 'šči', 'na'], ['['], ['slo', 'ˈʋe', 'nʃtʃi', 'na'], [']'], ['je'], ['zdru', 'že', 'ni'], ['na', 'ziv'], ['za'], ['ura', 'dni'], ['knji', 'žni'], ['je', 'zik'], ['Slo', 'ven', 'cev'], ['in'], ['sku', 'pno'], ['ime'], ['za'], ['na', 're', 'čja'], ['in'], ['go', 'vo', 're'], [','], ['ki'], ['jih'], ['go', 'vo', 'ri', 'jo'], ['ali'], ['so'], ['jih'], ['ne', 'koč'], ['go', 'vo', 'ri', 'li'], ['Slo', 'ven', 'ci'], ['.']]
    elif lang == 'spa':
        assert syls == [['El'], ['es', 'pa', 'ñol'], ['o'], ['cas', 'te', 'llano'], ['es'], ['una'], ['len', 'gua'], ['ro', 'man', 'ce'], ['pro', 'ce', 'den', 'te'], ['del'], ['la', 'tín'], ['ha', 'bla', 'do'], [','], ['per', 'te', 'ne', 'cien', 'te'], ['a'], ['la'], ['fa', 'mi', 'lia'], ['de'], ['len', 'guas'], ['in', 'doeu', 'ro', 'peas'], ['.']]
    elif lang == 'swe':
        assert syls == [['Svens', 'ka'], ['('], ['svens', 'ka'], ['('], ['in', 'fo'], [')'], [')'], ['är'], ['ett'], ['öst', 'nor', 'diskt'], ['språk'], ['som'], ['ta', 'las'], ['av'], ['un', 'ge', 'fär'], ['tio'], ['mil', 'jo', 'ner'], ['per', 'so', 'ner'], ['främst'], ['i'], ['Sve', 'ri', 'ge'], ['där'], ['språ', 'ket'], ['har'], ['en'], ['do', 'mi', 'nant'], ['ställ', 'ning'], ['som'], ['hu', 'vud', 'språk'], [','], ['men'], ['även'], ['som'], ['det'], ['ena'], ['na', 'tio', 'nal', 'språ', 'ket'], ['i'], ['Fin', 'land'], ['och'], ['som'], ['en', 'da'], ['of', 'fi', 'ci', 'el', 'la'], ['språk'], ['på'], ['Åland'], ['.']]
    elif lang == 'tel':
        assert syls == [['తె', 'లు', 'గు'], ['అనే', 'ది'], ['ద్రా', 'విడ'], ['భా', 'షల'], ['కు', 'టుం', 'బా', 'ని', 'కి'], ['చెం', 'దిన'], ['భాష'], ['.']]
    elif lang == 'tha':
        assert syls == [['ภา', 'ษา', 'ไทย'], ['หรือ'], ['ภา', 'ษา', 'ไทย'], ['กลาง'], ['เป็น'], ['ภา', 'ษา'], ['ใน'], ['กลุ่ม'], ['ภา', 'ษา'], ['ไท'], ['ซึ่ง'], ['เป็น'], ['กลุ่ม', 'ย่อย'], ['ของ'], ['ตระ', 'กูล'], ['ภา', 'ษา'], ['ข'], ['ร้า'], ['-'], ['ไท'], ['และ'], ['เป็น'], ['ภา', 'ษา', 'ราช', 'การ'], ['และ'], ['ภา', 'ษา', 'ประ', 'จำ', 'ชาติ'], ['ของ'], ['ประ', 'เทศ'], ['ไทย'], ['['], ['3'], [']['], ['4'], [']']]
    elif lang == 'ukr':
        assert syls == [['Укра', 'ї', '́', 'н', 'сь', 'ка'], ['мо', '́', 'ва'], ['('], ['МФА'], [':'], ['['], ['ukrɑ̽ˈjɪnʲsʲkɑ̽'], ['ˈmɔwɑ̽'], [']'], [','], ['іс', 'то', 'ри', 'ч', 'ні'], ['на', 'зви'], ['—'], ['ру', '́', 'сь', 'ка'], [','], ['ру', 'си', '́', 'н', 'сь', 'ка', '[10][11][12'], [']'], ['['], ['*'], ['1'], [']'], [')'], ['—'], ['на', 'ціо', 'на', 'ль', 'на'], ['мо', 'ва'], ['укра', 'ї', 'н', 'ців'], ['.']]
    elif lang == 'zul':
        assert syls == [['Zu', 'lu'], ['/ˈzu', 'ːlu', 'ː/'], [','], ['no', 'ma'], ['isi', 'Zu', 'lu'], ['wu', 'li', 'mi'], ['lwa', 'ba', 'ntu'], ['ba', 'se'], ['Ni', 'ngi', 'zi', 'mu'], ['neA', 'fri', 'ka'], ['aba', 'yi', 'ngxe', 'nye'], ['ya', 'ma', 'Ngu', 'ni'], ['.']]
    else:
        raise Exception(f'Error: Tests for language "{lang}" is skipped!')

    if syl_tokenizer_skipped:
        raise Exception(f'Error: Tests for syllable tokenizer "{syl_tokenizer}" is skipped!')

@pytest.mark.parametrize('lang, syl_tokenizer', test_syl_tokenizers)
def test_syl_tokenize_tokens_no_punc(lang, syl_tokenizer):
    tokens = wl_word_tokenization.wl_word_tokenize_flat(
        main,
        text = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}'),
        lang = lang
    )
    syls_tokens = wl_syl_tokenization.wl_syl_tokenize_tokens_no_puncs(
        main,
        tokens = tokens,
        lang = lang,
        syl_tokenizer = syl_tokenizer
    )

    # Check for empty syllables
    assert all(all(syls_token) for syls_token in syls_tokens)

    # The count of syllable should be more than the count of tokens
    assert sum((len(syls_token) for syls_token in syls_tokens)) > len(tokens)

    # Length of syllabified tokens should be equal to or less than the length of tokens
    assert len(syls_tokens) <= len(tokens)

    # Check for punctuation marks
    assert not any((
        bool(len(syls) == 1 and wl_checks_tokens.is_punc(syls[0]))
        for syls in syls_tokens
    ))

if __name__ == '__main__':
    for lang, syl_tokenizer in test_syl_tokenizers:
        test_syl_tokenize(lang, syl_tokenizer)

    for lang, syl_tokenizer in test_syl_tokenizers:
        test_syl_tokenize_tokens_no_punc(lang, syl_tokenizer)
