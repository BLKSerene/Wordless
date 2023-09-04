# ----------------------------------------------------------------------
# Wordless: Tests - NLP - Stanza - Vietnamese
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

from tests.wl_tests_nlp.wl_tests_stanza import test_stanza

def test_stanza_vie():
    test_stanza.wl_test_stanza(
        lang = 'vie',
        results_sentence_tokenize = ['Tiếng Việt, cũng gọi là tiếng Việt Nam[9] hay Việt ngữ là ngôn ngữ của người Việt và là ngôn ngữ chính thức tại Việt Nam.', 'Đây là tiếng mẹ đẻ của khoảng 85% dân cư Việt Nam cùng với hơn 4 triệu người Việt kiều.', 'Tiếng Việt còn là ngôn ngữ thứ hai của các dân tộc thiểu số tại Việt Nam và là ngôn ngữ dân tộc thiểu số được công nhận tại Cộng hòa Séc.'],
        results_word_tokenize = ['Tiếng', 'Việt', ',', 'cũng', 'gọi', 'là', 'tiếng', 'Việt Nam', '[9]', 'hay', 'Việt ngữ', 'là', 'ngôn', 'ngữ', 'của', 'người', 'Việt', 'và', 'là', 'ngôn', 'ngữ', 'chính thức', 'tại', 'Việt Nam', '.'],
        results_pos_tag = [('Tiếng', 'N'), ('Việt', 'Np'), (',', ','), ('cũng', 'R'), ('gọi', 'V'), ('là', 'V'), ('tiếng', 'N'), ('Việt Nam', 'Np'), ('[9]', 'RBKT'), ('hay', 'C'), ('Việt ngữ', 'Np'), ('là', 'V'), ('ngôn', 'Nc'), ('ngữ', 'N'), ('của', 'E'), ('người', 'N'), ('Việt', 'Np'), ('và', 'CC'), ('là', 'V'), ('ngôn', 'Nc'), ('ngữ', 'N'), ('chính thức', 'A'), ('tại', 'E'), ('Việt Nam', 'Np'), ('.', '.')],
        results_pos_tag_universal = [('Tiếng', 'NOUN'), ('Việt', 'NOUN'), (',', 'PUNCT'), ('cũng', 'X'), ('gọi', 'VERB'), ('là', 'AUX'), ('tiếng', 'NOUN'), ('Việt Nam', 'NOUN'), ('[9]', 'PUNCT'), ('hay', 'CCONJ'), ('Việt ngữ', 'NOUN'), ('là', 'AUX'), ('ngôn', 'NOUN'), ('ngữ', 'NOUN'), ('của', 'ADP'), ('người', 'NOUN'), ('Việt', 'NOUN'), ('và', 'SCONJ'), ('là', 'AUX'), ('ngôn', 'NOUN'), ('ngữ', 'NOUN'), ('chính thức', 'ADJ'), ('tại', 'ADP'), ('Việt Nam', 'NOUN'), ('.', 'PUNCT')],
        results_dependency_parse = [('Tiếng', 'gọi', 'nsubj', 4), ('Việt', 'Tiếng', 'compound', -1), (',', 'Tiếng', 'punct', -2), ('cũng', 'gọi', 'advmod', 1), ('gọi', 'gọi', 'root', 0), ('là', 'gọi', 'cop', -1), ('tiếng', 'gọi', 'obj', -2), ('Việt Nam', 'tiếng', 'nmod', -1), ('[9]', 'tiếng', 'punct', -2), ('hay', 'Việt ngữ', 'cc', 1), ('Việt ngữ', 'ngữ', 'nsubj', 3), ('là', 'ngữ', 'cop', 2), ('ngôn', 'ngữ', 'clf:det', 1), ('ngữ', 'tiếng', 'nmod', -7), ('của', 'người', 'case', 1), ('người', 'ngữ', 'nmod:poss', -2), ('Việt', 'người', 'compound', -1), ('và', 'ngữ', 'cc', 3), ('là', 'ngữ', 'cop', 2), ('ngôn', 'ngữ', 'clf:det', 1), ('ngữ', 'tiếng', 'conj', -14), ('chính thức', 'ngữ', 'amod', -1), ('tại', 'Việt Nam', 'case', 1), ('Việt Nam', 'ngữ', 'obl', -3), ('.', 'gọi', 'punct', -20)],
        results_sentiment_analayze = [-1]
    )

if __name__ == '__main__':
    test_stanza_vie()
