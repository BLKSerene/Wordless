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

    dependency_parser_skipped = False

    if lang == 'cat':
        assert dependencies == [('El', 'català', 'det', 1), ('català', 'llengua', 'nsubj', 46), ('(', 'denominació', 'punct', 1), ('denominació', 'català', 'appos', -2), ('oficial', 'denominació', 'amod', -1), ('a', 'Catalunya', 'case', 1), ('Catalunya', 'denominació', 'nmod', -3), (',', 'Illes', 'punct', 3), ('a', 'Illes', 'case', 2), ('les', 'Illes', 'det', 1), ('Illes', 'català', 'nmod', -9), ('Balears', 'Illes', 'flat', -1), (',', 'Andorra', 'punct', 2), ('a', 'Andorra', 'case', 1), ('Andorra', 'Illes', 'nmod', -4), (',', 'ciutat', 'punct', 3), ('a', 'ciutat', 'case', 2), ('la', 'ciutat', 'det', 1), ('ciutat', 'català', 'nmod', -17), ('de', 'Alguer', 'case', 2), ("l'", 'Alguer', 'det', 1), ('Alguer', 'ciutat', 'nmod', -3), ('i', 'tradicional', 'cc', 1), ('tradicional', 'Alguer', 'conj', -2), ('a', 'Catalunya', 'case', 1), ('Catalunya', 'ciutat', 'nmod', -7), ('d', 'Nord', 'case', 2), ('el', 'Nord', 'det', 1), ('Nord', 'Catalunya', 'flat', -3), (')', 'ciutat', 'punct', -11), ('o', 'valencià', 'cc', 1), ('valencià', 'català', 'conj', -30), ('(', 'denominació', 'punct', 1), ('denominació', 'valencià', 'appos', -2), ('oficial', 'denominació', 'amod', -1), ('a', 'País', 'case', 2), ('l', 'País', 'det', 1), ('País', 'denominació', 'nmod', -4), ('Valencià', 'País', 'flat', -1), ('i', 'tradicional', 'cc', 1), ('tradicional', 'País', 'conj', -3), ('a', 'Carxe', 'case', 2), ('l', 'Carxe', 'det', 1), ('Carxe', 'denominació', 'nmod', -10), (')', 'denominació', 'punct', -11), ('és', 'llengua', 'cop', 2), ('una', 'llengua', 'det', 1), ('llengua', 'llengua', 'ROOT', 0), ('romànica', 'llengua', 'amod', -1), ('parlada', 'llengua', 'amod', -2), ('a', 'Catalunya', 'case', 1), ('Catalunya', 'parlada', 'obj', -2), (',', 'País', 'punct', 2), ('el', 'País', 'det', 1), ('País', 'Catalunya', 'flat', -3), ('Valencià', 'País', 'flat', -1), ('(', 'tret', 'punct', 1), ('tret', 'llengua', 'dep', -10), ("d'", 'tret', 'fixed', -1), ('algunes', 'comarques', 'det', 1), ('comarques', 'tret', 'conj', -3), ('i', 'localitats', 'cc', 1), ('localitats', 'comarques', 'conj', -2), ('de', 'interior', 'case', 2), ("l'", 'interior', 'det', 1), ('interior', 'comarques', 'nmod', -5), (')', 'tret', 'punct', -9), (',', 'Illes', 'punct', 2), ('les', 'Illes', 'det', 1), ('Illes', 'llengua', 'appos', -22), ('Balears', 'Illes', 'flat', -1), (',', 'Andorra', 'punct', 1), ('Andorra', 'Illes', 'flat', -3), (',', 'Franja', 'punct', 2), ('la', 'Franja', 'det', 1), ('Franja', 'llengua', 'appos', -28), ('de', 'Ponent', 'case', 1), ('Ponent', 'Franja', 'flat', -2), ('(', 'Aragó', 'punct', 3), ('a', 'Aragó', 'case', 2), ("l'", 'Aragó', 'det', 1), ('Aragó', 'Franja', 'nmod', -6), (')', 'Aragó', 'punct', -1), (',', 'ciutat', 'punct', 2), ('la', 'ciutat', 'det', 1), ('ciutat', 'llengua', 'appos', -38), ('de', 'Alguer', 'case', 2), ("l'", 'Alguer', 'det', 1), ('Alguer', 'ciutat', 'nmod', -3), ('(', 'illa', 'punct', 3), ('a', 'illa', 'case', 2), ("l'", 'illa', 'det', 1), ('illa', 'ciutat', 'nmod', -7), ('de', 'Sardenya', 'case', 1), ('Sardenya', 'illa', 'nmod', -2), (')', 'illa', 'punct', -3), (',', 'Catalunya', 'punct', 2), ('la', 'Catalunya', 'det', 1), ('Catalunya', 'llengua', 'appos', -51), ('d', 'Nord,[8', 'case', 2), ('el', 'Nord,[8', 'det', 1), ('Nord,[8', 'Catalunya', 'flat', -3), (']', 'Catalunya', 'punct', -4), ('el', 'Carxe', 'det', 1), ('Carxe', 'Catalunya', 'flat', -6), ('(', 'territori', 'punct', 3), ('un', 'territori', 'det', 2), ('petit', 'territori', 'amod', 1), ('territori', 'Carxe', 'appos', -4), ('de', 'Múrcia', 'case', 1), ('Múrcia', 'territori', 'nmod', -2), ('poblat', 'territori', 'amod', -3), ('per', 'pobladors', 'case', 1), ('pobladors', 'poblat', 'obj', -2), ('valencians),[9][10', 'pobladors', 'amod', -1), (']', 'territori', 'punct', -7), ('i', 'comunitats', 'cc', 2), ('en', 'comunitats', 'case', 1), ('comunitats', 'llengua', 'conj', -71), ('arreu', 'comunitats', 'advmod', -1), ('d', 'món', 'case', 2), ('el', 'món', 'det', 1), ('món', 'arreu', 'obl', -3), ('(', 'destaca', 'punct', 4), ('entre', 'quals', 'case', 2), ('les', 'quals', 'det', 1), ('quals', 'destaca', 'obl', 1), ('destaca', 'comunitats', 'acl', -9), ('la', 'destaca', 'det', -1), ('de', 'la', 'case', -1), ("l'", 'Argentina', 'det', 1), ('Argentina', 'la', 'obj', -3), (',', 'parlants).[11', 'punct', 3), ('amb', 'parlants).[11', 'case', 2), ('200.000', 'parlants).[11', 'nummod', 1), ('parlants).[11', 'Argentina', 'nmod', -4), (']', 'parlants).[11', 'punct', -1)]
    elif lang == 'zho_cn':
        assert dependencies == [('汉语', '称', 'nsubj', 2), ('又', '称', 'advmod', 1), ('称', '称', 'ROOT', 0), ('华语', ']', 'compound:nn', 2), ('[3', ']', 'name', 1), (']', '唐话', 'conj', 2), ('、', '唐话', 'punct', 1), ('唐话', '[', 'nsubj', 1), ('[', '称', 'ccomp', -6), ('4', ']', 'dep', 1), (']', '[', 'dobj', -2), ('，', '称', 'punct', -9), ('概指', '称', 'conj', -10), ('由', '汉语', 'case', 2), ('上古', '汉语', 'compound:nn', 1), ('汉语', '发展', 'nmod:prep', 5), ('（', '先', 'punct', 1), ('先', '秦雅言', 'advmod', 1), ('秦雅言', '汉语', 'dep', -3), ('）', '秦雅言', 'punct', -1), ('发展', '概指', 'ccomp', -8), ('而', '来', 'aux:prtmod', 1), ('来', '发展', 'conj', -2), ('、', '发展', 'punct', -3), ('书面', '使用', 'advmod', 1), ('使用', '发展', 'conj', -5), ('汉字', '分析语', 'nmod:assmod', 2), ('的', '汉字', 'case', -1), ('分析语', '使用', 'dobj', -3), ('，', '称', 'punct', -27), ('为', '语族', 'cop', 8), ('汉藏', '语系', 'nmod:assmod', 1), ('语系', '大', 'nsubj', 2), ('最', '大', 'advmod', 1), ('大', '语族', 'amod', 4), ('的', '大', 'mark', -1), ('一', '语族', 'nummod', 2), ('支', '一', 'mark:clf', -1), ('语族', '称', 'conj', -36), ('。', '称', 'punct', -37)]
    elif lang == 'zho_tw':
        assert dependencies == [('漢語', '稱華', 'nsubj', 2), ('又', '稱華', 'advmod', 1), ('稱華', '稱華', 'ROOT', 0), ('語[', ']', 'compound:nn', 2), ('3', ']', 'dep', 1), (']', '稱華', 'dobj', -3), ('、', '稱華', 'punct', -4), ('唐話[', '稱華', 'dep', -5), ('4', ']', 'dep', 1), (']', '稱華', 'dobj', -7), ('，', '稱華', 'punct', -8), ('概指', '稱華', 'conj', -9), ('由', '漢語', 'case', 2), ('上古', '漢語', 'compound:nn', 1), ('漢語', '概指', 'nmod:prep', -3), ('（', '漢語', 'punct', -1), ('先', '秦雅言', 'advmod', 1), ('秦雅言', '漢語', 'parataxis:prnmod', -3), ('）', '秦雅言', 'punct', -1), ('發展', '漢語', 'dep', -5), ('而', '來', 'aux:prtmod', 1), ('來', '分析語', 'acl', 6), ('、', '來', 'punct', -1), ('書面', '使用', 'nsubj', 1), ('使用', '來', 'conj', -3), ('漢字', '使用', 'dobj', -1), ('的', '來', 'mark', -5), ('分析語', '概指', 'dobj', -16), ('，', '稱華', 'punct', -26), ('為漢', '藏語', 'nsubj', 1), ('藏語', '系', 'compound:nn', 1), ('系', '大', 'nsubj', 2), ('最', '大', 'advmod', 1), ('大', '語族', 'amod', 4), ('的', '大', 'mark', -1), ('一', '語族', 'nummod', 2), ('支', '一', 'mark:clf', -1), ('語族', '稱華', 'dobj', -35), ('。', '稱華', 'punct', -36)]
    elif lang == 'hrv':
        assert dependencies == [('Hrvatski', 'jezik', 'amod', 1), ('jezik', 'arhivirana', 'nsubj:pass', 13), ('(', 'ISO', 'punct', 1), ('ISO', 'jezik', 'appos', -2), ('639', 'ISO', 'compound', -1), ('-', 'ISO', 'nmod', -2), ('3', 'ISO', 'conj', -3), (':', 'ISO', 'punct', -4), ('hrv', 'arhivirana', 'nsubj:pass', 6), ('\u2002', 'hrv', 'dep', -1), ('Inačica', 'hrv', 'flat', -2), ('izvorne', 'stranice', 'amod', 1), ('stranice', 'Inačica', 'conj', -2), ('\u2002', 'stranice', 'dep', -1), ('arhivirana', 'arhivirana', 'ROOT', 0), ('18', 'rujna', 'amod', 2), ('.', 'rujna', 'amod', 1), ('rujna', 'arhivirana', 'obl', -3), ('2012', 'rujna', 'amod', -1), ('.', 'rujna', 'amod', -2), (')', 'arhivirana', 'punct', -6), ('skupni', 'skupni', 'ROOT', 0), ('je', 'skupni', 'cop', -1), ('naziv', 'skupni', 'nsubj', -2), ('za', 'jezik', 'case', 3), ('nacionalni', 'jezik', 'amod', 2), ('standardni', 'jezik', 'amod', 1), ('jezik', 'naziv', 'nmod', -4), ('Hrvata', 'jezik', 'nmod', -1), (',', 'skup', 'punct', 3), ('te', 'skup', 'cc', 2), ('za', 'skup', 'case', 1), ('skup', 'naziv', 'conj', -9), ('narječja', 'skup', 'nmod', -1), ('i', 'govora', 'cc', 1), ('govora', 'narječja', 'conj', -2), ('kojima', 'govore', 'obj', 1), ('govore', 'govora', 'acl', -2), ('ili', 'govorili', 'cc', 3), ('su', 'govorili', 'aux', 2), ('nekada', 'govorili', 'advmod', 1), ('govorili', 'govore', 'conj', -4), ('Hrvati', 'govorili', 'obj', -1), ('.', 'skupni', 'punct', -22)]
    elif lang == 'dan':
        assert dependencies == [('Dansk', 'sprog', 'nsubj', 4), ('er', 'sprog', 'cop', 3), ('et', 'sprog', 'det', 2), ('østnordisk', 'sprog', 'amod', 1), ('sprog', 'sprog', 'ROOT', 0), ('indenfor', 'gren', 'case', 3), ('den', 'gren', 'det', 2), ('germanske', 'gren', 'amod', 1), ('gren', 'sprog', 'nmod', -4), ('af', 'sprogfamilie', 'case', 3), ('den', 'sprogfamilie', 'det', 2), ('indoeuropæiske', 'sprogfamilie', 'amod', 1), ('sprogfamilie', 'gren', 'nmod', -4), ('.', 'sprog', 'punct', -9)]
    elif lang == 'nld':
        assert dependencies == [('Het', 'Nederlands', 'det', 1), ('Nederlands', 'taal', 'nsubj', 4), ('is', 'taal', 'cop', 3), ('een', 'taal', 'det', 2), ('West-Germaanse', 'taal', 'amod', 1), ('taal', 'taal', 'ROOT', 0), ('en', 'taal', 'cc', 3), ('de', 'taal', 'det', 2), ('officiële', 'taal', 'amod', 1), ('taal', 'taal', 'conj', -4), ('van', 'Nederland', 'case', 1), ('Nederland', 'taal', 'nmod', -2), (',', 'Suriname', 'punct', 1), ('Suriname', 'Nederland', 'conj', -2), ('en', 'een', 'cc', 1), ('een', 'taal', 'conj', -6), ('van', 'talen', 'case', 4), ('de', 'talen', 'det', 3), ('drie', 'talen', 'nummod', 2), ('officiële', 'talen', 'amod', 1), ('talen', 'een', 'nmod', -5), ('van', 'België', 'case', 1), ('België', 'talen', 'nmod', -2), ('.', 'taal', 'punct', -18)]
    elif lang.startswith('eng_'):
        assert dependencies == [('English', 'is', 'nsubj', 1), ('is', 'is', 'ROOT', 0), ('a', 'language', 'det', 3), ('West', 'Germanic', 'compound', 1), ('Germanic', 'language', 'compound', 1), ('language', 'is', 'attr', -4), ('of', 'language', 'prep', -1), ('the', 'family', 'det', 5), ('Indo', 'European', 'amod', 2), ('-', 'European', 'punct', 1), ('European', 'family', 'amod', 2), ('language', 'family', 'compound', 1), ('family', 'of', 'pobj', -6), (',', 'is', 'punct', -12), ('originally', 'spoken', 'advmod', 1), ('spoken', 'is', 'advcl', -14), ('by', 'spoken', 'agent', -1), ('the', 'inhabitants', 'det', 1), ('inhabitants', 'by', 'pobj', -2), ('of', 'inhabitants', 'prep', -1), ('early', 'England.[3][4][5', 'amod', 2), ('medieval', 'England.[3][4][5', 'amod', 1), ('England.[3][4][5', 'of', 'pobj', -3), (']', 'is', 'punct', -22)]
    elif lang == 'fin':
        assert dependencies == [('Suomen', 'kieli', 'nmod:poss', 1), ('kieli', 'kieli', 'nsubj:cop', 10), ('(', 'suomi', 'punct', 1), ('suomi', 'kieli', 'appos', -2), (')', 'suomi', 'punct', -1), ('on', 'kieli', 'cop', 6), ('uralilaisten', 'kielten', 'amod', 1), ('kielten', 'ryhmään', 'nmod:poss', 2), ('itämerensuomalaiseen', 'ryhmään', 'amod', 1), ('ryhmään', 'kuuluva', 'obl', 1), ('kuuluva', 'kieli', 'acl', 1), ('kieli', 'kieli', 'ROOT', 0), (',', 'puhuvat', 'punct', 2), ('jota', 'puhuvat', 'obj', 1), ('puhuvat', 'kieli', 'acl:relcl', -3), ('pääosin', 'suomalaiset', 'advmod', 1), ('suomalaiset', 'puhuvat', 'nsubj', -2), ('.', 'kieli', 'punct', -6)]
    elif lang == 'fra':
        assert dependencies == [('Le', 'français', 'det', 1), ('français', 'langue', 'nsubj', 3), ('est', 'langue', 'cop', 2), ('une', 'langue', 'det', 1), ('langue', 'langue', 'ROOT', 0), ('indo-européenne', 'langue', 'amod', -1), ('de', 'famille', 'case', 2), ('la', 'famille', 'det', 1), ('famille', 'langue', 'nmod', -4), ('des', 'langues', 'case', 1), ('langues', 'famille', 'nmod', -2), ('romanes', 'langues', 'nmod', -1), ('dont', 'locuteurs', 'nmod', 2), ('les', 'locuteurs', 'det', 1), ('locuteurs', 'appelés', 'nsubj:pass', 2), ('sont', 'appelés', 'aux:pass', 1), ('appelés', 'langue', 'advcl', -12), ('francophones', 'appelés', 'xcomp', -1), (',', 'appelés', 'punct', -2), ('également', 'surnommé', 'advmod', 1), ('surnommé', 'appelés', 'advcl', -4), ('la', 'langue', 'det', 1), ('langue', 'surnommé', 'obj', -2), ('de', 'Molière', 'case', 1), ('Molière', 'langue', 'nmod', -2), ('.', 'langue', 'punct', -21)]
    elif lang.startswith('deu_'):
        assert dependencies == [('Die', 'Sprache', 'nk', 2), ('deutsche', 'Sprache', 'nk', 1), ('Sprache', 'abgekürzt', 'sb', 7), ('bzw.', 'Sprache', 'cd', -1), ('Deutsch', 'bzw.', 'cj', -1), ('(', '[', 'punct', 1), ('[', 'Sprache', 'app', -4), ('dɔɪ̯tʃ];[26', '[', 'uc', -1), (']', '[', 'nk', -2), ('abgekürzt', 'abgekürzt', 'ROOT', 0), ('dt', 'dt', 'ROOT', 0), ('.', '.', 'ROOT', 0), ('oder', 'dtsch', 'ju', 1), ('dtsch', 'dtsch', 'ROOT', 0), ('.', 'dtsch', 'punct', -1), (')', 'ist', 'punct', 1), ('ist', 'ist', 'ROOT', 0), ('eine', 'Sprache', 'nk', 2), ('westgermanische', 'Sprache', 'nk', 1), ('Sprache', 'ist', 'pd', -3), (',', 'Sprache', 'punct', -1), ('die', 'dient', 'sb', 19), ('weltweit', 'Millionen', 'mo', 5), ('etwa', '90', 'mo', 1), ('90', 'Millionen', 'nmc', 3), ('bis', '90', 'cd', -1), ('105', 'bis', 'cj', -1), ('Millionen', 'dient', 'sb', 13), ('Menschen', 'Millionen', 'nk', -1), ('als', 'Millionen', 'mnr', -2), ('Muttersprache', 'als', 'nk', -1), ('und', 'Millionen', 'cd', -4), ('weiteren', 'Millionen', 'nk', 3), ('rund', 'Millionen', 'mo', 2), ('80', 'Millionen', 'nmc', 1), ('Millionen', 'und', 'cj', -4), ('als', 'dient', 'mo', 4), ('Zweit-', 'oder', 'cj', 1), ('oder', 'Fremdsprache', 'cd', 1), ('Fremdsprache', 'als', 'nk', -3), ('dient', 'Sprache', 'rc', -21), ('.', 'ist', 'punct', -25)]
    elif lang == 'ell':
        assert dependencies == [('Η', 'γλώσσα', 'det', 2), ('ελληνική', 'γλώσσα', 'amod', 1), ('γλώσσα', 'ανήκει', 'nsubj', 1), ('ανήκει', 'ανήκει', 'ROOT', 0), ('στην', ']', 'case', 3), ('ινδοευρωπαϊκή', ']', 'amod', 2), ('οικογένεια[9', ']', 'nmod', 1), (']', 'ανήκει', 'obl', -4), ('και', 'αποτελεί', 'cc', 1), ('αποτελεί', 'ανήκει', 'conj', -6), ('το', 'μέλος', 'det', 2), ('μοναδικό', 'μέλος', 'amod', 1), ('μέλος', 'αποτελεί', 'obj', -3), ('του', 'κλάδου', 'det', 2), ('ελληνικού', 'κλάδου', 'amod', 1), ('κλάδου', 'μέλος', 'nmod', -3), (',', 'γλώσσα', 'punct', 5), ('ενώ', 'γλώσσα', 'mark', 4), ('είναι', 'γλώσσα', 'cop', 3), ('η', 'γλώσσα', 'det', 2), ('επίσημη', 'γλώσσα', 'amod', 1), ('γλώσσα', 'ανήκει', 'advcl', -18), ('της', 'Ελλάδας', 'det', 1), ('Ελλάδας', 'γλώσσα', 'nmod', -2), ('και', 'Κύπρου', 'cc', 2), ('της', 'Κύπρου', 'det', 1), ('Κύπρου', 'Ελλάδας', 'conj', -3), ('.', 'ανήκει', 'punct', -24)]
    elif lang == 'ita':
        assert dependencies == [("L'", 'italiano', 'det', 1), ('italiano', 'lingua', 'nsubj', 11), ('(', 'itaˈljaːno][Nota', 'punct', 2), ('[', 'itaˈljaːno][Nota', 'punct', 1), ('itaˈljaːno][Nota', 'italiano', 'nmod', -3), ('1', 'itaˈljaːno][Nota', 'nummod', -1), (']', 'ascolta[?·info', 'punct', 1), ('ascolta[?·info', 'itaˈljaːno][Nota', 'conj', -3), (']', 'itaˈljaːno][Nota', 'punct', -4), (')', 'itaˈljaːno][Nota', 'punct', -5), ('è', 'lingua', 'cop', 2), ('una', 'lingua', 'det', 1), ('lingua', 'lingua', 'ROOT', 0), ('romanza', 'lingua', 'compound', -1), ('parlata', 'lingua', 'amod', -2), ('principalmente', 'parlata', 'advmod', -1), ('in', 'Italia', 'case', 1), ('Italia', 'parlata', 'obl', -3), ('.', 'lingua', 'punct', -6)]
    elif lang == 'jpn':
        assert dependencies == [('日本', '（', 'compound', 2), ('語', '（', 'compound', 1), ('（', 'ご', 'nmod', 2), ('にほん', 'ご', 'compound', 1), ('ご', '）', 'nmod', 8), ('、', 'ご', 'punct', -1), ('にっぽん', 'ご', 'compound', 1), ('ご', '）', 'compound', 5), ('[', '）', 'punct', 4), ('注', '）', 'compound', 3), ('2', '）', 'compound', 2), (']', '）', 'punct', 1), ('）', '言語', 'nsubj', 28), ('は', '）', 'case', -1), ('、', '）', 'punct', -2), ('日本', '内', 'compound', 2), ('国', '内', 'compound', 1), ('内', '領', 'nmod', 6), ('や', '内', 'case', -1), ('、', '内', 'punct', -2), ('かつて', '領', 'advmod', 3), ('の', 'かつて', 'case', -1), ('日本', '領', 'compound', 1), ('領', '国', 'acl', 3), ('だっ', '領', 'cop', -1), ('た', '領', 'aux', -2), ('国', '使用', 'obl', 9), ('、', '国', 'punct', -1), ('そして', '使用', 'cc', 7), ('日本', '同士', 'compound', 2), ('人', '同士', 'compound', 1), ('同士', '間', 'nmod', 2), ('の', '同士', 'case', -1), ('間', '使用', 'obl', 2), ('で', '間', 'case', -1), ('使用', '言語', 'acl', 5), ('さ', '使用', 'aux', -1), ('れ', '使用', 'aux', -2), ('て', '使用', 'mark', -3), ('いる', 'て', 'fixed', -1), ('言語', '言語', 'ROOT', 0), ('。', '言語', 'punct', -1)]
    elif lang == 'lit':
        assert dependencies == [('Lietuvių', 'kalba', 'nmod', 1), ('kalba', 'kalba', 'ROOT', 0), ('–', 'kilusi', 'punct', 4), ('iš', 'prokalbės', 'case', 2), ('baltų', 'prokalbės', 'acl', 1), ('prokalbės', 'kilusi', 'obl:arg', 1), ('kilusi', 'kilusi', 'ROOT', 0), ('lietuvių', 'tautos', 'nmod', 1), ('tautos', 'kalba', 'nmod', 1), ('kalba', 'kilusi', 'obl:arg', -3), (',', 'valstybinė', 'punct', 4), ('kuri', 'valstybinė', 'nsubj', 3), ('Lietuvoje', 'valstybinė', 'obl', 2), ('yra', 'valstybinė', 'cop', 1), ('valstybinė', 'kalba', 'acl:relcl', -5), (',', 'Sąjungoje', 'punct', 3), ('o', 'Sąjungoje', 'cc', 2), ('Europos', 'Sąjungoje', 'nmod', 1), ('Sąjungoje', 'valstybinė', 'conj', -4), ('–', 'viena', 'punct', 1), ('viena', 'valstybinė', 'conj', -6), ('iš', 'kalbų', 'case', 2), ('oficialiųjų', 'kalbų', 'det', 1), ('kalbų', 'viena', 'obl:arg', -3), ('.', 'kilusi', 'punct', -18)]
    elif lang == 'mkd':
        assert dependencies == [('Македонски', 'јазик', 'att', 1), ('јазик', 'јазик', 'ROOT', 0), ('—', 'јазик', 'punct', -1), ('јужнословенски', 'јазик', 'att', 1), ('јазик', 'јазик', 'dobj', -3), (',', 'јазик', 'punct', -4), ('дел', 'јазик', 'dep', -5), ('од', 'дел', 'prep', -1), ('групата', 'од', 'pobj', -1), ('на', 'групата', 'prep', -1), ('словенски', 'јазици', 'att', 1), ('јазици', 'групата', 'pobj', -3), ('од', 'јазици', 'prep', -1), ('јазичното', 'семејство', 'att', 1), ('семејство', 'од', 'pobj', -2), ('на', 'семејство', 'prep', -1), ('индоевропски', 'јазици', 'att', 1), ('јазици', 'на', 'pobj', -2), ('.', 'јазик', 'punct', -17)]
    elif lang == 'nob':
        assert dependencies == [('Bokmål', 'varietet', 'nsubj', 3), ('er', 'varietet', 'cop', 2), ('en', 'varietet', 'det', 1), ('varietet', 'varietet', 'ROOT', 0), ('av', 'språk', 'case', 2), ('norsk', 'språk', 'amod', 1), ('språk', 'varietet', 'nmod', -3), ('.', 'varietet', 'punct', -4)]
    elif lang == 'pol':
        assert dependencies == [('Język', 'Język', 'ROOT', 0), ('polski', 'Język', 'amod', -1), (',', 'polszczyzna', 'punct', 1), ('polszczyzna', 'Język', 'amod', -3), ('–', 'język', 'punct', 1), ('język', 'Język', 'conj', -5), ('lechicki', 'język', 'amod', -1), ('z', 'grupy', 'case', 1), ('grupy', 'język', 'nmod', -3), ('zachodniosłowiańskiej', 'grupy', 'amod', -1), ('(', 'należą', 'punct', 3), ('do', 'której', 'case', 1), ('której', 'należą', 'obl:arg', 1), ('należą', 'Język', 'acl:relcl', -13), ('również', 'czeski', 'advmod:emph', 1), ('czeski', 'należą', 'nsubj', -2), (',', 'kaszubski', 'punct', 1), ('kaszubski', 'czeski', 'conj', -2), (',', 'słowacki', 'punct', 1), ('słowacki', 'czeski', 'conj', -4), ('i', 'języki', 'cc', 1), ('języki', 'czeski', 'conj', -6), ('łużyckie', 'języki', 'amod', -1), (')', 'należą', 'punct', -10), (',', 'część', 'punct', 2), ('stanowiącej', 'część', 'acl', 1), ('część', 'Język', 'conj', -26), ('rodziny', 'część', 'nmod:arg', -1), ('indoeuropejskiej', 'rodziny', 'amod', -1), ('.', 'Język', 'punct', -29)]
    elif lang.startswith('por_'):
        assert dependencies == [('A', 'língua', 'det', 1), ('língua', 'língua', 'nsubj', 9), ('portuguesa', 'língua', 'amod', -1), (',', 'designada', 'punct', 2), ('também', 'designada', 'advmod', 1), ('designada', 'língua', 'acl', -4), ('português', 'designada', 'amod', -1), (',', 'designada', 'punct', -2), ('é', 'língua', 'cop', 2), ('uma', 'língua', 'det', 1), ('língua', 'língua', 'ROOT', 0), ('indo-europeia', 'língua', 'amod', -1), ('românica', 'língua', 'amod', -2), ('flexiva', 'língua', 'appos', -3), ('ocidental', 'flexiva', 'amod', -1), ('originada', 'flexiva', 'acl', -2), ('no', 'galego-português', 'case', 1), ('galego-português', 'originada', 'obl', -2), ('falado', 'galego-português', 'acl', -1), ('no', 'Reino', 'case', 1), ('Reino', 'falado', 'obl', -2), ('da', 'Galiza', 'case', 1), ('Galiza', 'Reino', 'nmod', -2), ('e', 'norte', 'cc', 2), ('no', 'norte', 'case', 1), ('norte', 'Reino', 'conj', -5), ('de', 'Portugal', 'case', 1), ('Portugal', 'norte', 'nmod', -2), ('.', 'língua', 'punct', -18)]
    elif lang == 'ron':
        assert dependencies == [('Limba', 'limbă', 'nsubj', 4), ('română', 'Limba', 'amod', -1), ('este', 'limbă', 'cop', 2), ('o', 'limbă', 'det', 1), ('limbă', 'limbă', 'ROOT', 0), ('indo-europeană', 'limbă', 'amod', -1), (',', 'grupul', 'punct', 2), ('din', 'grupul', 'case', 1), ('grupul', 'limbă', 'nmod', -4), ('italic', 'grupul', 'amod', -1), ('și', 'subgrupul', 'cc', 2), ('din', 'subgrupul', 'case', 1), ('subgrupul', 'grupul', 'conj', -4), ('oriental', 'subgrupul', 'amod', -1), ('al', 'limbilor', 'det', 1), ('limbilor', 'subgrupul', 'nmod', -3), ('romanice', 'limbilor', 'amod', -1), ('.', 'limbă', 'punct', -13)]
    elif lang == 'rus':
        assert dependencies == [('Ру́сский', 'язы́к', 'amod', 1), ('язы́к', 'Информация', 'nsubj', 6), ('(', 'ˈruskʲɪi̯', 'punct', 2), ('[', 'ˈruskʲɪi̯', 'punct', 1), ('ˈruskʲɪi̯', 'язы́к', 'parataxis', -3), ('jɪˈzɨk', 'ˈruskʲɪi̯', 'flat:foreign', -1), (']', 'ˈruskʲɪi̯', 'punct', -2), ('Информация', 'один', 'nsubj', 10), ('о', 'файле', 'case', 1), ('файле', 'Информация', 'nmod', -2), ('слушать)[~', 'файле', 'appos', -1), ('3', 'слушать)[~', 'appos', -1), (']', 'файле', 'punct', -3), ('[', '⇨', 'punct', 1), ('⇨', 'файле', 'appos', -5), (']', '⇨', 'punct', -1), ('—', 'один', 'punct', 1), ('один', 'один', 'ROOT', 0), ('из', 'языков', 'case', 2), ('восточнославянских', 'языков', 'amod', 1), ('языков', 'один', 'nmod', -3), (',', 'язык', 'punct', 2), ('национальный', 'язык', 'amod', 1), ('язык', 'один', 'conj', -6), ('русского', 'народа', 'amod', 1), ('народа', 'язык', 'nmod', -2), ('.', 'один', 'punct', -9)]
    elif lang == 'spa':
        assert dependencies == [('El', 'español', 'det', 1), ('español', 'lengua', 'nsubj', 5), ('o', 'castellano', 'cc', 1), ('castellano', 'español', 'conj', -2), ('es', 'lengua', 'cop', 2), ('una', 'lengua', 'det', 1), ('lengua', 'romance', 'amod', 1), ('romance', 'romance', 'ROOT', 0), ('procedente', 'romance', 'amod', -1), ('del', 'latín', 'case', 1), ('latín', 'procedente', 'nmod', -2), ('hablado', 'latín', 'amod', -1), (',', 'perteneciente', 'punct', 1), ('perteneciente', 'latín', 'amod', -3), ('a', 'familia', 'case', 2), ('la', 'familia', 'det', 1), ('familia', 'perteneciente', 'nmod', -3), ('de', 'lenguas', 'case', 1), ('lenguas', 'familia', 'nmod', -2), ('indoeuropeas', 'lenguas', 'amod', -1), ('.', 'romance', 'punct', -13)]
    elif lang == 'swe':
        assert dependencies == [('Svenska', 'språk', 'nsubj', 11), ('(', 'Svenska', 'punct', -1), ('svenska', 'Svenska', 'appos', -2), ('\u2009', 'svenska', 'dep', -1), ('(', 'svenska', 'punct', -2), ('info', 'svenska', 'appos', -3), (')', 'svenska', 'punct', -4), (')', 'Svenska', 'punct', -7), ('är', 'språk', 'cop', 3), ('ett', 'språk', 'det', 2), ('östnordiskt', 'språk', 'amod', 1), ('språk', 'språk', 'ROOT', 0), ('som', 'talas', 'nsubj:pass', 1), ('talas', 'språk', 'acl:relcl', -2), ('av', 'personer', 'case', 4), ('ungefär', 'tio', 'advmod', 1), ('tio', 'miljoner', 'nummod', 1), ('miljoner', 'personer', 'nmod', 1), ('personer', 'talas', 'obl:agent', -5), ('främst', 'talas', 'advmod', -6), ('i', 'Sverige', 'case', 1), ('Sverige', 'talas', 'obl', -8), ('där', 'har', 'advmod', 2), ('språket', 'har', 'nsubj', 1), ('har', 'språk', 'advcl', -13), ('en', 'ställning', 'det', 2), ('dominant', 'ställning', 'amod', 1), ('ställning', 'har', 'obj', -3), ('som', 'huvudspråk', 'mark', 1), ('huvudspråk', 'har', 'xcomp', -5), (',', 'nationalspråket', 'punct', 6), ('men', 'nationalspråket', 'cc', 5), ('även', 'nationalspråket', 'advmod', 4), ('som', 'även', 'fixed', -1), ('det', 'nationalspråket', 'det', 2), ('ena', 'nationalspråket', 'amod', 1), ('nationalspråket', 'har', 'conj', -12), ('i', 'Finland', 'case', 1), ('Finland', 'nationalspråket', 'nmod', -2), ('och', 'språk', 'cc', 4), ('som', 'språk', 'nsubj:pass', 3), ('enda', 'språk', 'amod', 2), ('officiella', 'språk', 'amod', 1), ('språk', 'Finland', 'conj', -5), ('på', 'Åland', 'case', 1), ('Åland', 'språk', 'nmod', -2), ('.', 'språk', 'punct', -35)]
    elif lang == 'ukr':
        assert dependencies == [('Украї́нська', 'мова', 'nsubj', 24), ('мо́ва', 'Украї́нська', 'flat:title', -1), ('(', 'МФА', 'punct', 1), ('МФА', 'Украї́нська', 'appos', -3), (':', '[', 'punct', 1), ('[', 'МФА', 'appos', -2), ('ukrɑ̽ˈjɪnʲsʲkɑ̽', '[', 'flat:title', -1), ('ˈmɔwɑ̽', 'МФА', 'punct', -4), (']', 'МФА', 'nmod', -5), (',', 'назви', 'punct', 2), ('історичні', 'назви', 'amod', 1), ('назви', 'МФА', 'conj', -8), ('—', 'ру́ська', 'punct', 1), ('ру́ська', 'назви', 'appos', -2), (',', 'руси́нська[10][11][12', 'punct', 1), ('руси́нська[10][11][12', 'ру́ська', 'conj', -2), (']', 'руси́нська[10][11][12', 'nmod', -1), ('[', 'назви', 'nmod', -6), ('*', 'МФА', 'punct', -15), ('1', ']', 'nummod', 1), (']', 'МФА', 'nmod', -17), (')', 'МФА', 'punct', -18), ('—', 'мова', 'punct', 2), ('національна', 'мова', 'amod', 1), ('мова', 'мова', 'ROOT', 0), ('українців', 'мова', 'nmod', -1), ('.', 'мова', 'punct', -2)]
    else:
        raise Exception(f'Error: Tests for language "{lang}" is skipped!')

    if dependency_parser_skipped:
        raise Exception(f'Error: Tests for dependency parser "{dependency_parser}" is skipped!')

if __name__ == '__main__':
    for lang, dependency_parser in test_dependency_parsers:
        test_dependency_parse(lang, dependency_parser)
