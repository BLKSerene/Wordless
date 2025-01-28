# ----------------------------------------------------------------------
# Tests: NLP - spaCy - Russian
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

from tests.tests_nlp.tests_spacy import test_spacy

def test_spacy_rus():
    results_sentence_tokenize = ['Ру́сский язы́к (МФА: [ˈruskʲɪi̯ jɪˈzɨk]ⓘ)[~ 3][⇨] — язык восточнославянской группы славянской ветви индоевропейской языковой семьи, национальный язык русского народа.', 'Является одним из наиболее распространённых языков мира — восьмым среди всех языков мира по общей численности говорящих[5] и седьмым по численности владеющих им как родным (2022)[2].', 'Русский является также самым распространённым славянским языком[8] и самым распространённым языком в Европе — географически и по числу носителей языка как родного[6].']
    results_pos_tag = [('Ру́сский', 'ADJ'), ('язы́к', 'PROPN'), ('(', 'PUNCT'), ('МФА', 'PROPN'), (':', 'PUNCT'), ('[', 'PUNCT'), ('ˈruskʲɪi̯', 'PUNCT'), ('jɪˈzɨk]', 'PROPN'), ('ⓘ', 'PUNCT'), (')[~', 'PUNCT'), ('3', 'NUM'), (']', 'PUNCT'), ('[', 'PUNCT'), ('⇨', 'PROPN'), (']', 'PUNCT'), ('—', 'PUNCT'), ('язык', 'NOUN'), ('восточнославянской', 'ADJ'), ('группы', 'NOUN'), ('славянской', 'ADJ'), ('ветви', 'NOUN'), ('индоевропейской', 'ADJ'), ('языковой', 'ADJ'), ('семьи', 'NOUN'), (',', 'PUNCT'), ('национальный', 'ADJ'), ('язык', 'NOUN'), ('русского', 'ADJ'), ('народа', 'NOUN'), ('.', 'PUNCT')]

    test_spacy.wl_test_spacy(
        lang = 'rus',
        results_sentence_tokenize_trf = results_sentence_tokenize,
        results_sentence_tokenize_lg = results_sentence_tokenize,
        results_word_tokenize = ['Ру́сский', 'язы́к', '(', 'МФА', ':', '[', 'ˈruskʲɪi̯', 'jɪˈzɨk]', 'ⓘ', ')[~', '3', ']', '[', '⇨', ']', '—', 'язык', 'восточнославянской', 'группы', 'славянской', 'ветви', 'индоевропейской', 'языковой', 'семьи', ',', 'национальный', 'язык', 'русского', 'народа', '.'],
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_lemmatize = ['ру́сский', 'язы́к', '(', 'мфа', ':', '[', 'ˈruskʲɪi̯', 'jɪˈzɨk]', 'ⓘ', ')[~', '3', ']', '[', '⇨', ']', '—', 'язык', 'восточнославянский', 'группа', 'славянский', 'ветвь', 'индоевропейский', 'языковой', 'семья', ',', 'национальный', 'язык', 'русский', 'народ', '.'],
        results_dependency_parse = [('Ру́сский', 'язы́к', 'amod', 1), ('язы́к', 'язы́к', 'ROOT', 0), ('(', 'МФА', 'punct', 1), ('МФА', 'язы́к', 'appos', -2), (':', 'МФА', 'punct', -1), ('[', 'ˈruskʲɪi̯', 'punct', 1), ('ˈruskʲɪi̯', 'МФА', 'parataxis', -3), ('jɪˈzɨk]', 'МФА', 'appos', -4), ('ⓘ', 'МФА', 'punct', -5), (')[~', 'МФА', 'punct', -6), ('3', 'МФА', 'appos', -7), (']', 'МФА', 'punct', -8), ('[', '⇨', 'punct', 1), ('⇨', 'МФА', 'appos', -10), (']', '⇨', 'punct', -1), ('—', 'язык', 'punct', 1), ('язык', 'МФА', 'appos', -13), ('восточнославянской', 'группы', 'amod', 1), ('группы', 'язык', 'nmod', -2), ('славянской', 'ветви', 'amod', 1), ('ветви', 'группы', 'nmod', -2), ('индоевропейской', 'семьи', 'amod', 2), ('языковой', 'семьи', 'amod', 1), ('семьи', 'ветви', 'nmod', -3), (',', 'язык', 'punct', 2), ('национальный', 'язык', 'amod', 1), ('язык', 'язык', 'conj', -10), ('русского', 'народа', 'amod', 1), ('народа', 'язык', 'nmod', -2), ('.', 'язы́к', 'punct', -28)]
    )

if __name__ == '__main__':
    test_spacy_rus()
