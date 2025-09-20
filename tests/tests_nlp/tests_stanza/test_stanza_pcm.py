# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Nigerian Pidgin
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

def test_stanza_pcm():
    results_pos_tag = [('Naijá', 'PROPN'), ('langwej', 'NOUN'), ('na', 'AUX'), ('popula', 'ADJ'), ('langwej', 'NOUN'), ('for', 'ADP'), ('Naija', 'PROPN'), ('an', 'NOUN'), ('pipul', 'NOUN'), ('wey', 'SCONJ'), ('dey', 'AUX'), ('spik', 'VERB'), ('am', 'PRON'), ('for', 'ADP'), ('Naijá', 'PROPN'), ('pas', 'NOUN'), ('75', 'X'), ('miliọn.', 'NOUN')]

    test_stanza.wl_test_stanza(
        lang = 'pcm',
        results_sentence_tokenize = ['Naijá langwej na popula langwej for Naija an pipul wey dey spik am for Naijá pas 75 miliọn. Naijá na pijin, a langwej for oda langwej. Naijá for Inglish an wey Afrikan langwej.'],
        results_word_tokenize = ['Naijá', 'langwej', 'na', 'popula', 'langwej', 'for', 'Naija', 'an', 'pipul', 'wey', 'dey', 'spik', 'am', 'for', 'Naijá', 'pas', '75', 'miliọn.'],
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_lemmatize = ['Naijá', 'langwej', 'na', 'popula', 'langwej', 'for', 'Naija', 'a', 'pipul', 'wey', 'dey', 'spik', 'am', 'for', 'Naijá', 'pas', '75', 'miliọn.'],
        results_dependency_parse = [('Naijá', 'langwej', 'compound', 1), ('langwej', 'langwej', 'nsubj', 3), ('na', 'langwej', 'cop', 2), ('popula', 'langwej', 'amod', 1), ('langwej', 'langwej', 'root', 0), ('for', 'pipul', 'case', 3), ('Naija', 'pipul', 'compound', 2), ('an', 'pipul', 'compound', 1), ('pipul', 'langwej', 'nmod', -4), ('wey', 'spik', 'mark', 2), ('dey', 'spik', 'aux', 1), ('spik', 'pipul', 'acl:relcl', -3), ('am', 'spik', 'obj', -1), ('for', 'pas', 'case', 2), ('Naijá', 'pas', 'compound', 1), ('pas', 'spik', 'obl:arg', -4), ('75', 'langwej', 'dep', -12), ('miliọn.', 'miliọn.', 'root', 0)]
    )

if __name__ == '__main__':
    test_stanza_pcm()
