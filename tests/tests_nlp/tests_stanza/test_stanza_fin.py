# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Finnish
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

def test_stanza_fin():
    test_stanza.wl_test_stanza(
        lang = 'fin',
        results_sentence_tokenize = ['Suomen kieli eli suomi on uralilaisten kielten itämerensuomalaiseen ryhmään kuuluva kieli, jota puhuvat pääosin suomalaiset.', 'Suomessa suomen kieltä puhuu äidinkielenään 4,8 miljoonaa ja toisena kielenään 0,5 miljoonaa ihmistä.', 'Suurimmat suomea puhuvat vähemmistöt ovat Ruotsissa, Norjassa ja Venäjällä.'],
        results_word_tokenize = ['Suomen', 'kieli', 'eli', 'suomi', 'on', 'uralilaisten', 'kielten', 'itämerensuomalaiseen', 'ryhmään', 'kuuluva', 'kieli', ',', 'jota', 'puhuvat', 'pääosin', 'suomalaiset', '.'],
        results_pos_tag = [('Suomen', 'N'), ('kieli', 'N'), ('eli', 'C'), ('suomi', 'N'), ('on', 'V'), ('uralilaisten', 'A'), ('kielten', 'N'), ('itämerensuomalaiseen', 'A'), ('ryhmään', 'N'), ('kuuluva', 'V'), ('kieli', 'N'), (',', 'Punct'), ('jota', 'Pron'), ('puhuvat', 'V'), ('pääosin', 'Adv'), ('suomalaiset', 'N'), ('.', 'Punct')],
        results_pos_tag_universal = [('Suomen', 'PROPN'), ('kieli', 'NOUN'), ('eli', 'CCONJ'), ('suomi', 'PROPN'), ('on', 'AUX'), ('uralilaisten', 'ADJ'), ('kielten', 'NOUN'), ('itämerensuomalaiseen', 'ADJ'), ('ryhmään', 'NOUN'), ('kuuluva', 'VERB'), ('kieli', 'NOUN'), (',', 'PUNCT'), ('jota', 'PRON'), ('puhuvat', 'VERB'), ('pääosin', 'ADV'), ('suomalaiset', 'NOUN'), ('.', 'PUNCT')],
        results_lemmatize = ['Suomi', 'kieli', 'eli', 'suomi', 'olla', 'uralilainen', 'kieli', 'itämerensuomalainen', 'ryhmä', 'kuulua', 'kieli', ',', 'joka', 'puhua', 'pääosin', 'suomalainen', '.'],
        results_dependency_parse = [('Suomen', 'kieli', 'nmod:poss', 1), ('kieli', 'kieli', 'nsubj:cop', 9), ('eli', 'suomi', 'cc', 1), ('suomi', 'kieli', 'conj', -2), ('on', 'kieli', 'cop', 6), ('uralilaisten', 'kielten', 'amod', 1), ('kielten', 'ryhmään', 'nmod:poss', 2), ('itämerensuomalaiseen', 'ryhmään', 'amod', 1), ('ryhmään', 'kuuluva', 'obl', 1), ('kuuluva', 'kieli', 'acl', 1), ('kieli', 'kieli', 'root', 0), (',', 'puhuvat', 'punct', 2), ('jota', 'puhuvat', 'obj', 1), ('puhuvat', 'kieli', 'acl:relcl', -3), ('pääosin', 'suomalaiset', 'advmod', 1), ('suomalaiset', 'puhuvat', 'nsubj', -2), ('.', 'kieli', 'punct', -6)]
    )

if __name__ == '__main__':
    test_stanza_fin()
