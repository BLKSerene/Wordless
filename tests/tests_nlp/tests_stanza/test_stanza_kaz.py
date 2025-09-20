# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Kazakh
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

def test_stanza_kaz():
    test_stanza.wl_test_stanza(
        lang = 'kaz',
        results_sentence_tokenize = ['Қазақ тілі (төте: قازاق ٴتىلى\u200e, латын: qazaq tılı) — Қазақстан Республикасының мемлекеттік тілі, сонымен қатар Ресей, Өзбекстан, Қытай, Моңғолия жəне т.б. елдерде тұратын қазақтардың ана тілі.', 'Қазақ тілі түркі тілдерінің қыпшақ тобына, соның ішінде қарақалпақ, ноғай, қарашай тілдерімен бірге қыпшақ-ноғай тармағына жатады.'],
        results_word_tokenize = ['Қазақ', 'тілі', '(', 'төте', ':', 'قازا', 'ق', 'ٴتىلى\u200e', ',', 'латын', ':', 'qazaq', 'tılı', ')', '—', 'Қазақстан', 'Республикасының', 'мемлекеттік', 'тілі', ',', 'сонымен', 'қатар', 'Ресей', ',', 'Өзбекстан', ',', 'Қытай', ',', 'Моңғолия', 'жəне', 'т.б.', 'елдерде', 'тұратын', 'қазақтардың', 'ана', 'тілі', '.'],
        results_pos_tag = [('Қазақ', 'n'), ('тілі', 'n'), ('(', 'lpar'), ('төте', 'num'), (':', 'sent'), ('قازا', 'num'), ('ق', 'sent'), ('ٴتىلى\u200e', 'num'), (',', 'cm'), ('латын', 'n'), (':', 'sent'), ('qazaq', 'num'), ('tılı', 'np'), (')', 'rpar'), ('—', 'guio'), ('Қазақстан', 'np'), ('Республикасының', 'n'), ('мемлекеттік', 'adj'), ('тілі', 'n'), (',', 'cm'), ('сонымен', 'prn'), ('қатар', 'post'), ('Ресей', 'np'), (',', 'cm'), ('Өзбекстан', 'np'), (',', 'cm'), ('Қытай', 'np'), (',', 'cm'), ('Моңғолия', 'np'), ('жəне', 'cnjcoo'), ('т.б.', 'abbr'), ('елдерде', 'n'), ('тұратын', 'v'), ('қазақтардың', 'n'), ('ана', 'n'), ('тілі', 'n'), ('.', 'sent')],
        results_pos_tag_universal = [('Қазақ', 'NOUN'), ('тілі', 'NOUN'), ('(', 'PUNCT'), ('төте', 'NUM'), (':', 'PUNCT'), ('قازا', 'NUM'), ('ق', 'PUNCT'), ('ٴتىلى\u200e', 'NUM'), (',', 'PUNCT'), ('латын', 'NOUN'), (':', 'PUNCT'), ('qazaq', 'NUM'), ('tılı', 'PROPN'), (')', 'PUNCT'), ('—', 'PUNCT'), ('Қазақстан', 'PROPN'), ('Республикасының', 'NOUN'), ('мемлекеттік', 'ADJ'), ('тілі', 'NOUN'), (',', 'PUNCT'), ('сонымен', 'PRON'), ('қатар', 'ADP'), ('Ресей', 'PROPN'), (',', 'PUNCT'), ('Өзбекстан', 'PROPN'), (',', 'PUNCT'), ('Қытай', 'PROPN'), (',', 'PUNCT'), ('Моңғолия', 'PROPN'), ('жəне', 'CCONJ'), ('т.б.', 'NOUN'), ('елдерде', 'NOUN'), ('тұратын', 'VERB'), ('қазақтардың', 'NOUN'), ('ана', 'NOUN'), ('тілі', 'NOUN'), ('.', 'PUNCT')],
        results_lemmatize = ['қазақ', 'тіл', '(', 'төте', ':', 'قازا', 'ق', 'зتз', ',', 'лат', ':', 'зa', 'tılı', ')', '—', 'Қазақстан', 'республика', 'мемлекеттік', 'тіл', ',', 'сол', 'қатар', 'Ресей', ',', 'Өзбекстан', ',', 'Қытай', ',', 'Моңғолия', 'жəне', 'т.б.', 'ел', 'тұр', 'қазақ', 'ана', 'тіл', '.'],
        results_dependency_parse = [('Қазақ', 'тілі', 'nmod:poss', 1), ('тілі', 'ана', 'nsubj', 33), ('(', 'төте', 'punct', 1), ('төте', 'тілі', 'appos', -2), (':', 'төте', 'punct', -1), ('قازا', 'төте', 'conj', -2), ('ق', 'ٴتىلى\u200e', 'punct', 1), ('ٴتىلى\u200e', 'төте', 'conj', -4), (',', 'латын', 'punct', 1), ('латын', 'төте', 'conj', -6), (':', 'qazaq', 'punct', 1), ('qazaq', 'латын', 'appos', -2), ('tılı', 'qazaq', 'punct', -1), (')', 'qazaq', 'punct', -2), ('—', 'тілі', 'punct', 4), ('Қазақстан', 'Республикасының', 'nmod:poss', 1), ('Республикасының', 'тілі', 'nmod:poss', 2), ('мемлекеттік', 'тілі', 'amod', 1), ('тілі', 'тілі', 'appos', -17), (',', 'Ресей', 'punct', 3), ('сонымен', 'тілі', 'obl', 15), ('қатар', 'сонымен', 'case', -1), ('Ресей', 'тілі', 'appos', -4), (',', 'Өзбекстан', 'punct', 1), ('Өзбекстан', 'Ресей', 'conj', -2), (',', 'Қытай', 'punct', 1), ('Қытай', 'төте', 'conj', -23), (',', 'Моңғолия', 'punct', 1), ('Моңғолия', 'төте', 'conj', -25), ('жəне', 'т.б.', 'cc', 1), ('т.б.', 'Ресей', 'conj', -8), ('елдерде', 'тұратын', 'obl', 1), ('тұратын', 'қазақтардың', 'acl', 1), ('қазақтардың', 'тілі', 'nmod:poss', 2), ('ана', 'тілі', 'compound', 1), ('тілі', 'тілі', 'root', 0), ('.', 'тілі', 'punct', -1)]
    )

if __name__ == '__main__':
    test_stanza_kaz()
