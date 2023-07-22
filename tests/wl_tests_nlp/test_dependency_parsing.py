# ----------------------------------------------------------------------
# Wordless: Tests - NLP - Dependency Parsing
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
from wordless.wl_nlp import wl_dependency_parsing, wl_word_tokenization

main = wl_test_init.Wl_Test_Main()

test_dependency_parsers = []

for lang, dependency_parsers in main.settings_global['dependency_parsers'].items():
    for dependency_parser in dependency_parsers:
        test_dependency_parsers.append((lang, dependency_parser))

@pytest.mark.parametrize('lang, dependency_parser', test_dependency_parsers)
def test_dependency_parse(lang, dependency_parser):
    # Untokenized
    dependencies = wl_dependency_parsing.wl_dependency_parse(
        main,
        inputs = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}'),
        lang = lang,
        dependency_parser = dependency_parser
    )

    # Tokenized
    tokens = wl_word_tokenization.wl_word_tokenize_flat(
        main,
        text = getattr(wl_test_lang_examples, f'SENTENCE_{lang.upper()}'),
        lang = lang
    )
    dependencies_tokenized = wl_dependency_parsing.wl_dependency_parse(
        main,
        inputs = tokens,
        lang = lang,
        dependency_parser = dependency_parser
    )

    # Tagged texts
    main.settings_custom['files']['tags']['body_tag_settings'] = [['Embedded', 'Part of speech', '_*', 'N/A']]

    dependencies_tokenized_tagged = wl_dependency_parsing.wl_dependency_parse(
        main,
        inputs = [token + '_TEST' for token in tokens],
        lang = lang,
        dependency_parser = dependency_parser,
        tagged = True
    )

    # Long texts
    dependencies_tokenized_long = wl_dependency_parsing.wl_dependency_parse(
        main,
        inputs = [str(i) for i in range(101) for j in range(50)],
        lang = lang,
        dependency_parser = dependency_parser
    )

    print(f'{lang} / {dependency_parser}:')
    print(f'{dependencies}\n')

    # Check for empty dependencies
    assert dependencies
    assert dependencies_tokenized
    assert all(dependencies)
    assert all(dependencies_tokenized)

    for dependency in dependencies + dependencies_tokenized:
        assert len(dependency) == 4

    # Tokenization should not be modified
    assert len(tokens) == len(dependencies_tokenized)

    # Tagged texts
    dependencies_tokenized = [
        (child + '_TEST', head + '_TEST', dependency_relation, dependency_dist)
        for child, head, dependency_relation, dependency_dist in dependencies_tokenized
    ]

    assert dependencies_tokenized_tagged == dependencies_tokenized

    # Long texts
    assert [dependency[0] for dependency in dependencies_tokenized_long] == [str(i) for i in range(101) for j in range(50)]

    if lang == 'cat':
        assert dependencies == [('El', 'català', 'det', 1), ('català', 'llengua', 'nsubj', 46), ('(', 'denominació', 'punct', 1), ('denominació', 'català', 'appos', -2), ('oficial', 'denominació', 'amod', -1), ('a', 'Catalunya', 'case', 1), ('Catalunya', 'denominació', 'nmod', -3), (',', 'Illes', 'punct', 3), ('a', 'Illes', 'case', 2), ('les', 'Illes', 'det', 1), ('Illes', 'denominació', 'nmod', -7), ('Balears', 'Illes', 'flat', -1), (',', 'Andorra', 'punct', 2), ('a', 'Andorra', 'case', 1), ('Andorra', 'denominació', 'nmod', -11), (',', 'ciutat', 'punct', 3), ('a', 'ciutat', 'case', 2), ('la', 'ciutat', 'det', 1), ('ciutat', 'català', 'nmod', -17), ('de', 'Alguer', 'case', 2), ("l'", 'Alguer', 'det', 1), ('Alguer', 'ciutat', 'nmod', -3), ('i', 'tradicional', 'cc', 1), ('tradicional', 'Alguer', 'conj', -2), ('a', 'Catalunya', 'case', 1), ('Catalunya', 'ciutat', 'nmod', -7), ('d', 'Nord', 'case', 2), ('el', 'Nord', 'det', 1), ('Nord', 'Catalunya', 'flat', -3), (')', 'ciutat', 'punct', -11), ('o', 'valencià', 'cc', 1), ('valencià', 'català', 'conj', -30), ('(', 'denominació', 'punct', 1), ('denominació', 'català', 'appos', -32), ('oficial', 'denominació', 'amod', -1), ('a', 'País', 'case', 2), ('l', 'País', 'det', 1), ('País', 'denominació', 'nmod', -4), ('Valencià', 'País', 'flat', -1), ('i', 'tradicional', 'cc', 1), ('tradicional', 'denominació', 'conj', -7), ('a', 'Carxe', 'case', 2), ('l', 'Carxe', 'det', 1), ('Carxe', 'tradicional', 'nmod', -3), (')', 'denominació', 'punct', -11), ('és', 'llengua', 'cop', 2), ('una', 'llengua', 'det', 1), ('llengua', 'llengua', 'ROOT', 0), ('romànica', 'llengua', 'amod', -1), ('parlada', 'llengua', 'amod', -2), ('a', 'Catalunya', 'case', 1), ('Catalunya', 'llengua', 'obl', -4), (',', 'País', 'punct', 2), ('el', 'País', 'det', 1), ('País', 'llengua', 'appos', -7), ('Valencià', 'País', 'flat', -1), ('(', 'tret', 'punct', 1), ('tret', 'País', 'appos', -3), ("d'", 'comarques', 'case', 2), ('algunes', 'comarques', 'det', 1), ('comarques', 'tret', 'nmod', -3), ('i', 'localitats', 'cc', 1), ('localitats', 'comarques', 'conj', -2), ('de', 'interior', 'case', 2), ("l'", 'interior', 'det', 1), ('interior', 'comarques', 'nmod', -5), (')', 'tret', 'punct', -9), (',', 'Illes', 'punct', 2), ('les', 'Illes', 'det', 1), ('Illes', 'llengua', 'appos', -22), ('Balears', 'Illes', 'flat', -1), ('(', 'rep', 'punct', 3), ('on', 'rep', 'obl', 2), ('també', 'rep', 'advmod', 1), ('rep', 'Illes', 'acl', -5), ('el', 'nom', 'det', 1), ('nom', 'rep', 'obj', -2), ('de', 'mallorquí', 'case', 1), ('mallorquí', 'nom', 'nmod', -2), (',', 'menorquí', 'punct', 1), ('menorquí', 'mallorquí', 'conj', -2), (',', 'eivissenc', 'punct', 1), ('eivissenc', 'mallorquí', 'conj', -4), ('o', 'formenterer', 'cc', 1), ('formenterer', 'mallorquí', 'conj', -6), ('segons', 'illa', 'case', 2), ("l'", 'illa', 'det', 1), ('illa', 'formenterer', 'obl', -3), (')', 'rep', 'punct', -14), (',', 'Andorra', 'punct', 1), ('Andorra', 'llengua', 'appos', -43), (',', 'Franja', 'punct', 2), ('la', 'Franja', 'det', 1), ('Franja', 'llengua', 'appos', -46), ('de', 'Ponent', 'case', 1), ('Ponent', 'Franja', 'flat', -2), ('(', 'Aragó', 'punct', 3), ('a', 'Aragó', 'case', 2), ("l'", 'Aragó', 'det', 1), ('Aragó', 'Franja', 'nmod', -6), (')', 'Aragó', 'punct', -1), (',', 'ciutat', 'punct', 2), ('la', 'ciutat', 'det', 1), ('ciutat', 'llengua', 'appos', -56), ('de', 'Alguer', 'case', 2), ("l'", 'Alguer', 'det', 1), ('Alguer', 'ciutat', 'nmod', -3), ('(', 'illa', 'punct', 3), ('a', 'illa', 'case', 2), ("l'", 'illa', 'det', 1), ('illa', 'ciutat', 'nmod', -7), ('de', 'Sardenya', 'case', 1), ('Sardenya', 'illa', 'nmod', -2), (')', 'illa', 'punct', -3), (',', 'Catalunya', 'punct', 2), ('la', 'Catalunya', 'det', 1), ('Catalunya', 'llengua', 'appos', -69), ('d', 'Nord,[8', 'case', 2), ('el', 'Nord,[8', 'det', 1), ('Nord,[8', 'Catalunya', 'flat', -3), (']', 'Carxe', 'punct', 2), ('el', 'Carxe', 'det', 1), ('Carxe', 'Catalunya', 'flat', -6), ('(', 'territori', 'punct', 3), ('un', 'territori', 'det', 2), ('petit', 'territori', 'amod', 1), ('territori', 'Carxe', 'appos', -4), ('de', 'Múrcia', 'case', 1), ('Múrcia', 'territori', 'nmod', -2), ('poblat', 'territori', 'amod', -3), ('per', 'pobladors', 'case', 1), ('pobladors', 'poblat', 'obj', -2), ('valencians),[9][10', 'pobladors', 'amod', -1), (']', 'poblat', 'punct', -4), ('i', 'comunitats', 'cc', 2), ('en', 'comunitats', 'case', 1), ('comunitats', 'llengua', 'conj', -89), ('arreu', 'comunitats', 'advmod', -1), ('d', 'món', 'case', 2), ('el', 'món', 'det', 1), ('món', 'arreu', 'obl', -3), ('(', 'destaca', 'punct', 4), ('entre', 'quals', 'case', 2), ('les', 'quals', 'det', 1), ('quals', 'destaca', 'obl', 1), ('destaca', 'món', 'acl', -5), ('la', 'destaca', 'det', -1), ('de', 'la', 'case', -1), ("l'", 'Argentina', 'det', 1), ('Argentina', 'la', 'obj', -3), (',', '200.000', 'punct', 2), ('amb', '200.000', 'case', 1), ('200.000', 'parlants).[11', 'nummod', 1), ('parlants).[11', 'destaca', 'nsubj', -8), (']', 'parlants).[11', 'punct', -1)]
    elif lang == 'zho_cn':
        assert dependencies == [('汉语', '称', 'nsubj', 2), ('又', '称', 'advmod', 1), ('称', '称', 'ROOT', 0), ('中文', '华语', 'conj', 2), ('、', '华语', 'punct', 1), ('华语', ']', 'nmod:assmod', 2), ('[3', '华语', 'punct', -1), (']', '称', 'dobj', -5), ('、', '称', 'punct', -6), ('唐话', '[', 'compound:nn', 1), ('[', ']', 'dep', 2), ('4', ']', 'nummod', 1), (']', '称', 'dobj', -10), ('，', '称', 'punct', -11), ('概指', '称', 'conj', -12), ('由', '汉语', 'case', 2), ('上古', '汉语', 'compound:nn', 1), ('汉语', '概指', 'nmod:prep', -3), ('（', '秦雅言', 'punct', 2), ('先', '秦雅言', 'advmod', 1), ('秦雅言', '汉语', 'parataxis:prnmod', -3), ('）', '称', 'punct', -19), ('发展', '称', 'ccomp', -20), ('而', '来', 'aux:prtmod', 1), ('来', '分析语', 'acl', 6), ('、', '来', 'punct', -1), ('书面', '使用', 'advmod', 1), ('使用', '来', 'conj', -3), ('汉字', '使用', 'dobj', -1), ('的', '来', 'mark', -5), ('分析语', '发展', 'dobj', -8), ('，', '称', 'punct', -29), ('为', '语族', 'case', 8), ('汉藏', '语系', 'nmod:assmod', 1), ('语系', '大', 'nsubj', 2), ('最', '大', 'advmod', 1), ('大', '语族', 'amod', 4), ('的', '大', 'mark', -1), ('一', '语族', 'nummod', 2), ('支', '一', 'mark:clf', -1), ('语族', '称', 'conj', -38), ('。', '称', 'punct', -39)]
    elif lang == 'zho_tw':
        assert dependencies == [('漢語', '稱', 'nsubj', 2), ('又', '稱', 'advmod', 1), ('稱', '稱', 'ROOT', 0), ('中文', '[', 'conj', 3), ('、', '[', 'punct', 2), ('華語', '[', 'compound:nn', 1), ('[', ']', 'dep', 2), ('3', ']', 'nummod', 1), (']', '稱', 'dobj', -6), ('、', '稱', 'punct', -7), ('唐話[', '稱', 'conj', -8), ('4', '稱', 'nmod:range', -9), (']', '4', 'mark:clf', -1), ('，', '稱', 'punct', -11), ('概指', '稱', 'conj', -12), ('由', '漢語', 'case', 2), ('上古', '漢語', 'compound:nn', 1), ('漢語', '概指', 'nmod:prep', -3), ('（', '秦雅言', 'punct', 2), ('先', '秦雅言', 'advmod', 1), ('秦雅言', '漢語', 'parataxis:prnmod', -3), ('）', '稱', 'punct', -19), ('發展', '分析語', 'compound:nn', 8), ('而', '來', 'aux:prtmod', 1), ('來', '分析語', 'acl', 6), ('、', '來', 'punct', -1), ('書面', '使用', 'nsubj', 1), ('使用', '來', 'conj', -3), ('漢字', '使用', 'dobj', -1), ('的', '來', 'mark', -5), ('分析語', '分析語', 'ROOT', 0), ('，', '藏語', 'punct', 2), ('為漢', '藏語', 'dep', 1), ('藏語', '分析語', 'conj', -3), ('系', '大', 'nsubj', 2), ('最', '大', 'advmod', 1), ('大', '語族', 'amod', 4), ('的', '大', 'mark', -1), ('一', '語族', 'nummod', 2), ('支', '一', 'mark:clf', -1), ('語族', '藏語', 'conj', -7), ('。', '分析語', 'punct', -11)]
    elif lang == 'hrv':
        assert dependencies == [('Hrvatski', 'jezik', 'amod', 1), ('jezik', 'naziv', 'nsubj', 11), ('(', 'ISO', 'punct', 1), ('ISO', 'jezik', 'appos', -2), ('639', 'ISO', 'nummod', -1), ('-', 'ISO', 'nmod', -2), ('3', 'ISO', 'nmod', -3), (':', 'hrv', 'punct', 1), ('hrv', 'ISO', 'parataxis', -5), (')', 'hrv', 'punct', -1), ('skupni', 'naziv', 'amod', 2), ('je', 'naziv', 'cop', 1), ('naziv', 'naziv', 'ROOT', 0), ('za', 'jezik', 'case', 3), ('nacionalni', 'jezik', 'amod', 2), ('standardni', 'jezik', 'amod', 1), ('jezik', 'naziv', 'nmod', -4), ('Hrvata', 'jezik', 'nmod', -1), (',', 'skup', 'punct', 3), ('te', 'skup', 'cc', 2), ('za', 'skup', 'case', 1), ('skup', 'jezik', 'conj', -5), ('narječja', 'skup', 'nmod', -1), ('i', 'govora', 'cc', 1), ('govora', 'narječja', 'conj', -2), ('kojima', 'govore', 'obj', 1), ('govore', 'skup', 'acl', -5), ('ili', 'govorili', 'cc', 3), ('su', 'govorili', 'aux', 2), ('nekada', 'govorili', 'advmod', 1), ('govorili', 'govore', 'conj', -4), ('Hrvati', 'govorili', 'iobj', -1), ('.', 'naziv', 'punct', -20)]
    elif lang == 'dan':
        assert dependencies == [('Dansk', 'sprog', 'nsubj', 4), ('er', 'sprog', 'cop', 3), ('et', 'sprog', 'det', 2), ('østnordisk', 'sprog', 'amod', 1), ('sprog', 'sprog', 'ROOT', 0), ('indenfor', 'gren', 'case', 3), ('den', 'gren', 'det', 2), ('germanske', 'gren', 'amod', 1), ('gren', 'sprog', 'nmod', -4), ('af', 'sprogfamilie', 'case', 3), ('den', 'sprogfamilie', 'det', 2), ('indoeuropæiske', 'sprogfamilie', 'amod', 1), ('sprogfamilie', 'gren', 'nmod', -4), ('.', 'sprog', 'punct', -9)]
    elif lang == 'nld':
        assert dependencies == [('Het', 'Nederlands', 'det', 1), ('Nederlands', 'taal', 'nsubj', 4), ('is', 'taal', 'cop', 3), ('een', 'taal', 'det', 2), ('West-Germaanse', 'taal', 'amod', 1), ('taal', 'taal', 'ROOT', 0), ('en', 'taal', 'cc', 3), ('de', 'taal', 'det', 2), ('officiële', 'taal', 'amod', 1), ('taal', 'taal', 'conj', -4), ('van', 'Nederland', 'case', 1), ('Nederland', 'taal', 'nmod', -2), (',', 'Suriname', 'punct', 1), ('Suriname', 'Nederland', 'conj', -2), ('en', 'een', 'cc', 1), ('een', 'taal', 'conj', -6), ('van', 'talen', 'case', 4), ('de', 'talen', 'det', 3), ('drie', 'talen', 'nummod', 2), ('officiële', 'talen', 'amod', 1), ('talen', 'een', 'nmod', -5), ('van', 'België', 'case', 1), ('België', 'talen', 'nmod', -2), ('.', 'taal', 'punct', -18)]
    elif lang.startswith('eng_'):
        assert dependencies == [('English', 'is', 'nsubj', 1), ('is', 'is', 'ROOT', 0), ('a', 'language', 'det', 3), ('West', 'Germanic', 'compound', 1), ('Germanic', 'language', 'compound', 1), ('language', 'is', 'attr', -4), ('in', 'language', 'prep', -1), ('the', 'family', 'det', 5), ('Indo', 'European', 'compound', 2), ('-', 'European', 'punct', 1), ('European', 'family', 'amod', 2), ('language', 'family', 'compound', 1), ('family', 'in', 'pobj', -6), (',', 'is', 'punct', -12), ('with', 'is', 'prep', -13), ('its', 'forms', 'poss', 2), ('earliest', 'forms', 'amod', 1), ('forms', 'with', 'pobj', -3), ('spoken', 'forms', 'acl', -1), ('by', 'spoken', 'agent', -1), ('the', 'inhabitants', 'det', 1), ('inhabitants', 'by', 'pobj', -2), ('of', 'inhabitants', 'prep', -1), ('early', 'England.[3][4][5', 'amod', 2), ('medieval', 'England.[3][4][5', 'amod', 1), ('England.[3][4][5', 'of', 'pobj', -3), (']', 'is', 'punct', -25)]
    elif lang == 'fin':
        assert dependencies == [('Suomen', 'kieli', 'nmod:poss', 1), ('kieli', 'kieli', 'nsubj:cop', 9), ('eli', 'suomi', 'cc', 1), ('suomi', 'kieli', 'nsubj:cop', 7), ('on', 'kieli', 'cop', 6), ('uralilaisten', 'kielten', 'amod', 1), ('kielten', 'ryhmään', 'nmod:poss', 2), ('itämerensuomalaiseen', 'ryhmään', 'amod', 1), ('ryhmään', 'kuuluva', 'obl', 1), ('kuuluva', 'kieli', 'acl', 1), ('kieli', 'kieli', 'ROOT', 0), (',', 'puhuvat', 'punct', 2), ('jota', 'puhuvat', 'obj', 1), ('puhuvat', 'kieli', 'acl:relcl', -3), ('pääosin', 'suomalaiset', 'advmod', 1), ('suomalaiset', 'puhuvat', 'obj', -2), ('.', 'kieli', 'punct', -6)]
    elif lang == 'fra':
        assert dependencies == [('Le', 'français', 'det', 1), ('français', 'parlé', 'nsubj', 2), ('est', 'parlé', 'cop', 1), ('parlé', 'parlé', 'ROOT', 0), (',', 'parlé', 'punct', -1), ('en', '2023', 'case', 1), ('2023', 'parlé', 'obl:mod', -3), (',', 'parlé', 'punct', -4), ('sur', 'continents', 'case', 3), ('tous', 'continents', 'amod', 2), ('les', 'continents', 'det', 1), ('continents', 'parlé', 'obl:arg', -8), ('par', 'millions', 'case', 3), ('environ', 'millions', 'advmod', 2), ('321', 'millions', 'nummod', 1), ('millions', 'continents', 'nmod', -4), ('de', 'personnes5,2', 'case', 1), ('personnes5,2', 'millions', 'nmod', -2), (':', 'millions', 'punct', -3), ('235', 'millions', 'nummod', 1), ('millions', 'emploient', 'nsubj', 2), ("l'", 'emploient', 'det', 1), ('emploient', 'continents', 'acl:relcl', -11), ('quotidiennement', 'emploient', 'advmod', -1), (',', 'emploient', 'punct', -2), ('et', 'millions3', 'cc', 2), ('90', 'millions3', 'nummod', 1), ('millions3', 'emploient', 'conj', -5), ('en', 'millions3', 'advmod', -1), ('sont', 'locuteurs', 'cop', 2), ('des', 'locuteurs', 'det', 1), ('locuteurs', 'millions3', 'dep', -4), ('natifs', 'locuteurs', 'amod', -1), ('.', 'parlé', 'punct', -30)]
    elif lang.startswith('deu_'):
        assert dependencies == [('Das', 'Deutsche', 'nk', 1), ('Deutsche', 'ist', 'sb', 1), ('ist', 'ist', 'ROOT', 0), ('eine', 'Sprache', 'nk', 2), ('plurizentrische', 'Sprache', 'nk', 1), ('Sprache', 'ist', 'pd', -3), (',', 'ist', 'punct', -4), ('enthält', 'ist', 'cj', -5), ('also', 'enthält', 'mo', -1), ('mehrere', 'Standardvarietäten', 'nk', 1), ('Standardvarietäten', 'enthält', 'oa', -3), ('in', 'Standardvarietäten', 'mnr', -1), ('verschiedenen', 'Regionen', 'nk', 1), ('Regionen', 'in', 'nk', -2), ('.', 'ist', 'punct', -12)]
    elif lang == 'ell':
        assert dependencies == [('Η', 'γλώσσα', 'det', 2), ('ελληνική', 'γλώσσα', 'amod', 1), ('γλώσσα', 'ανήκει', 'nsubj', 1), ('ανήκει', 'ανήκει', 'ROOT', 0), ('στην', 'οικογένεια[9', 'case', 2), ('ινδοευρωπαϊκή', 'στην', 'fixed', -1), ('οικογένεια[9', ']', 'amod', 1), (']', 'ανήκει', 'obj', -4), ('και', 'αποτελεί', 'cc', 1), ('αποτελεί', 'ανήκει', 'conj', -6), ('το', 'μέλος', 'det', 2), ('μοναδικό', 'μέλος', 'amod', 1), ('μέλος', 'αποτελεί', 'obj', -3), ('του', 'κλάδου', 'det', 2), ('ελληνικού', 'κλάδου', 'amod', 1), ('κλάδου', 'μέλος', 'nmod', -3), (',', 'γλώσσα', 'punct', 5), ('ενώ', 'γλώσσα', 'mark', 4), ('είναι', 'γλώσσα', 'cop', 3), ('η', 'γλώσσα', 'det', 2), ('επίσημη', 'γλώσσα', 'amod', 1), ('γλώσσα', 'ανήκει', 'conj', -18), ('της', 'Ελλάδας', 'det', 1), ('Ελλάδας', 'γλώσσα', 'nmod', -2), ('και', 'Κύπρου', 'cc', 2), ('της', 'Κύπρου', 'det', 1), ('Κύπρου', 'Ελλάδας', 'conj', -3), ('.', 'ανήκει', 'punct', -24)]
    elif lang == 'ita':
        assert dependencies == [('È', 'classificato', 'aux:pass', 1), ('classificato', 'classificato', 'ROOT', 0), ('al', '23º', 'case', 1), ('23º', 'posto', 'nummod', 1), ('posto', 'classificato', 'obl', -3), ('tra', 'lingue', 'case', 2), ('le', 'lingue', 'det', 1), ('lingue', 'posto', 'nmod', -3), ('per', 'numero', 'case', 1), ('numero', 'lingue', 'nmod', -2), ('di', 'parlanti', 'case', 1), ('parlanti', 'numero', 'nmod', -2), ('nel', 'mondo', 'case', 1), ('mondo', 'parlanti', 'nmod', -2), ('e', 'utilizzato', 'cc', 6), (',', 'utilizzato', 'punct', 5), ('in', 'Italia', 'case', 1), ('Italia', 'utilizzato', 'obl', 3), (',', 'Italia', 'punct', -1), ('è', 'utilizzato', 'aux:pass', 1), ('utilizzato', 'classificato', 'conj', -19), ('da', 'milioni', 'case', 3), ('circa', '58', 'advmod', 1), ('58', 'milioni', 'nummod', 1), ('milioni', 'utilizzato', 'obl', -4), ('di', 'residenti.[2', 'case', 1), ('residenti.[2', 'milioni', 'nmod', -2), (']', 'utilizzato', 'punct', -7)]
    elif lang == 'jpn':
        assert dependencies == [('日本', 'ご', 'compound', 4), ('語', 'ご', 'compound', 3), ('（', 'ご', 'compound', 2), ('にほん', 'ご', 'compound', 1), ('ご', '）', 'nmod', 8), ('、', 'ご', 'punct', -1), ('にっぽん', 'ご', 'compound', 1), ('ご', '）', 'compound', 5), ('[', '）', 'punct', 4), ('注', '）', 'compound', 3), ('2', '）', 'compound', 2), (']', '）', 'punct', 1), ('）', '言語', 'nsubj', 35), ('は', '）', 'case', -1), ('、', '）', 'punct', -2), ('日本', '内', 'compound', 2), ('国', '内', 'compound', 1), ('内', '領', 'nmod', 6), ('や', '内', 'case', -1), ('、', '内', 'punct', -2), ('かつて', '領', 'advmod', 3), ('の', 'かつて', 'case', -1), ('日本', '領', 'compound', 1), ('領', '国', 'acl', 3), ('だっ', '領', 'cop', -1), ('た', '領', 'aux', -2), ('国', '使用', 'obl', 16), ('、', '国', 'punct', -1), ('そして', '使用', 'cc', 14), ('国外', '移民', 'compound', 1), ('移民', '者', 'nmod', 3), ('や', '移民', 'case', -1), ('移住', '者', 'compound', 1), ('者', '含む', 'obj', 2), ('を', '者', 'case', -1), ('含む', '同士', 'acl', 3), ('日本', '同士', 'compound', 2), ('人', '同士', 'compound', 1), ('同士', '間', 'nmod', 2), ('の', '同士', 'case', -1), ('間', '使用', 'obl', 2), ('で', '間', 'case', -1), ('使用', '言語', 'acl', 5), ('さ', '使用', 'aux', -1), ('れ', '使用', 'aux', -2), ('て', '使用', 'mark', -3), ('いる', 'て', 'fixed', -1), ('言語', '言語', 'ROOT', 0), ('。', '言語', 'punct', -1)]
    elif lang == 'kor':
        assert dependencies == [('한국어', '공용어이다', 'dislocated', 7), ('(', '韓國語', 'punct', 1), ('韓國語', '한국어', 'appos', -2), (')', '韓國語', 'punct', -1), ('는', '한국어', 'case', -4), ('대한민국과', '조선민주주의인민공화국의', 'compound', 1), ('조선민주주의인민공화국의', '공용어이다', 'nsubj', 1), ('공용어이다', '공용어이다', 'ROOT', 0), ('.', '공용어이다', 'punct', -1)]
    elif lang == 'lit':
        assert dependencies == [('Lietuvių', 'kalba', 'nmod', 1), ('kalba', 'kalba', 'ROOT', 0), ('–', 'kalba', 'punct', 7), ('iš', 'prokalbės', 'case', 2), ('baltų', 'iš', 'advmod:emph', -1), ('prokalbės', 'kilusi', 'obl:arg', 1), ('kilusi', 'kalba', 'acl', 3), ('lietuvių', 'tautos', 'nmod', 1), ('tautos', 'kalba', 'nmod', 1), ('kalba', 'kalba', 'ROOT', 0), (',', 'kuri', 'punct', 1), ('kuri', 'kalba', 'conj', -2), ('Lietuvoje', 'kuri', 'advmod:emph', -1), ('yra', 'kuri', 'advmod:emph', -2), ('valstybinė', 'kuri', 'advmod:emph', -3), (',', 'Sąjungoje', 'punct', 3), ('o', 'Sąjungoje', 'cc', 2), ('Europos', 'Sąjungoje', 'nmod', 1), ('Sąjungoje', 'valstybinė', 'conj', -4), ('–', 'viena', 'punct', 1), ('viena', 'kuri', 'appos', -9), ('iš', 'kalbų', 'case', 2), ('oficialiųjų', 'kalbų', 'acl', 1), ('kalbų', 'viena', 'obl:arg', -3), ('.', '.', 'ROOT', 0)]
    elif lang == 'mkd':
        assert dependencies == [('Македонски', 'јазик', 'att', 1), ('јазик', 'јазик', 'ROOT', 0), ('—', 'јазик', 'punct', -1), ('јужнословенски', 'јазик', 'att', 1), ('јазик', 'јазик', 'dep', -3), (',', 'јазик', 'punct', -4), ('дел', 'јазик', 'dep', -5), ('од', 'дел', 'prep', -1), ('групата', 'од', 'pobj', -1), ('на', 'групата', 'prep', -1), ('словенски', 'јазици', 'att', 1), ('јазици', 'од', 'pobj', -4), ('од', 'јазици', 'prep', -1), ('јазичното', 'семејство', 'att', 1), ('семејство', 'од', 'dobj', -2), ('на', 'семејство', 'prep', -1), ('индоевропски', 'јазици', 'att', 1), ('јазици', 'на', 'pobj', -2), ('.', '.', 'ROOT', 0)]
    elif lang == 'nob':
        assert dependencies == [('Bokmål', 'varietet', 'nsubj', 3), ('er', 'varietet', 'cop', 2), ('en', 'varietet', 'det', 1), ('varietet', 'varietet', 'ROOT', 0), ('av', 'skriftspråk', 'case', 2), ('norsk', 'skriftspråk', 'amod', 1), ('skriftspråk', 'varietet', 'obl', -3), ('.', 'varietet', 'punct', -4)]
    elif lang == 'pol':
        assert dependencies == [('Język', 'Język', 'ROOT', 0), ('polski', 'Język', 'amod', -1), (',', 'polszczyzna', 'punct', 1), ('polszczyzna', 'Język', 'amod', -3), ('–', 'język', 'punct', 1), ('język', 'Język', 'appos', -5), ('lechicki', 'język', 'amod', -1), ('z', 'grupy', 'case', 1), ('grupy', 'język', 'nmod', -3), ('zachodniosłowiańskiej', 'grupy', 'amod', -1), ('(', 'należą', 'punct', 3), ('do', 'której', 'case', 1), ('której', 'należą', 'obl:arg', 1), ('należą', 'Język', 'acl:relcl', -13), ('również', 'czeski', 'advmod:emph', 1), ('czeski', 'należą', 'nsubj', -2), (',', 'kaszubski', 'punct', 1), ('kaszubski', 'należą', 'conj', -4), (',', 'słowacki', 'punct', 1), ('słowacki', 'należą', 'conj', -6), ('i', 'języki', 'cc', 1), ('języki', 'należą', 'conj', -8), ('łużyckie', 'języki', 'amod', -1), (')', 'należą', 'punct', -10), (',', 'stanowiącej', 'punct', 1), ('stanowiącej', 'Język', 'acl', -25), ('część', 'stanowiącej', 'xcomp:pred', -1), ('rodziny', 'część', 'nmod:arg', -1), ('indoeuropejskiej', 'rodziny', 'amod', -1), ('.', 'Język', 'punct', -29)]
    elif lang.startswith('por_'):
        assert dependencies == [('A', 'língua', 'det', 1), ('língua', 'língua', 'nsubj', 9), ('portuguesa', 'língua', 'amod', -1), (',', 'designada', 'punct', 2), ('também', 'designada', 'advmod', 1), ('designada', 'língua', 'acl', -4), ('português', 'designada', 'amod', -1), (',', 'designada', 'punct', -2), ('é', 'língua', 'cop', 2), ('uma', 'língua', 'det', 1), ('língua', 'língua', 'ROOT', 0), ('indo-europeia', 'língua', 'amod', -1), ('românica', 'indo-europeia', 'flat:name', -1), ('flexiva', 'língua', 'amod', -3), ('ocidental', 'língua', 'amod', -4), ('originada', 'língua', 'acl', -5), ('no', 'galego-português', 'case', 1), ('galego-português', 'originada', 'obl', -2), ('falado', 'galego-português', 'acl', -1), ('no', 'Reino', 'case', 1), ('Reino', 'falado', 'obl', -2), ('da', 'Galiza', 'case', 1), ('Galiza', 'Reino', 'nmod', -2), ('e', 'norte', 'cc', 2), ('no', 'norte', 'case', 1), ('norte', 'Reino', 'conj', -5), ('de', 'Portugal', 'case', 1), ('Portugal', 'norte', 'nmod', -2), ('.', 'língua', 'punct', -18)]
    elif lang == 'ron':
        assert dependencies == [('Limba', 'limbă', 'nsubj', 4), ('română', 'Limba', 'amod', -1), ('este', 'limbă', 'cop', 2), ('o', 'limbă', 'det', 1), ('limbă', 'limbă', 'ROOT', 0), ('indo-europeană', 'limbă', 'amod', -1), ('din', 'grupul', 'case', 1), ('grupul', 'limbă', 'nmod', -3), ('italic', 'grupul', 'amod', -1), ('și', 'subgrupul', 'cc', 2), ('din', 'subgrupul', 'case', 1), ('subgrupul', 'grupul', 'conj', -4), ('oriental', 'subgrupul', 'amod', -1), ('al', 'limbilor', 'det', 1), ('limbilor', 'subgrupul', 'nmod', -3), ('romanice', 'limbilor', 'amod', -1), ('.', 'limbă', 'punct', -12)]
    elif lang == 'rus':
        assert dependencies == [('Ру́сский', 'язы́к', 'amod', 1), ('язы́к', 'язык', 'nsubj', 16), ('(', 'ˈruskʲɪi̯', 'punct', 2), ('[', 'ˈruskʲɪi̯', 'punct', 1), ('ˈruskʲɪi̯', 'язы́к', 'appos', -3), ('jɪˈzɨk', 'ˈruskʲɪi̯', 'flat:foreign', -1), (']', 'ˈruskʲɪi̯', 'punct', -2), ('Информация', 'язы́к', 'appos', -6), ('о', 'файле', 'case', 1), ('файле', 'Информация', 'nmod', -2), ('слушать)[~', 'файле', 'nmod', -1), ('3', 'слушать)[~', 'appos', -1), (']', 'Информация', 'punct', -5), ('[', '⇨', 'punct', 1), ('⇨', 'Информация', 'appos', -7), (']', '⇨', 'punct', -1), ('—', 'язык', 'punct', 1), ('язык', 'язык', 'ROOT', 0), ('восточнославянской', 'группы', 'amod', 1), ('группы', 'язык', 'nmod', -2), ('славянской', 'ветви', 'amod', 1), ('ветви', 'группы', 'nmod', -2), ('индоевропейской', 'семьи', 'amod', 2), ('языковой', 'семьи', 'amod', 1), ('семьи', 'ветви', 'nmod', -3), (',', 'язык', 'punct', 2), ('национальный', 'язык', 'amod', 1), ('язык', 'язык', 'appos', -10), ('русского', 'народа', 'amod', 1), ('народа', 'язык', 'nmod', -2), ('.', 'язык', 'punct', -13)]
    elif lang == 'spa':
        assert dependencies == [('El', 'español', 'det', 1), ('español', 'lengua', 'nsubj', 5), ('o', 'castellano', 'cc', 1), ('castellano', 'español', 'conj', -2), ('es', 'lengua', 'cop', 2), ('una', 'lengua', 'det', 1), ('lengua', 'romance', 'amod', 1), ('romance', 'romance', 'ROOT', 0), ('procedente', 'romance', 'amod', -1), ('del', 'latín', 'case', 1), ('latín', 'procedente', 'nmod', -2), ('hablado', 'latín', 'amod', -1), (',', 'perteneciente', 'punct', 1), ('perteneciente', 'latín', 'amod', -3), ('a', 'familia', 'case', 2), ('la', 'familia', 'det', 1), ('familia', 'perteneciente', 'nmod', -3), ('de', 'lenguas', 'case', 1), ('lenguas', 'familia', 'nmod', -2), ('indoeuropeas', 'lenguas', 'amod', -1), ('.', 'romance', 'punct', -13)]
    elif lang == 'swe':
        assert dependencies == [('Svenska', 'språk', 'amod', 11), ('(', 'Svenska', 'punct', -1), ('svenska', 'Svenska', 'appos', -2), ('\u2009', 'svenska', 'dep', -1), ('(', 'svenska', 'punct', -2), ('info', 'svenska', 'appos', -3), (')', 'svenska', 'punct', -4), (')', 'Svenska', 'punct', -7), ('är', 'språk', 'cop', 3), ('ett', 'språk', 'det', 2), ('östnordiskt', 'språk', 'amod', 1), ('språk', 'språk', 'ROOT', 0), ('som', 'talas', 'nsubj:pass', 1), ('talas', 'språk', 'acl:relcl', -2), ('av', 'personer', 'case', 4), ('ungefär', 'tio', 'advmod', 1), ('tio', 'miljoner', 'nummod', 1), ('miljoner', 'personer', 'nmod', 1), ('personer', 'talas', 'obl:agent', -5), ('främst', 'personer', 'nmod', -1), ('i', 'Sverige', 'case', 1), ('Sverige', 'talas', 'obl', -8), ('där', 'har', 'advmod', 2), ('språket', 'har', 'nsubj', 1), ('har', 'talas', 'dep', -11), ('en', 'ställning', 'det', 2), ('dominant', 'ställning', 'amod', 1), ('ställning', 'har', 'obj', -3), ('som', 'huvudspråk', 'mark', 1), ('huvudspråk', 'ställning', 'acl', -2), (',', 'nationalspråket', 'punct', 6), ('men', 'nationalspråket', 'cc', 5), ('även', 'nationalspråket', 'advmod', 4), ('som', 'nationalspråket', 'case', 3), ('det', 'nationalspråket', 'det', 2), ('ena', 'nationalspråket', 'amod', 1), ('nationalspråket', 'huvudspråk', 'conj', -7), ('i', 'Finland', 'case', 1), ('Finland', 'nationalspråket', 'nmod', -2), ('och', 'språk', 'cc', 4), ('som', 'språk', 'mark', 3), ('enda', 'språk', 'amod', 2), ('officiella', 'språk', 'amod', 1), ('språk', 'Finland', 'conj', -5), ('på', 'Åland', 'case', 1), ('Åland', 'språk', 'nmod', -2), ('.', 'språk', 'punct', -35)]
    elif lang == 'ukr':
        assert dependencies == [('Украї́нська', 'мо́ва', 'amod', 1), ('мо́ва', 'ру́ська', 'nsubj', 12), ('(', 'МФА', 'punct', 1), ('МФА', 'мо́ва', 'appos', -2), (':', '[', 'punct', 1), ('[', 'МФА', 'parataxis', -2), ('ukrɑ̽ˈjɪnʲsʲkɑ̽', '[', 'flat:foreign', -1), ('ˈmɔwɑ̽', '[', 'flat:foreign', -2), (']', '[', 'punct', -3), (',', 'назви', 'punct', 2), ('історичні', 'назви', 'amod', 1), ('назви', 'мо́ва', 'conj', -10), ('—', 'ру́ська', 'punct', 1), ('ру́ська', 'ру́ська', 'ROOT', 0), (',', 'руси́нська[10][11][12', 'punct', 1), ('руси́нська[10][11][12', 'ру́ська', 'conj', -2), (']', 'ру́ська', 'punct', -3), ('[', 'ру́ська', 'nmod', -4), ('*', 'ру́ська', 'punct', -5), ('1', 'ру́ська', 'dep', -6), (']', 'ру́ська', 'parataxis', -7), (')', 'ру́ська', 'punct', -8), ('—', 'мова', 'punct', 2), ('національна', 'мова', 'amod', 1), ('мова', 'мова', 'ROOT', 0), ('українців', 'мова', 'nmod', -1), ('.', 'мова', 'punct', -2)]
    else:
        raise wl_test_init.Wl_Exception_Tests_Lang_Skipped(lang)

if __name__ == '__main__':
    for lang, dependency_parser in test_dependency_parsers:
        test_dependency_parse(lang, dependency_parser)
