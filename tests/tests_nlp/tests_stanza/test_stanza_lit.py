# ----------------------------------------------------------------------
# Wordless: Tests - NLP - Stanza - Lithuanian
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

def test_stanza_lit():
    test_stanza.wl_test_stanza(
        lang = 'lit',
        results_sentence_tokenize = ['Lietuvių kalba – iš baltų prokalbės kilusi lietuvių tautos kalba, kuri Lietuvoje yra valstybinė, o Europos Sąjungoje – viena iš oficialiųjų kalbų.', 'Lietuviškai kalba apie tris milijonus žmonių (dauguma jų gyvena Lietuvoje).', 'Drauge su latvių, mirusiomis prūsų, jotvingių ir kitomis baltų kalbomis priklauso indoeuropiečių kalbų šeimos baltų kalbų grupei.'],
        results_word_tokenize = ['Lietuvių', 'kalba', '–', 'iš', 'baltų', 'prokalbės', 'kilusi', 'lietuvių', 'tautos', 'kalba', ',', 'kuri', 'Lietuvoje', 'yra', 'valstybinė', ',', 'o', 'Europos', 'Sąjungoje', '–', 'viena', 'iš', 'oficialiųjų', 'kalbų', '.'],
        results_pos_tag = [('Lietuvių', 'dkt.vyr.dgs.K.'), ('kalba', 'dkt.mot.vns.V.'), ('–', 'skyr.'), ('iš', 'prl.K.'), ('baltų', 'dkt.mot.dgs.K.'), ('prokalbės', 'dkt.mot.vns.K.'), ('kilusi', 'vksm.dlv.veik.būt-k.mot.vns.V.'), ('lietuvių', 'dkt.vyr.dgs.K.'), ('tautos', 'dkt.mot.vns.K.'), ('kalba', 'dkt.mot.vns.Vn.'), (',', 'skyr.'), ('kuri', 'įv.mot.vns.V.'), ('Lietuvoje', 'dkt.tikr.mot.vns.Vt.'), ('yra', 'vksm.asm.tiesiog.es.vns.3.'), ('valstybinė', 'bdv.nelygin.mot.vns.V.'), (',', 'skyr.'), ('o', 'jng.'), ('Europos', 'dkt.tikr.mot.vns.K.'), ('Sąjungoje', 'dkt.mot.vns.Vt.'), ('–', 'skyr.'), ('viena', 'įv.mot.vns.V.'), ('iš', 'prl.K.'), ('oficialiųjų', 'bdv.nelygin.įvardž.mot.dgs.K.'), ('kalbų', 'dkt.mot.dgs.K.'), ('.', 'skyr.')],
        results_pos_tag_universal = [('Lietuvių', 'NOUN'), ('kalba', 'NOUN'), ('–', 'PUNCT'), ('iš', 'ADP'), ('baltų', 'NOUN'), ('prokalbės', 'NOUN'), ('kilusi', 'VERB'), ('lietuvių', 'NOUN'), ('tautos', 'NOUN'), ('kalba', 'NOUN'), (',', 'PUNCT'), ('kuri', 'DET'), ('Lietuvoje', 'PROPN'), ('yra', 'AUX'), ('valstybinė', 'ADJ'), (',', 'PUNCT'), ('o', 'CCONJ'), ('Europos', 'PROPN'), ('Sąjungoje', 'NOUN'), ('–', 'PUNCT'), ('viena', 'PRON'), ('iš', 'ADP'), ('oficialiųjų', 'ADJ'), ('kalbų', 'NOUN'), ('.', 'PUNCT')],
        results_lemmatize = ['lietuvis', 'kalba', '–', 'iš', 'baltas', 'prokalbė', 'kilti', 'lietuvis', 'tauta', 'kalba', ',', 'kuris', 'Lietuva', 'būti', 'valstybinis', ',', 'o', 'Europa', 'sąjunga', '–', 'vienas', 'iš', 'oficialus', 'kalba', '.'],
        results_dependency_parse = [('Lietuvių', 'kalba', 'nmod', 1), ('kalba', 'kalba', 'root', 0), ('–', 'kalba', 'punct', -1), ('iš', 'prokalbės', 'case', 2), ('baltų', 'prokalbės', 'nmod', 1), ('prokalbės', 'kilusi', 'obl', 1), ('kilusi', 'kalba', 'acl', -5), ('lietuvių', 'tautos', 'nmod', 1), ('tautos', 'kalba', 'nmod', 1), ('kalba', 'kilusi', 'obl:arg', -3), (',', 'valstybinė', 'punct', 4), ('kuri', 'valstybinė', 'nsubj', 3), ('Lietuvoje', 'valstybinė', 'obl', 2), ('yra', 'valstybinė', 'cop', 1), ('valstybinė', 'kalba', 'acl:relcl', -5), (',', 'Sąjungoje', 'punct', 3), ('o', 'Sąjungoje', 'cc', 2), ('Europos', 'Sąjungoje', 'nmod', 1), ('Sąjungoje', 'valstybinė', 'obl', -4), ('–', 'viena', 'punct', 1), ('viena', 'Sąjungoje', 'appos', -2), ('iš', 'kalbų', 'case', 2), ('oficialiųjų', 'kalbų', 'amod', 1), ('kalbų', 'viena', 'obl:arg', -3), ('.', 'kalba', 'punct', -23)]
    )

if __name__ == '__main__':
    test_stanza_lit()
