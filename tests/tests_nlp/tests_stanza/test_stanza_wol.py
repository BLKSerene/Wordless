# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Wolof
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

def test_stanza_wol():
    test_stanza.wl_test_stanza(
        lang = 'wol',
        results_sentence_tokenize = ['Wolof làkk la wu ñuy wax ci Gàmbi (Gàmbi Wolof), Gànnaar (Gànnaar Wolof), ak Senegaal (Senegaal Wolof).', 'Mi ngi bokk nag moom wolof ci bànqaasub atlas bu làkki Kongóo yu kojug nit ñu ñuul ñi.', 'Mbokkoo gi mu am ak làkku pël lu yàgg la.', 'Am na it lumu séq ak yeneen làkk ci gox bi niki séeréer, joolaa ak basari.'],
        results_word_tokenize = ['Wolof', 'làkk', 'la', 'wu', 'ñuy', 'wax', 'ci', 'Gàmbi', '(', 'Gàmbi', 'Wolof', ')', ',', 'Gànnaar', '(', 'Gànnaar', 'Wolof', ')', ',', 'ak', 'Senegaal', '(', 'Senegaal', 'Wolof', ')', '.'],
        results_pos_tag = [('Wolof', 'NAME'), ('làkk', 'NOUN'), ('la', 'COP'), ('wu', 'PRON'), ('ñu', 'PRON'), ('di', 'AUX'), ('wax', 'VERB'), ('ci', 'PREP'), ('Gàmbi', 'NAME'), ('(', 'PAREN'), ('Gàmbi', 'NAME'), ('Wolof', 'NAME'), (')', 'PAREN'), (',', 'COMMA'), ('Gànnaar', 'NAME'), ('(', 'PAREN'), ('Gànnaar', 'NAME'), ('Wolof', 'NAME'), (')', 'PAREN'), (',', 'COMMA'), ('ak', 'CONJ'), ('Senegaal', 'NAME'), ('(', 'PAREN'), ('Senegaal', 'NAME'), ('Wolof', 'NAME'), (')', 'PAREN'), ('.', 'PERIOD')],
        results_pos_tag_universal = [('Wolof', 'PROPN'), ('làkk', 'NOUN'), ('la', 'AUX'), ('wu', 'PRON'), ('ñu', 'PRON'), ('di', 'AUX'), ('wax', 'VERB'), ('ci', 'ADP'), ('Gàmbi', 'PROPN'), ('(', 'PUNCT'), ('Gàmbi', 'PROPN'), ('Wolof', 'PROPN'), (')', 'PUNCT'), (',', 'PUNCT'), ('Gànnaar', 'PROPN'), ('(', 'PUNCT'), ('Gànnaar', 'PROPN'), ('Wolof', 'PROPN'), (')', 'PUNCT'), (',', 'PUNCT'), ('ak', 'CCONJ'), ('Senegaal', 'PROPN'), ('(', 'PUNCT'), ('Senegaal', 'PROPN'), ('Wolof', 'PROPN'), (')', 'PUNCT'), ('.', 'PUNCT')],
        results_lemmatize = ['Wolof', 'làkk', 'la', 'bu', 'mu', 'di', 'wax', 'ci', 'Gàmbi', '(', 'Gàmbi', 'Wolof', ')', ',', 'Gànnaar', '(', 'Gànnaar', 'Wolof', ')', ',', 'ak', 'Senegaal', '(', 'Senegaal', 'Wolof', ')', '.'],
        results_dependency_parse = [('Wolof', 'làkk', 'nsubj', 1), ('làkk', 'làkk', 'root', 0), ('la', 'làkk', 'cop', -1), ('wu', 'wax', 'obj', 3), ('ñu', 'wax', 'nsubj', 2), ('di', 'wax', 'aux', 1), ('wax', 'làkk', 'acl:relcl', -5), ('ci', 'Gàmbi', 'case', 1), ('Gàmbi', 'wax', 'obl', -2), ('(', 'Gàmbi', 'punct', 1), ('Gàmbi', 'Gàmbi', 'appos', -2), ('Wolof', 'Gàmbi', 'nmod', -1), (')', 'Gàmbi', 'punct', -2), (',', 'Gànnaar', 'punct', 1), ('Gànnaar', 'Gàmbi', 'conj', -4), ('(', 'Gànnaar', 'punct', 1), ('Gànnaar', 'Gàmbi', 'nmod', -6), ('Wolof', 'Gànnaar', 'flat', -1), (')', 'Gànnaar', 'punct', -2), (',', 'Senegaal', 'punct', 2), ('ak', 'Senegaal', 'cc', 1), ('Senegaal', 'Gànnaar', 'conj', -5), ('(', 'Senegaal', 'punct', 1), ('Senegaal', 'Senegaal', 'appos', -2), ('Wolof', 'Senegaal', 'flat', -1), (')', 'Senegaal', 'punct', -2), ('.', 'làkk', 'punct', -25)]
    )

if __name__ == '__main__':
    test_stanza_wol()
