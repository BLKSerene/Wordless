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

from tests import wl_test_init, wl_test_lang_examples
from wordless.wl_nlp import wl_pos_tagging, wl_word_tokenization

main = wl_test_init.Wl_Test_Main()

test_pos_taggers = []

for lang, pos_taggers in main.settings_global['pos_taggers'].items():
    for pos_tagger in pos_taggers:
        test_pos_taggers.append((lang, pos_tagger))

@pytest.mark.parametrize('lang, pos_tagger', test_pos_taggers)
def test_pos_tag(lang, pos_tagger):
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

    tokens_tagged_long_text_tokenized = wl_pos_tagging.wl_pos_tag(
        main,
        inputs = [str(i) for i in range(101) for j in range(50)],
        lang = lang,
        pos_tagger = pos_tagger
    )

    print(f'{lang} / {pos_tagger}:')
    print(tokens_tagged)
    print(f'{tokens_tagged_universal}\n')

    # Check for empty tags
    assert all((tag for token, tag in tokens_tagged))
    assert all((tag for token, tag in tokens_tagged_universal))
    assert all((tag for token, tag in tokens_tagged_tokenized))
    assert all((tag for token, tag in tokens_tagged_universal_tokenized))
    # Universal tags should not all be "X"
    assert any((tag for token, tag in tokens_tagged_universal if tag != 'X'))
    assert any((tag for token, tag in tokens_tagged_universal_tokenized if tag != 'X'))

    # Tokenization should not be modified
    assert len(tokens) == len(tokens_tagged_tokenized) == len(tokens_tagged_universal_tokenized)

    # Test long texts
    assert [token[0] for token in tokens_tagged_long_text_tokenized] == [str(i) for i in range(101) for j in range(50)]

    if lang == 'cat':
        assert tokens_tagged == tokens_tagged_universal == [('El', 'DET'), ('català', 'NOUN'), ('(', 'PUNCT'), ('denominació', 'NOUN'), ('oficial', 'ADJ'), ('a', 'ADP'), ('Catalunya', 'PROPN'), (',', 'PUNCT'), ('a', 'ADP'), ('les', 'DET'), ('Illes', 'PROPN'), ('Balears', 'PROPN'), (',', 'PUNCT'), ('a', 'ADP'), ('Andorra', 'PROPN'), (',', 'PUNCT'), ('a', 'ADP'), ('la', 'DET'), ('ciutat', 'NOUN'), ('de', 'ADP'), ("l'", 'DET'), ('Alguer', 'PROPN'), ('i', 'CCONJ'), ('tradicional', 'ADJ'), ('a', 'ADP'), ('Catalunya', 'PROPN'), ('d', 'ADP'), ('el', 'DET'), ('Nord', 'PROPN'), (')', 'PUNCT'), ('o', 'CCONJ'), ('valencià', 'PROPN'), ('(', 'PUNCT'), ('denominació', 'NOUN'), ('oficial', 'ADJ'), ('a', 'ADP'), ('l', 'DET'), ('País', 'PROPN'), ('Valencià', 'PROPN'), ('i', 'CCONJ'), ('tradicional', 'ADJ'), ('a', 'ADP'), ('l', 'DET'), ('Carxe', 'PROPN'), (')', 'PUNCT'), ('és', 'AUX'), ('una', 'DET'), ('llengua', 'NOUN'), ('romànica', 'ADJ'), ('parlada', 'ADJ'), ('a', 'ADP'), ('Catalunya', 'PROPN'), (',', 'PUNCT'), ('el', 'DET'), ('País', 'PROPN'), ('Valencià', 'PROPN'), ('(', 'PUNCT'), ('tret', 'NOUN'), ("d'", 'ADP'), ('algunes', 'DET'), ('comarques', 'NOUN'), ('i', 'CCONJ'), ('localitats', 'NOUN'), ('de', 'ADP'), ("l'", 'DET'), ('interior', 'NOUN'), (')', 'PUNCT'), (',', 'PUNCT'), ('les', 'DET'), ('Illes', 'PROPN'), ('Balears', 'PROPN'), (',', 'PUNCT'), ('Andorra', 'PROPN'), (',', 'PUNCT'), ('la', 'DET'), ('Franja', 'PROPN'), ('de', 'ADP'), ('Ponent', 'PROPN'), ('(', 'PUNCT'), ('a', 'ADP'), ("l'", 'DET'), ('Aragó', 'PROPN'), (')', 'PUNCT'), (',', 'PUNCT'), ('la', 'DET'), ('ciutat', 'NOUN'), ('de', 'ADP'), ("l'", 'DET'), ('Alguer', 'PROPN'), ('(', 'PUNCT'), ('a', 'ADP'), ("l'", 'DET'), ('illa', 'NOUN'), ('de', 'ADP'), ('Sardenya', 'PROPN'), (')', 'PUNCT'), (',', 'PUNCT'), ('la', 'DET'), ('Catalunya', 'PROPN'), ('d', 'ADP'), ('el', 'DET'), ('Nord,[8', 'PROPN'), (']', 'PUNCT'), ('el', 'DET'), ('Carxe', 'PROPN'), ('(', 'PUNCT'), ('un', 'DET'), ('petit', 'ADJ'), ('territori', 'NOUN'), ('de', 'ADP'), ('Múrcia', 'PROPN'), ('poblat', 'ADJ'), ('per', 'ADP'), ('pobladors', 'NOUN'), ('valencians),[9][10', 'PROPN'), (']', 'PUNCT'), ('i', 'CCONJ'), ('en', 'ADP'), ('comunitats', 'NOUN'), ('arreu', 'ADV'), ('d', 'ADP'), ('el', 'DET'), ('món', 'NOUN'), ('(', 'PUNCT'), ('entre', 'ADP'), ('les', 'DET'), ('quals', 'PRON'), ('destaca', 'VERB'), ('la', 'DET'), ('de', 'ADP'), ("l'", 'DET'), ('Argentina', 'PROPN'), (',', 'PUNCT'), ('amb', 'ADP'), ('200.000', 'NUM'), ('parlants).[11', 'NOUN'), (']', 'PUNCT')]
    elif lang == 'zho_cn':
        if pos_tagger == 'jieba_zho':
            assert tokens_tagged == [('汉语', 'nz'), ('又称', 'n'), ('华语', 'nz'), ('[', 'x'), ('3', 'x'), (']', 'x'), ('、', 'x'), ('唐', 'nr'), ('话', 'n'), ('[', 'x'), ('4', 'x'), (']', 'x'), ('，', 'x'), ('概指', 'n'), ('由', 'p'), ('上', 'f'), ('古汉语', 'nr'), ('（', 'x'), ('先秦', 't'), ('雅言', 'nr'), ('）', 'x'), ('发展', 'vn'), ('而', 'c'), ('来', 'v'), ('、', 'x'), ('书面', 'n'), ('使用', 'v'), ('汉字', 'nz'), ('的', 'uj'), ('分析语', 'n'), ('，', 'x'), ('为', 'p'), ('汉藏语系', 'nz'), ('最大', 'a'), ('的', 'uj'), ('一支', 'm'), ('语族', 'n'), ('。', 'x')]
            assert tokens_tagged_universal == [('汉语', 'PROPN'), ('又称', 'NOUN'), ('华语', 'PROPN'), ('[', 'PUNCT/SYM'), ('3', 'PUNCT/SYM'), (']', 'PUNCT/SYM'), ('、', 'PUNCT/SYM'), ('唐', 'PRONP'), ('话', 'NOUN'), ('[', 'PUNCT/SYM'), ('4', 'PUNCT/SYM'), (']', 'PUNCT/SYM'), ('，', 'PUNCT/SYM'), ('概指', 'NOUN'), ('由', 'ADP'), ('上', 'ADP'), ('古汉语', 'PRONP'), ('（', 'PUNCT/SYM'), ('先秦', 'NOUN'), ('雅言', 'PRONP'), ('）', 'PUNCT/SYM'), ('发展', 'VERB'), ('而', 'CONJ'), ('来', 'VERB'), ('、', 'PUNCT/SYM'), ('书面', 'NOUN'), ('使用', 'VERB'), ('汉字', 'PROPN'), ('的', 'PART'), ('分析语', 'NOUN'), ('，', 'PUNCT/SYM'), ('为', 'ADP'), ('汉藏语系', 'PROPN'), ('最大', 'ADJ'), ('的', 'PART'), ('一支', 'NUM'), ('语族', 'NOUN'), ('。', 'PUNCT/SYM')]
        elif pos_tagger == 'spacy_zho':
            assert tokens_tagged == [('汉语', 'NN'), ('又', 'AD'), ('称', 'VV'), ('华语', 'NN'), ('[3', 'PU'), (']', 'NR'), ('、', 'PU'), ('唐话', 'NR'), ('[', 'NR'), ('4', 'CD'), (']', 'NN'), ('，', 'PU'), ('概指', 'VV'), ('由', 'P'), ('上古', 'NT'), ('汉语', 'NN'), ('（', 'PU'), ('先', 'AD'), ('秦雅言', 'NR'), ('）', 'PU'), ('发展', 'VV'), ('而', 'MSP'), ('来', 'VV'), ('、', 'PU'), ('书面', 'AD'), ('使用', 'VV'), ('汉字', 'NN'), ('的', 'DEG'), ('分析语', 'NN'), ('，', 'PU'), ('为', 'P'), ('汉藏', 'NR'), ('语系', 'NN'), ('最', 'AD'), ('大', 'VA'), ('的', 'DEC'), ('一', 'CD'), ('支', 'M'), ('语族', 'NN'), ('。', 'PU')]
            assert tokens_tagged_universal == [('汉语', 'NOUN'), ('又', 'ADV'), ('称', 'VERB'), ('华语', 'NOUN'), ('[3', 'PUNCT'), (']', 'PROPN'), ('、', 'PUNCT'), ('唐话', 'PROPN'), ('[', 'PROPN'), ('4', 'NUM'), (']', 'NOUN'), ('，', 'PUNCT'), ('概指', 'VERB'), ('由', 'ADP'), ('上古', 'NOUN'), ('汉语', 'NOUN'), ('（', 'PUNCT'), ('先', 'ADV'), ('秦雅言', 'PROPN'), ('）', 'PUNCT'), ('发展', 'VERB'), ('而', 'PART'), ('来', 'VERB'), ('、', 'PUNCT'), ('书面', 'ADV'), ('使用', 'VERB'), ('汉字', 'NOUN'), ('的', 'PART'), ('分析语', 'NOUN'), ('，', 'PUNCT'), ('为', 'ADP'), ('汉藏', 'PROPN'), ('语系', 'NOUN'), ('最', 'ADV'), ('大', 'VERB'), ('的', 'PART'), ('一', 'NUM'), ('支', 'NUM'), ('语族', 'NOUN'), ('。', 'PUNCT')]
        else:
            raise Exception(f'Error: Tests for POS tagger "{pos_tagger}" is skipped!')
    elif lang == 'zho_tw':
        if pos_tagger == 'jieba_zho':
            assert tokens_tagged == [('漢語', 'nz'), ('又', 'd'), ('稱', 'v'), ('華語', 'nz'), ('[', 'x'), ('3', 'x'), (']', 'x'), ('、', 'x'), ('唐', 'nr'), ('話', 'n'), ('[', 'x'), ('4', 'x'), (']', 'x'), ('，', 'x'), ('概指', 'n'), ('由', 'p'), ('上古', 'ns'), ('漢語', 'nz'), ('（', 'x'), ('先秦', 't'), ('雅言', 'nr'), ('）', 'x'), ('發展', 'vn'), ('而', 'c'), ('來', 'v'), ('、', 'x'), ('書面', 'n'), ('使用', 'v'), ('漢字', 'nz'), ('的', 'uj'), ('分析', 'vn'), ('語', 'x'), ('，', 'x'), ('為', 'p'), ('漢藏語', 'nz'), ('系', 'n'), ('最大', 'a'), ('的', 'uj'), ('一支', 'm'), ('語族', 'n'), ('。', 'x')]
            assert tokens_tagged_universal == [('漢語', 'PROPN'), ('又', 'ADV'), ('稱', 'VERB'), ('華語', 'PROPN'), ('[', 'PUNCT/SYM'), ('3', 'PUNCT/SYM'), (']', 'PUNCT/SYM'), ('、', 'PUNCT/SYM'), ('唐', 'PRONP'), ('話', 'NOUN'), ('[', 'PUNCT/SYM'), ('4', 'PUNCT/SYM'), (']', 'PUNCT/SYM'), ('，', 'PUNCT/SYM'), ('概指', 'NOUN'), ('由', 'ADP'), ('上古', 'PROPN'), ('漢語', 'PROPN'), ('（', 'PUNCT/SYM'), ('先秦', 'NOUN'), ('雅言', 'PRONP'), ('）', 'PUNCT/SYM'), ('發展', 'VERB'), ('而', 'CONJ'), ('來', 'VERB'), ('、', 'PUNCT/SYM'), ('書面', 'NOUN'), ('使用', 'VERB'), ('漢字', 'PROPN'), ('的', 'PART'), ('分析', 'VERB'), ('語', 'PUNCT/SYM'), ('，', 'PUNCT/SYM'), ('為', 'ADP'), ('漢藏語', 'PROPN'), ('系', 'NOUN'), ('最大', 'ADJ'), ('的', 'PART'), ('一支', 'NUM'), ('語族', 'NOUN'), ('。', 'PUNCT/SYM')]
        elif pos_tagger == 'spacy_zho':
            assert tokens_tagged == [('漢語', 'NN'), ('又', 'AD'), ('稱華', 'VV'), ('語[', 'CD'), ('3', 'CD'), (']', 'NN'), ('、', 'PU'), ('唐話[', 'NR'), ('4', 'CD'), (']', 'NN'), ('，', 'PU'), ('概指', 'VV'), ('由', 'P'), ('上古', 'NT'), ('漢語', 'NN'), ('（', 'PU'), ('先', 'AD'), ('秦雅言', 'NR'), ('）', 'PU'), ('發展', 'NN'), ('而', 'CC'), ('來', 'VV'), ('、', 'PU'), ('書面', 'NN'), ('使用', 'VV'), ('漢字', 'NN'), ('的', 'DEC'), ('分析語', 'NN'), ('，', 'PU'), ('為漢', 'NN'), ('藏語', 'NR'), ('系', 'NN'), ('最', 'AD'), ('大', 'VA'), ('的', 'DEC'), ('一', 'CD'), ('支', 'M'), ('語族', 'NN'), ('。', 'PU')]
            assert tokens_tagged_universal == [('漢語', 'NOUN'), ('又', 'ADV'), ('稱華', 'VERB'), ('語[', 'NUM'), ('3', 'NUM'), (']', 'NOUN'), ('、', 'PUNCT'), ('唐話[', 'PROPN'), ('4', 'NUM'), (']', 'NOUN'), ('，', 'PUNCT'), ('概指', 'VERB'), ('由', 'ADP'), ('上古', 'NOUN'), ('漢語', 'NOUN'), ('（', 'PUNCT'), ('先', 'ADV'), ('秦雅言', 'PROPN'), ('）', 'PUNCT'), ('發展', 'NOUN'), ('而', 'CCONJ'), ('來', 'VERB'), ('、', 'PUNCT'), ('書面', 'NOUN'), ('使用', 'VERB'), ('漢字', 'NOUN'), ('的', 'PART'), ('分析語', 'NOUN'), ('，', 'PUNCT'), ('為漢', 'NOUN'), ('藏語', 'PROPN'), ('系', 'NOUN'), ('最', 'ADV'), ('大', 'VERB'), ('的', 'PART'), ('一', 'NUM'), ('支', 'NUM'), ('語族', 'NOUN'), ('。', 'PUNCT')]
        else:
            raise Exception(f'Error: Tests for POS tagger "{pos_tagger}" is skipped!')
    elif lang == 'hrv':
        assert tokens_tagged == [('Hrvatski', 'Agpmsny'), ('jezik', 'Ncmsn'), ('(', 'Z'), ('ISO', 'Npmsn'), ('639', 'Mdc'), ('-', 'Npmsg'), ('3', 'Mdc'), (':', 'Z'), ('hrv', 'Xf'), ('Inačica', 'Ncfsn'), ('izvorne', 'Agpfsgy'), ('stranice', 'Ncfsg'), ('arhivirana', 'Agpfsny'), ('18', 'Mdo'), ('.', 'Mdo'), ('rujna', 'Ncmsg'), ('2012', 'Mdo'), ('.', 'Mdo'), (')', 'Z'), ('skupni', 'Agpmsny'), ('je', 'Var3s'), ('naziv', 'Ncmsn'), ('za', 'Sa'), ('nacionalni', 'Agpmsayn'), ('standardni', 'Agpmsayn'), ('jezik', 'Ncmsan'), ('Hrvata', 'Npmpg'), (',', 'Z'), ('te', 'Cc'), ('za', 'Sa'), ('skup', 'Ncmsan'), ('narječja', 'Ncnsg'), ('i', 'Cc'), ('govora', 'Ncmsg'), ('kojima', 'Pi-mpd'), ('govore', 'Vmr3p'), ('ili', 'Cc'), ('su', 'Var3p'), ('nekada', 'Rgp'), ('govorili', 'Vmp-pm'), ('Hrvati', 'Npmpn'), ('.', 'Z')]
        assert tokens_tagged_universal == [('Hrvatski', 'ADJ'), ('jezik', 'NOUN'), ('(', 'PUNCT'), ('ISO', 'PROPN'), ('639', 'NUM'), ('-', 'PROPN'), ('3', 'NUM'), (':', 'PUNCT'), ('hrv', 'X'), ('Inačica', 'NOUN'), ('izvorne', 'ADJ'), ('stranice', 'NOUN'), ('arhivirana', 'ADJ'), ('18', 'ADJ'), ('.', 'ADJ'), ('rujna', 'NOUN'), ('2012', 'ADJ'), ('.', 'ADJ'), (')', 'PUNCT'), ('skupni', 'ADJ'), ('je', 'AUX'), ('naziv', 'NOUN'), ('za', 'ADP'), ('nacionalni', 'ADJ'), ('standardni', 'ADJ'), ('jezik', 'NOUN'), ('Hrvata', 'PROPN'), (',', 'PUNCT'), ('te', 'CCONJ'), ('za', 'ADP'), ('skup', 'NOUN'), ('narječja', 'NOUN'), ('i', 'CCONJ'), ('govora', 'NOUN'), ('kojima', 'DET'), ('govore', 'VERB'), ('ili', 'CCONJ'), ('su', 'AUX'), ('nekada', 'ADV'), ('govorili', 'VERB'), ('Hrvati', 'PROPN'), ('.', 'PUNCT')]
    elif lang == 'dan':
        assert tokens_tagged == tokens_tagged_universal == [('Dansk', 'ADJ'), ('er', 'AUX'), ('et', 'DET'), ('østnordisk', 'ADJ'), ('sprog', 'NOUN'), ('indenfor', 'ADP'), ('den', 'DET'), ('germanske', 'ADJ'), ('gren', 'NOUN'), ('af', 'ADP'), ('den', 'DET'), ('indoeuropæiske', 'ADJ'), ('sprogfamilie', 'NOUN'), ('.', 'PUNCT')]
    elif lang == 'nld':
        assert tokens_tagged == [('Het', 'LID|bep|stan|evon'), ('Nederlands', 'N|eigen|ev|basis|onz|stan'), ('is', 'WW|pv|tgw|ev'), ('een', 'LID|onbep|stan|agr'), ('West-Germaanse', 'ADJ|prenom|basis|met-e|stan'), ('taal', 'N|soort|ev|basis|zijd|stan'), ('en', 'VG|neven'), ('de', 'LID|bep|stan|rest'), ('officiële', 'ADJ|prenom|basis|met-e|stan'), ('taal', 'N|soort|ev|basis|zijd|stan'), ('van', 'VZ|init'), ('Nederland', 'N|eigen|ev|basis|onz|stan'), (',', 'LET'), ('Suriname', 'N|eigen|ev|basis|onz|stan'), ('en', 'VG|neven'), ('een', 'TW|hoofd|nom|zonder-n|basis'), ('van', 'VZ|init'), ('de', 'LID|bep|stan|rest'), ('drie', 'TW|hoofd|prenom|stan'), ('officiële', 'ADJ|prenom|basis|met-e|stan'), ('talen', 'N|soort|mv|basis'), ('van', 'VZ|init'), ('België', 'N|eigen|ev|basis|onz|stan'), ('.', 'LET')]
        assert tokens_tagged_universal == [('Het', 'DET'), ('Nederlands', 'PROPN'), ('is', 'AUX'), ('een', 'DET'), ('West-Germaanse', 'ADJ'), ('taal', 'NOUN'), ('en', 'CCONJ'), ('de', 'DET'), ('officiële', 'ADJ'), ('taal', 'NOUN'), ('van', 'ADP'), ('Nederland', 'PROPN'), (',', 'PUNCT'), ('Suriname', 'PROPN'), ('en', 'CCONJ'), ('een', 'NUM'), ('van', 'ADP'), ('de', 'DET'), ('drie', 'NUM'), ('officiële', 'ADJ'), ('talen', 'NOUN'), ('van', 'ADP'), ('België', 'PROPN'), ('.', 'PUNCT')]
    elif lang.startswith('eng_'):
        if pos_tagger == 'nltk_perceptron':
            assert tokens_tagged == [('English', 'NNP'), ('is', 'VBZ'), ('a', 'DT'), ('West', 'NNP'), ('Germanic', 'NNP'), ('language', 'NN'), ('of', 'IN'), ('the', 'DT'), ('Indo', 'NNP'), ('-', ':'), ('European', 'JJ'), ('language', 'NN'), ('family', 'NN'), (',', ','), ('originally', 'RB'), ('spoken', 'VBN'), ('by', 'IN'), ('the', 'DT'), ('inhabitants', 'NNS'), ('of', 'IN'), ('early', 'JJ'), ('medieval', 'NN'), ('England.[3][4][5', 'NNP'), (']', 'NN')]
            assert tokens_tagged_universal == [('English', 'PROPN'), ('is', 'VERB'), ('a', 'DET'), ('West', 'PROPN'), ('Germanic', 'PROPN'), ('language', 'NOUN'), ('of', 'ADP/SCONJ'), ('the', 'DET'), ('Indo', 'PROPN'), ('-', 'PUNCT'), ('European', 'ADJ'), ('language', 'NOUN'), ('family', 'NOUN'), (',', 'PUNCT'), ('originally', 'ADV'), ('spoken', 'VERB'), ('by', 'ADP/SCONJ'), ('the', 'DET'), ('inhabitants', 'NOUN'), ('of', 'ADP/SCONJ'), ('early', 'ADJ'), ('medieval', 'NOUN'), ('England.[3][4][5', 'PROPN'), (']', 'NOUN')]
        elif pos_tagger == 'spacy_eng':
            assert tokens_tagged == [('English', 'NNP'), ('is', 'VBZ'), ('a', 'DT'), ('West', 'NNP'), ('Germanic', 'NNP'), ('language', 'NN'), ('of', 'IN'), ('the', 'DT'), ('Indo', 'NNP'), ('-', 'HYPH'), ('European', 'JJ'), ('language', 'NN'), ('family', 'NN'), (',', ','), ('originally', 'RB'), ('spoken', 'VBN'), ('by', 'IN'), ('the', 'DT'), ('inhabitants', 'NNS'), ('of', 'IN'), ('early', 'JJ'), ('medieval', 'JJ'), ('England.[3][4][5', 'NNP'), (']', '-RRB-')]
            assert tokens_tagged_universal == [('English', 'PROPN'), ('is', 'AUX'), ('a', 'DET'), ('West', 'PROPN'), ('Germanic', 'PROPN'), ('language', 'NOUN'), ('of', 'ADP'), ('the', 'DET'), ('Indo', 'PROPN'), ('-', 'PUNCT'), ('European', 'ADJ'), ('language', 'NOUN'), ('family', 'NOUN'), (',', 'PUNCT'), ('originally', 'ADV'), ('spoken', 'VERB'), ('by', 'ADP'), ('the', 'DET'), ('inhabitants', 'NOUN'), ('of', 'ADP'), ('early', 'ADJ'), ('medieval', 'ADJ'), ('England.[3][4][5', 'PROPN'), (']', 'PUNCT')]
        else:
            raise Exception(f'Error: Tests for POS tagger "{pos_tagger}" is skipped!')
    elif lang == 'fin':
        assert tokens_tagged == [('Suomen', 'N'), ('kieli', 'N'), ('(', 'Punct'), ('suomi', 'N'), (')', 'Punct'), ('on', 'V'), ('uralilaisten', 'A'), ('kielten', 'N'), ('itämerensuomalaiseen', 'N'), ('ryhmään', 'N'), ('kuuluva', 'V'), ('kieli', 'N'), (',', 'Punct'), ('jota', 'Pron'), ('puhuvat', 'V'), ('pääosin', 'Adv'), ('suomalaiset', 'N'), ('.', 'Punct')]
        assert tokens_tagged_universal == [('Suomen', 'PROPN'), ('kieli', 'NOUN'), ('(', 'PUNCT'), ('suomi', 'PROPN'), (')', 'PUNCT'), ('on', 'AUX'), ('uralilaisten', 'ADJ'), ('kielten', 'NOUN'), ('itämerensuomalaiseen', 'NOUN'), ('ryhmään', 'NOUN'), ('kuuluva', 'VERB'), ('kieli', 'NOUN'), (',', 'PUNCT'), ('jota', 'PRON'), ('puhuvat', 'VERB'), ('pääosin', 'ADV'), ('suomalaiset', 'NOUN'), ('.', 'PUNCT')]
    elif lang == 'fra':
        assert tokens_tagged == tokens_tagged_universal == [('Le', 'DET'), ('français', 'NOUN'), ('est', 'AUX'), ('une', 'DET'), ('langue', 'NOUN'), ('indo-européenne', 'ADJ'), ('de', 'ADP'), ('la', 'DET'), ('famille', 'NOUN'), ('des', 'ADP'), ('langues', 'NOUN'), ('romanes', 'NOUN'), ('dont', 'PRON'), ('les', 'DET'), ('locuteurs', 'NOUN'), ('sont', 'AUX'), ('appelés', 'VERB'), ('francophones', 'NOUN'), (',', 'PUNCT'), ('également', 'ADV'), ('surnommé', 'VERB'), ('la', 'DET'), ('langue', 'NOUN'), ('de', 'ADP'), ('Molière', 'NOUN'), ('.', 'PUNCT')]
    elif lang.startswith('deu_'):
        assert tokens_tagged == [('Die', 'ART'), ('deutsche', 'ADJA'), ('Sprache', 'NN'), ('bzw.', 'KON'), ('Deutsch', 'NN'), ('(', '$('), ('[', 'NE'), ('dɔɪ̯tʃ];[26', 'NE'), (']', 'NE'), ('abgekürzt', 'VVPP'), ('dt', 'NE'), ('.', '$.'), ('oder', 'KON'), ('dtsch', 'ADJD'), ('.', '$.'), (')', '$('), ('ist', 'VAFIN'), ('eine', 'ART'), ('westgermanische', 'ADJA'), ('Sprache', 'NN'), (',', '$,'), ('die', 'PRELS'), ('weltweit', 'ADJD'), ('etwa', 'ADV'), ('90', 'CARD'), ('bis', 'KON'), ('105', 'CARD'), ('Millionen', 'NN'), ('Menschen', 'NN'), ('als', 'APPR'), ('Muttersprache', 'NN'), ('und', 'KON'), ('weiteren', 'ADJA'), ('rund', 'ADV'), ('80', 'CARD'), ('Millionen', 'NN'), ('als', 'APPR'), ('Zweit-', 'TRUNC'), ('oder', 'KON'), ('Fremdsprache', 'NN'), ('dient', 'VVFIN'), ('.', '$.')]
        assert tokens_tagged_universal == [('Die', 'DET'), ('deutsche', 'ADJ'), ('Sprache', 'NOUN'), ('bzw.', 'CCONJ'), ('Deutsch', 'NOUN'), ('(', 'PUNCT'), ('[', 'PROPN'), ('dɔɪ̯tʃ];[26', 'PROPN'), (']', 'X'), ('abgekürzt', 'VERB'), ('dt', 'PROPN'), ('.', 'PUNCT'), ('oder', 'CCONJ'), ('dtsch', 'ADV'), ('.', 'PUNCT'), (')', 'PUNCT'), ('ist', 'AUX'), ('eine', 'DET'), ('westgermanische', 'ADJ'), ('Sprache', 'NOUN'), (',', 'PUNCT'), ('die', 'PRON'), ('weltweit', 'ADV'), ('etwa', 'ADV'), ('90', 'NUM'), ('bis', 'CCONJ'), ('105', 'NUM'), ('Millionen', 'NOUN'), ('Menschen', 'NOUN'), ('als', 'ADP'), ('Muttersprache', 'NOUN'), ('und', 'CCONJ'), ('weiteren', 'ADJ'), ('rund', 'ADV'), ('80', 'NUM'), ('Millionen', 'NOUN'), ('als', 'ADP'), ('Zweit-', 'X'), ('oder', 'CCONJ'), ('Fremdsprache', 'NOUN'), ('dient', 'VERB'), ('.', 'PUNCT')]
    elif lang == 'ell':
        assert tokens_tagged == tokens_tagged_universal == [('Η', 'DET'), ('ελληνική', 'ADJ'), ('γλώσσα', 'NOUN'), ('ανήκει', 'VERB'), ('στην', 'ADP'), ('ινδοευρωπαϊκή', 'ADJ'), ('οικογένεια[9', 'NOUN'), (']', 'NOUN'), ('και', 'CCONJ'), ('αποτελεί', 'VERB'), ('το', 'DET'), ('μοναδικό', 'ADJ'), ('μέλος', 'NOUN'), ('του', 'DET'), ('ελληνικού', 'ADJ'), ('κλάδου', 'NOUN'), (',', 'PUNCT'), ('ενώ', 'SCONJ'), ('είναι', 'AUX'), ('η', 'DET'), ('επίσημη', 'ADJ'), ('γλώσσα', 'NOUN'), ('της', 'DET'), ('Ελλάδας', 'PROPN'), ('και', 'CCONJ'), ('της', 'DET'), ('Κύπρου', 'PROPN'), ('.', 'PUNCT')]
    elif lang == 'ita':
        assert tokens_tagged == [("L'", 'RD'), ('italiano', 'S'), ('(', 'FB'), ('[', 'FB'), ('itaˈljaːno][Nota', 'S'), ('1', 'N'), (']', 'FB'), ('ascolta[?·info', 'SP'), (']', 'FB'), (')', 'FB'), ('è', 'V'), ('una', 'RI'), ('lingua', 'S'), ('romanza', 'S'), ('parlata', 'A'), ('principalmente', 'B'), ('in', 'E'), ('Italia', 'SP'), ('.', 'FS')]
        assert tokens_tagged_universal == [("L'", 'DET'), ('italiano', 'NOUN'), ('(', 'PUNCT'), ('[', 'PUNCT'), ('itaˈljaːno][Nota', 'NOUN'), ('1', 'NUM'), (']', 'PUNCT'), ('ascolta[?·info', 'PROPN'), (']', 'PUNCT'), (')', 'PUNCT'), ('è', 'AUX'), ('una', 'DET'), ('lingua', 'NOUN'), ('romanza', 'NOUN'), ('parlata', 'ADJ'), ('principalmente', 'ADV'), ('in', 'ADP'), ('Italia', 'PROPN'), ('.', 'PUNCT')]
    elif lang == 'jpn':
        if pos_tagger == 'spacy_jpn':
            assert tokens_tagged == [('日本', '名詞-固有名詞-地名-国'), ('語', '名詞-普通名詞-一般'), ('（', '補助記号-括弧開'), ('にほん', '名詞-固有名詞-地名-国'), ('ご', '接尾辞-名詞的-一般'), ('、', '補助記号-読点'), ('にっぽん', '名詞-固有名詞-地名-国'), ('ご', '接尾辞-名詞的-一般'), ('[', '補助記号-括弧開'), ('注', '名詞-普通名詞-一般'), ('2', '名詞-数詞'), (']', '補助記号-括弧閉'), ('）', '補助記号-括弧閉'), ('は', '助詞-係助詞'), ('、', '補助記号-読点'), ('日本', '名詞-固有名詞-地名-国'), ('国', '接尾辞-名詞的-一般'), ('内', '接尾辞-名詞的-一般'), ('や', '助詞-副助詞'), ('、', '補助記号-読点'), ('かつて', '副詞'), ('の', '助詞-格助詞'), ('日本', '名詞-固有名詞-地名-国'), ('領', '接尾辞-名詞的-一般'), ('だっ', '助動詞'), ('た', '助動詞'), ('国', '名詞-普通名詞-一般'), ('、', '補助記号-読点'), ('そして', '接続詞'), ('日本', '名詞-固有名詞-地名-国'), ('人', '接尾辞-名詞的-一般'), ('同士', '接尾辞-名詞的-一般'), ('の', '助詞-格助詞'), ('間', '名詞-普通名詞-副詞可能'), ('で', '助詞-格助詞'), ('使用', '名詞-普通名詞-サ変可能'), ('さ', '動詞-非自立可能'), ('れ', '助動詞'), ('て', '助詞-接続助詞'), ('いる', '動詞-非自立可能'), ('言語', '名詞-普通名詞-一般'), ('。', '補助記号-句点')]
            assert tokens_tagged_universal == [('日本', 'PROPN'), ('語', 'NOUN'), ('（', 'NOUN'), ('にほん', 'PROPN'), ('ご', 'NOUN'), ('、', 'PUNCT'), ('にっぽん', 'PROPN'), ('ご', 'NOUN'), ('[', 'PUNCT'), ('注', 'NOUN'), ('2', 'NUM'), (']', 'PUNCT'), ('）', 'NOUN'), ('は', 'ADP'), ('、', 'PUNCT'), ('日本', 'PROPN'), ('国', 'NOUN'), ('内', 'NOUN'), ('や', 'ADP'), ('、', 'PUNCT'), ('かつて', 'ADV'), ('の', 'ADP'), ('日本', 'PROPN'), ('領', 'NOUN'), ('だっ', 'AUX'), ('た', 'AUX'), ('国', 'NOUN'), ('、', 'PUNCT'), ('そして', 'CCONJ'), ('日本', 'PROPN'), ('人', 'NOUN'), ('同士', 'NOUN'), ('の', 'ADP'), ('間', 'NOUN'), ('で', 'ADP'), ('使用', 'VERB'), ('さ', 'AUX'), ('れ', 'AUX'), ('て', 'SCONJ'), ('いる', 'VERB'), ('言語', 'NOUN'), ('。', 'PUNCT')]
        elif pos_tagger == 'sudachipy_jpn':
            assert tokens_tagged == [('日本語', '名詞-普通名詞-一般'), ('（', '補助記号-括弧開'), ('にほん', '名詞-固有名詞-地名-国'), ('ご', '接尾辞-名詞的-一般'), ('、', '補助記号-読点'), ('にっぽん', '名詞-固有名詞-地名-国'), ('ご', '接尾辞-名詞的-一般'), ('[', '補助記号-括弧開'), ('注', '名詞-普通名詞-一般'), ('2', '名詞-数詞'), (']', '補助記号-括弧閉'), ('）', '補助記号-括弧閉'), ('は', '助詞-係助詞'), ('、', '補助記号-読点'), ('日本', '名詞-固有名詞-地名-国'), ('国', '接尾辞-名詞的-一般'), ('内', '接尾辞-名詞的-一般'), ('や', '助詞-副助詞'), ('、', '補助記号-読点'), ('かつて', '副詞'), ('の', '助詞-格助詞'), ('日本', '名詞-固有名詞-地名-国'), ('領', '接尾辞-名詞的-一般'), ('だっ', '助動詞'), ('た', '助動詞'), ('国', '名詞-普通名詞-一般'), ('、', '補助記号-読点'), ('そして', '接続詞'), ('日本人', '名詞-普通名詞-一般'), ('同士', '接尾辞-名詞的-一般'), ('の', '助詞-格助詞'), ('間', '名詞-普通名詞-副詞可能'), ('で', '助詞-格助詞'), ('使用', '名詞-普通名詞-サ変可能'), ('さ', '動詞-非自立可能'), ('れ', '助動詞'), ('て', '助詞-接続助詞'), ('いる', '動詞-非自立可能'), ('言語', '名詞-普通名詞-一般'), ('。', '補助記号-句点')]
            assert tokens_tagged_universal == [('日本語', 'NOUN'), ('（', 'PUNCT'), ('にほん', 'NOUN'), ('ご', 'PART'), ('、', 'PUNCT'), ('にっぽん', 'NOUN'), ('ご', 'PART'), ('[', 'PUNCT'), ('注', 'NOUN'), ('2', 'NOUN'), (']', 'PUNCT'), ('）', 'PUNCT'), ('は', 'PART'), ('、', 'PUNCT'), ('日本', 'NOUN'), ('国', 'PART'), ('内', 'PART'), ('や', 'PART'), ('、', 'PUNCT'), ('かつて', 'ADV'), ('の', 'PART'), ('日本', 'NOUN'), ('領', 'PART'), ('だっ', 'AUX'), ('た', 'AUX'), ('国', 'NOUN'), ('、', 'PUNCT'), ('そして', 'CONJ'), ('日本人', 'NOUN'), ('同士', 'PART'), ('の', 'PART'), ('間', 'NOUN'), ('で', 'PART'), ('使用', 'NOUN'), ('さ', 'VERB'), ('れ', 'AUX'), ('て', 'PART'), ('いる', 'VERB'), ('言語', 'NOUN'), ('。', 'PUNCT')]
        else:
            raise Exception(f'Error: Tests for POS tagger "{pos_tagger}" is skipped!')
    elif lang == 'lit':
        assert tokens_tagged == [('Lietuvių', 'dkt.vyr.dgs.K.'), ('kalba', 'dkt.mot.vns.Įn.'), ('–', 'skyr.'), ('iš', 'prl.K.'), ('baltų', 'vksm.dlv.neveik.būt.vyr.dgs.K.'), ('prokalbės', 'dkt.mot.vns.K.'), ('kilusi', 'vksm.dlv.veik.būt-k.mot.vns.V.'), ('lietuvių', 'dkt.vyr.dgs.K.'), ('tautos', 'dkt.mot.vns.K.'), ('kalba', 'dkt.mot.vns.Įn.'), (',', 'skyr.'), ('kuri', 'įv.mot.vns.V.'), ('Lietuvoje', 'dkt.tikr.mot.vns.Vt.'), ('yra', 'vksm.asm.tiesiog.es.vns.3.'), ('valstybinė', 'bdv.nelygin.mot.vns.V.'), (',', 'skyr.'), ('o', 'jng.'), ('Europos', 'dkt.tikr.mot.vns.K.'), ('Sąjungoje', 'dkt.mot.vns.Vt.'), ('–', 'skyr.'), ('viena', 'įv.mot.vns.V.'), ('iš', 'prl.K.'), ('oficialiųjų', 'vksm.dlv.neveik.es.įvardž.vyr.dgs.K.'), ('kalbų', 'dkt.vyr.vns.V.'), ('.', 'skyr.')]
        assert tokens_tagged_universal == [('Lietuvių', 'NOUN'), ('kalba', 'NOUN'), ('–', 'PUNCT'), ('iš', 'ADP'), ('baltų', 'VERB'), ('prokalbės', 'NOUN'), ('kilusi', 'VERB'), ('lietuvių', 'NOUN'), ('tautos', 'NOUN'), ('kalba', 'NOUN'), (',', 'PUNCT'), ('kuri', 'DET'), ('Lietuvoje', 'PROPN'), ('yra', 'AUX'), ('valstybinė', 'ADJ'), (',', 'PUNCT'), ('o', 'CCONJ'), ('Europos', 'PROPN'), ('Sąjungoje', 'NOUN'), ('–', 'PUNCT'), ('viena', 'PRON'), ('iš', 'ADP'), ('oficialiųjų', 'VERB'), ('kalbų', 'NOUN'), ('.', 'PUNCT')]
    elif lang == 'mkd':
        assert tokens_tagged == tokens_tagged_universal == [('Македонски', 'ADJ'), ('јазик', 'NOUN'), ('—', 'PUNCT'), ('јужнословенски', 'ADJ'), ('јазик', 'NOUN'), (',', 'PUNCT'), ('дел', 'NOUN'), ('од', 'ADP'), ('групата', 'NOUN'), ('на', 'ADP'), ('словенски', 'ADJ'), ('јазици', 'NOUN'), ('од', 'ADP'), ('јазичното', 'ADJ'), ('семејство', 'NOUN'), ('на', 'ADP'), ('индоевропски', 'ADJ'), ('јазици', 'NOUN'), ('.', 'PUNCT')]
    elif lang == 'nob':
        assert tokens_tagged == tokens_tagged_universal == [('Bokmål', 'ADV'), ('er', 'AUX'), ('en', 'DET'), ('varietet', 'NOUN'), ('av', 'ADP'), ('norsk', 'ADJ'), ('språk', 'NOUN'), ('.', 'PUNCT')]
    elif lang == 'pol':
        assert tokens_tagged == [('Język', 'SUBST'), ('polski', '_SP'), (',', 'INTERP'), ('polszczyzna', 'ADJ'), ('–', 'INTERP'), ('język', 'SUBST'), ('lechicki', 'SUBST'), ('z', 'PREP'), ('grupy', 'SUBST'), ('zachodniosłowiańskiej', 'ADJ'), ('(', 'INTERP'), ('do', 'PREP'), ('której', 'ADJ'), ('należą', 'FIN'), ('również', 'QUB'), ('czeski', 'ADJ'), (',', 'INTERP'), ('kaszubski', 'SUBST'), (',', 'INTERP'), ('słowacki', 'SUBST'), ('i', 'CONJ'), ('języki', 'SUBST'), ('łużyckie', 'ADJ'), (')', 'SUBST'), (',', 'INTERP'), ('stanowiącej', 'PACT'), ('część', 'SUBST'), ('rodziny', 'SUBST'), ('indoeuropejskiej', 'SUBST'), ('.', 'SUBST')]
        assert tokens_tagged_universal == [('Język', 'NOUN'), ('polski', 'ADJ'), (',', 'PUNCT'), ('polszczyzna', 'ADJ'), ('–', 'PUNCT'), ('język', 'NOUN'), ('lechicki', 'ADJ'), ('z', 'ADP'), ('grupy', 'NOUN'), ('zachodniosłowiańskiej', 'ADJ'), ('(', 'PUNCT'), ('do', 'ADP'), ('której', 'DET'), ('należą', 'VERB'), ('również', 'PART'), ('czeski', 'ADJ'), (',', 'PUNCT'), ('kaszubski', 'ADJ'), (',', 'PUNCT'), ('słowacki', 'ADJ'), ('i', 'CCONJ'), ('języki', 'NOUN'), ('łużyckie', 'ADJ'), (')', 'PUNCT'), (',', 'PUNCT'), ('stanowiącej', 'ADJ'), ('część', 'NOUN'), ('rodziny', 'NOUN'), ('indoeuropejskiej', 'ADJ'), ('.', 'PUNCT')]
    elif lang.startswith('por_'):
        assert tokens_tagged == tokens_tagged_universal == [('A', 'DET'), ('língua', 'NOUN'), ('portuguesa', 'ADJ'), (',', 'PUNCT'), ('também', 'ADV'), ('designada', 'VERB'), ('português', 'ADJ'), (',', 'PUNCT'), ('é', 'AUX'), ('uma', 'DET'), ('língua', 'NOUN'), ('indo-europeia', 'ADJ'), ('românica', 'ADJ'), ('flexiva', 'NOUN'), ('ocidental', 'ADJ'), ('originada', 'VERB'), ('no', 'ADP'), ('galego-português', 'NOUN'), ('falado', 'VERB'), ('no', 'ADP'), ('Reino', 'PROPN'), ('da', 'ADP'), ('Galiza', 'PROPN'), ('e', 'CCONJ'), ('no', 'ADP'), ('norte', 'NOUN'), ('de', 'ADP'), ('Portugal', 'PROPN'), ('.', 'PUNCT')]
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
            assert tokens_tagged == tokens_tagged_universal == [('Ру́сский', 'ADJ'), ('язы́к', 'NOUN'), ('(', 'PUNCT'), ('[', 'PUNCT'), ('ˈruskʲɪi̯', 'X'), ('jɪˈzɨk', 'PROPN'), (']', 'PUNCT'), ('Информация', 'NOUN'), ('о', 'ADP'), ('файле', 'NOUN'), ('слушать)[~', 'PROPN'), ('3', 'NUM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('⇨', 'NOUN'), (']', 'PUNCT'), ('—', 'PUNCT'), ('один', 'NUM'), ('из', 'ADP'), ('восточнославянских', 'ADJ'), ('языков', 'NOUN'), (',', 'PUNCT'), ('национальный', 'ADJ'), ('язык', 'NOUN'), ('русского', 'ADJ'), ('народа', 'NOUN'), ('.', 'PUNCT')]
        else:
            raise Exception(f'Error: Tests for POS tagger "{pos_tagger}" is skipped!')
    elif lang == 'spa':
        assert tokens_tagged == tokens_tagged_universal == [('El', 'DET'), ('español', 'NOUN'), ('o', 'CCONJ'), ('castellano', 'NOUN'), ('es', 'AUX'), ('una', 'DET'), ('lengua', 'ADJ'), ('romance', 'NOUN'), ('procedente', 'ADJ'), ('del', 'ADP'), ('latín', 'NOUN'), ('hablado', 'ADJ'), (',', 'PUNCT'), ('perteneciente', 'ADJ'), ('a', 'ADP'), ('la', 'DET'), ('familia', 'NOUN'), ('de', 'ADP'), ('lenguas', 'NOUN'), ('indoeuropeas', 'ADJ'), ('.', 'PUNCT')]
    elif lang == 'swe':
        assert tokens_tagged == [('Svenska', 'JJ|POS|UTR/NEU|SIN|DEF|NOM'), ('(', 'PAD'), ('svenska', 'JJ|POS|UTR/NEU|SIN|DEF|NOM'), ('(', 'PAD'), ('info', 'AB'), (')', 'PAD'), (')', 'PAD'), ('är', 'VB|PRS|AKT'), ('ett', 'DT|NEU|SIN|IND'), ('östnordiskt', 'JJ|POS|NEU|SIN|IND|NOM'), ('språk', 'NN|NEU|SIN|IND|NOM'), ('som', 'HP|-|-|-'), ('talas', 'VB|PRS|SFO'), ('av', 'PP'), ('ungefär', 'AB'), ('tio', 'RG|NOM'), ('miljoner', 'NN|UTR|PLU|IND|NOM'), ('personer', 'NN|UTR|PLU|IND|NOM'), ('främst', 'AB|SUV'), ('i', 'PP'), ('Sverige', 'PM|NOM'), ('där', 'HA'), ('språket', 'AB|POS'), ('har', 'VB|PRS|AKT'), ('en', 'DT|UTR|SIN|IND'), ('dominant', 'JJ|POS|UTR|SIN|IND|NOM'), ('ställning', 'NN|UTR|SIN|IND|NOM'), ('som', 'KN'), ('huvudspråk', 'NN|NEU|SIN|IND|NOM'), (',', 'MID'), ('men', 'KN'), ('även', 'AB'), ('som', 'KN'), ('det', 'DT|NEU|SIN|DEF'), ('ena', 'JJ|POS|UTR/NEU|SIN/PLU|IND/DEF|NOM'), ('nationalspråket', 'NN|NEU|SIN|DEF|NOM'), ('i', 'PP'), ('Finland', 'PM|NOM'), ('och', 'KN'), ('som', 'HP|-|-|-'), ('enda', 'JJ|POS|UTR/NEU|SIN/PLU|IND/DEF|NOM'), ('officiella', 'JJ|POS|UTR/NEU|PLU|IND/DEF|NOM'), ('språk', 'NN|NEU|PLU|IND|NOM'), ('på', 'PP'), ('Åland', 'PM|NOM'), ('.', 'MAD')]
        assert tokens_tagged_universal == [('Svenska', 'ADJ'), ('(', 'PUNCT'), ('svenska', 'ADJ'), ('(', 'PUNCT'), ('info', 'ADV'), (')', 'PUNCT'), (')', 'PUNCT'), ('är', 'AUX'), ('ett', 'DET'), ('östnordiskt', 'ADJ'), ('språk', 'NOUN'), ('som', 'PRON'), ('talas', 'VERB'), ('av', 'ADP'), ('ungefär', 'ADV'), ('tio', 'NUM'), ('miljoner', 'NOUN'), ('personer', 'NOUN'), ('främst', 'ADV'), ('i', 'ADP'), ('Sverige', 'PROPN'), ('där', 'ADV'), ('språket', 'ADV'), ('har', 'VERB'), ('en', 'DET'), ('dominant', 'ADJ'), ('ställning', 'NOUN'), ('som', 'SCONJ'), ('huvudspråk', 'NOUN'), (',', 'PUNCT'), ('men', 'CCONJ'), ('även', 'ADV'), ('som', 'SCONJ'), ('det', 'DET'), ('ena', 'ADJ'), ('nationalspråket', 'NOUN'), ('i', 'ADP'), ('Finland', 'PROPN'), ('och', 'CCONJ'), ('som', 'PRON'), ('enda', 'ADJ'), ('officiella', 'ADJ'), ('språk', 'NOUN'), ('på', 'ADP'), ('Åland', 'PROPN'), ('.', 'PUNCT')]
    elif lang == 'tha':
        if pos_tagger == 'pythainlp_perceptron_lst20':
            assert tokens_tagged == [('ภาษาไทย', 'NN'), ('หรือ', 'CC'), ('ภาษาไทย', 'NN'), ('กลาง', 'NN'), ('เป็น', 'VV'), ('ภาษา', 'NN'), ('ใน', 'PS'), ('กลุ่ม', 'NN'), ('ภาษา', 'NN'), ('ไท', 'NN'), ('ซึ่ง', 'CC'), ('เป็น', 'VV'), ('กลุ่มย่อย', 'NN'), ('ของ', 'PS'), ('ตระกูล', 'NN'), ('ภาษา', 'NN'), ('ข', 'NN'), ('ร้า', 'NN'), ('-', 'PU'), ('ไท', 'NN'), ('และ', 'CC'), ('เป็น', 'VV'), ('ภาษาราชการ', 'NN'), ('และ', 'CC'), ('ภาษาประจำชาติ', 'NN'), ('ของ', 'PS'), ('ประเทศ', 'NN'), ('ไทย', 'NN'), ('[', 'NN'), ('3', 'NU'), ('][', 'NN'), ('4', 'NU'), (']', 'NN')]
            assert tokens_tagged_universal == [('ภาษาไทย', 'NOUN'), ('หรือ', 'CCONJ'), ('ภาษาไทย', 'NOUN'), ('กลาง', 'NOUN'), ('เป็น', 'VERB'), ('ภาษา', 'NOUN'), ('ใน', 'ADP'), ('กลุ่ม', 'NOUN'), ('ภาษา', 'NOUN'), ('ไท', 'NOUN'), ('ซึ่ง', 'CCONJ'), ('เป็น', 'VERB'), ('กลุ่มย่อย', 'NOUN'), ('ของ', 'ADP'), ('ตระกูล', 'NOUN'), ('ภาษา', 'NOUN'), ('ข', 'NOUN'), ('ร้า', 'NOUN'), ('-', 'PUNCT'), ('ไท', 'NOUN'), ('และ', 'CCONJ'), ('เป็น', 'VERB'), ('ภาษาราชการ', 'NOUN'), ('และ', 'CCONJ'), ('ภาษาประจำชาติ', 'NOUN'), ('ของ', 'ADP'), ('ประเทศ', 'NOUN'), ('ไทย', 'NOUN'), ('[', 'NOUN'), ('3', 'NUM'), ('][', 'NOUN'), ('4', 'NUM'), (']', 'NOUN')]
        elif pos_tagger == 'pythainlp_perceptron_orchid':
            assert tokens_tagged == [('ภาษาไทย', 'NPRP'), ('หรือ', 'JCRG'), ('ภาษาไทย', 'NPRP'), ('กลาง', 'VATT'), ('เป็น', 'VSTA'), ('ภาษา', 'NCMN'), ('ใน', 'RPRE'), ('กลุ่ม', 'NCMN'), ('ภาษา', 'NCMN'), ('ไท', 'NCMN'), ('ซึ่ง', 'PREL'), ('เป็น', 'VSTA'), ('กลุ่มย่อย', 'NCMN'), ('ของ', 'RPRE'), ('ตระกูล', 'NCMN'), ('ภาษา', 'NCMN'), ('ข', 'NCMN'), ('ร้า', 'NCMN'), ('-', 'PUNC'), ('ไท', 'NCMN'), ('และ', 'JCRG'), ('เป็น', 'VSTA'), ('ภาษาราชการ', 'NCMN'), ('และ', 'JCRG'), ('ภาษาประจำชาติ', 'NCMN'), ('ของ', 'RPRE'), ('ประเทศ', 'NCMN'), ('ไทย', 'NPRP'), ('[', 'NCMN'), ('3', 'NCNM'), ('][', 'PUNC'), ('4', 'NCNM'), (']', 'CMTR')]
            assert tokens_tagged_universal == [('ภาษาไทย', 'PROPN'), ('หรือ', 'CCONJ'), ('ภาษาไทย', 'PROPN'), ('กลาง', 'ADJ'), ('เป็น', 'VERB'), ('ภาษา', 'NOUN'), ('ใน', 'ADP'), ('กลุ่ม', 'NOUN'), ('ภาษา', 'NOUN'), ('ไท', 'NOUN'), ('ซึ่ง', 'SCONJ'), ('เป็น', 'VERB'), ('กลุ่มย่อย', 'NOUN'), ('ของ', 'ADP'), ('ตระกูล', 'NOUN'), ('ภาษา', 'NOUN'), ('ข', 'NOUN'), ('ร้า', 'NOUN'), ('-', 'PUNCT'), ('ไท', 'NOUN'), ('และ', 'CCONJ'), ('เป็น', 'VERB'), ('ภาษาราชการ', 'NOUN'), ('และ', 'CCONJ'), ('ภาษาประจำชาติ', 'NOUN'), ('ของ', 'ADP'), ('ประเทศ', 'NOUN'), ('ไทย', 'PROPN'), ('[', 'NOUN'), ('3', 'NUM'), ('][', 'PUNCT'), ('4', 'NUM'), (']', 'NOUN')]
        elif pos_tagger == 'pythainlp_perceptron_pud':
            assert tokens_tagged == tokens_tagged_universal == [('ภาษาไทย', 'NOUN'), ('หรือ', 'CCONJ'), ('ภาษาไทย', 'NOUN'), ('กลาง', 'NOUN'), ('เป็น', 'AUX'), ('ภาษา', 'NOUN'), ('ใน', 'ADP'), ('กลุ่ม', 'NOUN'), ('ภาษา', 'NOUN'), ('ไท', 'PROPN'), ('ซึ่ง', 'DET'), ('เป็น', 'AUX'), ('กลุ่มย่อย', 'NOUN'), ('ของ', 'ADP'), ('ตระกูล', 'NOUN'), ('ภาษา', 'NOUN'), ('ข', 'NOUN'), ('ร้า', 'NOUN'), ('-', 'PUNCT'), ('ไท', 'PROPN'), ('และ', 'CCONJ'), ('เป็น', 'AUX'), ('ภาษาราชการ', 'NOUN'), ('และ', 'CCONJ'), ('ภาษาประจำชาติ', 'NOUN'), ('ของ', 'ADP'), ('ประเทศ', 'NOUN'), ('ไทย', 'PROPN'), ('[', 'NOUN'), ('3', 'NUM'), ('][', 'NOUN'), ('4', 'NUM'), (']', 'NOUN')]
        else:
            raise Exception(f'Error: Tests for POS tagger "{pos_tagger}" is skipped!')
    elif lang == 'bod':
        assert tokens_tagged == [('བོད་', 'PROPN'), ('ཀྱི་', 'PART'), ('སྐད་ཡིག་', 'NOUN'), ('ནི་', 'NO_POS'), ('བོད་ཡུལ་', 'PROPN'), ('དང་', 'NO_POS'), ('དེ', 'DET'), ('འི་', 'PART'), ('ཉེ་འཁོར་', 'NOUN'), ('གྱི་', 'PART'), ('ས་ཁུལ་', 'OTHER'), ('ཏེ', 'PART'), ('།', 'PUNCT')]
        assert tokens_tagged_universal == [('བོད་', 'PROPN'), ('ཀྱི་', 'PART'), ('སྐད་ཡིག་', 'NOUN'), ('ནི་', 'X'), ('བོད་ཡུལ་', 'PROPN'), ('དང་', 'X'), ('དེ', 'DET'), ('འི་', 'PART'), ('ཉེ་འཁོར་', 'NOUN'), ('གྱི་', 'PART'), ('ས་ཁུལ་', 'X'), ('ཏེ', 'PART'), ('།', 'PUNCT')]
    elif lang == 'ukr':
        if pos_tagger == 'pymorphy2_morphological_analyzer':
            assert tokens_tagged == [('Украї́нська', 'ADJF'), ('мо́ва', 'ADJF'), ('(', 'PNCT'), ('МФА', 'UNKN'), (':', 'PNCT'), ('[', 'PNCT'), ('ukrɑ̽ˈjɪnʲsʲkɑ̽', 'UNKN'), ('ˈmɔwɑ̽', 'UNKN'), (']', 'PNCT'), (',', 'PNCT'), ('історичні', 'ADJF'), ('назви', 'NOUN'), ('—', 'PNCT'), ('ру́ська', 'ADJF'), (',', 'PNCT'), ('руси́нська[10][11][12', 'UNKN'), (']', 'PNCT'), ('[', 'PNCT'), ('*', 'PNCT'), ('1', 'NUMB'), (']', 'PNCT'), (')', 'PNCT'), ('—', 'PNCT'), ('національна', 'ADJF'), ('мова', 'NOUN'), ('українців', 'NOUN'), ('.', 'PNCT')]
            assert tokens_tagged_universal == [('Украї́нська', 'ADJ'), ('мо́ва', 'ADJ'), ('(', 'PUNCT'), ('МФА', 'SYM/X'), (':', 'PUNCT'), ('[', 'PUNCT'), ('ukrɑ̽ˈjɪnʲsʲkɑ̽', 'SYM/X'), ('ˈmɔwɑ̽', 'SYM/X'), (']', 'PUNCT'), (',', 'PUNCT'), ('історичні', 'ADJ'), ('назви', 'NOUN'), ('—', 'PUNCT'), ('ру́ська', 'ADJ'), (',', 'PUNCT'), ('руси́нська[10][11][12', 'SYM/X'), (']', 'PUNCT'), ('[', 'PUNCT'), ('*', 'PUNCT'), ('1', 'NUM'), (']', 'PUNCT'), (')', 'PUNCT'), ('—', 'PUNCT'), ('національна', 'ADJ'), ('мова', 'NOUN'), ('українців', 'NOUN'), ('.', 'PUNCT')]
        elif pos_tagger == 'spacy_ukr':
            assert tokens_tagged == tokens_tagged_universal == [('Украї́нська', 'ADJ'), ('мо́ва', 'PROPN'), ('(', 'PUNCT'), ('МФА', 'NOUN'), (':', 'PUNCT'), ('[', 'X'), ('ukrɑ̽ˈjɪnʲsʲkɑ̽', 'X'), ('ˈmɔwɑ̽', 'X'), (']', 'PROPN'), (',', 'PUNCT'), ('історичні', 'ADJ'), ('назви', 'NOUN'), ('—', 'PUNCT'), ('ру́ська', 'ADJ'), (',', 'PUNCT'), ('руси́нська[10][11][12', 'NOUN'), (']', 'PROPN'), ('[', 'PROPN'), ('*', 'SYM'), ('1', 'NUM'), (']', 'PROPN'), (')', 'PUNCT'), ('—', 'PUNCT'), ('національна', 'ADJ'), ('мова', 'NOUN'), ('українців', 'NOUN'), ('.', 'PUNCT')]
    elif lang == 'vie':
        assert tokens_tagged == [('Tiếng', 'N'), ('Việt', 'Np'), (',', 'CH'), ('cũng', 'R'), ('gọi là', 'X'), ('tiếng', 'N'), ('Việt Nam', 'Np'), ('[', 'V'), ('8 ]', 'N'), ('hay', 'C'), ('Việt ngữ', 'V'), ('là', 'V'), ('ngôn ngữ', 'N'), ('của', 'E'), ('người', 'Nc'), ('Việt', 'Np'), ('và', 'C'), ('là', 'V'), ('ngôn ngữ', 'N'), ('chính thức', 'A'), ('tại', 'E'), ('Việt Nam', 'Np'), ('.', 'CH')]
        assert tokens_tagged_universal == [('Tiếng', 'NOUN'), ('Việt', 'PROPN'), (',', 'PUNCT'), ('cũng', 'X'), ('gọi là', 'X'), ('tiếng', 'NOUN'), ('Việt Nam', 'PROPN'), ('[', 'VERB'), ('8 ]', 'NOUN'), ('hay', 'CCONJ'), ('Việt ngữ', 'VERB'), ('là', 'VERB'), ('ngôn ngữ', 'NOUN'), ('của', 'ADP'), ('người', 'NOUN'), ('Việt', 'PROPN'), ('và', 'CCONJ'), ('là', 'VERB'), ('ngôn ngữ', 'NOUN'), ('chính thức', 'ADJ'), ('tại', 'ADP'), ('Việt Nam', 'PROPN'), ('.', 'PUNCT')]
    else:
        raise Exception(f'Error: Tests for language "{lang}" is skipped!')

if __name__ == '__main__':
    for lang, pos_tagger in test_pos_taggers:
        test_pos_tag(lang, pos_tagger)
