# ----------------------------------------------------------------------
# Tests: NLP - spaCy - Slovenian
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

from tests.tests_nlp.tests_spacy import test_spacy

def test_spacy_slv():
    test_spacy.wl_test_spacy(
        lang = 'slv',
        results_sentence_tokenize_trf = ['Slovenščina [sloˈʋenʃtʃina] je združeni naziv za uradni knjižni jezik Slovencev in skupno ime za narečja in govore, ki jih govorijo ali so jih nekoč govorili Slovenci.', 'Govori ga okoli 2,5 (dva in pol) milijona govorcev po svetu, od katerih jih večina živi v Sloveniji.', 'Glede na število govorcev ima razmeroma veliko narečij.', 'Slovenščina je zahodni južnoslovanski jezik in eden redkih indoevropskih jezikov, ki je ohranil dvojino.', 'Za zapisovanje slovenskega jezika se danes uporablja gajica, pisava imenovana po hrvaškem jezikoslovcu Ljudevitu Gaju, ki jo je priredil po češkem črkopisu.', 'Slovenska gajica se imenuje slovenica.', 'Pišemo jo od marčne revolucije', '1848.', 'Do takrat smo uporabljali bohoričico.'],
        results_word_tokenize = ['Slovenščina', '[', 'sloˈʋenʃtʃina', ']', 'je', 'združeni', 'naziv', 'za', 'uradni', 'knjižni', 'jezik', 'Slovencev', 'in', 'skupno', 'ime', 'za', 'narečja', 'in', 'govore', ',', 'ki', 'jih', 'govorijo', 'ali', 'so', 'jih', 'nekoč', 'govorili', 'Slovenci', '.'],
        results_pos_tag = [('Slovenščina', 'Npfsn'), ('[', 'Z'), ('sloˈʋenʃtʃina', 'Xf'), (']', 'Z'), ('je', 'Va-r3s-n'), ('združeni', 'Appmsny'), ('naziv', 'Ncmsn'), ('za', 'Sa'), ('uradni', 'Agpmsay'), ('knjižni', 'Agpmsay'), ('jezik', 'Ncmsan'), ('Slovencev', 'Npmpg'), ('in', 'Cc'), ('skupno', 'Agpnsn'), ('ime', 'Ncnsn'), ('za', 'Sa'), ('narečja', 'Ncnpa'), ('in', 'Cc'), ('govore', 'Ncmpa'), (',', 'Z'), ('ki', 'Cs'), ('jih', 'Pp3mpa--y'), ('govorijo', 'Vmpr3p'), ('ali', 'Cc'), ('so', 'Va-r3p-n'), ('jih', 'Pp3mpa--y'), ('nekoč', 'Rgp'), ('govorili', 'Vmpp-pm'), ('Slovenci', 'Npmpn'), ('.', 'Z')],
        results_pos_tag_universal = [('Slovenščina', 'PROPN'), ('[', 'PUNCT'), ('sloˈʋenʃtʃina', 'X'), (']', 'PUNCT'), ('je', 'AUX'), ('združeni', 'ADJ'), ('naziv', 'NOUN'), ('za', 'ADP'), ('uradni', 'ADJ'), ('knjižni', 'ADJ'), ('jezik', 'NOUN'), ('Slovencev', 'PROPN'), ('in', 'CCONJ'), ('skupno', 'ADJ'), ('ime', 'NOUN'), ('za', 'ADP'), ('narečja', 'NOUN'), ('in', 'CCONJ'), ('govore', 'NOUN'), (',', 'PUNCT'), ('ki', 'SCONJ'), ('jih', 'PRON'), ('govorijo', 'VERB'), ('ali', 'CCONJ'), ('so', 'AUX'), ('jih', 'PRON'), ('nekoč', 'ADV'), ('govorili', 'VERB'), ('Slovenci', 'PROPN'), ('.', 'PUNCT')],
        results_lemmatize = ['Slovenščina', '[', 'sloˈʋenʃtʃina', ']', 'biti', 'združen', 'naziv', 'za', 'uraden', 'knjižen', 'jezik', 'Slovenec', 'in', 'skupen', 'ime', 'za', 'narečje', 'in', 'govor', ',', 'ki', 'on', 'govoriti', 'ali', 'biti', 'on', 'nekoč', 'govoriti', 'Slovenec', '.'],
        results_dependency_parse = [('Slovenščina', 'naziv', 'nsubj', 6), ('[', 'sloˈʋenʃtʃina', 'punct', 1), ('sloˈʋenʃtʃina', 'Slovenščina', 'appos', -2), (']', 'sloˈʋenʃtʃina', 'punct', -1), ('je', 'naziv', 'cop', 2), ('združeni', 'naziv', 'amod', 1), ('naziv', 'naziv', 'ROOT', 0), ('za', 'jezik', 'case', 3), ('uradni', 'jezik', 'amod', 2), ('knjižni', 'jezik', 'amod', 1), ('jezik', 'naziv', 'nmod', -4), ('Slovencev', 'jezik', 'nmod', -1), ('in', 'ime', 'cc', 2), ('skupno', 'ime', 'amod', 1), ('ime', 'jezik', 'conj', -4), ('za', 'narečja', 'case', 1), ('narečja', 'ime', 'nmod', -2), ('in', 'govore', 'cc', 1), ('govore', 'narečja', 'conj', -2), (',', 'govorijo', 'punct', 3), ('ki', 'govorijo', 'mark', 2), ('jih', 'govorijo', 'obj', 1), ('govorijo', 'govore', 'acl', -4), ('ali', 'govorili', 'cc', 4), ('so', 'govorili', 'aux', 3), ('jih', 'govorili', 'obj', 2), ('nekoč', 'govorili', 'advmod', 1), ('govorili', 'govorijo', 'conj', -5), ('Slovenci', 'govorili', 'nsubj', -1), ('.', 'naziv', 'punct', -23)]
    )

if __name__ == '__main__':
    test_spacy_slv()
