#
# Wordless: Tests - Text - Syllable Tokenization
#
# Copyright (C) 2018-2021  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import sys

sys.path.append('.')

import pytest

from wl_tests import wl_test_init, wl_test_lang_examples
from wl_text import wl_syl_tokenization, wl_word_tokenization
from wl_utils import wl_conversion, wl_misc

test_syl_tokenizers = []

main = wl_test_init.Wl_Test_Main()

for lang, syl_tokenizers in main.settings_global['syl_tokenizers'].items():
    for syl_tokenizer in syl_tokenizers:
        if lang not in ['other']:
            test_syl_tokenizers.append((lang, syl_tokenizer))

@pytest.mark.parametrize('lang, syl_tokenizer', test_syl_tokenizers)
def test_syl_tokenize(lang, syl_tokenizer):
    lang_text = wl_conversion.to_lang_text(main, lang)

    print(f'{lang_text} ({lang}) / {syl_tokenizer}:')

    tokens = wl_word_tokenization.wl_word_tokenize(
        main,
        text = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}'),
        lang = lang
    )
    tokens = list(wl_misc.flatten_list(tokens))
    
    syls = wl_syl_tokenization.wl_syl_tokenize(
        main,
        tokens = tokens,
        lang = lang,
        syl_tokenizer = syl_tokenizer
    )

    print(syls)

    # The count of syllables should be more than 1
    assert sum([len(syls_token) for syls_token in syls]) > 1

    if lang == 'afr':
        assert syls == [['Afri', 'kaans'], ['is'], ['ti', 'po', 'lo', 'gies'], ['be', 'skou'], ["'"], ['n'], ['In', 'do'], ['', ''], ['Eu', 'ro', 'pe', 'se'], [','], ['Wes'], ['', ''], ['Ger', 'maan', 'se'], [','], ['Ne', 'derfran', 'kie', 'se'], ['taal', ',[2'], [']'], ['wat'], ['aan'], ['die'], ['suid', 'punt'], ['van'], ['Afri', 'ka'], ['on', 'der'], ['in', 'vloed'], ['van'], ['ver', 'skeie'], ['an', 'der'], ['ta', 'le'], ['en'], ['taal', 'groe', 'pe'], ['ont', 'staan'], ['het'], ['.']]
    elif lang == 'sqi':
        assert syls == [['Gju', 'ha'], ['shqi', 'pe'], ['('], ['ose'], ['thje', 'sh', 'të'], ['shqi', 'p', 'ja'], [')'], ['ësh', 'të'], ['gju', 'hë'], ['dhe'], ['de', 'gë'], ['e'], ['ve', 'ça', 'n', 'të'], ['e'], ['fa', 'mi', 'l', 'jes'], ['in', 'do'], ['', ''], ['ev', 'ro', 'pi', 'ane'], ['të'], ['fo', 'lur'], ['nga'], ['më'], ['shu', 'më'], ['se'], ['6'], ['mi', 'li', 'onë'], ['nje', 'rëz[4'], [']'], [','], ['kry', 'esisht'], ['në'], ['Shqi', 'pë', 'ri'], [','], ['Ko', 'so', 'vë'], ['dhe'], ['Re', 'pu', 'b', 'li', 'kën'], ['e'], ['Ma', 'qe', 'do', 'ni', 'së'], [','], ['por'], ['edhe'], ['në'], ['zo', 'na'], ['të'], ['tje', 'ra'], ['të'], ['Ev', 'ro', 'pës'], ['Ju', 'go', 're'], ['ku'], ['ka'], ['një'], ['po', 'pu', 'll', 'si'], ['shqi', 'p', 'ta', 're'], [','], ['du', 'ke'], ['pë', 'r', 'f', 'shi', 'rë'], ['Ma', 'lin'], ['e'], ['Zi'], ['dhe'], ['Lu', 'gi', 'nën'], ['e'], ['Pre', 'she', 'vës'], ['.']]
    elif lang == 'bel':
        assert syls == [['Бе', 'ла', 'ру́с', 'кая'], ['мо́', 'ва'], ['—'], ['на', 'цы', 'я', 'на', 'ль', 'ная'], ['мо', 'ва'], ['бе', 'ла', 'ру', 'саў'], [','], ['ува', 'хо', 'дзіць'], ['у'], ['ін', 'да', 'еў', 'ра', 'пей', 'с', 'кую'], ['моў', 'ную'], ['ся', "м'ю"], [','], ['сла', 'вя', 'н', 'с', 'кую'], ['гру', 'пу'], [','], ['ус', 'хо', 'д', 'не', 'с', 'ла', 'вя', 'н', 'с', 'кую'], ['па', 'д', 'г', 'ру', 'пу'], ['.']]
    elif lang == 'bul':
        assert syls == [['Бъ', '̀л', 'гар', 'с', 'ки', 'ят'], ['ез', 'ѝк'], ['е'], ['ин', 'до', 'ев', 'ро', 'пейс', 'ки'], ['език'], ['от'], ['гру', 'па', 'та'], ['на'], ['юж', 'нос', 'ла', 'вян', 'с', 'ки', 'те'], ['ези', 'ци'], ['.']]
    elif lang == 'hrv':
        assert syls == [['Hr', 'vat', 'ski'], ['je', 'zik'], ['('], ['ISO'], ['639'], ['', ''], ['3'], [':'], ['hrv'], [')'], ['skup', 'ni'], ['je'], ['na', 'ziv'], ['za'], ['na', 'ci', 'onal', 'ni'], ['stan', 'dard', 'ni'], ['je', 'zik'], ['Hr', 'va', 'ta'], [','], ['te'], ['za'], ['skup'], ['na', 'rje', 'čja'], ['i'], ['go', 'vo', 'ra'], ['ko', 'ji', 'ma'], ['go', 'vo', 're'], ['ili'], ['su'], ['ne', 'ka', 'da'], ['go', 'vo', 'ri', 'li'], ['Hr', 'va', 'ti'], ['.']]
    elif lang == 'ces':
        assert syls == [['Češ', 'ti', 'na'], ['ne', 'bo', 'li'], ['čes', 'ký'], ['ja', 'zyk'], ['je'], ['zá', 'pa', 'doslo', 'van', 'ský'], ['ja', 'zyk'], [','], ['nej', 'bliž', 'ší'], ['slo', 'ven', 'šti', 'ně'], [','], ['po', 'té'], ['lužic', 'ké'], ['srbšti', 'ně'], ['a'], ['pol', 'šti', 'ně'], ['.']]
    elif lang == 'dan':
        assert syls == [['Dansk'], ['er'], ['et'], ['nord', 'ger', 'mansk'], ['sprog'], ['af'], ['den'], ['øst', 'n', 'or', 'di', 'ske'], ['('], ['kon', 'ti', 'nen', 'tale'], [')'], ['grup', 'pe'], [','], ['der'], ['ta', 'les'], ['af'], ['ca.'], ['seks'], ['mil', 'li', 'o', 'ner'], ['men', 'ne', 'sker'], ['.']]
    elif lang == 'nld':
        assert syls == [['Het'], ['Ne', 'der', 'lands'], ['is'], ['een'], ['Wes', 't', 'Ger', 'maan', 'se'], ['taal'], ['en'], ['de'], ['of', 'fi', 'ci', 'ë', 'le'], ['taal'], ['van'], ['Ne', 'der', 'land'], [','], ['Su', 'ri', 'na', 'me'], ['en'], ['een'], ['van'], ['de'], ['drie'], ['of', 'fi', 'ci', 'ë', 'le'], ['ta', 'len'], ['van'], ['Bel', 'gië'], ['.']]
    elif lang == 'eng_gb':
        assert syls == [['Eng', 'lish'], ['is'], ['a'], ['West'], ['Ger', 'man', 'ic'], ['lan', 'guage'], ['ori', 'gin', 'ally'], ['spoken'], ['by'], ['the'], ['in', 'hab', 'it', 'ants'], ['of'], ['early'], ['me', 'di', 'ev', 'al'], ['Eng', 'land.[3][4][5'], [']']]
    elif lang == 'eng_us':
        assert syls == [['Eng', 'lish'], ['is'], ['a'], ['West'], ['Ger', 'man', 'ic'], ['lan', 'guage'], ['orig', 'i', 'nal', 'ly'], ['spo', 'ken'], ['by'], ['the'], ['in', 'hab', 'i', 'tants'], ['of'], ['ear', 'ly'], ['me', 'dieval'], ['Eng', 'land.[3][4][5'], [']']]
    elif lang == 'epo':
        assert syls == [['Es', 'pe', 'r', 'anto'], [','], ['ori', 'gi', 'ne'], ['la'], ['Lin', 'g', 'vo'], ['In', 'ter', 'na', 'ci', 'a', ',[4'], [']'], ['es', 'tas'], ['la'], ['plej'], ['dis', 'vas', 't', 'iĝ', 'inta'], ['in', 'ter', 'na', 'cia'], ['plan', 'lin', 'g', 'vo', '.[5'], [']']]
    elif lang == 'est':
        assert syls == [['Ees', 'ti'], ['keel'], ['('], ['vara', 'sem'], ['ni', 'me', 'tus'], ['maa', 'keel'], [')'], ['on'], ['lää', 'ne', 'me', 're', 'soo', 'me'], ['lõu', 'na', 'rüh', 'ma'], ['kuu', 'luv'], ['keel'], ['.']]
    elif lang == 'fra':
        assert syls == [['Le'], ['fran', 'çais'], ['est'], ['une'], ['langue'], ['in', 'do', 'eu', 'ro', 'péenne'], ['de'], ['la'], ['fa', 'mille'], ['des'], ['langues'], ['ro', 'manes'], ['dont'], ['les'], ['lo', 'cu', 'teurs'], ['sont'], ['ap', 'pe', 'lés'], ['fran', 'co', 'phones'], ['.']]
    elif lang == 'glg':
        assert syls == [['O'], ['ga', 'le', 'go'], ['('], ['['], ['ɡaˈleɣo̝'], [']'], [')'], ['é'], ['unha'], ['lin', 'gua'], ['in', 'do', 'eu', 'ro', 'pea'], ['que'], ['per', 'ten', 'ce'], ['á'], ['póla'], ['de'], ['lin', 'guas'], ['ro', 'má', 'ni', 'cas'], ['.']]
    elif lang in ['deu_at', 'deu_de', 'deu_ch']:
        assert syls == [['Die'], ['deut', 'sche'], ['Spra', 'che'], ['bzw.'], ['das'], ['Deut', 'sche'], ['('], ['['], ['dɔɪ̯tʃ];[26'], [']'], ['ab', 'ge', 'kürzt'], ['dt'], ['.'], ['oder'], ['dtsch'], ['.'], [')'], ['ist'], ['ei', 'ne'], ['west', 'ger', 'ma', 'ni', 'sche'], ['Spra', 'che'], [','], ['die'], ['welt', 'weit'], ['et', 'wa'], ['90'], ['bis'], ['105'], ['Mil', 'li', 'o', 'nen'], ['Men', 'schen'], ['als'], ['Mut', 'ter', 'spra', 'che'], ['und'], ['wei', 'te', 'ren'], ['rund'], ['80'], ['Mil', 'li', 'o', 'nen'], ['als'], ['Zweit', ''], ['oder'], ['Fremd', 'spra', 'che'], ['dient'], ['.']]
    elif lang == 'ell':
        assert syls == [['Η'], ['ελ', 'λη', 'νι', 'κή'], ['γλώσ', 'σα'], ['ανή', 'κει'], ['στην'], ['ιν', 'δο', 'ευ', 'ρω', 'παϊκή'], ['οι', 'κο', 'γένεια', '[10'], [']'], ['και'], ['απο', 'τε', 'λεί'], ['το'], ['μο', 'να', 'δι', 'κό'], ['μέλος'], ['του'], ['ελ', 'λη', 'νι', 'κού'], ['κλάδου'], [','], ['ενώ'], ['εί', 'ναι'], ['η'], ['επί', 'ση', 'μη'], ['γλώσ', 'σα'], ['της'], ['Ελ', 'λάδος'], ['και'], ['της'], ['Κύ', 'πρου'], ['.']]
    elif lang == 'hun':
        assert syls == [['A'], ['ma', 'gyar'], ['nyelv'], ['az'], ['urá', 'li'], ['nyelv', 'csa', 'lád'], ['tag', 'ja'], [','], ['a'], ['finn', 'ugor'], ['nyel', 'vek'], ['kö', 'zé'], ['tar', 'to', 'zó'], ['ugor'], ['nyel', 'vek'], ['egyi', 'ke'], ['.']]
    elif lang == 'isl':
        assert syls == [['Ís', 'lenska'], ['er'], ['vest', 'ur', 'nor', 'rænt'], [','], ['germ', 'anskt'], ['og'], ['indó', 'evr', 'ópskt'], ['tungu', 'mál'], ['sem'], ['er'], ['eink', 'um'], ['tal', 'að'], ['og'], ['rit', 'að'], ['á'], ['Ís', 'landi'], ['og'], ['er'], ['móð', 'ur', 'mál'], ['lang', 'flestra'], ['Ís', 'lend', 'inga'], ['.'], ['['], ['4'], [']']]
    elif lang == 'ind':
        assert syls == [['Ba', 'ha', 'sa'], ['In', 'do', 'ne', 'sia'], ['ada', 'lah'], ['ba', 'ha', 'sa'], ['Me', 'la', 'yu'], ['ba', 'ku'], ['yang'], ['di', 'ja', 'di', 'kan'], ['se', 'ba', 'gai'], ['ba', 'ha', 'sa'], ['res', 'mi'], ['Re', 'pub', 'lik'], ['In', 'do', 'ne', 'si', 'a[1'], [']'], ['dan'], ['ba', 'ha', 'sa'], ['per', 'sa', 'tu', 'an'], ['bang', 'sa'], ['In', 'do', 'ne', 'si', 'a.[2'], [']']]
    elif lang == 'ita':
        assert syls == [["L'"], ['ita', 'lia', 'no'], ['('], ['['], ['itaˈ', 'l', 'jaː', 'no][', 'No', 'ta'], ['1'], [']'], ['ascol', 'ta[?·in', 'fo'], [']'], [')'], ['è'], ['una'], ['lin', 'gua'], ['ro', 'man', 'za'], ['par', 'la', 'ta'], ['prin', 'ci', 'pal', 'men', 'te'], ['in'], ['Ita', 'lia'], ['.']]
    elif lang == 'lit':
        assert syls == [['Lie', 'tu', 'vių'], ['kal', 'ba'], ['–'], ['iš'], ['bal', 'tų'], ['pro', 'kal', 'bės'], ['ki', 'lu', 'si'], ['lie', 'tu', 'vių'], ['tau', 'tos'], ['kal', 'ba'], [','], ['ku', 'ri'], ['Lie', 'tu', 'vo', 'je'], ['yra'], ['vals', 'ty', 'bi', 'nė'], [','], ['o'], ['Eu', 'ro', 'pos'], ['Są', 'jun', 'go', 'je'], ['–'], ['vie', 'na'], ['iš'], ['ofi', 'cia', 'lių', 'jų'], ['kal', 'bų'], ['.']]
    elif lang == 'lav':
        assert syls == [['Lat', 'vie', 'šu'], ['va', 'lo', 'da'], ['ir'], ['dzim', 'tā'], ['va', 'lo', 'da'], ['ap', 'mē', 'ram'], ['1,7'], ['mil', 'jo', 'niem'], ['cil', 'vē', 'ku'], [','], ['gal', 've', 'no', 'kārt'], ['Lat', 'vi', 'jā'], [','], ['kur'], ['tā'], ['ir'], ['vien', 'ī', 'gā'], ['valsts'], ['va', 'lo', 'da.[3'], [']']]
    elif lang == 'lav':
        assert syls == [['Lat', 'vie', 'šu'], ['va', 'lo', 'da'], ['ir'], ['dzim', 'tā'], ['va', 'lo', 'da'], ['ap', 'mē', 'ram'], ['1,7'], ['mil', 'jo', 'niem'], ['cil', 'vē', 'ku'], [','], ['gal', 've', 'no', 'kārt'], ['Lat', 'vi', 'jā'], [','], ['kur'], ['tā'], ['ir'], ['vien', 'ī', 'gā'], ['valsts'], ['va', 'lo', 'da.[3'], [']']]
    elif lang == 'mon':
        assert syls == [['Мон', 'гол'], ['хэл'], ['нь'], ['Мон', 'гол'], ['ул', 'сын'], ['ал', 'бан'], ['ёс', 'ны'], ['хэл'], ['юм'], ['.']]
    elif lang == 'nob':
        assert syls == [['Bok', 'mål'], ['er'], ['en'], ['va', 'rie', 'tet'], ['av'], ['norsk'], ['språk'], ['.']]
    elif lang == 'nno':
        assert syls == [['Ny', 'norsk'], [','], ['før'], ['1929'], ['of', 'fi', 'si', 'elt'], ['kal', 'la'], ['lands', 'mål'], [','], ['er'], ['si', 'dan'], ['jam', 'stil', 'lings', 'ved', 'ta', 'ket'], ['av'], ['12'], ['.'], ['mai'], ['1885'], ['ei'], ['av'], ['dei'], ['to'], ['of', 'fi', 'si', 'el', 'le'], ['mål', 'for', 'me', 'ne'], ['av'], ['norsk'], [';'], ['den'], ['and', 're'], ['for', 'ma'], ['er'], ['bok', 'mål'], ['.']]
    elif lang == 'pol':
        assert syls == [['Ję', 'zyk'], ['pol', 'ski'], [','], ['pol', 'sz', 'czy', 'zna'], ['–'], ['ję', 'zyk'], ['le', 'chic', 'ki'], ['z'], ['gru', 'py'], ['za', 'chod', 'nio', 'sło', 'wiań', 'skiej'], ['('], ['do'], ['któ', 'rej'], ['na', 'le', 'żą'], ['rów', 'nież'], ['cze', 'ski'], [','], ['ka', 'szub', 'ski'], [','], ['sło', 'wac', 'ki'], ['i'], ['ję', 'zy', 'ki'], ['łu', 'życ', 'kie'], [')'], [','], ['sta', 'no', 'wią', 'cej'], ['część'], ['ro', 'dzi', 'ny'], ['in', 'do', 'eu', 'ro', 'pej', 'skiej'], ['.']]
    elif lang in ['por_br', 'por_pt']:
        assert syls == [['A'], ['lín', 'gua'], ['por', 'tu', 'gue', 'sa'], [','], ['tam', 'bém'], ['de', 'sig', 'na', 'da'], ['por', 'tu', 'guês'], [','], ['é'], ['uma'], ['lín', 'gua'], ['ro', 'mâ', 'ni', 'ca'], ['fle', 'xi', 'va'], ['oci', 'den', 'tal'], ['ori', 'gi', 'na', 'da'], ['no'], ['ga', 'le', 'go', 'por', 'tu', 'guês'], ['fa', 'la', 'do'], ['no'], ['Rei', 'no'], ['da'], ['Ga', 'li', 'za'], ['e'], ['no'], ['nor', 'te'], ['de'], ['Por', 'tu', 'gal'], ['.']]
    elif lang == 'ron':
        assert syls == [['Lim', 'ba'], ['ro', 'mâ', 'nă'], ['es', 'te'], ['o'], ['lim', 'bă'], ['in', 'do', 'e', 'u', 'ro', 'pe', 'a', 'nă'], [','], ['din'], ['gru', 'pul'], ['ita', 'lic'], ['și'], ['din'], ['sub', 'gru', 'pul'], ['orien', 'tal'], ['al'], ['lim', 'bi', 'lor'], ['ro', 'ma', 'ni', 'ce'], ['.']]
    elif lang == 'rus':
        assert syls == [['Ру́с', 'ский'], ['язы́к'], ['('], ['['], ['ˈruskʲɪi̯'], ['jɪˈzɨk'], [']'], ['Ин', 'фор', 'ма', 'ция'], ['о'], ['фай', 'ле'], ['слу', 'шать'], [')'], ['['], ['~'], ['3'], [']'], ['['], ['⇨'], [']'], ['—'], ['один'], ['из'], ['вос', 'точ', 'но', 'сла', 'вян', 'ских'], ['язы', 'ков'], [','], ['на', 'ци', 'о', 'наль', 'ный'], ['язык'], ['рус', 'ско', 'го'], ['на', 'ро', 'да'], ['.']]
    elif lang == 'srp_cyrl':
        assert syls == [['Срп', 'ски'], ['је', 'зик'], ['при', 'па', 'да'], ['сло', 'вен', 'ској'], ['гру', 'пи'], ['је', 'зи', 'ка'], ['по', 'ро', 'ди', 'це'], ['ин', 'до', 'е', 'вроп', 'ских'], ['је', 'зи', 'ка', '.[12'], [']']]
    elif lang == 'srp_latn':
        assert syls == [['Srpski'], ['jezik'], ['pripada'], ['slovenskoj'], ['grupi'], ['jezika'], ['porodice'], ['indoevropskih'], ['jezika.[12'], [']']]
    elif lang == 'slk':
        assert syls == [['Slo', 'ven', 'či', 'na'], ['pat', 'rí'], ['do'], ['sku', 'pi', 'ny'], ['zá', 'pa', 'do', 'slo', 'van', 'ských'], ['ja', 'zy', 'kov'], ['('], ['spo', 'lu'], ['s'], ['češ', 'ti', 'nou'], [','], ['poľš', 'ti', 'nou'], [','], ['hor', 'nou'], ['a'], ['dol', 'nou'], ['lu', 'žic', 'kou'], ['srb', 'či', 'nou'], ['a'], ['ka', 'šub', 'či', 'nou'], [')'], ['.']]
    elif lang == 'slv':
        assert syls == [['Slo', 'ven', 'šči', 'na'], ['['], ['slo', 'vén', 'šči', 'na'], [']'], ['/'], ['['], ['slo', 'ˈʋe', 'nʃtʃi', 'na'], [']'], ['je'], ['zdru', 'že', 'ni'], ['na', 'ziv'], ['za'], ['ura', 'dni'], ['knji', 'žni'], ['je', 'zik'], ['Slo', 'ven', 'cev'], ['in'], ['sku', 'pno'], ['ime'], ['za'], ['na', 're', 'čja'], ['in'], ['go', 'vo', 're'], [','], ['ki'], ['jih'], ['go', 'vo', 'ri', 'jo'], ['ali'], ['so'], ['jih'], ['ne', 'koč'], ['go', 'vo', 'ri', 'li'], ['Slo', 'ven', 'ci'], ['.']]
    elif lang == 'spa':
        assert syls == [['El'], ['es', 'pa', 'ñol'], ['o'], ['cas', 'te', 'llano'], ['es'], ['una'], ['len', 'gua'], ['ro', 'man', 'ce'], ['pro', 'ce', 'den', 'te'], ['del'], ['la', 'tín'], ['ha', 'bla', 'do'], ['.']]
    elif lang == 'swe':
        assert syls == [['Svens', 'ka'], ['('], ['svens', 'ka'], ['('], ['in', 'fo'], [')'], [')'], ['är'], ['ett'], ['öst', 'nor', 'diskt'], ['språk'], ['som'], ['ta', 'las'], ['av'], ['un', 'ge', 'fär'], ['tio'], ['mil', 'jo', 'ner'], ['per', 'so', 'ner'], ['främst'], ['i'], ['Sve', 'ri', 'ge'], ['där'], ['språ', 'ket'], ['har'], ['en'], ['do', 'mi', 'nant'], ['ställ', 'ning'], ['som'], ['hu', 'vud', 'språk'], [','], ['men'], ['även'], ['som'], ['det'], ['ena'], ['na', 'tio', 'nal', 'språ', 'ket'], ['i'], ['Fin', 'land'], ['och'], ['som'], ['en', 'da'], ['of', 'fi', 'ci', 'el', 'la'], ['språk'], ['på'], ['Åland'], ['.']]
    elif lang == 'tel':
        assert syls == [['ఆం', 'ధ్ర'], ['ప్ర', 'దే', 'శ్'], [','], ['తె', 'లం', 'గాణ'], ['రా', 'ష్ట్రాల'], ['అధి', 'కార'], ['భాష'], ['తె', 'లు', 'గు'], ['.']]
    elif lang == 'ukr':
        assert syls == [['Укра', 'ї', '́', 'н', 'сь', 'ка'], ['мо', '́', 'ва'], ['('], ['МФА'], [':'], ['['], ['ukrɑ̽ˈjɪnʲsʲkɑ̽'], ['ˈmɔwɑ̽'], [']'], [','], ['іс', 'то', 'ри', 'ч', 'ні'], ['на', 'зви'], ['—'], ['ру', '́', 'сь', 'ка'], [','], ['ру', 'си', '́', 'н', 'сь', 'ка', '[9][10][11'], [']'], ['['], ['*'], ['2'], [']'], [')'], ['—'], ['на', 'ціо', 'на', 'ль', 'на'], ['мо', 'ва'], ['укра', 'ї', 'н', 'ців'], ['.']]
    elif lang == 'zul':
        assert syls == [['Zu', 'lu'], ['/ˈzu', 'ːlu', 'ː/'], [','], ['no', 'ma'], ['isi', 'Zu', 'lu'], ['wu', 'li', 'mi'], ['lwa', 'ba', 'ntu'], ['ba', 'se'], ['Ni', 'ngi', 'zi', 'mu'], ['neA', 'fri', 'ka'], ['aba', 'yi', 'ngxe', 'nye'], ['ya', 'ma', 'Ngu', 'ni'], ['.']]
    else:
        raise Exception(f'Warning: language code "{lang}" is absent from the list!')

if __name__ == '__main__':
    for lang, syl_tokenizer in test_syl_tokenizers:
        test_syl_tokenize(lang, syl_tokenizer)

