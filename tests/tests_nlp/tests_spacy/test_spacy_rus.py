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
    results_sentence_tokenize = ['Русский язык (МФА: [ˈruskʲɪɪ̯ ɪ̯ɪˈzɨk]о файле)[~ 3] — язык восточнославянской группы славянской ветви индоевропейской языковой семьи, национальный язык русского народа.', 'Является одним из наиболее распространённых языков мира — восьмым среди всех языков мира по общей численности говорящих[5] и седьмым по численности владеющих им как родным (2022)[2].']
    results_pos_tag = [('Русский', 'ADJ'), ('язык', 'NOUN'), ('(', 'PUNCT'), ('МФА', 'PROPN'), (':', 'PUNCT'), ('[', 'PUNCT'), ('ˈruskʲɪɪ̯', 'ADP'), ('ɪ̯ɪˈzɨk]о', 'PROPN'), ('файле)[~', 'PROPN'), ('3', 'NUM'), (']', 'PUNCT'), ('—', 'PUNCT'), ('язык', 'NOUN'), ('восточнославянской', 'ADJ'), ('группы', 'NOUN'), ('славянской', 'ADJ'), ('ветви', 'NOUN'), ('индоевропейской', 'ADJ'), ('языковой', 'ADJ'), ('семьи', 'NOUN'), (',', 'PUNCT'), ('национальный', 'ADJ'), ('язык', 'NOUN'), ('русского', 'ADJ'), ('народа', 'NOUN'), ('.', 'PUNCT')]

    test_spacy.wl_test_spacy(
        lang = 'rus',
        results_sentence_tokenize_dependency_parser = results_sentence_tokenize,
        results_sentence_tokenize_sentence_recognizer = results_sentence_tokenize,
        results_word_tokenize = ['Русский', 'язык', '(', 'МФА', ':', '[', 'ˈruskʲɪɪ̯', 'ɪ̯ɪˈzɨk]о', 'файле)[~', '3', ']', '—', 'язык', 'восточнославянской', 'группы', 'славянской', 'ветви', 'индоевропейской', 'языковой', 'семьи', ',', 'национальный', 'язык', 'русского', 'народа', '.'],
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_lemmatize = ['русский', 'язык', '(', 'мфа', ':', '[', 'ˈruskʲɪɪ̯', 'ɪ̯ɪˈzɨk]о', 'файле)[~', '3', ']', '—', 'язык', 'восточнославянский', 'группа', 'славянский', 'ветвь', 'индоевропейский', 'языковой', 'семья', ',', 'национальный', 'язык', 'русский', 'народ', '.'],
        results_dependency_parse = [('Русский', 'язык', 'amod', 1), ('язык', 'язык', 'nsubj', 11), ('(', 'МФА', 'punct', 1), ('МФА', 'язык', 'appos', -2), (':', 'МФА', 'punct', -1), ('[', 'ˈruskʲɪɪ̯', 'punct', 1), ('ˈruskʲɪɪ̯', 'МФА', 'parataxis', -3), ('ɪ̯ɪˈzɨk]о', 'МФА', 'appos', -4), ('файле)[~', 'МФА', 'appos', -5), ('3', 'файле)[~', 'appos', -1), (']', 'МФА', 'punct', -7), ('—', 'язык', 'punct', 1), ('язык', 'язык', 'ROOT', 0), ('восточнославянской', 'группы', 'amod', 1), ('группы', 'язык', 'nmod', -2), ('славянской', 'ветви', 'amod', 1), ('ветви', 'группы', 'nmod', -2), ('индоевропейской', 'семьи', 'amod', 2), ('языковой', 'семьи', 'amod', 1), ('семьи', 'ветви', 'nmod', -3), (',', 'язык', 'punct', 2), ('национальный', 'язык', 'amod', 1), ('язык', 'язык', 'conj', -10), ('русского', 'народа', 'amod', 1), ('народа', 'язык', 'nmod', -2), ('.', 'язык', 'punct', -13)]
    )

if __name__ == '__main__':
    test_spacy_rus()
