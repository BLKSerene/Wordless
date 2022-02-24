# ----------------------------------------------------------------------
# Wordless: Tests - NLP - POS Tagging
# Copyright (C) 2018-2022  Ye Lei (叶磊)
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

from wl_nlp import wl_pos_tagging, wl_word_tokenization
from wl_tests import wl_test_init, wl_test_lang_examples
from wl_utils import wl_conversion

test_pos_taggers = []

main = wl_test_init.Wl_Test_Main()

for lang, pos_taggers in main.settings_global['pos_taggers'].items():
    for pos_tagger in pos_taggers:
        if lang not in ['other']:
            test_pos_taggers.append((lang, pos_tagger))

@pytest.mark.parametrize('lang, pos_tagger', test_pos_taggers)
def test_pos_tag(lang, pos_tagger):
    lang_text = wl_conversion.to_lang_text(main, lang)

    print(f'{lang_text} ({lang}) / {pos_tagger}:')

    # Untokenized
    tokens_tagged = wl_pos_tagging.wl_pos_tag(
        main,
        inputs = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}'),
        lang = lang,
        pos_tagger = pos_tagger
    )
    tokens_tagged_universal = wl_pos_tagging.wl_pos_tag(
        main,
        inputs = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}'),
        lang = lang,
        pos_tagger = pos_tagger,
        tagset = 'universal'
    )

    # Tokenized
    tokens = wl_word_tokenization.wl_word_tokenize_flat(
        main,
        text = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}'),
        lang = lang
    )
    tokens_tagged_tokenized = wl_pos_tagging.wl_pos_tag(
        main,
        inputs = tokens,
        lang = lang,
        pos_tagger = pos_tagger
    )
    tokens_tagged_universal_tokenized = wl_pos_tagging.wl_pos_tag(
        main,
        inputs = tokens,
        lang = lang,
        pos_tagger = pos_tagger,
        tagset = 'universal'
    )

    # Use 0 to 9 only since nagisa would split numerals into single numbers (except 24 and maybe some others)
    tokens_tagged_long_text = wl_pos_tagging.wl_pos_tag(
        main,
        inputs = ''.join([f'{i % 10}\n' for i in range(101)]),
        lang = lang,
        pos_tagger = pos_tagger
    )
    tokens_tagged_long_text_tokenized = wl_pos_tagging.wl_pos_tag(
        main,
        inputs = [str(i % 10) for i in range(101) for j in range(50)],
        lang = lang,
        pos_tagger = pos_tagger
    )

    print(tokens_tagged)
    print(tokens_tagged_universal)

    # Check for missing tags
    assert all([tag for token, tag in tokens_tagged])
    assert all([tag for token, tag in tokens_tagged_universal])
    assert all([tag for token, tag in tokens_tagged_tokenized])
    assert all([tag for token, tag in tokens_tagged_universal_tokenized])
    # Universal tags should not all be "X"
    assert any([tag for token, tag in tokens_tagged_universal if tag != 'X'])
    assert any([tag for token, tag in tokens_tagged_universal_tokenized if tag != 'X'])

    # Tokenization should not be modified
    assert len(tokens) == len(tokens_tagged_tokenized) == len(tokens_tagged_universal_tokenized)

    # Test long texts
    if pos_tagger == 'botok_bod':
        assert [token[0] for token in tokens_tagged_long_text] == ['\n'.join([str(i % 10) for i in range(100)]), '0']
    else:
        assert [token[0] for token in tokens_tagged_long_text] == [str(i % 10) for i in range(101)]
    assert [token[0] for token in tokens_tagged_long_text_tokenized] == [str(i % 10) for i in range(101) for j in range(50)]

    if lang == 'cat':
        assert tokens_tagged == tokens_tagged_universal == [('El', 'DET'), ('català', 'NOUN'), ('(', 'PUNCT'), ('denominació', 'NOUN'), ('oficial', 'ADJ'), ('a', 'ADP'), ('Catalunya', 'PROPN'), (',', 'PUNCT'), ('a', 'ADP'), ('les', 'DET'), ('Illes', 'PROPN'), ('Balears', 'PROPN'), (',', 'PUNCT'), ('a', 'ADP'), ('Andorra', 'PROPN'), (',', 'PUNCT'), ('a', 'ADP'), ('la', 'DET'), ('ciutat', 'NOUN'), ('de', 'ADP'), ("l'", 'DET'), ('Alguer', 'PROPN'), ('i', 'CCONJ'), ('tradicional', 'ADJ'), ('a', 'ADP'), ('Catalunya', 'PROPN'), ('Nord', 'PROPN'), (')', 'PUNCT'), ('o', 'CCONJ'), ('valencià', 'PROPN'), ('(', 'PUNCT'), ('denominació', 'NOUN'), ('oficial', 'ADJ'), ('a', 'ADP'), ('l', 'DET'), ('País', 'PROPN'), ('Valencià', 'PROPN'), ('i', 'CCONJ'), ('tradicional', 'ADJ'), ('a', 'ADP'), ('l', 'DET'), ('Carxe', 'PROPN'), (')', 'PUNCT'), ('és', 'AUX'), ('una', 'DET'), ('llengua', 'NOUN'), ('romànica', 'ADJ'), ('parlada', 'ADJ'), ('a', 'ADP'), ('Catalunya', 'PROPN'), (',', 'PUNCT'), ('el', 'DET'), ('País', 'PROPN'), ('Valencià', 'PROPN'), ('(', 'PUNCT'), ('tret', 'NOUN'), ("d'", 'ADP'), ('algunes', 'DET'), ('comarques', 'NOUN'), ('i', 'CCONJ'), ('localitats', 'NOUN'), ('de', 'ADP'), ("l'", 'DET'), ('interior', 'NOUN'), (')', 'PUNCT'), (',', 'PUNCT'), ('les', 'DET'), ('Illes', 'PROPN'), ('Balears', 'PROPN'), (',', 'PUNCT'), ('Andorra', 'PROPN'), (',', 'PUNCT'), ('la', 'DET'), ('Franja', 'PROPN'), ('de', 'ADP'), ('Ponent', 'PROPN'), ('(', 'PUNCT'), ('a', 'ADP'), ("l'", 'DET'), ('Aragó', 'PROPN'), (')', 'PUNCT'), (',', 'PUNCT'), ('la', 'DET'), ('ciutat', 'NOUN'), ('de', 'ADP'), ("l'", 'DET'), ('Alguer', 'PROPN'), ('(', 'PUNCT'), ('a', 'ADP'), ("l'", 'DET'), ('illa', 'NOUN'), ('de', 'ADP'), ('Sardenya', 'PROPN'), (')', 'PUNCT'), (',', 'PUNCT'), ('la', 'DET'), ('Catalunya', 'PROPN'), ('d', 'ADP'), ('el', 'DET'), ('Nord,[8', 'PROPN'), (']', 'PUNCT'), ('el', 'DET'), ('Carxe', 'PROPN'), ('(', 'PUNCT'), ('un', 'DET'), ('petit', 'ADJ'), ('territori', 'NOUN'), ('de', 'ADP'), ('Múrcia', 'PROPN'), ('poblat', 'ADJ'), ('per', 'ADP'), ('immigrats', 'NOUN'), ('valencians),[9][10', 'ADJ'), (']', 'PUNCT'), ('i', 'CCONJ'), ('en', 'ADP'), ('comunitats', 'NOUN'), ('arreu', 'ADV'), ('d', 'ADP'), ('el', 'DET'), ('món', 'NOUN'), ('(', 'PUNCT'), ('entre', 'ADP'), ('les', 'DET'), ('quals', 'PRON'), ('destaca', 'VERB'), ('la', 'DET'), ('de', 'ADP'), ("l'", 'DET'), ('Argentina', 'PROPN'), (',', 'PUNCT'), ('amb', 'ADP'), ('198.000', 'NUM'), ('parlants).[11', 'PROPN'), (']', 'PUNCT')]
    elif lang == 'zho_cn':
        if pos_tagger == 'jieba_zho':
            assert tokens_tagged == [('汉语', 'nz'), ('，', 'x'), ('又称', 'n'), ('汉文', 'nz'), ('、', 'x'), ('中文', 'nz'), ('、', 'x'), ('中国', 'ns'), ('话', 'n'), ('、', 'x'), ('中国', 'ns'), ('语', 'ng'), ('、', 'x'), ('华语', 'nz'), ('、', 'x'), ('华文', 'nz'), ('、', 'x'), ('唐', 'nr'), ('话', 'n'), ('[', 'x'), ('2', 'x'), (']', 'x'), ('，', 'x'), ('或', 'c'), ('被', 'p'), ('视为', 'v'), ('一个', 'm'), ('语族', 'n'), ('，', 'x'), ('或', 'c'), ('被', 'p'), ('视为', 'v'), ('隶属于', 'n'), ('汉藏语系', 'nz'), ('汉语', 'nz'), ('族', 'ng'), ('之', 'u'), ('一种', 'm'), ('语言', 'n'), ('。', 'x')]
            assert tokens_tagged_universal == [('汉语', 'PROPN'), ('，', 'PUNCT/SYM'), ('又称', 'NOUN'), ('汉文', 'PROPN'), ('、', 'PUNCT/SYM'), ('中文', 'PROPN'), ('、', 'PUNCT/SYM'), ('中国', 'PROPN'), ('话', 'NOUN'), ('、', 'PUNCT/SYM'), ('中国', 'PROPN'), ('语', 'NOUN'), ('、', 'PUNCT/SYM'), ('华语', 'PROPN'), ('、', 'PUNCT/SYM'), ('华文', 'PROPN'), ('、', 'PUNCT/SYM'), ('唐', 'PRONP'), ('话', 'NOUN'), ('[', 'PUNCT/SYM'), ('2', 'PUNCT/SYM'), (']', 'PUNCT/SYM'), ('，', 'PUNCT/SYM'), ('或', 'CONJ'), ('被', 'ADP'), ('视为', 'VERB'), ('一个', 'NUM'), ('语族', 'NOUN'), ('，', 'PUNCT/SYM'), ('或', 'CONJ'), ('被', 'ADP'), ('视为', 'VERB'), ('隶属于', 'NOUN'), ('汉藏语系', 'PROPN'), ('汉语', 'PROPN'), ('族', 'NOUN'), ('之', 'PART'), ('一种', 'NUM'), ('语言', 'NOUN'), ('。', 'PUNCT/SYM')]
        elif pos_tagger == 'spacy_zho':
            assert tokens_tagged == [('汉语', 'NN'), ('，', 'PU'), ('又', 'AD'), ('称', 'VV'), ('汉文', 'NR'), ('、', 'PU'), ('中文', 'NN'), ('、', 'PU'), ('中国话', 'NN'), ('、', 'PU'), ('中国语', 'NR'), ('、', 'PU'), ('华语', 'NR'), ('、', 'PU'), ('华文', 'NN'), ('、', 'PU'), ('唐话', 'NR'), ('[', 'NR'), ('2', 'CD'), (']', 'M'), ('，', 'PU'), ('或', 'CC'), ('被', 'SB'), ('视为', 'VV'), ('一个', 'AD'), ('语族', 'NN'), ('，', 'PU'), ('或', 'CC'), ('被', 'SB'), ('视为', 'VV'), ('隶属于', 'VV'), ('汉藏', 'NR'), ('语系', 'NN'), ('汉语族', 'NN'), ('之一', 'NN'), ('种', 'VV'), ('语言', 'NN'), ('。', 'PU')]
            assert tokens_tagged_universal == [('汉语', 'NOUN'), ('，', 'PUNCT'), ('又', 'ADV'), ('称', 'VERB'), ('汉文', 'PROPN'), ('、', 'PUNCT'), ('中文', 'NOUN'), ('、', 'PUNCT'), ('中国话', 'NOUN'), ('、', 'PUNCT'), ('中国语', 'PROPN'), ('、', 'PUNCT'), ('华语', 'PROPN'), ('、', 'PUNCT'), ('华文', 'NOUN'), ('、', 'PUNCT'), ('唐话', 'PROPN'), ('[', 'PROPN'), ('2', 'NUM'), (']', 'NUM'), ('，', 'PUNCT'), ('或', 'CCONJ'), ('被', 'X'), ('视为', 'VERB'), ('一个', 'ADV'), ('语族', 'NOUN'), ('，', 'PUNCT'), ('或', 'CCONJ'), ('被', 'X'), ('视为', 'VERB'), ('隶属于', 'VERB'), ('汉藏', 'PROPN'), ('语系', 'NOUN'), ('汉语族', 'NOUN'), ('之一', 'NOUN'), ('种', 'VERB'), ('语言', 'NOUN'), ('。', 'PUNCT')]
        else:
            raise Exception(f'Error: Tests for POS tagger "{pos_tagger}" is skipped!')
    elif lang == 'zho_tw':
        if pos_tagger == 'jieba_zho':
            assert tokens_tagged == [('漢語', 'nz'), ('，', 'x'), ('又', 'd'), ('稱', 'v'), ('漢文', 'nz'), ('、', 'x'), ('中文', 'nz'), ('、', 'x'), ('中國', 'ns'), ('話', 'n'), ('、', 'x'), ('中國', 'ns'), ('語', 'n'), ('、', 'x'), ('華語', 'nz'), ('、', 'x'), ('華文', 'nz'), ('、', 'x'), ('唐', 'nr'), ('話', 'n'), ('[', 'x'), ('2', 'x'), (']', 'x'), ('，', 'x'), ('或', 'c'), ('被', 'p'), ('視為', 'v'), ('一個', 'm'), ('語族', 'n'), ('，', 'x'), ('或', 'c'), ('被', 'p'), ('視為', 'v'), ('隸屬', 'v'), ('於', 'nr'), ('漢藏語', 'nz'), ('系漢', 'n'), ('語族', 'n'), ('之一', 'r'), ('種', 'm'), ('語言', 'n'), ('。', 'x')]
            assert tokens_tagged_universal == [('漢語', 'PROPN'), ('，', 'PUNCT/SYM'), ('又', 'ADV'), ('稱', 'VERB'), ('漢文', 'PROPN'), ('、', 'PUNCT/SYM'), ('中文', 'PROPN'), ('、', 'PUNCT/SYM'), ('中國', 'PROPN'), ('話', 'NOUN'), ('、', 'PUNCT/SYM'), ('中國', 'PROPN'), ('語', 'NOUN'), ('、', 'PUNCT/SYM'), ('華語', 'PROPN'), ('、', 'PUNCT/SYM'), ('華文', 'PROPN'), ('、', 'PUNCT/SYM'), ('唐', 'PRONP'), ('話', 'NOUN'), ('[', 'PUNCT/SYM'), ('2', 'PUNCT/SYM'), (']', 'PUNCT/SYM'), ('，', 'PUNCT/SYM'), ('或', 'CONJ'), ('被', 'ADP'), ('視為', 'VERB'), ('一個', 'NUM'), ('語族', 'NOUN'), ('，', 'PUNCT/SYM'), ('或', 'CONJ'), ('被', 'ADP'), ('視為', 'VERB'), ('隸屬', 'VERB'), ('於', 'PRONP'), ('漢藏語', 'PROPN'), ('系漢', 'NOUN'), ('語族', 'NOUN'), ('之一', 'PRON'), ('種', 'NUM'), ('語言', 'NOUN'), ('。', 'PUNCT/SYM')]
        elif pos_tagger == 'spacy_zho':
            assert tokens_tagged == [('漢語', 'NN'), ('，', 'PU'), ('又', 'AD'), ('稱', 'VV'), ('漢文', 'NN'), ('、', 'PU'), ('中文', 'NN'), ('、', 'PU'), ('中國話', 'NR'), ('、', 'PU'), ('中國語', 'NN'), ('、', 'PU'), ('華語', 'NN'), ('、', 'PU'), ('華文', 'NN'), ('、', 'PU'), ('唐話[', 'NR'), ('2', 'CD'), (']', 'M'), ('，', 'PU'), ('或', 'CC'), ('被', 'SB'), ('視為', 'VV'), ('一', 'CD'), ('個', 'M'), ('語族', 'NN'), ('，', 'PU'), ('或', 'CC'), ('被', 'SB'), ('視為', 'VV'), ('隸屬', 'NR'), ('於漢', 'VV'), ('藏語', 'VV'), ('系漢', 'VV'), ('語族', 'NN'), ('之一', 'NN'), ('種', 'AD'), ('語言', 'VV'), ('。', 'PU')]
            assert tokens_tagged_universal == [('漢語', 'NOUN'), ('，', 'PUNCT'), ('又', 'ADV'), ('稱', 'VERB'), ('漢文', 'NOUN'), ('、', 'PUNCT'), ('中文', 'NOUN'), ('、', 'PUNCT'), ('中國話', 'PROPN'), ('、', 'PUNCT'), ('中國語', 'NOUN'), ('、', 'PUNCT'), ('華語', 'NOUN'), ('、', 'PUNCT'), ('華文', 'NOUN'), ('、', 'PUNCT'), ('唐話[', 'PROPN'), ('2', 'NUM'), (']', 'NUM'), ('，', 'PUNCT'), ('或', 'CCONJ'), ('被', 'X'), ('視為', 'VERB'), ('一', 'NUM'), ('個', 'NUM'), ('語族', 'NOUN'), ('，', 'PUNCT'), ('或', 'CCONJ'), ('被', 'X'), ('視為', 'VERB'), ('隸屬', 'PROPN'), ('於漢', 'VERB'), ('藏語', 'VERB'), ('系漢', 'VERB'), ('語族', 'NOUN'), ('之一', 'NOUN'), ('種', 'ADV'), ('語言', 'VERB'), ('。', 'PUNCT')]
        else:
            raise Exception(f'Error: Tests for POS tagger "{pos_tagger}" is skipped!')
    elif lang == 'dan':
        assert tokens_tagged == [('Dansk', 'ADJ'), ('er', 'AUX'), ('et', 'DET'), ('nordgermansk', 'ADJ'), ('sprog', 'NOUN'), ('af', 'ADP'), ('den', 'DET'), ('østnordiske', 'ADJ'), ('(', 'PUNCT'), ('kontinentale', 'NOUN'), (')', 'PUNCT'), ('gruppe', 'NOUN'), (',', 'PUNCT'), ('der', 'PRON'), ('tales', 'VERB'), ('af', 'ADP'), ('ca.', 'ADV'), ('seks', 'NUM'), ('millioner', 'NOUN'), ('mennesker', 'NOUN'), ('.', 'PUNCT')]
        assert tokens_tagged_universal == [('Dansk', 'ADJ'), ('er', 'AUX'), ('et', 'DET'), ('nordgermansk', 'ADJ'), ('sprog', 'NOUN'), ('af', 'ADP'), ('den', 'DET'), ('østnordiske', 'ADJ'), ('(', 'PUNCT'), ('kontinentale', 'NOUN'), (')', 'PUNCT'), ('gruppe', 'NOUN'), (',', 'PUNCT'), ('der', 'PRON'), ('tales', 'VERB'), ('af', 'ADP'), ('ca.', 'ADV'), ('seks', 'NUM'), ('millioner', 'NOUN'), ('mennesker', 'NOUN'), ('.', 'PUNCT')]
    elif lang == 'nld':
        assert tokens_tagged == [('Het', 'LID|bep|stan|evon'), ('Nederlands', 'N|eigen|ev|basis|onz|stan'), ('is', 'WW|pv|tgw|ev'), ('een', 'LID|onbep|stan|agr'), ('West-Germaanse', 'ADJ|prenom|basis|met-e|stan'), ('taal', 'N|soort|ev|basis|zijd|stan'), ('en', 'VG|neven'), ('de', 'LID|bep|stan|rest'), ('officiële', 'ADJ|prenom|basis|met-e|stan'), ('taal', 'N|soort|ev|basis|zijd|stan'), ('van', 'VZ|init'), ('Nederland', 'N|eigen|ev|basis|onz|stan'), (',', 'LET'), ('Suriname', 'N|eigen|ev|basis|onz|stan'), ('en', 'VG|neven'), ('een', 'TW|hoofd|nom|zonder-n|basis'), ('van', 'VZ|init'), ('de', 'LID|bep|stan|rest'), ('drie', 'TW|hoofd|prenom|stan'), ('officiële', 'ADJ|prenom|basis|met-e|stan'), ('talen', 'N|soort|mv|basis'), ('van', 'VZ|init'), ('België', 'N|eigen|ev|basis|onz|stan'), ('.', 'LET')]
        assert tokens_tagged_universal == [('Het', 'DET'), ('Nederlands', 'PROPN'), ('is', 'AUX'), ('een', 'DET'), ('West-Germaanse', 'ADJ'), ('taal', 'NOUN'), ('en', 'CCONJ'), ('de', 'DET'), ('officiële', 'ADJ'), ('taal', 'NOUN'), ('van', 'ADP'), ('Nederland', 'PROPN'), (',', 'PUNCT'), ('Suriname', 'PROPN'), ('en', 'CCONJ'), ('een', 'NUM'), ('van', 'ADP'), ('de', 'DET'), ('drie', 'NUM'), ('officiële', 'ADJ'), ('talen', 'NOUN'), ('van', 'ADP'), ('België', 'PROPN'), ('.', 'PUNCT')]
    elif lang in ['eng_gb', 'eng_us']:
        if pos_tagger == 'nltk_perceptron':
            assert tokens_tagged == [('English', 'NNP'), ('is', 'VBZ'), ('a', 'DT'), ('West', 'NNP'), ('Germanic', 'NNP'), ('language', 'NN'), ('of', 'IN'), ('the', 'DT'), ('Indo', 'NNP'), ('-', ':'), ('European', 'JJ'), ('language', 'NN'), ('family', 'NN'), (',', ','), ('originally', 'RB'), ('spoken', 'VBN'), ('by', 'IN'), ('the', 'DT'), ('inhabitants', 'NNS'), ('of', 'IN'), ('early', 'JJ'), ('medieval', 'NN'), ('England.[3][4][5', 'NNP'), (']', 'NN')]
            assert tokens_tagged_universal == [('English', 'PROPN'), ('is', 'VERB'), ('a', 'DET'), ('West', 'PROPN'), ('Germanic', 'PROPN'), ('language', 'NOUN'), ('of', 'ADP/SCONJ'), ('the', 'DET'), ('Indo', 'PROPN'), ('-', 'PUNCT'), ('European', 'ADJ'), ('language', 'NOUN'), ('family', 'NOUN'), (',', 'PUNCT'), ('originally', 'ADV'), ('spoken', 'VERB'), ('by', 'ADP/SCONJ'), ('the', 'DET'), ('inhabitants', 'NOUN'), ('of', 'ADP/SCONJ'), ('early', 'ADJ'), ('medieval', 'NOUN'), ('England.[3][4][5', 'PROPN'), (']', 'NOUN')]
        elif pos_tagger == 'spacy_eng':
            assert tokens_tagged == [('English', 'NNP'), ('is', 'VBZ'), ('a', 'DT'), ('West', 'NNP'), ('Germanic', 'NNP'), ('language', 'NN'), ('of', 'IN'), ('the', 'DT'), ('Indo', 'NNP'), ('-', 'HYPH'), ('European', 'JJ'), ('language', 'NN'), ('family', 'NN'), (',', ','), ('originally', 'RB'), ('spoken', 'VBN'), ('by', 'IN'), ('the', 'DT'), ('inhabitants', 'NNS'), ('of', 'IN'), ('early', 'JJ'), ('medieval', 'JJ'), ('England.[3][4][5', 'NNS'), (']', '-RRB-')]
            assert tokens_tagged_universal == [('English', 'PROPN'), ('is', 'AUX'), ('a', 'DET'), ('West', 'PROPN'), ('Germanic', 'PROPN'), ('language', 'NOUN'), ('of', 'ADP'), ('the', 'DET'), ('Indo', 'PROPN'), ('-', 'PUNCT'), ('European', 'ADJ'), ('language', 'NOUN'), ('family', 'NOUN'), (',', 'PUNCT'), ('originally', 'ADV'), ('spoken', 'VERB'), ('by', 'ADP'), ('the', 'DET'), ('inhabitants', 'NOUN'), ('of', 'ADP'), ('early', 'ADJ'), ('medieval', 'ADJ'), ('England.[3][4][5', 'NOUN'), (']', 'PUNCT')]
        else:
            raise Exception(f'Error: Tests for POS tagger "{pos_tagger}" is skipped!')
    elif lang == 'fra':
        assert tokens_tagged == tokens_tagged_universal == [('Le', 'DET'), ('français', 'NOUN'), ('est', 'AUX'), ('une', 'DET'), ('langue', 'NOUN'), ('indo-européenne', 'ADJ'), ('de', 'ADP'), ('la', 'DET'), ('famille', 'NOUN'), ('des', 'ADP'), ('langues', 'ADJ'), ('romanes', 'ADJ'), ('dont', 'PRON'), ('les', 'DET'), ('locuteurs', 'NOUN'), ('sont', 'AUX'), ('appelés', 'VERB'), ('francophones', 'ADJ'), ('.', 'PUNCT')]
    elif lang in ['deu_at', 'deu_de', 'deu_ch']:
        assert tokens_tagged == [('Die', 'ART'), ('deutsche', 'ADJA'), ('Sprache', 'NN'), ('bzw.', 'KON'), ('das', 'ART'), ('Deutsche', 'NN'), ('(', '$('), ('[', 'NE'), ('dɔɪ̯tʃ];[26', 'NE'), (']', 'NN'), ('abgekürzt', 'VVFIN'), ('dt', 'NE'), ('.', '$.'), ('oder', 'KON'), ('dtsch', 'ADJD'), ('.', '$.'), (')', '$('), ('ist', 'VAFIN'), ('eine', 'ART'), ('westgermanische', 'ADJA'), ('Sprache', 'NN'), (',', '$,'), ('die', 'PRELS'), ('weltweit', 'ADJD'), ('etwa', 'ADV'), ('90', 'CARD'), ('bis', 'KON'), ('105', 'CARD'), ('Millionen', 'NN'), ('Menschen', 'NN'), ('als', 'APPR'), ('Muttersprache', 'NN'), ('und', 'KON'), ('weiteren', 'ADJA'), ('rund', 'ADV'), ('80', 'CARD'), ('Millionen', 'NN'), ('als', 'APPR'), ('Zweit-', 'TRUNC'), ('oder', 'KON'), ('Fremdsprache', 'NN'), ('dient', 'VVFIN'), ('.', '$.')]
        assert tokens_tagged_universal == [('Die', 'DET'), ('deutsche', 'ADJ'), ('Sprache', 'NOUN'), ('bzw.', 'CCONJ'), ('das', 'DET'), ('Deutsche', 'ADJ'), ('(', 'PUNCT'), ('[', 'NOUN'), ('dɔɪ̯tʃ];[26', 'PROPN'), (']', 'NOUN'), ('abgekürzt', 'VERB'), ('dt', 'PROPN'), ('.', 'PUNCT'), ('oder', 'CCONJ'), ('dtsch', 'ADV'), ('.', 'PUNCT'), (')', 'PUNCT'), ('ist', 'AUX'), ('eine', 'DET'), ('westgermanische', 'ADJ'), ('Sprache', 'NOUN'), (',', 'PUNCT'), ('die', 'PRON'), ('weltweit', 'ADV'), ('etwa', 'ADV'), ('90', 'NUM'), ('bis', 'CCONJ'), ('105', 'NUM'), ('Millionen', 'NOUN'), ('Menschen', 'NOUN'), ('als', 'ADP'), ('Muttersprache', 'NOUN'), ('und', 'CCONJ'), ('weiteren', 'ADJ'), ('rund', 'ADV'), ('80', 'NUM'), ('Millionen', 'NOUN'), ('als', 'ADP'), ('Zweit-', 'X'), ('oder', 'CCONJ'), ('Fremdsprache', 'NOUN'), ('dient', 'VERB'), ('.', 'PUNCT')]
    elif lang == 'ell':
        assert tokens_tagged == [('Η', 'DET'), ('ελληνική', 'ADJ'), ('γλώσσα', 'NOUN'), ('ανήκει', 'VERB'), ('στην', 'ADP'), ('ινδοευρωπαϊκή', 'ADJ'), ('οικογένεια[10', 'NOUN'), (']', 'NOUN'), ('και', 'CCONJ'), ('αποτελεί', 'VERB'), ('το', 'DET'), ('μοναδικό', 'ADJ'), ('μέλος', 'NOUN'), ('του', 'DET'), ('ελληνικού', 'ADJ'), ('κλάδου', 'NOUN'), (',', 'PUNCT'), ('ενώ', 'SCONJ'), ('είναι', 'AUX'), ('η', 'DET'), ('επίσημη', 'ADJ'), ('γλώσσα', 'NOUN'), ('της', 'DET'), ('Ελλάδος', 'PROPN'), ('και', 'CCONJ'), ('της', 'DET'), ('Κύπρου', 'PROPN'), ('.', 'PUNCT')]
        assert tokens_tagged_universal == [('Η', 'DET'), ('ελληνική', 'ADJ'), ('γλώσσα', 'NOUN'), ('ανήκει', 'VERB'), ('στην', 'ADP'), ('ινδοευρωπαϊκή', 'ADJ'), ('οικογένεια[10', 'NOUN'), (']', 'NOUN'), ('και', 'CCONJ'), ('αποτελεί', 'VERB'), ('το', 'DET'), ('μοναδικό', 'ADJ'), ('μέλος', 'NOUN'), ('του', 'DET'), ('ελληνικού', 'ADJ'), ('κλάδου', 'NOUN'), (',', 'PUNCT'), ('ενώ', 'SCONJ'), ('είναι', 'AUX'), ('η', 'DET'), ('επίσημη', 'ADJ'), ('γλώσσα', 'NOUN'), ('της', 'DET'), ('Ελλάδος', 'PROPN'), ('και', 'CCONJ'), ('της', 'DET'), ('Κύπρου', 'PROPN'), ('.', 'PUNCT')]
    elif lang == 'ita':
        assert tokens_tagged == [("L'", 'RD'), ('italiano', 'S'), ('(', 'FB'), ('[', 'FB'), ('itaˈljaːno][Nota', 'S'), ('1', 'N'), (']', 'FB'), ('ascolta[?·info', 'SP'), (']', 'FB'), (')', 'FB'), ('è', 'V'), ('una', 'RI'), ('lingua', 'S'), ('romanza', 'S'), ('parlata', 'V'), ('principalmente', 'B'), ('in', 'E'), ('Italia', 'SP'), ('.', 'FS')]
        assert tokens_tagged_universal == [("L'", 'DET'), ('italiano', 'NOUN'), ('(', 'PUNCT'), ('[', 'PUNCT'), ('itaˈljaːno][Nota', 'VERB'), ('1', 'NUM'), (']', 'PUNCT'), ('ascolta[?·info', 'PROPN'), (']', 'PUNCT'), (')', 'PUNCT'), ('è', 'AUX'), ('una', 'DET'), ('lingua', 'NOUN'), ('romanza', 'NOUN'), ('parlata', 'VERB'), ('principalmente', 'ADV'), ('in', 'ADP'), ('Italia', 'PROPN'), ('.', 'PUNCT')]
    elif lang == 'jpn':
        if pos_tagger == 'nagisa_jpn':
            assert tokens_tagged == [('日本', '名詞'), ('語', '名詞'), ('(', '補助記号'), ('にほんご', '名詞'), ('、', '補助記号'), ('にっぽん', '名詞'), ('ご', '接尾辞'), ('[', '補助記号'), ('注', '名詞'), ('2', '名詞'), (']', '補助記号'), ('、', '補助記号'), ('英', '名詞'), (':', '補助記号'), ('Japanese', '名詞'), (')', '補助記号'), ('は', '助詞'), ('、', '補助記号'), ('日本', '名詞'), ('国', '接尾辞'), ('内', '接尾辞'), ('や', '助詞'), ('、', '補助記号'), ('かつて', '副詞'), ('の', '助詞'), ('日本', '名詞'), ('領', '接尾辞'), ('だっ', '助動詞'), ('た', '助動詞'), ('国', '名詞'), ('、', '補助記号'), ('そして', '接続詞'), ('日本', '名詞'), ('人', '接尾辞'), ('同士', '接尾辞'), ('の', '助詞'), ('間', '名詞'), ('で', '助詞'), ('使用', '名詞'), ('さ', '動詞'), ('れ', '助動詞'), ('て', '助詞'), ('いる', '動詞'), ('言語', '名詞'), ('。', '補助記号')]
            assert tokens_tagged_universal == [('日本', 'NOUN'), ('語', 'NOUN'), ('(', 'PUNCT/SYM'), ('にほんご', 'NOUN'), ('、', 'PUNCT/SYM'), ('にっぽん', 'NOUN'), ('ご', 'PART'), ('[', 'PUNCT/SYM'), ('注', 'NOUN'), ('2', 'NOUN'), (']', 'PUNCT/SYM'), ('、', 'PUNCT/SYM'), ('英', 'NOUN'), (':', 'PUNCT/SYM'), ('Japanese', 'NOUN'), (')', 'PUNCT/SYM'), ('は', 'PART'), ('、', 'PUNCT/SYM'), ('日本', 'NOUN'), ('国', 'PART'), ('内', 'PART'), ('や', 'PART'), ('、', 'PUNCT/SYM'), ('かつて', 'ADV'), ('の', 'PART'), ('日本', 'NOUN'), ('領', 'PART'), ('だっ', 'AUX'), ('た', 'AUX'), ('国', 'NOUN'), ('、', 'PUNCT/SYM'), ('そして', 'CONJ'), ('日本', 'NOUN'), ('人', 'PART'), ('同士', 'PART'), ('の', 'PART'), ('間', 'NOUN'), ('で', 'PART'), ('使用', 'NOUN'), ('さ', 'VERB'), ('れ', 'AUX'), ('て', 'PART'), ('いる', 'VERB'), ('言語', 'NOUN'), ('。', 'PUNCT/SYM')]
        elif pos_tagger == 'spacy_jpn':
            assert tokens_tagged == [('日本', '名詞-固有名詞-地名-国'), ('語', '名詞-普通名詞-一般'), ('（', '補助記号-括弧開'), ('にほん', '名詞-固有名詞-地名-国'), ('ご', '接尾辞-名詞的-一般'), ('、', '補助記号-読点'), ('にっぽん', '名詞-固有名詞-地名-国'), ('ご', '接尾辞-名詞的-一般'), ('[', '補助記号-括弧開'), ('注', '名詞-普通名詞-一般'), ('2', '名詞-数詞'), (']', '補助記号-括弧閉'), ('、', '補助記号-読点'), ('英', '名詞-普通名詞-一般'), (':', '補助記号-一般'), ('Japanese', '名詞-普通名詞-一般'), ('）', '補助記号-括弧閉'), ('は', '助詞-係助詞'), ('、', '補助記号-読点'), ('日本', '名詞-固有名詞-地名-国'), ('国', '接尾辞-名詞的-一般'), ('内', '接尾辞-名詞的-一般'), ('や', '助詞-副助詞'), ('、', '補助記号-読点'), ('かつて', '副詞'), ('の', '助詞-格助詞'), ('日本', '名詞-固有名詞-地名-国'), ('領', '接尾辞-名詞的-一般'), ('だっ', '助動詞'), ('た', '助動詞'), ('国', '名詞-普通名詞-一般'), ('、', '補助記号-読点'), ('そして', '接続詞'), ('日本', '名詞-固有名詞-地名-国'), ('人', '接尾辞-名詞的-一般'), ('同士', '接尾辞-名詞的-一般'), ('の', '助詞-格助詞'), ('間', '名詞-普通名詞-副詞可能'), ('で', '助詞-格助詞'), ('使用', '名詞-普通名詞-サ変可能'), ('さ', '動詞-非自立可能'), ('れ', '助動詞'), ('て', '助詞-接続助詞'), ('いる', '動詞-非自立可能'), ('言語', '名詞-普通名詞-一般'), ('。', '補助記号-句点')]
            assert tokens_tagged_universal == [('日本', 'PROPN'), ('語', 'NOUN'), ('（', 'NOUN'), ('にほん', 'PROPN'), ('ご', 'NOUN'), ('、', 'PUNCT'), ('にっぽん', 'PROPN'), ('ご', 'NOUN'), ('[', 'PUNCT'), ('注', 'NOUN'), ('2', 'NUM'), (']', 'PUNCT'), ('、', 'PUNCT'), ('英', 'NOUN'), (':', 'SYM'), ('Japanese', 'PROPN'), ('）', 'NOUN'), ('は', 'ADP'), ('、', 'PUNCT'), ('日本', 'PROPN'), ('国', 'NOUN'), ('内', 'NOUN'), ('や', 'ADP'), ('、', 'PUNCT'), ('かつて', 'ADV'), ('の', 'ADP'), ('日本', 'PROPN'), ('領', 'NOUN'), ('だっ', 'AUX'), ('た', 'AUX'), ('国', 'NOUN'), ('、', 'PUNCT'), ('そして', 'CCONJ'), ('日本', 'PROPN'), ('人', 'NOUN'), ('同士', 'NOUN'), ('の', 'ADP'), ('間', 'NOUN'), ('で', 'ADP'), ('使用', 'VERB'), ('さ', 'AUX'), ('れ', 'AUX'), ('て', 'SCONJ'), ('いる', 'VERB'), ('言語', 'NOUN'), ('。', 'PUNCT')]
        elif pos_tagger == 'sudachipy_jpn':
            assert tokens_tagged == [('日本語', '名詞-普通名詞-一般'), ('（', '補助記号-括弧開'), ('にほん', '名詞-固有名詞-地名-国'), ('ご', '接尾辞-名詞的-一般'), ('、', '補助記号-読点'), ('にっぽん', '名詞-固有名詞-地名-国'), ('ご', '接尾辞-名詞的-一般'), ('[', '補助記号-括弧開'), ('注', '名詞-普通名詞-一般'), ('2', '名詞-数詞'), (']', '補助記号-括弧閉'), ('、', '補助記号-読点'), ('英', '名詞-普通名詞-一般'), (':', '補助記号-一般'), ('Japanese', '名詞-普通名詞-一般'), ('）', '補助記号-括弧閉'), ('は', '助詞-係助詞'), ('、', '補助記号-読点'), ('日本', '名詞-固有名詞-地名-国'), ('国', '接尾辞-名詞的-一般'), ('内', '接尾辞-名詞的-一般'), ('や', '助詞-副助詞'), ('、', '補助記号-読点'), ('かつて', '副詞'), ('の', '助詞-格助詞'), ('日本', '名詞-固有名詞-地名-国'), ('領', '接尾辞-名詞的-一般'), ('だっ', '助動詞'), ('た', '助動詞'), ('国', '名詞-普通名詞-一般'), ('、', '補助記号-読点'), ('そして', '接続詞'), ('日本人', '名詞-普通名詞-一般'), ('同士', '接尾辞-名詞的-一般'), ('の', '助詞-格助詞'), ('間', '名詞-普通名詞-副詞可能'), ('で', '助詞-格助詞'), ('使用', '名詞-普通名詞-サ変可能'), ('さ', '動詞-非自立可能'), ('れ', '助動詞'), ('て', '助詞-接続助詞'), ('いる', '動詞-非自立可能'), ('言語', '名詞-普通名詞-一般'), ('。', '補助記号-句点')]
            assert tokens_tagged_universal == [('日本語', 'NOUN'), ('（', 'PUNCT'), ('にほん', 'NOUN'), ('ご', 'PART'), ('、', 'PUNCT'), ('にっぽん', 'NOUN'), ('ご', 'PART'), ('[', 'PUNCT'), ('注', 'NOUN'), ('2', 'NOUN'), (']', 'PUNCT'), ('、', 'PUNCT'), ('英', 'NOUN'), (':', 'SYM'), ('Japanese', 'NOUN'), ('）', 'PUNCT'), ('は', 'PART'), ('、', 'PUNCT'), ('日本', 'NOUN'), ('国', 'PART'), ('内', 'PART'), ('や', 'PART'), ('、', 'PUNCT'), ('かつて', 'ADV'), ('の', 'PART'), ('日本', 'NOUN'), ('領', 'PART'), ('だっ', 'AUX'), ('た', 'AUX'), ('国', 'NOUN'), ('、', 'PUNCT'), ('そして', 'CONJ'), ('日本人', 'NOUN'), ('同士', 'PART'), ('の', 'PART'), ('間', 'NOUN'), ('で', 'PART'), ('使用', 'NOUN'), ('さ', 'VERB'), ('れ', 'AUX'), ('て', 'PART'), ('いる', 'VERB'), ('言語', 'NOUN'), ('。', 'PUNCT')]
        else:
            raise Exception(f'Error: Tests for POS tagger "{pos_tagger}" is skipped!')
    elif lang == 'lit':
        assert tokens_tagged == [('Lietuvių', 'dkt.vyr.dgs.K.'), ('kalba', 'dkt.mot.vns.Įn.'), ('–', 'skyr.'), ('iš', 'prl.K.'), ('baltų', 'vksm.asm.tar.vns.3.'), ('prokalbės', 'dkt.mot.vns.K.'), ('kilusi', 'vksm.dlv.veik.būt-k.mot.vns.V.'), ('lietuvių', 'dkt.vyr.dgs.K.'), ('tautos', 'dkt.mot.vns.K.'), ('kalba', 'dkt.mot.vns.V.'), (',', 'skyr.'), ('kuri', 'įv.mot.vns.V.'), ('Lietuvoje', 'dkt.tikr.mot.vns.Vt.'), ('yra', 'vksm.asm.tiesiog.es.vns.3.'), ('valstybinė', 'bdv.nelygin.mot.vns.V.'), (',', 'skyr.'), ('o', 'jng.'), ('Europos', 'dkt.tikr.mot.vns.K.'), ('Sąjungoje', 'dkt.mot.vns.Vt.'), ('–', 'skyr.'), ('viena', 'įv.mot.vns.V.'), ('iš', 'prl.K.'), ('oficialiųjų', 'vksm.dlv.neveik.es.įvardž.vyr.dgs.K.'), ('kalbų', 'dkt.vyr.dgs.K.'), ('.', 'skyr.')]
        assert tokens_tagged_universal == [('Lietuvių', 'NOUN'), ('kalba', 'NOUN'), ('–', 'PUNCT'), ('iš', 'ADP'), ('baltų', 'ADJ'), ('prokalbės', 'NOUN'), ('kilusi', 'VERB'), ('lietuvių', 'NOUN'), ('tautos', 'NOUN'), ('kalba', 'NOUN'), (',', 'PUNCT'), ('kuri', 'DET'), ('Lietuvoje', 'PROPN'), ('yra', 'AUX'), ('valstybinė', 'ADJ'), (',', 'PUNCT'), ('o', 'CCONJ'), ('Europos', 'PROPN'), ('Sąjungoje', 'NOUN'), ('–', 'PUNCT'), ('viena', 'PRON'), ('iš', 'ADP'), ('oficialiųjų', 'VERB'), ('kalbų', 'NOUN'), ('.', 'PUNCT')]
    elif lang == 'mkd':
        assert tokens_tagged == tokens_tagged_universal == [('Македонски', 'ADJ'), ('јазик', 'NOUN'), ('—', 'PUNCT'), ('јужнословенски', 'ADJ'), ('јазик', 'NOUN'), (',', 'PUNCT'), ('дел', 'NOUN'), ('од', 'ADP'), ('групата', 'NOUN'), ('на', 'ADP'), ('словенски', 'ADJ'), ('јазици', 'NOUN'), ('од', 'ADP'), ('јазичното', 'ADJ'), ('семејство', 'NOUN'), ('на', 'ADP'), ('индоевропски', 'ADJ'), ('јазици', 'NOUN'), ('.', 'NOUN')]
    elif lang == 'nob':
        assert tokens_tagged == tokens_tagged_universal == [('Bokmål', 'NOUN'), ('er', 'AUX'), ('en', 'DET'), ('varietet', 'ADJ'), ('av', 'ADP'), ('norsk', 'ADJ'), ('språk', 'NOUN'), ('.', 'PUNCT')]
    elif lang == 'pol':
        assert tokens_tagged == [('Język', 'SUBST'), ('polski', 'ADJ'), (',', 'INTERP'), ('polszczyzna', 'SUBST'), ('–', 'INTERP'), ('język', 'SUBST'), ('lechicki', 'ADJ'), ('z', 'PREP'), ('grupy', 'SUBST'), ('zachodniosłowiańskiej', 'ADJ'), ('(', 'INTERP'), ('do', 'PREP'), ('której', 'ADJ'), ('należą', 'FIN'), ('również', 'QUB'), ('czeski', 'SUBST'), (',', 'SUBST'), ('kaszubski', 'SUBST'), (',', 'INTERP'), ('słowacki', 'SUBST'), ('i', 'CONJ'), ('języki', 'SUBST'), ('łużyckie', 'SUBST'), (')', 'SUBST'), (',', 'INTERP'), ('stanowiącej', 'PACT'), ('część', 'SUBST'), ('rodziny', 'SUBST'), ('indoeuropejskiej', 'SUBST'), ('.', 'SUBST')]
        assert tokens_tagged_universal == [('Język', 'NOUN'), ('polski', 'ADJ'), (',', 'PUNCT'), ('polszczyzna', 'ADJ'), ('–', 'PUNCT'), ('język', 'NOUN'), ('lechicki', 'ADJ'), ('z', 'ADP'), ('grupy', 'NOUN'), ('zachodniosłowiańskiej', 'ADJ'), ('(', 'PUNCT'), ('do', 'ADP'), ('której', 'DET'), ('należą', 'VERB'), ('również', 'PART'), ('czeski', 'ADJ'), (',', 'PUNCT'), ('kaszubski', 'PROPN'), (',', 'PUNCT'), ('słowacki', 'ADJ'), ('i', 'CCONJ'), ('języki', 'NOUN'), ('łużyckie', 'ADJ'), (')', 'PUNCT'), (',', 'PUNCT'), ('stanowiącej', 'ADJ'), ('część', 'NOUN'), ('rodziny', 'NOUN'), ('indoeuropejskiej', 'ADJ'), ('.', 'PUNCT')]
    elif lang in ['por_br', 'por_pt']:
        assert tokens_tagged == tokens_tagged_universal == [('A', 'DET'), ('língua', 'NOUN'), ('portuguesa', 'ADJ'), (',', 'PUNCT'), ('também', 'ADV'), ('designada', 'VERB'), ('português', 'ADJ'), (',', 'PUNCT'), ('é', 'AUX'), ('uma', 'DET'), ('língua', 'NOUN'), ('românica', 'ADJ'), ('flexiva', 'ADJ'), ('ocidental', 'ADJ'), ('originada', 'VERB'), ('no', 'ADP'), ('galego-português', 'NOUN'), ('falado', 'VERB'), ('no', 'ADP'), ('Reino', 'PROPN'), ('da', 'ADP'), ('Galiza', 'PROPN'), ('e', 'CCONJ'), ('no', 'ADP'), ('norte', 'NOUN'), ('de', 'ADP'), ('Portugal', 'PROPN'), ('.', 'PUNCT')]
    elif lang == 'ron':
        assert tokens_tagged == [('Limba', 'Ncfsry'), ('română', 'Afpfsrn'), ('este', 'Vaip3s'), ('o', 'Tifsr'), ('limbă', 'Ncfsrn'), ('indo-europeană', 'Afpfsrn'), (',', 'COMMA'), ('din', 'Spsa'), ('grupul', 'Ncmsry'), ('italic', 'Afpms-n'), ('și', 'Crssp'), ('din', 'Spsa'), ('subgrupul', 'Ncmsry'), ('oriental', 'Afpms-n'), ('al', 'Tsms'), ('limbilor', 'Ncfpoy'), ('romanice', 'Afpfp-n'), ('.', 'PERIOD')]
        assert tokens_tagged_universal == [('Limba', 'NOUN'), ('română', 'ADJ'), ('este', 'AUX'), ('o', 'DET'), ('limbă', 'NOUN'), ('indo-europeană', 'ADJ'), (',', 'PUNCT'), ('din', 'ADP'), ('grupul', 'NOUN'), ('italic', 'ADJ'), ('și', 'CCONJ'), ('din', 'ADP'), ('subgrupul', 'NOUN'), ('oriental', 'ADJ'), ('al', 'DET'), ('limbilor', 'NOUN'), ('romanice', 'ADJ'), ('.', 'PUNCT')]
    elif lang == 'rus':
        if pos_tagger == 'nltk_perceptron':
            assert tokens_tagged == [('Ру́сский', 'A=m'), ('язы́к', 'S'), ('(', 'NONLEX'), ('[', 'NONLEX'), ('ˈruskʲɪi̯', 'NONLEX'), ('jɪˈzɨk', 'NONLEX'), (']', 'NONLEX'), ('Информация', 'S'), ('о', 'PR'), ('файле', 'S'), ('слушать)[~', 'S'), ('3', 'NUM=ciph'), (']', 'NONLEX'), ('[', 'NONLEX'), ('⇨', 'NONLEX'), (']', 'NONLEX'), ('—', 'NONLEX'), ('один', 'A-PRO=m'), ('из', 'PR'), ('восточнославянских', 'A=pl'), ('языков', 'S'), (',', 'NONLEX'), ('национальный', 'A=m'), ('язык', 'S'), ('русского', 'A=m'), ('народа', 'S'), ('.', 'NONLEX')]
            assert tokens_tagged_universal == [('Ру́сский', 'ADJ'), ('язы́к', 'NOUN'), ('(', 'PUNCT'), ('[', 'PUNCT'), ('ˈruskʲɪi̯', 'PUNCT'), ('jɪˈzɨk', 'PUNCT'), (']', 'PUNCT'), ('Информация', 'NOUN'), ('о', 'ADP'), ('файле', 'NOUN'), ('слушать)[~', 'NOUN'), ('3', 'NUM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('⇨', 'PUNCT'), (']', 'PUNCT'), ('—', 'PUNCT'), ('один', 'PRON'), ('из', 'ADP'), ('восточнославянских', 'ADJ'), ('языков', 'NOUN'), (',', 'PUNCT'), ('национальный', 'ADJ'), ('язык', 'NOUN'), ('русского', 'ADJ'), ('народа', 'NOUN'), ('.', 'PUNCT')]
        elif pos_tagger == 'pymorphy2_morphological_analyzer':
            assert tokens_tagged == [('Ру́сский', 'NOUN'), ('язы́к', 'NOUN'), ('(', 'PNCT'), ('[', 'PNCT'), ('ˈruskʲɪi̯', 'UNKN'), ('jɪˈzɨk', 'UNKN'), (']', 'PNCT'), ('Информация', 'NOUN'), ('о', 'PREP'), ('файле', 'NOUN'), ('слушать)[~', 'UNKN'), ('3', 'NUMB'), (']', 'PNCT'), ('[', 'PNCT'), ('⇨', 'UNKN'), (']', 'PNCT'), ('—', 'PNCT'), ('один', 'ADJF'), ('из', 'PREP'), ('восточнославянских', 'ADJF'), ('языков', 'NOUN'), (',', 'PNCT'), ('национальный', 'ADJF'), ('язык', 'NOUN'), ('русского', 'ADJF'), ('народа', 'NOUN'), ('.', 'PNCT')]
            assert tokens_tagged_universal == [('Ру́сский', 'NOUN'), ('язы́к', 'NOUN'), ('(', 'PUNCT'), ('[', 'PUNCT'), ('ˈruskʲɪi̯', 'SYM/X'), ('jɪˈzɨk', 'SYM/X'), (']', 'PUNCT'), ('Информация', 'NOUN'), ('о', 'ADP'), ('файле', 'NOUN'), ('слушать)[~', 'SYM/X'), ('3', 'NUM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('⇨', 'SYM/X'), (']', 'PUNCT'), ('—', 'PUNCT'), ('один', 'ADJ'), ('из', 'ADP'), ('восточнославянских', 'ADJ'), ('языков', 'NOUN'), (',', 'PUNCT'), ('национальный', 'ADJ'), ('язык', 'NOUN'), ('русского', 'ADJ'), ('народа', 'NOUN'), ('.', 'PUNCT')]
        elif pos_tagger == 'spacy_rus':
            assert tokens_tagged == tokens_tagged_universal == [('Ру́сский', 'ADJ'), ('язы́к', 'NOUN'), ('(', 'PUNCT'), ('[', 'PUNCT'), ('ˈruskʲɪi̯', 'X'), ('jɪˈzɨk', 'X'), (']', 'PUNCT'), ('Информация', 'NOUN'), ('о', 'ADP'), ('файле', 'NOUN'), ('слушать)[~', 'PROPN'), ('3', 'NUM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('⇨', 'VERB'), (']', 'PUNCT'), ('—', 'PUNCT'), ('один', 'NUM'), ('из', 'ADP'), ('восточнославянских', 'ADJ'), ('языков', 'NOUN'), (',', 'PUNCT'), ('национальный', 'ADJ'), ('язык', 'NOUN'), ('русского', 'ADJ'), ('народа', 'NOUN'), ('.', 'PUNCT')]
        else:
            raise Exception(f'Error: Tests for POS tagger "{pos_tagger}" is skipped!')
    elif lang == 'spa':
        assert tokens_tagged == tokens_tagged_universal == [('El', 'DET'), ('español', 'NOUN'), ('o', 'CCONJ'), ('castellano', 'NOUN'), ('es', 'AUX'), ('una', 'DET'), ('lengua', 'NOUN'), ('romance', 'NOUN'), ('procedente', 'ADJ'), ('del', 'ADP'), ('latín', 'NOUN'), ('hablado', 'ADJ'), (',', 'PUNCT'), ('perteneciente', 'ADJ'), ('a', 'ADP'), ('la', 'DET'), ('familia', 'NOUN'), ('de', 'ADP'), ('lenguas', 'NOUN'), ('indoeuropeas', 'ADJ'), ('.', 'PUNCT')]
    elif lang == 'tha':
        if pos_tagger == 'pythainlp_perceptron_lst20':
            assert tokens_tagged == [('ภาษาไทย', 'NN'), ('หรือ', 'CC'), ('ภาษาไทย', 'NN'), ('กลาง', 'NN'), ('เป็น', 'VV'), ('ภาษาราชการ', 'NN'), ('และ', 'CC'), ('ภาษาประจำชาติ', 'NN'), ('ของ', 'PS'), ('ประเทศ', 'NN'), ('ไทย', 'NN')]
            assert tokens_tagged_universal == [('ภาษาไทย', 'NOUN'), ('หรือ', 'CCONJ'), ('ภาษาไทย', 'NOUN'), ('กลาง', 'NOUN'), ('เป็น', 'VERB'), ('ภาษาราชการ', 'NOUN'), ('และ', 'CCONJ'), ('ภาษาประจำชาติ', 'NOUN'), ('ของ', 'ADP'), ('ประเทศ', 'NOUN'), ('ไทย', 'NOUN')]
        elif pos_tagger == 'pythainlp_perceptron_orchid':
            assert tokens_tagged == [('ภาษาไทย', 'NPRP'), ('หรือ', 'JCRG'), ('ภาษาไทย', 'NPRP'), ('กลาง', 'VATT'), ('เป็น', 'VSTA'), ('ภาษาราชการ', 'NCMN'), ('และ', 'JCRG'), ('ภาษาประจำชาติ', 'NCMN'), ('ของ', 'RPRE'), ('ประเทศ', 'NCMN'), ('ไทย', 'NPRP')]
            assert tokens_tagged_universal == [('ภาษาไทย', 'PROPN'), ('หรือ', 'CCONJ'), ('ภาษาไทย', 'PROPN'), ('กลาง', 'ADJ'), ('เป็น', 'VERB'), ('ภาษาราชการ', 'NOUN'), ('และ', 'CCONJ'), ('ภาษาประจำชาติ', 'NOUN'), ('ของ', 'ADP'), ('ประเทศ', 'NOUN'), ('ไทย', 'PROPN')]
        elif pos_tagger == 'pythainlp_perceptron_pud':
            assert tokens_tagged == tokens_tagged_universal == [('ภาษาไทย', 'NOUN'), ('หรือ', 'CCONJ'), ('ภาษาไทย', 'NOUN'), ('กลาง', 'NOUN'), ('เป็น', 'AUX'), ('ภาษาราชการ', 'NOUN'), ('และ', 'CCONJ'), ('ภาษาประจำชาติ', 'NOUN'), ('ของ', 'ADP'), ('ประเทศ', 'NOUN'), ('ไทย', 'PROPN')]
        else:
            raise Exception(f'Error: Tests for POS tagger "{pos_tagger}" is skipped!')
    elif lang == 'bod':
        assert tokens_tagged == [('བོད་', 'PROPN'), ('ཀྱི་', 'PART'), ('སྐད་ཡིག་', 'NOUN'), ('ནི་', 'NO_POS'), ('བོད་ཡུལ་', 'PROPN'), ('དང་', 'NO_POS'), ('དེ', 'DET'), ('འི་', 'PART'), ('ཉེ་འཁོར་', 'NOUN'), ('གྱི་', 'PART'), ('ས་ཁུལ་', 'OTHER'), ('ཏེ', 'PART'), ('།', 'PUNCT')]
        assert tokens_tagged_universal == [('བོད་', 'PROPN'), ('ཀྱི་', 'PART'), ('སྐད་ཡིག་', 'NOUN'), ('ནི་', 'X'), ('བོད་ཡུལ་', 'PROPN'), ('དང་', 'X'), ('དེ', 'DET'), ('འི་', 'PART'), ('ཉེ་འཁོར་', 'NOUN'), ('གྱི་', 'PART'), ('ས་ཁུལ་', 'X'), ('ཏེ', 'PART'), ('།', 'PUNCT')]
    elif lang == 'ukr':
        assert tokens_tagged == [('Украї́нська', 'ADJF'), ('мо́ва', 'ADJF'), ('(', 'PNCT'), ('МФА', 'UNKN'), (':', 'PNCT'), ('[', 'PNCT'), ('ukrɑ̽ˈjɪnʲsʲkɑ̽', 'UNKN'), ('ˈmɔwɑ̽', 'UNKN'), (']', 'PNCT'), (',', 'PNCT'), ('історичні', 'ADJF'), ('назви', 'NOUN'), ('—', 'PNCT'), ('ру́ська', 'ADJF'), (',', 'PNCT'), ('руси́нська[9][10][11', 'UNKN'), (']', 'PNCT'), ('[', 'PNCT'), ('*', 'PNCT'), ('2', 'NUMB'), (']', 'PNCT'), (')', 'PNCT'), ('—', 'PNCT'), ('національна', 'ADJF'), ('мова', 'NOUN'), ('українців', 'NOUN'), ('.', 'PNCT')]
        assert tokens_tagged_universal == [('Украї́нська', 'ADJ'), ('мо́ва', 'ADJ'), ('(', 'PUNCT'), ('МФА', 'SYM/X'), (':', 'PUNCT'), ('[', 'PUNCT'), ('ukrɑ̽ˈjɪnʲsʲkɑ̽', 'SYM/X'), ('ˈmɔwɑ̽', 'SYM/X'), (']', 'PUNCT'), (',', 'PUNCT'), ('історичні', 'ADJ'), ('назви', 'NOUN'), ('—', 'PUNCT'), ('ру́ська', 'ADJ'), (',', 'PUNCT'), ('руси́нська[9][10][11', 'SYM/X'), (']', 'PUNCT'), ('[', 'PUNCT'), ('*', 'PUNCT'), ('2', 'NUM'), (']', 'PUNCT'), (')', 'PUNCT'), ('—', 'PUNCT'), ('національна', 'ADJ'), ('мова', 'NOUN'), ('українців', 'NOUN'), ('.', 'PUNCT')]
    elif lang == 'vie':
        assert tokens_tagged == [('Tiếng', 'N'), ('Việt', 'Np'), (',', 'CH'), ('cũng', 'R'), ('gọi là', 'X'), ('tiếng', 'N'), ('Việt Nam', 'Np'), ('[', 'V'), ('5 ]', 'N'), ('hay', 'C'), ('Việt ngữ', 'V'), ('là', 'V'), ('ngôn ngữ', 'N'), ('của', 'E'), ('người', 'Nc'), ('Việt', 'Np'), ('và', 'C'), ('là', 'V'), ('ngôn ngữ', 'N'), ('chính thức', 'A'), ('tại', 'E'), ('Việt Nam', 'Np'), ('.', 'CH')]
        assert tokens_tagged_universal == [('Tiếng', 'NOUN'), ('Việt', 'PROPN'), (',', 'PUNCT'), ('cũng', 'X'), ('gọi là', 'X'), ('tiếng', 'NOUN'), ('Việt Nam', 'PROPN'), ('[', 'VERB'), ('5 ]', 'NOUN'), ('hay', 'CCONJ'), ('Việt ngữ', 'VERB'), ('là', 'VERB'), ('ngôn ngữ', 'NOUN'), ('của', 'ADP'), ('người', 'NOUN'), ('Việt', 'PROPN'), ('và', 'CCONJ'), ('là', 'VERB'), ('ngôn ngữ', 'NOUN'), ('chính thức', 'ADJ'), ('tại', 'ADP'), ('Việt Nam', 'PROPN'), ('.', 'PUNCT')]
    else:
        raise Exception(f'Error: Tests for language "{lang}" is skipped!')

if __name__ == '__main__':
    for lang, pos_tagger in test_pos_taggers:
        test_pos_tag(lang, pos_tagger)
