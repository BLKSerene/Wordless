#
# Wordless: Tests - Text - POS Tagging
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
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
from wl_text import wl_pos_tagging, wl_word_tokenization
from wl_utils import wl_conversion

test_pos_taggers = []

main = wl_test_init.Wl_Test_Main()

for lang, pos_taggers in main.settings_global['pos_taggers'].items():
    for pos_tagger in pos_taggers:
        if lang not in ['other']:
            test_pos_taggers.append((lang, pos_tagger))

@pytest.mark.parametrize('lang, pos_tagger', test_pos_taggers)
def test_pos_tag(lang, pos_tagger, show_results = False):
    lang_text = wl_conversion.to_lang_text(main, lang)

    tokens = wl_word_tokenization.wl_word_tokenize(
        main,
        text = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}'),
        lang = lang
    )

    tokens_tagged = wl_pos_tagging.wl_pos_tag(
        main,
        tokens = tokens,
        lang = lang,
        pos_tagger = pos_tagger
    )
    tokens_tagged_universal = wl_pos_tagging.wl_pos_tag(
        main,
        tokens = tokens,
        lang = lang,
        pos_tagger = pos_tagger,
        tagset = 'universal'
    )

    if show_results:
        print(f'{lang} / {pos_tagger}:')
        print(tokens_tagged)
        print(tokens_tagged_universal)

    if lang == 'zho_cn':
        assert tokens_tagged == [('汉语', 'nz'), ('，', 'x'), ('又称', 'n'), ('汉文', 'nz'), ('、', 'x'), ('中文', 'nz'), ('、', 'x'), ('中国', 'ns'), ('话', 'n'), ('、', 'x'), ('中国', 'ns'), ('语', 'ng'), ('、', 'x'), ('华语', 'nz'), ('、', 'x'), ('华文', 'nz'), ('、', 'x'), ('唐', 'nr'), ('话', 'n'), ('[', 'x'), ('2', 'x'), (']', 'x'), ('，', 'x'), ('或', 'c'), ('被', 'p'), ('视为', 'v'), ('一个', 'm'), ('语族', 'n'), ('，', 'x'), ('或', 'c'), ('被', 'p'), ('视为', 'v'), ('隶属于', 'n'), ('汉藏语系', 'nz'), ('汉语', 'nz'), ('族', 'ng'), ('之', 'u'), ('一种', 'm'), ('语言', 'n'), ('。', 'x')]
        assert tokens_tagged_universal == [('汉语', 'PROPN'), ('，', 'PUNCT/SYM'), ('又称', 'NOUN'), ('汉文', 'PROPN'), ('、', 'PUNCT/SYM'), ('中文', 'PROPN'), ('、', 'PUNCT/SYM'), ('中国', 'PROPN'), ('话', 'NOUN'), ('、', 'PUNCT/SYM'), ('中国', 'PROPN'), ('语', 'NOUN'), ('、', 'PUNCT/SYM'), ('华语', 'PROPN'), ('、', 'PUNCT/SYM'), ('华文', 'PROPN'), ('、', 'PUNCT/SYM'), ('唐', 'PRONP'), ('话', 'NOUN'), ('[', 'PUNCT/SYM'), ('2', 'PUNCT/SYM'), (']', 'PUNCT/SYM'), ('，', 'PUNCT/SYM'), ('或', 'CONJ'), ('被', 'ADP'), ('视为', 'VERB'), ('一个', 'NUM'), ('语族', 'NOUN'), ('，', 'PUNCT/SYM'), ('或', 'CONJ'), ('被', 'ADP'), ('视为', 'VERB'), ('隶属于', 'NOUN'), ('汉藏语系', 'PROPN'), ('汉语', 'PROPN'), ('族', 'NOUN'), ('之', 'PART'), ('一种', 'NUM'), ('语言', 'NOUN'), ('。', 'PUNCT/SYM')]
    elif lang == 'zho_tw':
        assert tokens_tagged == [('漢語', 'nz'), ('，', 'x'), ('又', 'd'), ('稱', 'v'), ('漢文', 'nz'), ('、', 'x'), ('中文', 'nz'), ('、', 'x'), ('中國', 'ns'), ('話', 'n'), ('、', 'x'), ('中國', 'ns'), ('語', 'n'), ('、', 'x'), ('華語', 'nz'), ('、', 'x'), ('華文', 'nz'), ('、', 'x'), ('唐', 'nr'), ('話', 'n'), ('[', 'x'), ('2', 'x'), (']', 'x'), ('，', 'x'), ('或', 'c'), ('被', 'p'), ('視為', 'v'), ('一個', 'm'), ('語族', 'n'), ('，', 'x'), ('或', 'c'), ('被', 'p'), ('視為', 'v'), ('隸', 'j'), ('屬', 'v'), ('於', 'nr'), ('漢藏語', 'nz'), ('系漢', 'n'), ('語族', 'n'), ('之一', 'r'), ('種語', 'n'), ('言', 'vg'), ('。', 'x')]
        assert tokens_tagged_universal == [('漢語', 'PROPN'), ('，', 'PUNCT/SYM'), ('又', 'ADV'), ('稱', 'VERB'), ('漢文', 'PROPN'), ('、', 'PUNCT/SYM'), ('中文', 'PROPN'), ('、', 'PUNCT/SYM'), ('中國', 'PROPN'), ('話', 'NOUN'), ('、', 'PUNCT/SYM'), ('中國', 'PROPN'), ('語', 'NOUN'), ('、', 'PUNCT/SYM'), ('華語', 'PROPN'), ('、', 'PUNCT/SYM'), ('華文', 'PROPN'), ('、', 'PUNCT/SYM'), ('唐', 'PRONP'), ('話', 'NOUN'), ('[', 'PUNCT/SYM'), ('2', 'PUNCT/SYM'), (']', 'PUNCT/SYM'), ('，', 'PUNCT/SYM'), ('或', 'CONJ'), ('被', 'ADP'), ('視為', 'VERB'), ('一個', 'NUM'), ('語族', 'NOUN'), ('，', 'PUNCT/SYM'), ('或', 'CONJ'), ('被', 'ADP'), ('視為', 'VERB'), ('隸', 'X'), ('屬', 'VERB'), ('於', 'PRONP'), ('漢藏語', 'PROPN'), ('系漢', 'NOUN'), ('語族', 'NOUN'), ('之一', 'PRON'), ('種語', 'NOUN'), ('言', 'VERB'), ('。', 'PUNCT/SYM')]
    elif lang == 'dan':
        assert tokens_tagged == [('Dansk', 'ADJ__Definite=Ind|Degree=Pos|Number=Sing'), ('er', 'AUX__Mood=Ind|Tense=Pres|VerbForm=Fin|Voice=Act'), ('et', 'DET__Gender=Neut|Number=Sing|PronType=Ind'), ('nordgermansk', 'ADJ__Definite=Ind|Degree=Pos|Number=Sing'), ('sprog', 'NOUN__Definite=Ind|Gender=Neut|Number=Sing'), ('af', 'ADP__AdpType=Prep'), ('den', 'DET__Gender=Com|Number=Sing|PronType=Dem'), ('østnordiske', 'ADJ__Definite=Def|Degree=Pos|Number=Sing'), ('(', 'PUNCT'), ('kontinentale', 'ADJ__Degree=Pos|Number=Plur'), (')', 'PUNCT'), ('gruppe', 'NOUN__Definite=Ind|Gender=Com|Number=Sing'), (',', 'PUNCT'), ('der', 'PRON__PartType=Inf'), ('tales', 'VERB__Mood=Ind|Tense=Pres|VerbForm=Fin|Voice=Pass'), ('af', 'ADP__AdpType=Prep'), ('ca.', 'ADV'), ('seks', 'NUM__NumType=Card'), ('millioner', 'NOUN__Definite=Ind|Gender=Com|Number=Plur'), ('mennesker', 'NOUN__Definite=Ind|Gender=Neut|Number=Plur'), ('.', 'PUNCT')]
        assert tokens_tagged_universal == [('Dansk', 'ADJ'), ('er', 'AUX'), ('et', 'DET'), ('nordgermansk', 'ADJ'), ('sprog', 'NOUN'), ('af', 'ADP'), ('den', 'DET'), ('østnordiske', 'ADJ'), ('(', 'PUNCT'), ('kontinentale', 'ADJ'), (')', 'PUNCT'), ('gruppe', 'NOUN'), (',', 'PUNCT'), ('der', 'PRON'), ('tales', 'VERB'), ('af', 'ADP'), ('ca.', 'ADV'), ('seks', 'NUM'), ('millioner', 'NOUN'), ('mennesker', 'NOUN'), ('.', 'PUNCT')]
    elif lang == 'nld':
        assert tokens_tagged == [('Het', 'LID|bep|stan|evon__Definite=Def'), ('Nederlands', 'N|eigen|ev|basis|onz|stan__Gender=Neut|Number=Sing'), ('is', 'WW|pv|tgw|ev__Number=Sing|Tense=Pres|VerbForm=Fin'), ('een', 'LID|onbep|stan|agr__Definite=Ind'), ('West-Germaanse', 'ADJ|prenom|basis|met-e|stan__Degree=Pos'), ('taal', 'N|soort|ev|basis|zijd|stan__Gender=Com|Number=Sing'), ('en', 'VG|neven'), ('de', 'LID|bep|stan|rest__Definite=Def'), ('moedertaal', 'N|soort|ev|basis|zijd|stan__Gender=Com|Number=Sing'), ('van', 'VZ|init'), ('de', 'LID|bep|stan|rest__Definite=Def'), ('meeste', 'VNW|onbep|grad|stan|prenom|met-e|agr|sup'), ('inwoners', 'N|soort|mv|basis__Number=Plur'), ('van', 'VZ|init'), ('Nederland', 'N|eigen|ev|basis|onz|stan__Gender=Neut|Number=Sing'), (',', 'LET'), ('België', 'N|eigen|ev|basis|onz|stan__Gender=Neut|Number=Sing'), ('en', 'VG|neven'), ('Suriname', 'N|eigen|ev|basis|onz|stan__Gender=Neut|Number=Sing'), ('.', 'LET')]
        assert tokens_tagged_universal == [('Het', 'DET'), ('Nederlands', 'PROPN'), ('is', 'VERB'), ('een', 'DET'), ('West-Germaanse', 'ADJ'), ('taal', 'NOUN'), ('en', 'CCONJ'), ('de', 'DET'), ('moedertaal', 'NOUN'), ('van', 'ADP'), ('de', 'DET'), ('meeste', 'ADV'), ('inwoners', 'NOUN'), ('van', 'ADP'), ('Nederland', 'PROPN'), (',', 'SYM'), ('België', 'PROPN'), ('en', 'CCONJ'), ('Suriname', 'PROPN'), ('.', 'SYM')]
    elif lang == 'eng':
        if pos_tagger == 'NLTK - Perceptron POS Tagger':
            assert tokens_tagged == [('English', 'NNP'), ('is', 'VBZ'), ('a', 'DT'), ('West', 'NNP'), ('Germanic', 'NNP'), ('language', 'NN'), ('that', 'WDT'), ('was', 'VBD'), ('first', 'RB'), ('spoken', 'VBN'), ('in', 'IN'), ('early', 'JJ'), ('medieval', 'NN'), ('England', 'NNP'), ('and', 'CC'), ('eventually', 'RB'), ('became', 'VBD'), ('a', 'DT'), ('global', 'JJ'), ('lingua', 'NN'), ('franca.[4][5', 'NN'), (']', 'NN')]
            assert tokens_tagged_universal == [('English', 'PROPN'), ('is', 'VERB'), ('a', 'DET'), ('West', 'PROPN'), ('Germanic', 'PROPN'), ('language', 'NOUN'), ('that', 'DET'), ('was', 'VERB'), ('first', 'ADV'), ('spoken', 'VERB'), ('in', 'ADP/SCONJ'), ('early', 'ADJ'), ('medieval', 'NOUN'), ('England', 'PROPN'), ('and', 'CCONJ'), ('eventually', 'ADV'), ('became', 'VERB'), ('a', 'DET'), ('global', 'ADJ'), ('lingua', 'NOUN'), ('franca.[4][5', 'NOUN'), (']', 'NOUN')]
        elif pos_tagger == 'spaCy - English POS Tagger':
            assert tokens_tagged == [('English', 'NNP'), ('is', 'VBZ'), ('a', 'DT'), ('West', 'NNP'), ('Germanic', 'NNP'), ('language', 'NN'), ('that', 'WDT'), ('was', 'VBD'), ('first', 'RB'), ('spoken', 'VBN'), ('in', 'IN'), ('early', 'JJ'), ('medieval', 'JJ'), ('England', 'NNP'), ('and', 'CC'), ('eventually', 'RB'), ('became', 'VBD'), ('a', 'DT'), ('global', 'JJ'), ('lingua', 'NN'), ('franca.[4][5', 'NNP'), (']', '-RRB-')]
            assert tokens_tagged_universal == [('English', 'PROPN'), ('is', 'AUX'), ('a', 'DET'), ('West', 'PROPN'), ('Germanic', 'PROPN'), ('language', 'NOUN'), ('that', 'DET'), ('was', 'AUX'), ('first', 'ADV'), ('spoken', 'VERB'), ('in', 'ADP'), ('early', 'ADJ'), ('medieval', 'ADJ'), ('England', 'PROPN'), ('and', 'CCONJ'), ('eventually', 'ADV'), ('became', 'VERB'), ('a', 'DET'), ('global', 'ADJ'), ('lingua', 'NOUN'), ('franca.[4][5', 'PROPN'), (']', 'PUNCT')]
    elif lang == 'fra':
        assert tokens_tagged == [('Le', 'DET__Definite=Def|Gender=Masc|Number=Sing|PronType=Art'), ('français', 'ADJ__Gender=Masc'), ('est', 'AUX__Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin'), ('une', 'DET__Definite=Ind|Gender=Fem|Number=Sing|PronType=Art'), ('langue', 'NOUN__Gender=Fem|Number=Sing'), ('indo-européenne', 'ADJ__Gender=Fem|Number=Sing'), ('de', 'ADP'), ('la', 'DET__Definite=Def|Gender=Fem|Number=Sing|PronType=Art'), ('famille', 'NOUN__Gender=Fem|Number=Sing'), ('des', 'ADP_DET__Definite=Def|Number=Plur|PronType=Art'), ('langues', 'NOUN__Gender=Fem|Number=Plur'), ('romanes', 'ADJ__Gender=Fem|Number=Plur'), ('.', 'PUNCT')]
        assert tokens_tagged_universal == [('Le', 'DET'), ('français', 'ADJ'), ('est', 'AUX'), ('une', 'DET'), ('langue', 'NOUN'), ('indo-européenne', 'ADJ'), ('de', 'ADP'), ('la', 'DET'), ('famille', 'NOUN'), ('des', 'ADP'), ('langues', 'NOUN'), ('romanes', 'ADJ'), ('.', 'PUNCT')]
    elif lang == 'deu':
        assert tokens_tagged == [('Die', 'ART'), ('deutsche', 'ADJA'), ('Sprache', 'NN'), ('bzw.', 'ADJA'), ('Deutsch', 'NN'), ('(', '$('), ('[', 'NE'), ('dɔʏ̯t͡ʃ', 'NE'), (']', 'NE'), (';', '$.'), ('abgekürzt', 'VVFIN'), ('dt', 'NE'), ('.', '$.'), ('oder', 'KON'), ('dtsch', 'ADJD'), ('.', '$.'), (')', '$('), ('ist', 'VAFIN'), ('eine', 'ART'), ('westgermanische', 'ADJA'), ('Sprache', 'NN'), ('.', '$.')]
        assert tokens_tagged_universal == [('Die', 'DET'), ('deutsche', 'ADJ'), ('Sprache', 'NOUN'), ('bzw.', 'ADJ'), ('Deutsch', 'NOUN'), ('(', 'PUNCT'), ('[', 'PROPN'), ('dɔʏ̯t͡ʃ', 'PROPN'), (']', 'PROPN'), (';', 'PUNCT'), ('abgekürzt', 'VERB'), ('dt', 'PROPN'), ('.', 'PUNCT'), ('oder', 'CCONJ'), ('dtsch', 'ADJ'), ('.', 'PUNCT'), (')', 'PUNCT'), ('ist', 'AUX'), ('eine', 'DET'), ('westgermanische', 'ADJ'), ('Sprache', 'NOUN'), ('.', 'PUNCT')]
    elif lang == 'ell':
        assert tokens_tagged == [('Η', 'DET__Case=Nom|Definite=Def|Gender=Fem|Number=Sing|PronType=Art'), ('ελληνική', 'ADJ__Case=Nom|Gender=Fem|Number=Sing'), ('γλώσσα', 'NOUN__Case=Nom|Gender=Fem|Number=Sing'), ('ανήκει', 'VERB__Aspect=Imp|Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act'), ('στην', 'AsPpSp_AtDf__Case=Acc|Gender=Fem|Number=Sing'), ('ινδοευρωπαϊκή', 'ADJ__Case=Acc|Gender=Fem|Number=Sing'), ('οικογένεια[9', 'NOUN__Case=Acc|Gender=Fem|Number=Sing'), (']', 'VERB__Aspect=Perf|Mood=Ind|Number=Plur|Person=2|Tense=Past|VerbForm=Fin|Voice=Pass'), ('και', 'CCONJ'), ('συγκεκριμένα', 'ADV'), ('στον', 'AsPpSp_AtDf__Case=Acc|Gender=Masc|Number=Sing'), ('ελληνικό', 'ADJ__Case=Acc|Gender=Masc|Number=Sing'), ('κλάδο', 'NOUN__Case=Acc|Gender=Masc|Number=Sing'), (',', 'PUNCT'), ('μαζί', 'ADV'), ('με', 'ADP'), ('την', 'DET__Case=Acc|Definite=Def|Gender=Fem|Number=Sing|PronType=Art'), ('τσακωνική', 'NOUN__Case=Acc|Gender=Fem|Number=Sing'), (',', 'PUNCT'), ('ενώ', 'SCONJ'), ('είναι', 'AUX__Aspect=Imp|Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Pass'), ('η', 'DET__Case=Nom|Definite=Def|Gender=Fem|Number=Sing|PronType=Art'), ('επίσημη', 'ADJ__Case=Nom|Gender=Fem|Number=Sing'), ('γλώσσα', 'NOUN__Case=Nom|Gender=Fem|Number=Sing'), ('της', 'DET__Case=Gen|Definite=Def|Gender=Fem|Number=Sing|PronType=Art'), ('Ελλάδος', 'PROPN__Case=Gen|Gender=Fem|Number=Sing'), ('και', 'CCONJ'), ('της', 'DET__Case=Gen|Definite=Def|Gender=Fem|Number=Sing|PronType=Art'), ('Κύπρου', 'PROPN__Case=Gen|Gender=Fem|Number=Sing'), ('.', 'PUNCT')]
        assert tokens_tagged_universal == [('Η', 'DET'), ('ελληνική', 'ADJ'), ('γλώσσα', 'NOUN'), ('ανήκει', 'VERB'), ('στην', 'ADP'), ('ινδοευρωπαϊκή', 'ADJ'), ('οικογένεια[9', 'NOUN'), (']', 'VERB'), ('και', 'CCONJ'), ('συγκεκριμένα', 'ADV'), ('στον', 'ADP'), ('ελληνικό', 'ADJ'), ('κλάδο', 'NOUN'), (',', 'PUNCT'), ('μαζί', 'ADV'), ('με', 'ADP'), ('την', 'DET'), ('τσακωνική', 'NOUN'), (',', 'PUNCT'), ('ενώ', 'SCONJ'), ('είναι', 'AUX'), ('η', 'DET'), ('επίσημη', 'ADJ'), ('γλώσσα', 'NOUN'), ('της', 'DET'), ('Ελλάδος', 'PROPN'), ('και', 'CCONJ'), ('της', 'DET'), ('Κύπρου', 'PROPN'), ('.', 'PUNCT')]
    elif lang == 'ita':
        assert tokens_tagged == [("L'", 'RD__Definite=Def|Number=Sing|PronType=Art'), ('italiano', 'S__Gender=Masc|Number=Sing'), ('(', 'FB'), ('[', 'FB'), ('itaˈljaːno][Nota', 'S__Gender=Masc|Number=Sing'), ('1', 'N__NumType=Card'), (']', 'FB'), ('ascolta[?·info', 'S'), (']', 'FB'), (')', 'FB'), ('è', 'V__Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin'), ('una', 'RI__Definite=Ind|Gender=Fem|Number=Sing|PronType=Art'), ('lingua', 'S__Gender=Fem|Number=Sing'), ('romanza', 'S__Gender=Fem|Number=Sing'), ('parlata', 'A__Gender=Fem|Number=Sing'), ('principalmente', 'B'), ('in', 'E'), ('Italia', 'SP'), ('.', 'FS')]
        assert tokens_tagged_universal == [("L'", 'DET'), ('italiano', 'NOUN'), ('(', 'PUNCT'), ('[', 'PUNCT'), ('itaˈljaːno][Nota', 'NOUN'), ('1', 'NUM'), (']', 'PUNCT'), ('ascolta[?·info', 'NOUN'), (']', 'PUNCT'), (')', 'PUNCT'), ('è', 'VERB'), ('una', 'DET'), ('lingua', 'NOUN'), ('romanza', 'NOUN'), ('parlata', 'ADJ'), ('principalmente', 'ADV'), ('in', 'ADP'), ('Italia', 'PROPN'), ('.', 'PUNCT')]
    elif lang == 'jpn':
        assert tokens_tagged == [('日本', '名詞'), ('語', '名詞'), ('(', '補助記号'), ('にほんご', '名詞'), ('、', '補助記号'), ('にっぽん', '名詞'), ('ご', '接尾辞'), ('[', '補助記号'), ('注', '名詞'), ('1', '名詞'), (']', '補助記号'), (')', '補助記号'), ('は', '助詞'), ('、', '補助記号'), ('主に', '副詞'), ('日本', '名詞'), ('国', '接尾辞'), ('内', '接尾辞'), ('や', '助詞'), ('日本', '名詞'), ('人', '接尾辞'), ('同士', '接尾辞'), ('の', '助詞'), ('間', '名詞'), ('で', '助詞'), ('使用', '名詞'), ('さ', '動詞'), ('れ', '助動詞'), ('て', '助詞'), ('いる', '動詞'), ('言語', '名詞'), ('で', '助動詞'), ('ある', '動詞'), ('。', '補助記号')]
        assert tokens_tagged_universal == [('日本', 'NOUN'), ('語', 'NOUN'), ('(', 'PUNCT/SYM'), ('にほんご', 'NOUN'), ('、', 'PUNCT/SYM'), ('にっぽん', 'NOUN'), ('ご', 'PART'), ('[', 'PUNCT/SYM'), ('注', 'NOUN'), ('1', 'NOUN'), (']', 'PUNCT/SYM'), (')', 'PUNCT/SYM'), ('は', 'PART'), ('、', 'PUNCT/SYM'), ('主に', 'ADV'), ('日本', 'NOUN'), ('国', 'PART'), ('内', 'PART'), ('や', 'PART'), ('日本', 'NOUN'), ('人', 'PART'), ('同士', 'PART'), ('の', 'PART'), ('間', 'NOUN'), ('で', 'PART'), ('使用', 'NOUN'), ('さ', 'VERB'), ('れ', 'AUX'), ('て', 'PART'), ('いる', 'VERB'), ('言語', 'NOUN'), ('で', 'AUX'), ('ある', 'VERB'), ('。', 'PUNCT/SYM')]
    elif lang == 'lit':
        assert tokens_tagged == [('Lietuvių', 'dkt.vyr.dgs.K.__Case=Gen|Gender=Masc|Number=Plur'), ('kalba', 'dkt.mot.vns.Įn.__Case=Ins|Gender=Fem|Number=Sing'), ('–', 'skyr.'), ('iš', 'prl.K.__AdpType=Prep|Case=Gen'), ('baltų', 'bdv.nelygin.mot.vns.K.__Case=Gen|Definite=Ind|Degree=Pos|Gender=Fem|Number=Sing'), ('prokalbės', 'dkt.mot.vns.K.__Case=Gen|Gender=Fem|Number=Sing'), ('kilusi', 'bdv.aukšč.vyr.dgs.V.__Case=Nom|Definite=Ind|Degree=Sup|Gender=Masc|Number=Plur'), ('lietuvių', 'dkt.vyr.dgs.K.__Case=Gen|Gender=Masc|Number=Plur'), ('tautos', 'dkt.mot.vns.K.__Case=Gen|Gender=Fem|Number=Sing'), ('kalba', 'dkt.mot.vns.Įn.__Case=Ins|Gender=Fem|Number=Sing'), (',', 'skyr.'), ('kuri', 'įv.mot.vns.V.__Case=Nom|Definite=Ind|Gender=Fem|Number=Sing|PronType=Int'), ('Lietuvoje', 'dkt.tikr.mot.vns.Vt.__Case=Loc|Gender=Fem|Number=Sing'), ('yra', 'vksm.asm.tiesiog.es.vns.3.__Mood=Ind|Number=Sing|Person=3|Polarity=Pos|Tense=Pres|VerbForm=Fin'), ('valstybinė', 'bdv.nelygin.mot.vns.V.__Case=Nom|Definite=Ind|Degree=Pos|Gender=Fem|Number=Sing'), (',', 'skyr.'), ('o', 'jng.'), ('Europos', 'dkt.tikr.mot.vns.K.__Case=Gen|Gender=Fem|Number=Sing'), ('Sąjungoje', 'dkt.mot.vns.Vt.__Case=Loc|Gender=Fem|Number=Sing'), ('–', 'skyr.'), ('viena', 'įv.mot.vns.V.__Case=Nom|Definite=Ind|Gender=Fem|Number=Sing|PronType=Ind'), ('iš', 'prl.K.__AdpType=Prep|Case=Gen'), ('oficialiųjų', 'bdv.nelygin.įvardž.vyr.dgs.K.__Case=Gen|Definite=Def|Degree=Pos|Gender=Masc|Number=Plur'), ('kalbų', 'dkt.vyr.dgs.V.__Case=Nom|Gender=Masc|Number=Plur'), ('.', 'skyr.')]
        assert tokens_tagged_universal == [('Lietuvių', 'NOUN'), ('kalba', 'NOUN'), ('–', 'PUNCT'), ('iš', 'ADP'), ('baltų', 'ADJ'), ('prokalbės', 'NOUN'), ('kilusi', 'ADJ'), ('lietuvių', 'NOUN'), ('tautos', 'NOUN'), ('kalba', 'NOUN'), (',', 'PUNCT'), ('kuri', 'DET'), ('Lietuvoje', 'PROPN'), ('yra', 'AUX'), ('valstybinė', 'ADJ'), (',', 'PUNCT'), ('o', 'CCONJ'), ('Europos', 'PROPN'), ('Sąjungoje', 'NOUN'), ('–', 'PUNCT'), ('viena', 'PRON'), ('iš', 'ADP'), ('oficialiųjų', 'ADJ'), ('kalbų', 'NOUN'), ('.', 'PUNCT')]
    elif lang == 'nob':
        assert tokens_tagged == [('Bokmål', 'PROPN'), ('er', 'AUX__Mood=Ind|Tense=Pres|VerbForm=Fin'), ('en', 'DET__Gender=Masc|Number=Sing|PronType=Art'), ('varietet', 'NOUN__Definite=Ind|Gender=Masc|Number=Sing'), ('av', 'ADP'), ('norsk', 'ADJ__Definite=Ind|Degree=Pos|Gender=Neut|Number=Sing'), ('språk', 'NOUN__Definite=Ind|Gender=Neut|Number=Sing'), ('.', 'PUNCT')]
        assert tokens_tagged_universal == [('Bokmål', 'PROPN'), ('er', 'AUX'), ('en', 'DET'), ('varietet', 'NOUN'), ('av', 'ADP'), ('norsk', 'ADJ'), ('språk', 'NOUN'), ('.', 'PUNCT')]
    elif lang == 'pol':
        assert tokens_tagged == [('Język', 'SUBST'), ('polski', 'ADJ'), (',', 'INTERP'), ('polszczyzna', 'SUBST'), (',', 'INTERP'), ('skrót', 'SUBST'), (':', 'INTERP'), ('pol', 'BREV'), ('.', 'INTERP'), ('–', 'INTERP'), ('język', 'SUBST'), ('naturalny', 'ADJ'), ('należący', 'PACT'), ('do', 'PREP'), ('grupy', 'SUBST'), ('języków', 'SUBST'), ('zachodniosłowiańskich', 'ADJ'), ('(', 'INTERP'), ('do', 'PREP'), ('której', 'ADJ'), ('należą', 'FIN'), ('również', 'QUB'), ('czeski', 'ADJ'), (',', 'INTERP'), ('słowacki', 'ADJ'), (',', 'INTERP'), ('kaszubski', 'ADJ'), (',', 'INTERP'), ('dolnołużycki', 'ADJ'), (',', 'INTERP'), ('górnołużycki', 'SUBST'), ('i', 'CONJ'), ('wymarły', 'SUBST'), ('połabski', 'ADJ'), (')', 'INTERP'), (',', 'INTERP'), ('stanowiącej', 'PACT'), ('część', 'SUBST'), ('rodziny', 'SUBST'), ('języków', 'SUBST'), ('indoeuropejskich', 'ADJ'), ('.', 'INTERP')]
        assert tokens_tagged_universal == [('Język', 'NOUN'), ('polski', 'ADJ'), (',', 'PUNCT'), ('polszczyzna', 'NOUN'), (',', 'PUNCT'), ('skrót', 'NOUN'), (':', 'PUNCT'), ('pol', 'X'), ('.', 'PUNCT'), ('–', 'PUNCT'), ('język', 'NOUN'), ('naturalny', 'ADJ'), ('należący', 'VERB'), ('do', 'ADP'), ('grupy', 'NOUN'), ('języków', 'NOUN'), ('zachodniosłowiańskich', 'ADJ'), ('(', 'PUNCT'), ('do', 'ADP'), ('której', 'ADJ'), ('należą', 'VERB'), ('również', 'PART'), ('czeski', 'ADJ'), (',', 'PUNCT'), ('słowacki', 'ADJ'), (',', 'PUNCT'), ('kaszubski', 'ADJ'), (',', 'PUNCT'), ('dolnołużycki', 'ADJ'), (',', 'PUNCT'), ('górnołużycki', 'NOUN'), ('i', 'CCONJ'), ('wymarły', 'NOUN'), ('połabski', 'ADJ'), (')', 'PUNCT'), (',', 'PUNCT'), ('stanowiącej', 'VERB'), ('część', 'NOUN'), ('rodziny', 'NOUN'), ('języków', 'NOUN'), ('indoeuropejskich', 'ADJ'), ('.', 'PUNCT')]
    elif lang == 'por':
        assert tokens_tagged == [('A', 'DET__Definite=Def|Gender=Fem|Number=Sing|PronType=Art'), ('língua', 'NOUN__Gender=Fem|Number=Sing'), ('portuguesa', 'ADJ__Gender=Fem|Number=Sing'), (',', 'PUNCT'), ('também', 'ADV'), ('designada', 'VERB__Gender=Fem|Number=Sing|VerbForm=Part'), ('português', 'NOUN__Gender=Masc|Number=Sing'), (',', 'PUNCT'), ('é', 'AUX__Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin'), ('uma', 'DET__Definite=Ind|Gender=Fem|Number=Sing|PronType=Art'), ('língua', 'NOUN__Gender=Fem|Number=Sing'), ('românica', 'ADJ__Gender=Fem|Number=Sing'), ('flexiva', 'ADJ__Gender=Fem|Number=Sing'), ('ocidental', 'ADJ__Gender=Fem|Number=Sing'), ('originada', 'VERB__Gender=Fem|Number=Sing|VerbForm=Part'), ('no', 'ADP_DET__Definite=Def|Gender=Masc|Number=Sing|PronType=Art'), ('galego-português', 'NOUN__Gender=Masc|Number=Sing'), ('falado', 'VERB__Gender=Masc|Number=Sing|VerbForm=Part'), ('no', 'ADP_DET__Definite=Def|Gender=Masc|Number=Sing|PronType=Art'), ('Reino', 'PROPN__Gender=Masc|Number=Sing'), ('da', 'ADP_DET__Definite=Def|Gender=Fem|Number=Sing|PronType=Art'), ('Galiza', 'PROPN__Number=Sing'), ('e', 'CCONJ'), ('no', 'ADP_DET__Definite=Def|Gender=Masc|Number=Sing|PronType=Art'), ('norte', 'NOUN__Gender=Masc|Number=Sing'), ('de', 'ADP'), ('Portugal', 'PROPN__Gender=Masc|Number=Sing'), ('.', 'PUNCT')]
        assert tokens_tagged_universal == [('A', 'DET'), ('língua', 'NOUN'), ('portuguesa', 'ADJ'), (',', 'PUNCT'), ('também', 'ADV'), ('designada', 'VERB'), ('português', 'NOUN'), (',', 'PUNCT'), ('é', 'AUX'), ('uma', 'DET'), ('língua', 'NOUN'), ('românica', 'ADJ'), ('flexiva', 'ADJ'), ('ocidental', 'ADJ'), ('originada', 'VERB'), ('no', 'DET'), ('galego-português', 'NOUN'), ('falado', 'VERB'), ('no', 'DET'), ('Reino', 'PROPN'), ('da', 'DET'), ('Galiza', 'PROPN'), ('e', 'CCONJ'), ('no', 'DET'), ('norte', 'NOUN'), ('de', 'ADP'), ('Portugal', 'PROPN'), ('.', 'PUNCT')]
    elif lang == 'rus':
        if pos_tagger == 'NLTK - Perceptron POS Tagger':
            assert tokens_tagged == [('Ру́сский', 'A=m'), ('язы́к', 'S'), ('(', 'NONLEX'), ('[', 'NONLEX'), ('ˈruskʲɪi̯', 'NONLEX'), ('jɪˈzɨk', 'NONLEX'), (']', 'NONLEX'), ('Информация', 'S'), ('о', 'PR'), ('файле', 'S'), ('слушать', 'V'), (')', 'NONLEX'), ('[', 'NONLEX'), ('~', 'NONLEX'), ('3', 'NUM=ciph'), (']', 'NONLEX'), ('[', 'NONLEX'), ('⇨', 'NONLEX'), (']', 'NONLEX'), ('—', 'NONLEX'), ('один', 'A-PRO=m'), ('из', 'PR'), ('восточнославянских', 'A=pl'), ('языков', 'S'), (',', 'NONLEX'), ('национальный', 'A=m'), ('язык', 'S'), ('русского', 'A=m'), ('народа', 'S'), ('.', 'NONLEX')]
            assert tokens_tagged_universal == [('Ру́сский', 'ADJ'), ('язы́к', 'NOUN'), ('(', 'PUNCT'), ('[', 'PUNCT'), ('ˈruskʲɪi̯', 'PUNCT'), ('jɪˈzɨk', 'PUNCT'), (']', 'PUNCT'), ('Информация', 'NOUN'), ('о', 'ADP'), ('файле', 'NOUN'), ('слушать', 'VERB'), (')', 'PUNCT'), ('[', 'PUNCT'), ('~', 'PUNCT'), ('3', 'NUM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('⇨', 'PUNCT'), (']', 'PUNCT'), ('—', 'PUNCT'), ('один', 'PRON'), ('из', 'ADP'), ('восточнославянских', 'ADJ'), ('языков', 'NOUN'), (',', 'PUNCT'), ('национальный', 'ADJ'), ('язык', 'NOUN'), ('русского', 'ADJ'), ('народа', 'NOUN'), ('.', 'PUNCT')]
        elif pos_tagger == 'pymorphy2 - Morphological Analyzer':
            assert tokens_tagged == [('Ру́сский', 'NOUN'), ('язы́к', 'NOUN'), ('(', 'PNCT'), ('[', 'PNCT'), ('ˈruskʲɪi̯', 'UNKN'), ('jɪˈzɨk', 'UNKN'), (']', 'PNCT'), ('Информация', 'NOUN'), ('о', 'PREP'), ('файле', 'NOUN'), ('слушать', 'INFN'), (')', 'PNCT'), ('[', 'PNCT'), ('~', 'UNKN'), ('3', 'NUMB'), (']', 'PNCT'), ('[', 'PNCT'), ('⇨', 'UNKN'), (']', 'PNCT'), ('—', 'PNCT'), ('один', 'ADJF'), ('из', 'PREP'), ('восточнославянских', 'ADJF'), ('языков', 'NOUN'), (',', 'PNCT'), ('национальный', 'ADJF'), ('язык', 'NOUN'), ('русского', 'ADJF'), ('народа', 'NOUN'), ('.', 'PNCT')]
            assert tokens_tagged_universal == [('Ру́сский', 'NOUN'), ('язы́к', 'NOUN'), ('(', 'PUNCT'), ('[', 'PUNCT'), ('ˈruskʲɪi̯', 'SYM/X'), ('jɪˈzɨk', 'SYM/X'), (']', 'PUNCT'), ('Информация', 'NOUN'), ('о', 'ADP'), ('файле', 'NOUN'), ('слушать', 'VERB'), (')', 'PUNCT'), ('[', 'PUNCT'), ('~', 'SYM/X'), ('3', 'NUM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('⇨', 'SYM/X'), (']', 'PUNCT'), ('—', 'PUNCT'), ('один', 'ADJ'), ('из', 'ADP'), ('восточнославянских', 'ADJ'), ('языков', 'NOUN'), (',', 'PUNCT'), ('национальный', 'ADJ'), ('язык', 'NOUN'), ('русского', 'ADJ'), ('народа', 'NOUN'), ('.', 'PUNCT')]
    elif lang == 'spa':
        assert tokens_tagged == [('El', 'DET__Definite=Def|Gender=Masc|Number=Sing|PronType=Art'), ('español', 'NOUN__Gender=Masc|Number=Sing'), ('o', 'CCONJ'), ('castellano', 'NOUN__Gender=Masc|Number=Sing'), ('es', 'AUX__Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin'), ('una', 'DET__Definite=Ind|Gender=Fem|Number=Sing|PronType=Art'), ('lengua', 'NOUN__Gender=Fem|Number=Sing'), ('romance', 'NOUN__Gender=Masc|Number=Sing'), ('procedente', 'ADJ__Number=Sing'), ('del', 'ADP__AdpType=Preppron'), ('latín', 'NOUN__Gender=Masc|Number=Sing'), ('hablado', 'ADJ__Gender=Masc|Number=Sing|VerbForm=Part'), ('.', 'PUNCT__PunctType=Peri')]
        assert tokens_tagged_universal == [('El', 'DET'), ('español', 'NOUN'), ('o', 'CCONJ'), ('castellano', 'NOUN'), ('es', 'AUX'), ('una', 'DET'), ('lengua', 'NOUN'), ('romance', 'NOUN'), ('procedente', 'ADJ'), ('del', 'ADP'), ('latín', 'NOUN'), ('hablado', 'ADJ'), ('.', 'PUNCT')]
    elif lang == 'tha':
        if pos_tagger == 'PyThaiNLP - Perceptron Tagger (ORCHID)':
            assert tokens_tagged == [('ภาษาไทย', 'NPRP'), ('หรือ', 'JCRG'), ('ภาษาไทย', 'NPRP'), ('กลาง', 'VATT'), ('เป็น', 'VSTA'), ('ภาษาราชการ', 'NCMN'), ('และ', 'JCRG'), ('ภาษาประจำชาติ', 'NCMN'), ('ของ', 'RPRE'), ('ประเทศ', 'NCMN'), ('ไทย', 'NPRP')]
            assert tokens_tagged_universal == [('ภาษาไทย', 'PROPN'), ('หรือ', 'CCONJ'), ('ภาษาไทย', 'PROPN'), ('กลาง', 'VERB'), ('เป็น', 'VERB'), ('ภาษาราชการ', 'NOUN'), ('และ', 'CCONJ'), ('ภาษาประจำชาติ', 'NOUN'), ('ของ', 'ADP'), ('ประเทศ', 'NOUN'), ('ไทย', 'PROPN')]
        elif pos_tagger == 'PyThaiNLP - Perceptron Tagger (PUD)':
            assert tokens_tagged == [('ภาษาไทย', 'NOUN'), ('หรือ', 'CCONJ'), ('ภาษาไทย', 'NOUN'), ('กลาง', 'NOUN'), ('เป็น', 'AUX'), ('ภาษาราชการ', 'NOUN'), ('และ', 'CCONJ'), ('ภาษาประจำชาติ', 'NOUN'), ('ของ', 'ADP'), ('ประเทศ', 'NOUN'), ('ไทย', 'PROPN')]
            assert tokens_tagged_universal == [('ภาษาไทย', 'NOUN'), ('หรือ', 'CCONJ'), ('ภาษาไทย', 'NOUN'), ('กลาง', 'NOUN'), ('เป็น', 'AUX'), ('ภาษาราชการ', 'NOUN'), ('และ', 'CCONJ'), ('ภาษาประจำชาติ', 'NOUN'), ('ของ', 'ADP'), ('ประเทศ', 'NOUN'), ('ไทย', 'PROPN')]
    elif lang == 'bod':
        assert tokens_tagged == [('བོད་', 'PROPN'), ('ཀྱི་', 'NO_POS'), ('སྐད་ཡིག་', 'NOUN'), ('ནི་', 'NO_POS'), ('བོད་ཡུལ་', 'PROPN'), ('དང་', 'NO_POS'), ('དེ', 'DET'), ('འི་', 'PART'), ('ཉེ་འཁོར་', 'NOUN'), ('གྱི་', 'NO_POS'), ('ས་ཁུལ་', 'OTHER'), ('ཏེ', 'NO_POS'), ('།', 'PUNCT')]
        assert tokens_tagged_universal == [('བོད་', 'PROPN'), ('ཀྱི་', 'X'), ('སྐད་ཡིག་', 'NOUN'), ('ནི་', 'X'), ('བོད་ཡུལ་', 'PROPN'), ('དང་', 'X'), ('དེ', 'DET'), ('འི་', 'PART'), ('ཉེ་འཁོར་', 'NOUN'), ('གྱི་', 'X'), ('ས་ཁུལ་', 'X'), ('ཏེ', 'X'), ('།', 'PUNCT')]
    elif lang == 'ukr':
        assert tokens_tagged == [('Украї́нська', 'ADJF'), ('мо́ва', 'ADJF'), ('(', 'PNCT'), ('МФА', 'UNKN'), (':', 'PNCT'), ('[', 'PNCT'), ('ukrɑ̽ˈjɪnʲsʲkɑ̽', 'UNKN'), ('ˈmɔwɑ̽', 'UNKN'), (']', 'PNCT'), (',', 'PNCT'), ('історичні', 'ADJF'), ('назви', 'NOUN'), ('—', 'PNCT'), ('ру́ська', 'ADJF'), (',', 'PNCT'), ('руси́нська[9][10][11', 'UNKN'), (']', 'PNCT'), ('[', 'PNCT'), ('*', 'PNCT'), ('2', 'NUMB'), (']', 'PNCT'), (')', 'PNCT'), ('—', 'PNCT'), ('національна', 'ADJF'), ('мова', 'NOUN'), ('українців', 'NOUN'), ('.', 'PNCT')]
        assert tokens_tagged_universal == [('Украї́нська', 'ADJ'), ('мо́ва', 'ADJ'), ('(', 'PUNCT'), ('МФА', 'SYM/X'), (':', 'PUNCT'), ('[', 'PUNCT'), ('ukrɑ̽ˈjɪnʲsʲkɑ̽', 'SYM/X'), ('ˈmɔwɑ̽', 'SYM/X'), (']', 'PUNCT'), (',', 'PUNCT'), ('історичні', 'ADJ'), ('назви', 'NOUN'), ('—', 'PUNCT'), ('ру́ська', 'ADJ'), (',', 'PUNCT'), ('руси́нська[9][10][11', 'SYM/X'), (']', 'PUNCT'), ('[', 'PUNCT'), ('*', 'PUNCT'), ('2', 'NUM'), (']', 'PUNCT'), (')', 'PUNCT'), ('—', 'PUNCT'), ('національна', 'ADJ'), ('мова', 'NOUN'), ('українців', 'NOUN'), ('.', 'PUNCT')]
    elif lang == 'vie':
        assert tokens_tagged == [('Tiếng', 'N'), ('Việt', 'Np'), (',', 'CH'), ('còn', 'C'), ('gọi', 'V'), ('tiếng', 'N'), ('Việt Nam', 'Np'), ('[', 'V'), ('5', 'M'), (']', 'CH'), (',', 'CH'), ('tiếng Kinh', 'N'), ('hay', 'C'), ('Việt ngữ', 'V'), (',', 'CH'), ('là', 'V'), ('ngôn ngữ', 'N'), ('của', 'E'), ('người', 'Nc'), ('Việt', 'Np'), ('(', 'CH'), ('dân tộc', 'N'), ('Kinh', 'Np'), (')', 'CH'), ('và', 'C'), ('là', 'V'), ('ngôn ngữ', 'N'), ('chính thức', 'A'), ('tại', 'E'), ('Việt Nam', 'Np'), ('.', 'CH')]
        assert tokens_tagged_universal == [('Tiếng', 'NOUN'), ('Việt', 'PROPN'), (',', 'PUNCT'), ('còn', 'CCONJ'), ('gọi', 'VERB'), ('tiếng', 'NOUN'), ('Việt Nam', 'PROPN'), ('[', 'VERB'), ('5', 'NUM'), (']', 'PUNCT'), (',', 'PUNCT'), ('tiếng Kinh', 'NOUN'), ('hay', 'CCONJ'), ('Việt ngữ', 'VERB'), (',', 'PUNCT'), ('là', 'VERB'), ('ngôn ngữ', 'NOUN'), ('của', 'ADP'), ('người', 'NOUN'), ('Việt', 'PROPN'), ('(', 'PUNCT'), ('dân tộc', 'NOUN'), ('Kinh', 'PROPN'), (')', 'PUNCT'), ('và', 'CCONJ'), ('là', 'VERB'), ('ngôn ngữ', 'NOUN'), ('chính thức', 'ADJ'), ('tại', 'ADP'), ('Việt Nam', 'PROPN'), ('.', 'PUNCT')]

if __name__ == '__main__':
    for lang, pos_tagger in test_pos_taggers:
        test_pos_tag(lang, pos_tagger, show_results = True)
