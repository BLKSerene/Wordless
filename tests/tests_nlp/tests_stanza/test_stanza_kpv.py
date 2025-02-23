# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Komi (Zyrian)
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

def test_stanza_kpv():
    test_stanza.wl_test_stanza(
        lang = 'kpv',
        results_sentence_tokenize = ['Коми кыв — финн-йӧгра кывъясысь ӧти, коми войтырлӧн чужан кыв.', 'Коми кывйын кызь гӧгӧр сёрнисикас да кык гижӧда кыв: зырян коми да перым коми.', 'Коми кыв — Коми Республикаын каналан кыв (кыдзи и роч кыв).', 'Комиӧн сёрнитӧны Коми Республикаса вужвойтыр — комияс (зыряна, матӧ 156 сюрс морт).', 'Лунвылынджык, Перым Коми кытшын, перым комияслӧн (пермякъяслӧн, матӧ 63 сюрс морт) сӧвмӧ ас гижӧд кыв.', 'Комиясыд и сэні вужвойтыр.'],
        results_word_tokenize = ['Коми', 'кыв', '—', 'финн-йӧгра', 'кывъясысь', 'ӧти', ',', 'коми', 'войтырлӧн', 'чужан', 'кыв', '.'],
        results_pos_tag = [('Коми', 'N'), ('кыв', 'N'), ('—', 'PUNCT'), ('финн-йӧгра', 'Adv'), ('кывъясысь', 'N'), ('ӧти', 'Num'), (',', 'CLB'), ('коми', 'N'), ('войтырлӧн', 'N'), ('чужан', 'V'), ('кыв', 'N'), ('.', 'CLB')],
        results_pos_tag_universal = [('Коми', 'NOUN'), ('кыв', 'NOUN'), ('—', 'PUNCT'), ('финн-йӧгра', 'ADV'), ('кывъясысь', 'NOUN'), ('ӧти', 'NUM'), (',', 'PUNCT'), ('коми', 'NOUN'), ('войтырлӧн', 'NOUN'), ('чужан', 'VERB'), ('кыв', 'NOUN'), ('.', 'PUNCT')],
        results_lemmatize = ['коми', 'кыв', '—', 'финн-йӧгра', 'кыв', 'ӧти', ',', 'коми', 'войтыр', 'чужан', 'кыв', '.'],
        results_dependency_parse = [('Коми', 'кыв', 'obl', 1), ('кыв', 'кыв', 'root', 0), ('—', 'кывъясысь', 'punct', 2), ('финн-йӧгра', 'кывъясысь', 'advmod', 1), ('кывъясысь', 'кыв', 'appos', -3), ('ӧти', 'кывъясысь', 'nummod', -1), (',', 'кыв', 'punct', 4), ('коми', 'войтырлӧн', 'nmod', 1), ('войтырлӧн', 'чужан', 'obl:lmod', 1), ('чужан', 'кыв', 'acl', 1), ('кыв', 'кыв', 'nsubj:cop', -9), ('.', 'кыв', 'punct', -10)]
    )

if __name__ == '__main__':
    test_stanza_kpv()
