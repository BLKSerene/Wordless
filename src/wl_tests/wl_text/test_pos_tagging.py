#
# Wordless: Tests - Text - POS Tagging
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
from wl_text import wl_pos_tagging, wl_word_tokenization
from wl_utils import wl_conversion, wl_misc

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
    tokens = list(wl_misc.flatten_list(tokens))

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
        assert tokens_tagged == [('汉语', 'nz'), ('，', 'x'), ('又', 'd'), ('称', 'v'), ('汉文', 'nz'), ('、', 'x'), ('中文', 'nz'), ('、', 'x'), ('中国', 'ns'), ('话', 'n'), ('、', 'x'), ('中国', 'ns'), ('语', 'ng'), ('、', 'x'), ('华语', 'nz'), ('、', 'x'), ('华文', 'nz'), ('、', 'x'), ('唐', 'nr'), ('话', 'n'), ('[', 'x'), ('2', 'x'), (']', 'x'), ('，', 'x'), ('或', 'c'), ('被', 'p'), ('视为', 'v'), ('一个', 'm'), ('语族', 'n'), ('，', 'x'), ('或', 'c'), ('被', 'p'), ('视为', 'v'), ('隶属于', 'n'), ('汉藏', 'ns'), ('语系', 'n'), ('汉语', 'nz'), ('族', 'ng'), ('之一', 'r'), ('种', 'm'), ('语言', 'n'), ('。', 'x')]
        assert tokens_tagged_universal == [('汉语', 'PROPN'), ('，', 'PUNCT/SYM'), ('又', 'ADV'), ('称', 'VERB'), ('汉文', 'PROPN'), ('、', 'PUNCT/SYM'), ('中文', 'PROPN'), ('、', 'PUNCT/SYM'), ('中国', 'PROPN'), ('话', 'NOUN'), ('、', 'PUNCT/SYM'), ('中国', 'PROPN'), ('语', 'NOUN'), ('、', 'PUNCT/SYM'), ('华语', 'PROPN'), ('、', 'PUNCT/SYM'), ('华文', 'PROPN'), ('、', 'PUNCT/SYM'), ('唐', 'PRONP'), ('话', 'NOUN'), ('[', 'PUNCT/SYM'), ('2', 'PUNCT/SYM'), (']', 'PUNCT/SYM'), ('，', 'PUNCT/SYM'), ('或', 'CONJ'), ('被', 'ADP'), ('视为', 'VERB'), ('一个', 'NUM'), ('语族', 'NOUN'), ('，', 'PUNCT/SYM'), ('或', 'CONJ'), ('被', 'ADP'), ('视为', 'VERB'), ('隶属于', 'NOUN'), ('汉藏', 'PROPN'), ('语系', 'NOUN'), ('汉语', 'PROPN'), ('族', 'NOUN'), ('之一', 'PRON'), ('种', 'NUM'), ('语言', 'NOUN'), ('。', 'PUNCT/SYM')]
    elif lang == 'zho_tw':
        assert tokens_tagged == [('漢語', 'nz'), ('，', 'x'), ('又', 'd'), ('稱', 'zg'), ('漢文', 'nz'), ('、', 'x'), ('中文', 'nz'), ('、', 'x'), ('中', 'f'), ('國話', 'n'), ('、', 'x'), ('中國', 'ns'), ('語', 'n'), ('、', 'x'), ('華語', 'nz'), ('、', 'x'), ('華文', 'nz'), ('、', 'x'), ('唐', 'nr'), ('話', 'x'), ('[', 'x'), ('2', 'x'), (']', 'x'), ('，', 'x'), ('或', 'c'), ('被', 'p'), ('視為', 'v'), ('一', 'm'), ('個', 'zg'), ('語族', 'n'), ('，', 'x'), ('或', 'c'), ('被', 'p'), ('視', 'x'), ('為', 'p'), ('隸', 'j'), ('屬', 'v'), ('於', 'nr'), ('漢', 'j'), ('藏', 'j'), ('語系', 'n'), ('漢語', 'nz'), ('族', 'ng'), ('之一', 'r'), ('種', 'x'), ('語言', 'n'), ('。', 'x')]
        assert tokens_tagged_universal == [('漢語', 'PROPN'), ('，', 'PUNCT/SYM'), ('又', 'ADV'), ('稱', 'PART'), ('漢文', 'PROPN'), ('、', 'PUNCT/SYM'), ('中文', 'PROPN'), ('、', 'PUNCT/SYM'), ('中', 'ADP'), ('國話', 'NOUN'), ('、', 'PUNCT/SYM'), ('中國', 'PROPN'), ('語', 'NOUN'), ('、', 'PUNCT/SYM'), ('華語', 'PROPN'), ('、', 'PUNCT/SYM'), ('華文', 'PROPN'), ('、', 'PUNCT/SYM'), ('唐', 'PRONP'), ('話', 'PUNCT/SYM'), ('[', 'PUNCT/SYM'), ('2', 'PUNCT/SYM'), (']', 'PUNCT/SYM'), ('，', 'PUNCT/SYM'), ('或', 'CONJ'), ('被', 'ADP'), ('視為', 'VERB'), ('一', 'NUM'), ('個', 'PART'), ('語族', 'NOUN'), ('，', 'PUNCT/SYM'), ('或', 'CONJ'), ('被', 'ADP'), ('視', 'PUNCT/SYM'), ('為', 'ADP'), ('隸', 'X'), ('屬', 'VERB'), ('於', 'PRONP'), ('漢', 'X'), ('藏', 'X'), ('語系', 'NOUN'), ('漢語', 'PROPN'), ('族', 'NOUN'), ('之一', 'PRON'), ('種', 'PUNCT/SYM'), ('語言', 'NOUN'), ('。', 'PUNCT/SYM')]
    elif lang == 'dan':
        assert tokens_tagged == [('Dansk', 'ADJ'), ('er', 'AUX'), ('et', 'DET'), ('nordgermansk', 'ADJ'), ('sprog', 'NOUN'), ('af', 'ADP'), ('den', 'DET'), ('østnordiske', 'ADJ'), ('(', 'PUNCT'), ('kontinentale', 'NOUN'), (')', 'PUNCT'), ('gruppe', 'NOUN'), (',', 'PUNCT'), ('der', 'PRON'), ('tales', 'VERB'), ('af', 'ADP'), ('ca.', 'ADV'), ('seks', 'NUM'), ('millioner', 'NOUN'), ('mennesker', 'NOUN'), ('.', 'PUNCT')]
        assert tokens_tagged_universal == [('Dansk', 'ADJ'), ('er', 'AUX'), ('et', 'DET'), ('nordgermansk', 'ADJ'), ('sprog', 'NOUN'), ('af', 'ADP'), ('den', 'DET'), ('østnordiske', 'ADJ'), ('(', 'PUNCT'), ('kontinentale', 'NOUN'), (')', 'PUNCT'), ('gruppe', 'NOUN'), (',', 'PUNCT'), ('der', 'PRON'), ('tales', 'VERB'), ('af', 'ADP'), ('ca.', 'ADV'), ('seks', 'NUM'), ('millioner', 'NOUN'), ('mennesker', 'NOUN'), ('.', 'PUNCT')]
    elif lang == 'nld':
        assert tokens_tagged == [('Het', 'LID|bep|stan|evon'), ('Nederlands', 'N|eigen|ev|basis|onz|stan'), ('is', 'WW|pv|tgw|ev'), ('een', 'LID|onbep|stan|agr'), ('West-Germaanse', 'ADJ|prenom|basis|met-e|stan'), ('taal', 'N|soort|ev|basis|zijd|stan'), ('en', 'VG|neven'), ('de', 'LID|bep|stan|rest'), ('officiële', 'ADJ|prenom|basis|met-e|stan'), ('taal', 'N|soort|ev|basis|zijd|stan'), ('van', 'VZ|init'), ('Nederland', 'N|eigen|ev|basis|onz|stan'), (',', 'LET'), ('Suriname', 'N|eigen|ev|basis|onz|stan'), ('en', 'VG|neven'), ('een', 'TW|hoofd|nom|zonder-n|basis'), ('van', 'VZ|init'), ('de', 'LID|bep|stan|rest'), ('drie', 'TW|hoofd|prenom|stan'), ('officiële', 'ADJ|prenom|basis|met-e|stan'), ('talen', 'N|soort|mv|basis'), ('van', 'VZ|init'), ('België', 'N|eigen|ev|basis|onz|stan'), ('.', 'LET')]
        assert tokens_tagged_universal == [('Het', 'DET'), ('Nederlands', 'PROPN'), ('is', 'AUX'), ('een', 'DET'), ('West-Germaanse', 'ADJ'), ('taal', 'NOUN'), ('en', 'CCONJ'), ('de', 'DET'), ('officiële', 'ADJ'), ('taal', 'NOUN'), ('van', 'ADP'), ('Nederland', 'PROPN'), (',', 'PUNCT'), ('Suriname', 'PROPN'), ('en', 'CCONJ'), ('een', 'NUM'), ('van', 'ADP'), ('de', 'DET'), ('drie', 'NUM'), ('officiële', 'ADJ'), ('talen', 'NOUN'), ('van', 'ADP'), ('België', 'PROPN'), ('.', 'PUNCT')]
    elif lang == 'eng':
        if pos_tagger == 'NLTK - Perceptron POS Tagger':
            assert tokens_tagged == [('English', 'NNP'), ('is', 'VBZ'), ('a', 'DT'), ('West', 'NNP'), ('Germanic', 'NNP'), ('language', 'NN'), ('originally', 'RB'), ('spoken', 'VBN'), ('by', 'IN'), ('the', 'DT'), ('early', 'JJ'), ('medieval', 'NN'), ('England.[3][4][5', 'NNP'), (']', 'NN')]
            assert tokens_tagged_universal == [('English', 'PROPN'), ('is', 'VERB'), ('a', 'DET'), ('West', 'PROPN'), ('Germanic', 'PROPN'), ('language', 'NOUN'), ('originally', 'ADV'), ('spoken', 'VERB'), ('by', 'ADP/SCONJ'), ('the', 'DET'), ('early', 'ADJ'), ('medieval', 'NOUN'), ('England.[3][4][5', 'PROPN'), (']', 'NOUN')]
        elif pos_tagger == 'spaCy - English POS Tagger':
            assert tokens_tagged == [('English', 'NNP'), ('is', 'VBZ'), ('a', 'DT'), ('West', 'NNP'), ('Germanic', 'NNP'), ('language', 'NN'), ('originally', 'RB'), ('spoken', 'VBN'), ('by', 'IN'), ('the', 'DT'), ('early', 'JJ'), ('medieval', 'NN'), ('England.[3][4][5', 'NNP'), (']', '-RRB-')]
            assert tokens_tagged_universal == [('English', 'PROPN'), ('is', 'AUX'), ('a', 'DET'), ('West', 'PROPN'), ('Germanic', 'PROPN'), ('language', 'NOUN'), ('originally', 'ADV'), ('spoken', 'VERB'), ('by', 'ADP'), ('the', 'DET'), ('early', 'ADJ'), ('medieval', 'NOUN'), ('England.[3][4][5', 'PROPN'), (']', 'PUNCT')]
    elif lang == 'fra':
        assert tokens_tagged == [('Le', 'DET'), ('français', 'ADJ'), ('est', 'AUX'), ('une', 'DET'), ('langue', 'NOUN'), ('indo-européenne', 'ADJ'), ('de', 'ADP'), ('la', 'DET'), ('famille', 'NOUN'), ('des', 'ADP'), ('langues', 'ADJ'), ('romanes', 'NOUN'), ('dont', 'PRON'), ('les', 'DET'), ('locuteurs', 'NOUN'), ('sont', 'AUX'), ('appelés', 'VERB'), ('francophones', 'ADJ'), ('.', 'PUNCT')]
        assert tokens_tagged_universal == [('Le', 'DET'), ('français', 'ADJ'), ('est', 'AUX'), ('une', 'DET'), ('langue', 'NOUN'), ('indo-européenne', 'ADJ'), ('de', 'ADP'), ('la', 'DET'), ('famille', 'NOUN'), ('des', 'ADP'), ('langues', 'ADJ'), ('romanes', 'NOUN'), ('dont', 'PRON'), ('les', 'DET'), ('locuteurs', 'NOUN'), ('sont', 'AUX'), ('appelés', 'VERB'), ('francophones', 'ADJ'), ('.', 'PUNCT')]
    elif lang == 'deu':
        assert tokens_tagged == [('Die', 'ART'), ('deutsche', 'ADJA'), ('Sprache', 'NN'), ('bzw.', 'KON'), ('das', 'ART'), ('Deutsche', 'NN'), ('(', '$('), ('[', 'NE'), ('dɔɪ̯tʃ];[26', 'PROAV'), (']', 'ADJD'), ('abgekürzt', 'VVPP'), ('dt', 'XY'), ('.', '$.'), ('oder', 'KON'), ('dtsch', 'ADJD'), ('.', '$.'), (')', '$('), ('ist', 'VAFIN'), ('eine', 'ART'), ('westgermanische', 'ADJA'), ('Sprache', 'NN'), (',', '$,'), ('die', 'PRELS'), ('weltweit', 'ADJD'), ('etwa', 'ADV'), ('90', 'CARD'), ('bis', 'KON'), ('105', 'CARD'), ('Millionen', 'NN'), ('Menschen', 'NN'), ('als', 'APPR'), ('Muttersprache', 'NN'), ('und', 'KON'), ('weiteren', 'ADJA'), ('rund', 'ADV'), ('80', 'CARD'), ('Millionen', 'NN'), ('als', 'APPR'), ('Zweit-', 'TRUNC'), ('oder', 'KON'), ('Fremdsprache', 'NN'), ('dient', 'VVFIN'), ('.', '$.')]
        assert tokens_tagged_universal == [('Die', 'DET'), ('deutsche', 'ADJ'), ('Sprache', 'NOUN'), ('bzw.', 'CCONJ'), ('das', 'DET'), ('Deutsche', 'ADJ'), ('(', 'PUNCT'), ('[', 'NOUN'), ('dɔɪ̯tʃ];[26', 'X'), (']', 'ADV'), ('abgekürzt', 'VERB'), ('dt', 'PRON'), ('.', 'PUNCT'), ('oder', 'CCONJ'), ('dtsch', 'ADV'), ('.', 'PUNCT'), (')', 'PUNCT'), ('ist', 'AUX'), ('eine', 'DET'), ('westgermanische', 'ADJ'), ('Sprache', 'NOUN'), (',', 'PUNCT'), ('die', 'PRON'), ('weltweit', 'ADV'), ('etwa', 'ADV'), ('90', 'NUM'), ('bis', 'CCONJ'), ('105', 'NUM'), ('Millionen', 'NOUN'), ('Menschen', 'NOUN'), ('als', 'ADP'), ('Muttersprache', 'NOUN'), ('und', 'CCONJ'), ('weiteren', 'ADJ'), ('rund', 'ADV'), ('80', 'NUM'), ('Millionen', 'NOUN'), ('als', 'ADP'), ('Zweit-', 'X'), ('oder', 'CCONJ'), ('Fremdsprache', 'NOUN'), ('dient', 'VERB'), ('.', 'PUNCT')]
    elif lang == 'ell':
        assert tokens_tagged == [('Η', 'DET'), ('ελληνική', 'ADJ'), ('γλώσσα', 'NOUN'), ('ανήκει', 'VERB'), ('στην', 'ADP'), ('ινδοευρωπαϊκή', 'ADJ'), ('οικογένεια[10', 'NOUN'), (']', 'NOUN'), ('και', 'CCONJ'), ('αποτελεί', 'VERB'), ('το', 'DET'), ('μοναδικό', 'ADJ'), ('μέλος', 'NOUN'), ('του', 'DET'), ('ελληνικού', 'ADJ'), ('κλάδου', 'NOUN'), (',', 'PUNCT'), ('ενώ', 'SCONJ'), ('είναι', 'AUX'), ('η', 'DET'), ('επίσημη', 'ADJ'), ('γλώσσα', 'NOUN'), ('της', 'DET'), ('Ελλάδος', 'PROPN'), ('και', 'CCONJ'), ('της', 'DET'), ('Κύπρου', 'PROPN'), ('.', 'PUNCT')]
        assert tokens_tagged_universal == [('Η', 'DET'), ('ελληνική', 'ADJ'), ('γλώσσα', 'NOUN'), ('ανήκει', 'VERB'), ('στην', 'ADP'), ('ινδοευρωπαϊκή', 'ADJ'), ('οικογένεια[10', 'NOUN'), (']', 'NOUN'), ('και', 'CCONJ'), ('αποτελεί', 'VERB'), ('το', 'DET'), ('μοναδικό', 'ADJ'), ('μέλος', 'NOUN'), ('του', 'DET'), ('ελληνικού', 'ADJ'), ('κλάδου', 'NOUN'), (',', 'PUNCT'), ('ενώ', 'SCONJ'), ('είναι', 'AUX'), ('η', 'DET'), ('επίσημη', 'ADJ'), ('γλώσσα', 'NOUN'), ('της', 'DET'), ('Ελλάδος', 'PROPN'), ('και', 'CCONJ'), ('της', 'DET'), ('Κύπρου', 'PROPN'), ('.', 'PUNCT')]
    elif lang == 'ita':
        assert tokens_tagged == [('L', 'PC'), ("'", 'FB'), ('italiano', 'A'), ('(', 'FB'), ('[', 'FB'), ('itaˈljaːno][Nota', 'S'), ('1', 'N'), (']', 'FB'), ('ascolta[?·info', 'S'), (']', 'FB'), (')', 'FB'), ('è', 'V'), ('una', 'RI'), ('lingua', 'S'), ('romanza', 'S'), ('parlata', 'A'), ('principalmente', 'B'), ('in', 'E'), ('Italia', 'SP'), ('.', 'FS')]
        assert tokens_tagged_universal == [('L', 'PRON'), ("'", 'PUNCT'), ('italiano', 'ADJ'), ('(', 'PUNCT'), ('[', 'PUNCT'), ('itaˈljaːno][Nota', 'NOUN'), ('1', 'NUM'), (']', 'PUNCT'), ('ascolta[?·info', 'NOUN'), (']', 'PUNCT'), (')', 'PUNCT'), ('è', 'AUX'), ('una', 'DET'), ('lingua', 'NOUN'), ('romanza', 'NOUN'), ('parlata', 'ADJ'), ('principalmente', 'ADV'), ('in', 'ADP'), ('Italia', 'PROPN'), ('.', 'PUNCT')]
    elif lang == 'jpn':
        assert tokens_tagged == [('日本', '名詞'), ('語', '名詞'), ('(', '補助記号'), ('にほんご', '名詞'), ('、', '補助記号'), ('にっぽん', '名詞'), ('ご', '接尾辞'), ('[', '補助記号'), ('注', '名詞'), ('2', '名詞'), (']', '補助記号'), ('、', '補助記号'), ('英', '名詞'), (':', '補助記号'), ('Japanese', '英単語'), (')', '補助記号'), ('は', '助詞'), ('、', '補助記号'), ('主に', '副詞'), ('日本', '名詞'), ('国', '接尾辞'), ('内', '接尾辞'), ('や', '助詞'), ('日本', '名詞'), ('人', '接尾辞'), ('同士', '接尾辞'), ('の', '助詞'), ('間', '名詞'), ('で', '助詞'), ('使用', '名詞'), ('さ', '動詞'), ('れ', '助動詞'), ('て', '助詞'), ('いる', '動詞'), ('言語', '名詞'), ('。', '補助記号')]
        assert tokens_tagged_universal == [('日本', 'NOUN'), ('語', 'NOUN'), ('(', 'PUNCT/SYM'), ('にほんご', 'NOUN'), ('、', 'PUNCT/SYM'), ('にっぽん', 'NOUN'), ('ご', 'PART'), ('[', 'PUNCT/SYM'), ('注', 'NOUN'), ('2', 'NOUN'), (']', 'PUNCT/SYM'), ('、', 'PUNCT/SYM'), ('英', 'NOUN'), (':', 'PUNCT/SYM'), ('Japanese', 'X'), (')', 'PUNCT/SYM'), ('は', 'PART'), ('、', 'PUNCT/SYM'), ('主に', 'ADV'), ('日本', 'NOUN'), ('国', 'PART'), ('内', 'PART'), ('や', 'PART'), ('日本', 'NOUN'), ('人', 'PART'), ('同士', 'PART'), ('の', 'PART'), ('間', 'NOUN'), ('で', 'PART'), ('使用', 'NOUN'), ('さ', 'VERB'), ('れ', 'AUX'), ('て', 'PART'), ('いる', 'VERB'), ('言語', 'NOUN'), ('。', 'PUNCT/SYM')]
    elif lang == 'lit':
        assert tokens_tagged == [('Lietuvių', 'dkt.vyr.dgs.K.'), ('kalba', 'dkt.mot.vns.Įn.'), ('–', 'skyr.'), ('iš', 'prl.K.'), ('baltų', 'bdv.aukšt.vyr.dgs.Įn.'), ('prokalbės', 'dkt.mot.vns.K.'), ('kilusi', 'vksm.dlv.veik.būt-k.mot.vns.V.'), ('lietuvių', 'dkt.vyr.dgs.K.'), ('tautos', 'dkt.mot.vns.K.'), ('kalba', 'dkt.mot.vns.Įn.'), (',', 'skyr.'), ('kuri', 'įv.mot.vns.V.'), ('Lietuvoje', 'dkt.tikr.mot.vns.Vt.'), ('yra', 'vksm.asm.tiesiog.es.vns.3.'), ('valstybinė', 'bdv.nelygin.mot.vns.V.'), (',', 'skyr.'), ('o', 'jng.'), ('Europos', 'dkt.tikr.mot.vns.K.'), ('Sąjungoje', 'dkt.mot.vns.Vt.'), ('–', 'skyr.'), ('viena', 'įv.mot.vns.V.'), ('iš', 'prl.K.'), ('oficialiųjų', 'vksm.dlv.veik.būt-k.mot.vns.K.'), ('kalbų', 'dkt.vyr.vns.V.'), ('.', 'skyr.')]
        assert tokens_tagged_universal == [('Lietuvių', 'NOUN'), ('kalba', 'NOUN'), ('–', 'PUNCT'), ('iš', 'ADP'), ('baltų', 'VERB'), ('prokalbės', 'NOUN'), ('kilusi', 'VERB'), ('lietuvių', 'NOUN'), ('tautos', 'NOUN'), ('kalba', 'NOUN'), (',', 'PUNCT'), ('kuri', 'DET'), ('Lietuvoje', 'PROPN'), ('yra', 'AUX'), ('valstybinė', 'ADJ'), (',', 'PUNCT'), ('o', 'CCONJ'), ('Europos', 'PROPN'), ('Sąjungoje', 'NOUN'), ('–', 'PUNCT'), ('viena', 'PRON'), ('iš', 'ADP'), ('oficialiųjų', 'VERB'), ('kalbų', 'NOUN'), ('.', 'PUNCT')]
    elif lang == 'nob':
        assert tokens_tagged == [('Bokmål', 'NOUN'), ('er', 'AUX'), ('en', 'DET'), ('varietet', 'NOUN'), ('av', 'ADP'), ('norsk', 'ADJ'), ('språk', 'NOUN'), ('.', 'PUNCT')]
        assert tokens_tagged_universal == [('Bokmål', 'NOUN'), ('er', 'AUX'), ('en', 'DET'), ('varietet', 'NOUN'), ('av', 'ADP'), ('norsk', 'ADJ'), ('språk', 'NOUN'), ('.', 'PUNCT')]
    elif lang == 'pol':
        assert tokens_tagged == [('Język', 'SUBST'), ('polski', 'ADJ'), (',', 'INTERP'), ('polszczyzna', 'ADJ'), ('–', 'INTERP'), ('język', 'SUBST'), ('lechicki', 'SUBST'), ('z', 'PREP'), ('grupy', 'SUBST'), ('zachodniosłowiańskiej', 'ADJ'), ('(', 'INTERP'), ('do', 'PREP'), ('której', 'ADJ'), ('należą', 'FIN'), ('również', 'QUB'), ('czeski', 'ADJ'), (',', 'INTERP'), ('kaszubski', 'ADJ'), (',', 'INTERP'), ('słowacki', 'ADJ'), ('i', 'CONJ'), ('języki', 'SUBST'), ('łużyckie', 'ADJ'), (')', 'INTERP'), (',', 'INTERP'), ('stanowiącej', 'PACT'), ('część', 'SUBST'), ('rodziny', 'SUBST'), ('indoeuropejskiej', 'ADJ'), ('.', 'INTERP')]
        assert tokens_tagged_universal == [('Język', 'NOUN'), ('polski', 'ADJ'), (',', 'PUNCT'), ('polszczyzna', 'ADJ'), ('–', 'PUNCT'), ('język', 'NOUN'), ('lechicki', 'NOUN'), ('z', 'ADP'), ('grupy', 'NOUN'), ('zachodniosłowiańskiej', 'ADJ'), ('(', 'PUNCT'), ('do', 'ADP'), ('której', 'DET'), ('należą', 'VERB'), ('również', 'PART'), ('czeski', 'PROPN'), (',', 'PUNCT'), ('kaszubski', 'ADJ'), (',', 'PUNCT'), ('słowacki', 'ADJ'), ('i', 'CCONJ'), ('języki', 'NOUN'), ('łużyckie', 'ADJ'), (')', 'PUNCT'), (',', 'PUNCT'), ('stanowiącej', 'ADJ'), ('część', 'NOUN'), ('rodziny', 'NOUN'), ('indoeuropejskiej', 'ADJ'), ('.', 'PUNCT')]
    elif lang == 'por':
        assert tokens_tagged == [('A', 'DET'), ('língua', 'NOUN'), ('portuguesa', 'ADJ'), (',', 'PUNCT'), ('também', 'ADV'), ('designada', 'VERB'), ('português', 'ADJ'), (',', 'PUNCT'), ('é', 'AUX'), ('uma', 'DET'), ('língua', 'NOUN'), ('românica', 'ADJ'), ('flexiva', 'NOUN'), ('ocidental', 'ADJ'), ('originada', 'VERB'), ('no', 'ADP'), ('galego-português', 'NOUN'), ('falado', 'VERB'), ('no', 'ADP'), ('Reino', 'PROPN'), ('da', 'ADP'), ('Galiza', 'PROPN'), ('e', 'CCONJ'), ('no', 'ADP'), ('norte', 'NOUN'), ('de', 'ADP'), ('Portugal', 'PROPN'), ('.', 'PUNCT')]
        assert tokens_tagged_universal == [('A', 'DET'), ('língua', 'NOUN'), ('portuguesa', 'ADJ'), (',', 'PUNCT'), ('também', 'ADV'), ('designada', 'VERB'), ('português', 'ADJ'), (',', 'PUNCT'), ('é', 'AUX'), ('uma', 'DET'), ('língua', 'NOUN'), ('românica', 'ADJ'), ('flexiva', 'NOUN'), ('ocidental', 'ADJ'), ('originada', 'VERB'), ('no', 'ADP'), ('galego-português', 'NOUN'), ('falado', 'VERB'), ('no', 'ADP'), ('Reino', 'PROPN'), ('da', 'ADP'), ('Galiza', 'PROPN'), ('e', 'CCONJ'), ('no', 'ADP'), ('norte', 'NOUN'), ('de', 'ADP'), ('Portugal', 'PROPN'), ('.', 'PUNCT')]
    elif lang == 'ron':
        assert tokens_tagged == [('Limba', 'Ncfsry'), ('română', 'Afpfsrn'), ('este', 'Vmip3s'), ('o', 'Tifsr'), ('limbă', 'Ncfsrn'), ('indo-europeană', 'Afpfsrn'), (',', 'COMMA'), ('din', 'Spsa'), ('grupul', 'Ncmsry'), ('italic', 'Afpms-n'), ('și', 'Crssp'), ('din', 'Spsa'), ('subgrupul', 'Ncmsry'), ('oriental', 'Afpms-n'), ('al', 'Tsms'), ('limbilor', 'Ncfpoy'), ('romanice', 'Afpfp-n'), ('.', 'PERIOD')]
        assert tokens_tagged_universal == [('Limba', 'NOUN'), ('română', 'ADJ'), ('este', 'AUX'), ('o', 'DET'), ('limbă', 'NOUN'), ('indo-europeană', 'ADJ'), (',', 'PUNCT'), ('din', 'ADP'), ('grupul', 'NOUN'), ('italic', 'ADJ'), ('și', 'CCONJ'), ('din', 'ADP'), ('subgrupul', 'NOUN'), ('oriental', 'ADJ'), ('al', 'DET'), ('limbilor', 'NOUN'), ('romanice', 'ADJ'), ('.', 'PUNCT')]
    elif lang == 'rus':
        if pos_tagger == 'NLTK - Perceptron POS Tagger':
            assert tokens_tagged == [('Ру́сский', 'A=m'), ('язы́к', 'S'), ('(', 'NONLEX'), ('[', 'NONLEX'), ('ˈruskʲɪi̯', 'NONLEX'), ('jɪˈzɨk', 'NONLEX'), (']', 'NONLEX'), ('Информация', 'S'), ('о', 'PR'), ('файле', 'S'), ('слушать', 'V'), (')', 'NONLEX'), ('[', 'NONLEX'), ('~', 'NONLEX'), ('3', 'NUM=ciph'), (']', 'NONLEX'), ('[', 'NONLEX'), ('⇨', 'NONLEX'), (']', 'NONLEX'), ('—', 'NONLEX'), ('один', 'A-PRO=m'), ('из', 'PR'), ('восточнославянских', 'A=pl'), ('языков', 'S'), (',', 'NONLEX'), ('национальный', 'A=m'), ('язык', 'S'), ('русского', 'A=m'), ('народа', 'S'), ('.', 'NONLEX')]
            assert tokens_tagged_universal == [('Ру́сский', 'ADJ'), ('язы́к', 'NOUN'), ('(', 'PUNCT'), ('[', 'PUNCT'), ('ˈruskʲɪi̯', 'PUNCT'), ('jɪˈzɨk', 'PUNCT'), (']', 'PUNCT'), ('Информация', 'NOUN'), ('о', 'ADP'), ('файле', 'NOUN'), ('слушать', 'VERB'), (')', 'PUNCT'), ('[', 'PUNCT'), ('~', 'PUNCT'), ('3', 'NUM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('⇨', 'PUNCT'), (']', 'PUNCT'), ('—', 'PUNCT'), ('один', 'PRON'), ('из', 'ADP'), ('восточнославянских', 'ADJ'), ('языков', 'NOUN'), (',', 'PUNCT'), ('национальный', 'ADJ'), ('язык', 'NOUN'), ('русского', 'ADJ'), ('народа', 'NOUN'), ('.', 'PUNCT')]
        elif pos_tagger == 'pymorphy2 - Morphological Analyzer':
            assert tokens_tagged == [('Ру́сский', 'NOUN'), ('язы́к', 'NOUN'), ('(', 'PNCT'), ('[', 'PNCT'), ('ˈruskʲɪi̯', 'UNKN'), ('jɪˈzɨk', 'UNKN'), (']', 'PNCT'), ('Информация', 'NOUN'), ('о', 'PREP'), ('файле', 'NOUN'), ('слушать', 'INFN'), (')', 'PNCT'), ('[', 'PNCT'), ('~', 'UNKN'), ('3', 'NUMB'), (']', 'PNCT'), ('[', 'PNCT'), ('⇨', 'UNKN'), (']', 'PNCT'), ('—', 'PNCT'), ('один', 'ADJF'), ('из', 'PREP'), ('восточнославянских', 'ADJF'), ('языков', 'NOUN'), (',', 'PNCT'), ('национальный', 'ADJF'), ('язык', 'NOUN'), ('русского', 'ADJF'), ('народа', 'NOUN'), ('.', 'PNCT')]
            assert tokens_tagged_universal == [('Ру́сский', 'NOUN'), ('язы́к', 'NOUN'), ('(', 'PUNCT'), ('[', 'PUNCT'), ('ˈruskʲɪi̯', 'SYM/X'), ('jɪˈzɨk', 'SYM/X'), (']', 'PUNCT'), ('Информация', 'NOUN'), ('о', 'ADP'), ('файле', 'NOUN'), ('слушать', 'VERB'), (')', 'PUNCT'), ('[', 'PUNCT'), ('~', 'SYM/X'), ('3', 'NUM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('⇨', 'SYM/X'), (']', 'PUNCT'), ('—', 'PUNCT'), ('один', 'ADJ'), ('из', 'ADP'), ('восточнославянских', 'ADJ'), ('языков', 'NOUN'), (',', 'PUNCT'), ('национальный', 'ADJ'), ('язык', 'NOUN'), ('русского', 'ADJ'), ('народа', 'NOUN'), ('.', 'PUNCT')]
        elif pos_tagger == 'spaCy - Russian POS Tagger':
            assert tokens_tagged == [('Ру́сский', 'ADJ'), ('язы́к', 'PROPN'), ('(', 'PUNCT'), ('[', 'PUNCT'), ('ˈruskʲɪi̯', 'PROPN'), ('jɪˈzɨk', 'X'), (']', 'PUNCT'), ('Информация', 'NOUN'), ('о', 'ADP'), ('файле', 'NOUN'), ('слушать', 'VERB'), (')', 'PUNCT'), ('[', 'PUNCT'), ('~', 'PUNCT'), ('3', 'NUM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('⇨', 'NOUN'), (']', 'PUNCT'), ('—', 'PUNCT'), ('один', 'NUM'), ('из', 'ADP'), ('восточнославянских', 'ADJ'), ('языков', 'NOUN'), (',', 'PUNCT'), ('национальный', 'ADJ'), ('язык', 'NOUN'), ('русского', 'ADJ'), ('народа', 'NOUN'), ('.', 'PUNCT')]
            assert tokens_tagged_universal == [('Ру́сский', 'ADJ'), ('язы́к', 'PROPN'), ('(', 'PUNCT'), ('[', 'PUNCT'), ('ˈruskʲɪi̯', 'PROPN'), ('jɪˈzɨk', 'X'), (']', 'PUNCT'), ('Информация', 'NOUN'), ('о', 'ADP'), ('файле', 'NOUN'), ('слушать', 'VERB'), (')', 'PUNCT'), ('[', 'PUNCT'), ('~', 'PUNCT'), ('3', 'NUM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('⇨', 'NOUN'), (']', 'PUNCT'), ('—', 'PUNCT'), ('один', 'NUM'), ('из', 'ADP'), ('восточнославянских', 'ADJ'), ('языков', 'NOUN'), (',', 'PUNCT'), ('национальный', 'ADJ'), ('язык', 'NOUN'), ('русского', 'ADJ'), ('народа', 'NOUN'), ('.', 'PUNCT')]
    elif lang == 'spa':
        assert tokens_tagged == [('El', 'DET'), ('español', 'NOUN'), ('o', 'CCONJ'), ('castellano', 'NOUN'), ('es', 'AUX'), ('una', 'DET'), ('lengua', 'ADJ'), ('romance', 'NOUN'), ('procedente', 'ADJ'), ('del', 'ADP'), ('latín', 'NOUN'), ('hablado', 'ADJ'), ('.', 'PUNCT')]
        assert tokens_tagged_universal == [('El', 'DET'), ('español', 'NOUN'), ('o', 'CCONJ'), ('castellano', 'NOUN'), ('es', 'AUX'), ('una', 'DET'), ('lengua', 'ADJ'), ('romance', 'NOUN'), ('procedente', 'ADJ'), ('del', 'ADP'), ('latín', 'NOUN'), ('hablado', 'ADJ'), ('.', 'PUNCT')]
    elif lang == 'tha':
        if pos_tagger == 'PyThaiNLP - Perceptron Tagger (LST20)':
            assert tokens_tagged == [('ภาษาไทย', 'NN'), ('หรือ', 'CC'), ('ภาษาไทย', 'NN'), ('กลาง', 'NN'), ('เป็น', 'VV'), ('ภาษาราชการ', 'NN'), ('และ', 'CC'), ('ภาษาประจำชาติ', 'NN'), ('ของ', 'PS'), ('ประเทศ', 'NN'), ('ไทย', 'NN')]
            assert tokens_tagged_universal == [('ภาษาไทย', 'NOUN'), ('หรือ', 'CCONJ'), ('ภาษาไทย', 'NOUN'), ('กลาง', 'NOUN'), ('เป็น', 'VERB'), ('ภาษาราชการ', 'NOUN'), ('และ', 'CCONJ'), ('ภาษาประจำชาติ', 'NOUN'), ('ของ', 'ADP'), ('ประเทศ', 'NOUN'), ('ไทย', 'NOUN')]
        elif pos_tagger == 'PyThaiNLP - Perceptron Tagger (ORCHID)':
            assert tokens_tagged == [('ภาษาไทย', 'NPRP'), ('หรือ', 'JCRG'), ('ภาษาไทย', 'NPRP'), ('กลาง', 'VATT'), ('เป็น', 'VSTA'), ('ภาษาราชการ', 'NCMN'), ('และ', 'JCRG'), ('ภาษาประจำชาติ', 'NCMN'), ('ของ', 'RPRE'), ('ประเทศ', 'NCMN'), ('ไทย', 'NPRP')]
            assert tokens_tagged_universal == [('ภาษาไทย', 'PROPN'), ('หรือ', 'CCONJ'), ('ภาษาไทย', 'PROPN'), ('กลาง', 'ADJ'), ('เป็น', 'VERB'), ('ภาษาราชการ', 'NOUN'), ('และ', 'CCONJ'), ('ภาษาประจำชาติ', 'NOUN'), ('ของ', 'ADP'), ('ประเทศ', 'NOUN'), ('ไทย', 'PROPN')]
        elif pos_tagger == 'PyThaiNLP - Perceptron Tagger (PUD)':
            assert tokens_tagged == [('ภาษาไทย', 'NOUN'), ('หรือ', 'CCONJ'), ('ภาษาไทย', 'NOUN'), ('กลาง', 'NOUN'), ('เป็น', 'AUX'), ('ภาษาราชการ', 'NOUN'), ('และ', 'CCONJ'), ('ภาษาประจำชาติ', 'NOUN'), ('ของ', 'ADP'), ('ประเทศ', 'NOUN'), ('ไทย', 'PROPN')]
            assert tokens_tagged_universal == [('ภาษาไทย', 'NOUN'), ('หรือ', 'CCONJ'), ('ภาษาไทย', 'NOUN'), ('กลาง', 'NOUN'), ('เป็น', 'AUX'), ('ภาษาราชการ', 'NOUN'), ('และ', 'CCONJ'), ('ภาษาประจำชาติ', 'NOUN'), ('ของ', 'ADP'), ('ประเทศ', 'NOUN'), ('ไทย', 'PROPN')]
    elif lang == 'bod':
        assert tokens_tagged == [('བོད་', 'PROPN'), ('ཀྱི་', 'PART'), ('སྐད་ཡིག་', 'NOUN'), ('ནི་', 'NO_POS'), ('བོད་ཡུལ་', 'PROPN'), ('དང་', 'NO_POS'), ('དེ', 'DET'), ('འི་', 'PART'), ('ཉེ་འཁོར་', 'NOUN'), ('གྱི་', 'PART'), ('ས་ཁུལ་', 'OTHER'), ('ཏེ', 'PART'), ('།', 'PUNCT')]
        assert tokens_tagged_universal == [('བོད་', 'PROPN'), ('ཀྱི་', 'PART'), ('སྐད་ཡིག་', 'NOUN'), ('ནི་', 'X'), ('བོད་ཡུལ་', 'PROPN'), ('དང་', 'X'), ('དེ', 'DET'), ('འི་', 'PART'), ('ཉེ་འཁོར་', 'NOUN'), ('གྱི་', 'PART'), ('ས་ཁུལ་', 'X'), ('ཏེ', 'PART'), ('།', 'PUNCT')]
    elif lang == 'ukr':
        assert tokens_tagged == [('Украї́нська', 'ADJF'), ('мо́ва', 'ADJF'), ('(', 'PNCT'), ('МФА', 'UNKN'), (':', 'PNCT'), ('[', 'PNCT'), ('ukrɑ̽ˈjɪnʲsʲkɑ̽', 'UNKN'), ('ˈmɔwɑ̽', 'UNKN'), (']', 'PNCT'), (',', 'PNCT'), ('історичні', 'ADJF'), ('назви', 'NOUN'), ('—', 'PNCT'), ('ру́ська', 'ADJF'), (',', 'PNCT'), ('руси́нська[9][10][11', 'UNKN'), (']', 'PNCT'), ('[', 'PNCT'), ('*', 'PNCT'), ('2', 'NUMB'), (']', 'PNCT'), (')', 'PNCT'), ('—', 'PNCT'), ('національна', 'ADJF'), ('мова', 'NOUN'), ('українців', 'NOUN'), ('.', 'PNCT')]
        assert tokens_tagged_universal == [('Украї́нська', 'ADJ'), ('мо́ва', 'ADJ'), ('(', 'PUNCT'), ('МФА', 'SYM/X'), (':', 'PUNCT'), ('[', 'PUNCT'), ('ukrɑ̽ˈjɪnʲsʲkɑ̽', 'SYM/X'), ('ˈmɔwɑ̽', 'SYM/X'), (']', 'PUNCT'), (',', 'PUNCT'), ('історичні', 'ADJ'), ('назви', 'NOUN'), ('—', 'PUNCT'), ('ру́ська', 'ADJ'), (',', 'PUNCT'), ('руси́нська[9][10][11', 'SYM/X'), (']', 'PUNCT'), ('[', 'PUNCT'), ('*', 'PUNCT'), ('2', 'NUM'), (']', 'PUNCT'), (')', 'PUNCT'), ('—', 'PUNCT'), ('національна', 'ADJ'), ('мова', 'NOUN'), ('українців', 'NOUN'), ('.', 'PUNCT')]
    elif lang == 'vie':
        assert tokens_tagged == [('Tiếng', 'N'), ('Việt', 'Np'), (',', 'CH'), ('còn', 'C'), ('gọi', 'V'), ('tiếng', 'N'), ('Việt Nam', 'Np'), ('[', 'V'), ('5', 'M'), (']', 'CH'), (',', 'CH'), ('tiếng Kinh', 'N'), ('hay', 'C'), ('Việt ngữ', 'V'), (',', 'CH'), ('là', 'V'), ('ngôn ngữ', 'N'), ('của', 'E'), ('người', 'Nc'), ('Việt', 'Np'), ('(', 'CH'), ('dân tộc', 'N'), ('Kinh', 'Np'), (')', 'CH'), ('và', 'C'), ('là', 'V'), ('ngôn ngữ', 'N'), ('chính thức', 'A'), ('tại', 'E'), ('Việt Nam', 'Np'), ('.', 'CH')]
        assert tokens_tagged_universal == [('Tiếng', 'NOUN'), ('Việt', 'PROPN'), (',', 'PUNCT'), ('còn', 'CCONJ'), ('gọi', 'VERB'), ('tiếng', 'NOUN'), ('Việt Nam', 'PROPN'), ('[', 'VERB'), ('5', 'NUM'), (']', 'PUNCT'), (',', 'PUNCT'), ('tiếng Kinh', 'NOUN'), ('hay', 'CCONJ'), ('Việt ngữ', 'VERB'), (',', 'PUNCT'), ('là', 'VERB'), ('ngôn ngữ', 'NOUN'), ('của', 'ADP'), ('người', 'NOUN'), ('Việt', 'PROPN'), ('(', 'PUNCT'), ('dân tộc', 'NOUN'), ('Kinh', 'PROPN'), (')', 'PUNCT'), ('và', 'CCONJ'), ('là', 'VERB'), ('ngôn ngữ', 'NOUN'), ('chính thức', 'ADJ'), ('tại', 'ADP'), ('Việt Nam', 'PROPN'), ('.', 'PUNCT')]
    else:
        raise Exception(f'Warning: language code "{lang}" is absent from the list!')

if __name__ == '__main__':
    for lang, pos_tagger in test_pos_taggers:
        test_pos_tag(lang, pos_tagger, show_results = True)
