# ----------------------------------------------------------------------
# Wordless: Tests - NLP - Stanza - Russian
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

from tests.tests_nlp.tests_stanza import test_stanza

def test_stanza_rus():
    results_pos_tag = [('Ру́сский', 'ADJ'), ('язы́к', 'NOUN'), ('(', 'PUNCT'), ('[', 'PUNCT'), ('ˈruskʲɪi̯', 'X'), ('jɪˈzɨk', 'X'), (']', 'PUNCT'), ('Информация', 'NOUN'), ('о', 'ADP'), ('файле', 'NOUN'), ('слушать', 'VERB'), (')', 'PUNCT'), ('[', 'PUNCT'), ('~', 'SYM'), ('3', 'NUM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('⇨', 'PROPN'), (']', 'PUNCT'), ('—', 'PUNCT'), ('язык', 'NOUN'), ('восточнославянской', 'ADJ'), ('группы', 'NOUN'), ('славянской', 'ADJ'), ('ветви', 'NOUN'), ('индоевропейской', 'ADJ'), ('языковой', 'ADJ'), ('семьи', 'NOUN'), (',', 'PUNCT'), ('национальный', 'ADJ'), ('язык', 'NOUN'), ('русского', 'ADJ'), ('народа', 'NOUN'), ('.', 'PUNCT')]

    test_stanza.wl_test_stanza(
        lang = 'rus',
        results_sentence_tokenize = ['Ру́сский язы́к ([ˈruskʲɪi̯ jɪˈzɨk] Информация о файле слушать)[~ 3][⇨] — язык восточнославянской группы славянской ветви индоевропейской языковой семьи, национальный язык русского народа.', 'Является одним из наиболее распространённых языков мира — восьмым среди всех языков мира по общей численности говорящих[5] и седьмым по численности владеющих им как родным (2022)[2].', 'Русский является также самым распространённым славянским языком[8] и самым распространённым языком в Европе — географически и по числу носителей языка как родного[6].'],
        results_word_tokenize = ['Ру́сский', 'язы́к', '(', '[', 'ˈruskʲɪi̯', 'jɪˈzɨk', ']', 'Информация', 'о', 'файле', 'слушать', ')', '[', '~', '3', ']', '[', '⇨', ']', '—', 'язык', 'восточнославянской', 'группы', 'славянской', 'ветви', 'индоевропейской', 'языковой', 'семьи', ',', 'национальный', 'язык', 'русского', 'народа', '.'],
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_lemmatize = ['ру́сский', 'язы́к', '(', '[', 'ˈruskʲɪi̯', 'jɪˈzɨk', ']', 'информация', 'о', 'файл', 'слушать', ')', '[', '~', '3', ']', '[', '⇨', ']', '—', 'язык', 'восточнославянский', 'группа', 'славянский', 'ветвь', 'индоевропейский', 'языковой', 'семья', ',', 'национальный', 'язык', 'русский', 'народ', '.'],
        results_dependency_parse = [('Ру́сский', 'язы́к', 'amod', 1), ('язы́к', 'язык', 'nsubj', 19), ('(', 'ˈruskʲɪi̯', 'punct', 2), ('[', 'ˈruskʲɪi̯', 'punct', 1), ('ˈruskʲɪi̯', 'язы́к', 'parataxis', -3), ('jɪˈzɨk', 'ˈruskʲɪi̯', 'flat:foreign', -1), (']', 'ˈruskʲɪi̯', 'punct', -2), ('Информация', 'язы́к', 'parataxis', -6), ('о', 'файле', 'case', 1), ('файле', 'Информация', 'nmod', -2), ('слушать', 'Информация', 'obl', -3), (')', 'ˈruskʲɪi̯', 'punct', -7), ('[', '~', 'punct', 1), ('~', 'язы́к', 'appos', -12), ('3', '~', 'nummod:entity', -1), (']', '~', 'punct', -2), ('[', '⇨', 'punct', 1), ('⇨', 'язы́к', 'flat:foreign', -16), (']', '⇨', 'punct', -1), ('—', 'язык', 'punct', 1), ('язык', 'язык', 'root', 0), ('восточнославянской', 'группы', 'amod', 1), ('группы', 'язык', 'nmod', -2), ('славянской', 'ветви', 'amod', 1), ('ветви', 'группы', 'nmod', -2), ('индоевропейской', 'семьи', 'amod', 2), ('языковой', 'семьи', 'amod', 1), ('семьи', 'ветви', 'nmod', -3), (',', 'язык', 'punct', 2), ('национальный', 'язык', 'amod', 1), ('язык', 'язык', 'conj', -10), ('русского', 'народа', 'amod', 1), ('народа', 'язык', 'nmod', -2), ('.', 'язык', 'punct', -13)]
    )

if __name__ == '__main__':
    test_stanza_rus()
