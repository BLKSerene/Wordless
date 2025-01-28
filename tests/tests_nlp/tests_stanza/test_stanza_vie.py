# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Vietnamese
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

from tests.tests_nlp.tests_stanza import test_stanza

def test_stanza_vie():
    test_stanza.wl_test_stanza(
        lang = 'vie',
        results_sentence_tokenize = ['Tiếng Việt, cũng gọi là tiếng Việt Nam[9] hay Việt ngữ là ngôn ngữ của người Việt và là ngôn ngữ chính thức tại Việt Nam.', 'Đây là tiếng mẹ đẻ của khoảng 85% dân cư Việt Nam cùng với hơn 4 triệu người Việt kiều.', 'Tiếng Việt còn là ngôn ngữ thứ hai của các dân tộc thiểu số tại Việt Nam và là ngôn ngữ dân tộc thiểu số được công nhận tại Cộng hòa Séc.'],
        results_word_tokenize = ['Tiếng', 'Việ', 't,', 'cũng', 'gọi', 'là', 'tiếng', 'Việt Nam', '[9]', 'hay', 'Việt ngữ', 'là', 'ngôn', 'ngữ', 'của', 'người', 'Việt', 'và', 'là', 'ngôn', 'ngữ', 'chính thức', 'tại', 'Việt Nam.'],
        results_pos_tag = [('Tiếng', 'N'), ('Việ', 'NNP'), ('t,', '...'), ('cũng', 'Adv'), ('gọi', 'V'), ('là', 'V'), ('tiếng', 'N'), ('Việt Nam', 'NNP'), ('[9]', '``'), ('hay', 'CC'), ('Việt ngữ', 'NNP'), ('là', 'V'), ('ngôn', 'N'), ('ngữ', 'N'), ('của', 'Pre'), ('người', 'N'), ('Việt', 'NNP'), ('và', 'CC'), ('là', 'V'), ('ngôn', 'N'), ('ngữ', 'N'), ('chính thức', 'Adj'), ('tại', 'Pre'), ('Việt Nam.', '.')],
        results_pos_tag_universal = [('Tiếng', 'NOUN'), ('Việ', 'PROPN'), ('t,', 'PUNCT'), ('cũng', 'ADV'), ('gọi', 'VERB'), ('là', 'AUX'), ('tiếng', 'NOUN'), ('Việt Nam', 'PROPN'), ('[9]', 'PUNCT'), ('hay', 'CCONJ'), ('Việt ngữ', 'PROPN'), ('là', 'AUX'), ('ngôn', 'NOUN'), ('ngữ', 'NOUN'), ('của', 'ADP'), ('người', 'NOUN'), ('Việt', 'PROPN'), ('và', 'CCONJ'), ('là', 'AUX'), ('ngôn', 'NOUN'), ('ngữ', 'NOUN'), ('chính thức', 'ADJ'), ('tại', 'ADP'), ('Việt Nam.', 'PUNCT')],
        results_dependency_parse = [('Tiếng', 'gọi', 'nsubj', 4), ('Việ', 'Tiếng', 'compound', -1), ('t,', 'Tiếng', 'punct', -2), ('cũng', 'gọi', 'advmod', 1), ('gọi', 'gọi', 'root', 0), ('là', 'gọi', 'cop', -1), ('tiếng', 'gọi', 'obj', -2), ('Việt Nam', 'tiếng', 'compound', -1), ('[9]', 'tiếng', 'punct', -2), ('hay', 'ngôn', 'cc', 3), ('Việt ngữ', 'ngôn', 'conj', 2), ('là', 'ngôn', 'cop', 1), ('ngôn', 'gọi', 'conj', -8), ('ngữ', 'ngôn', 'compound', -1), ('của', 'người', 'case', 1), ('người', 'ngôn', 'nmod:poss', -3), ('Việt', 'người', 'nmod', -1), ('và', 'ngôn', 'cc', 2), ('là', 'ngôn', 'cop', 1), ('ngôn', 'ngôn', 'conj', -7), ('ngữ', 'ngôn', 'nmod', -1), ('chính thức', 'ngữ', 'amod', -1), ('tại', 'Việt Nam.', 'case', 1), ('Việt Nam.', 'gọi', 'obl', -19)],
        results_sentiment_analayze = [-1]
    )

if __name__ == '__main__':
    test_stanza_vie()
