# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Belarusian
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

def test_stanza_bel():
    test_stanza.wl_test_stanza(
        lang = 'bel',
        results_sentence_tokenize = ["Белару́ская мо́ва — нацыянальная мова беларусаў, уваходзіць у індаеўрапейскую моўную сям'ю, славянскую групу, усходнеславянскую падгрупу.", 'Пашырана ў асноўным у Беларусі.', 'Распаўсюджана таксама і ў іншых краінах, галоўным чынам у Польшчы, Украіне, Расіі, Літве, Латвіі[2].', 'Беларуская мова мае шмат агульных граматычных і лексічных уласцівасцей з іншымі ўсходнеславянскімі мовамі.'],
        results_word_tokenize = ['Белару́ская', 'мо́ва', '—', 'нацыянальная', 'мова', 'беларусаў', ',', 'уваходзіць', 'у', 'індаеўрапейскую', 'моўную', "сям'ю", ',', 'славянскую', 'групу', ',', 'усходнеславянскую', 'падгрупу', '.'],
        results_pos_tag = [('Белару́ская', 'JJL'), ('мо́ва', 'NN'), ('—', 'PUNCT'), ('нацыянальная', 'JJL'), ('мова', 'NN'), ('беларусаў', 'NN'), (',', 'PUNCT'), ('уваходзіць', 'VBC'), ('у', 'IN'), ('індаеўрапейскую', 'JJL'), ('моўную', 'JJL'), ("сям'ю", 'NN'), (',', 'PUNCT'), ('славянскую', 'JJL'), ('групу', 'NN'), (',', 'PUNCT'), ('усходнеславянскую', 'JJL'), ('падгрупу', 'NN'), ('.', 'PUNCT')],
        results_pos_tag_universal = [('Белару́ская', 'ADJ'), ('мо́ва', 'NOUN'), ('—', 'PUNCT'), ('нацыянальная', 'ADJ'), ('мова', 'NOUN'), ('беларусаў', 'NOUN'), (',', 'PUNCT'), ('уваходзіць', 'VERB'), ('у', 'ADP'), ('індаеўрапейскую', 'ADJ'), ('моўную', 'ADJ'), ("сям'ю", 'NOUN'), (',', 'PUNCT'), ('славянскую', 'ADJ'), ('групу', 'NOUN'), (',', 'PUNCT'), ('усходнеславянскую', 'ADJ'), ('падгрупу', 'NOUN'), ('.', 'PUNCT')],
        results_lemmatize = ['беларускі', 'мова', '—', 'нацыянальны', 'мова', 'беларус', ',', 'уваходзіць', 'у', 'індаеўрапейскі', 'моўны', 'сям’я', ',', 'славянскі', 'група', ',', 'усходнеславянскі', 'падгруп', '.'],
        results_dependency_parse = [('Белару́ская', 'мо́ва', 'amod', 1), ('мо́ва', 'мова', 'nsubj', 3), ('—', 'мова', 'punct', 2), ('нацыянальная', 'мова', 'amod', 1), ('мова', 'мова', 'root', 0), ('беларусаў', 'мова', 'nmod', -1), (',', 'уваходзіць', 'punct', 1), ('уваходзіць', 'мова', 'conj', -3), ('у', "сям'ю", 'case', 3), ('індаеўрапейскую', "сям'ю", 'amod', 2), ('моўную', "сям'ю", 'amod', 1), ("сям'ю", 'уваходзіць', 'obl', -4), (',', 'групу', 'punct', 2), ('славянскую', 'групу', 'amod', 1), ('групу', "сям'ю", 'conj', -3), (',', 'падгрупу', 'punct', 2), ('усходнеславянскую', 'падгрупу', 'amod', 1), ('падгрупу', "сям'ю", 'conj', -6), ('.', 'мова', 'punct', -14)]
    )

if __name__ == '__main__':
    test_stanza_bel()
