# ----------------------------------------------------------------------
# Wordless: Tests - NLP - Stanza - Kazakh
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

def test_stanza_kaz():
    test_stanza.wl_test_stanza(
        lang = 'kaz',
        results_sentence_tokenize = ['Қазақ тілі (төте: قازاق ٴتىلى\u200e, латын: qazaq tili) — Қазақстан Республикасының мемлекеттік тілі, сонымен қатар Ресей, Өзбекстан, Қытай, Моңғолия жəне т.б. елдерде тұратын қазақтардың ана тілі.'],
        results_word_tokenize = ['Қазақ', 'тілі', '(', 'төте', ':', 'قازاق', 'ٴتىلى\u200e', ',', 'латын', ':', 'qazaq', 'tili', ')', '—', 'Қазақстан', 'Республикасының', 'мемлекеттік', 'тілі', ',', 'сонымен', 'қатар', 'Ресей', ',', 'Өзбекстан', ',', 'Қытай', ',', 'Моңғолия', 'жəне', 'т.б.'],
        results_pos_tag = [('Қазақ', 'n'), ('тілі', 'n'), ('(', 'lpar'), ('төте', 'n'), (':', 'sent'), ('قازاق', 'num'), ('ٴتىلى\u200e', 'np'), (',', 'cm'), ('латын', 'n'), (':', 'sent'), ('qazaq', 'num'), ('tili', 'num'), (')', 'rpar'), ('—', 'guio'), ('Қазақстан', 'np'), ('Республикасының', 'n'), ('мемлекеттік', 'adj'), ('тілі', 'n'), (',', 'cm'), ('сонымен', 'prn'), ('қатар', 'post'), ('Ресей', 'np'), (',', 'cm'), ('Өзбекстан', 'np'), (',', 'cm'), ('Қытай', 'np'), (',', 'cm'), ('Моңғолия', 'np'), ('жəне', 'cnjcoo'), ('т.б.', 'abbr')],
        results_pos_tag_universal = [('Қазақ', 'NOUN'), ('тілі', 'NOUN'), ('(', 'PUNCT'), ('төте', 'NOUN'), (':', 'PUNCT'), ('قازاق', 'NUM'), ('ٴتىلى\u200e', 'PROPN'), (',', 'PUNCT'), ('латын', 'NOUN'), (':', 'PUNCT'), ('qazaq', 'NUM'), ('tili', 'NUM'), (')', 'PUNCT'), ('—', 'PUNCT'), ('Қазақстан', 'PROPN'), ('Республикасының', 'NOUN'), ('мемлекеттік', 'ADJ'), ('тілі', 'NOUN'), (',', 'PUNCT'), ('сонымен', 'PRON'), ('қатар', 'ADP'), ('Ресей', 'PROPN'), (',', 'PUNCT'), ('Өзбекстан', 'PROPN'), (',', 'PUNCT'), ('Қытай', 'PROPN'), (',', 'PUNCT'), ('Моңғолия', 'PROPN'), ('жəне', 'CCONJ'), ('т.б.', 'NOUN')],
        results_lemmatize = ['қазақ', 'тіл', '(', 'төте', ':', 'قازاق', 'ٴتىلى\u200e', ',', 'латын', ':', 'qazaq', 'tili', ')', '—', 'Қазақстан', 'республика', 'мемлекеттік', 'тіл', ',', 'сол', 'қатар', 'Ресей', ',', 'Өзбекстан', ',', 'Қытай', ',', 'Моңғолия', 'жəне', 'т.б.'],
        results_dependency_parse = [('Қазақ', 'тілі', 'nmod:poss', 1), ('тілі', 'т.б.', 'nsubj', 28), ('(', 'төте', 'punct', 1), ('төте', 'төте', 'root', 0), (':', 'قازاق', 'punct', 1), ('قازاق', 'төте', 'conj', -2), ('ٴتىلى\u200e', 'төте', 'flat:name', -3), (',', 'латын', 'punct', 1), ('латын', 'төте', 'conj', -5), (':', 'tili', 'punct', 2), ('qazaq', 'tili', 'punct', 1), ('tili', 'латын', 'appos', -3), (')', 'tili', 'punct', -1), ('—', 'тілі', 'punct', 4), ('Қазақстан', 'Республикасының', 'nmod:poss', 1), ('Республикасының', 'тілі', 'nmod:poss', 2), ('мемлекеттік', 'тілі', 'amod', 1), ('тілі', 'тілі', 'appos', -16), (',', 'Ресей', 'punct', 3), ('сонымен', 'т.б.', 'nmod', 10), ('қатар', 'сонымен', 'case', -1), ('Ресей', 'төте', 'conj', -18), (',', 'Өзбекстан', 'punct', 1), ('Өзбекстан', 'төте', 'conj', -20), (',', 'Қытай', 'punct', 1), ('Қытай', 'төте', 'conj', -22), (',', 'Моңғолия', 'punct', 1), ('Моңғолия', 'төте', 'conj', -24), ('жəне', 'т.б.', 'cc', 1), ('т.б.', 'төте', 'conj', -26)]
    )

if __name__ == '__main__':
    test_stanza_kaz()
