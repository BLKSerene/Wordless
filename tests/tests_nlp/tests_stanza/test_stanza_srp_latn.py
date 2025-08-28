# ----------------------------------------------------------------------
# Tests: NLP - Stanza - Serbian (Latin script)
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

def test_stanza_srp_latn():
    test_stanza.wl_test_stanza(
        lang = 'srp_latn',
        results_sentence_tokenize = ['Srpski jezik pripada slovenskoj grupi jezika porodice indoevropskih jezika.[12]', 'Srpski jezik je zvaničan u Srbiji, Bosni i Hercegovini i Crnoj Gori i govori ga oko 12 miliona ljudi.[13]'],
        results_word_tokenize = ['Srpski', 'jezik', 'pripada', 'slovenskoj', 'grupi', 'jezika', 'porodice', 'indoevropskih', 'jezika', '.[', '12', ']'],
        results_pos_tag = [('Srpski', 'Agpmsny'), ('jezik', 'Ncmsn'), ('pripada', 'Vmr3s'), ('slovenskoj', 'Agpfsdy'), ('grupi', 'Ncfsd'), ('jezika', 'Ncmsg'), ('porodice', 'Ncfsg'), ('indoevropskih', 'Agpmpgy'), ('jezika', 'Ncmpg'), ('.[', 'Sg'), ('12', 'Mdc'), (']', 'Z')],
        results_pos_tag_universal = [('Srpski', 'ADJ'), ('jezik', 'NOUN'), ('pripada', 'VERB'), ('slovenskoj', 'ADJ'), ('grupi', 'NOUN'), ('jezika', 'NOUN'), ('porodice', 'NOUN'), ('indoevropskih', 'ADJ'), ('jezika', 'NOUN'), ('.[', 'ADP'), ('12', 'NUM'), (']', 'PUNCT')],
        results_lemmatize = ['srpski', 'jezik', 'pripadati', 'slovenski', 'grupa', 'jezik', 'porodica', 'indoevropski', 'jezik', '.[', '12', ']'],
        results_dependency_parse = [('Srpski', 'jezik', 'amod', 1), ('jezik', 'pripada', 'nsubj', 1), ('pripada', 'pripada', 'root', 0), ('slovenskoj', 'grupi', 'amod', 1), ('grupi', 'pripada', 'obl', -2), ('jezika', 'grupi', 'nmod', -1), ('porodice', 'jezika', 'nmod', -1), ('indoevropskih', 'jezika', 'amod', 1), ('jezika', 'porodice', 'nmod', -2), ('.[', '12', 'case', 1), ('12', 'pripada', 'obl', -8), (']', '12', 'punct', -1)]
    )

def test_stanza_srp_cyrl():
    test_stanza.wl_test_stanza(
        lang = 'srp_cyrl',
        results_sentence_tokenize = ['Српски језик припада словенској групи језика породице индоевропских језика.[12]', 'Српски језик је званичан у Србији, Босни и Херцеговини и Црној Гори и говори га око 12 милиона људи.[13]'],
        results_pos_tag = [('Српски', 'Agpmsny'), ('језик', 'Ncmsn'), ('припада', 'Vmr3s'), ('словенској', 'Agpfsdy'), ('групи', 'Ncfsd'), ('језика', 'Ncmsg'), ('породице', 'Ncfsg'), ('индоевропских', 'Agpmpgy'), ('језика', 'Ncmpg'), ('.[', 'Sg'), ('12', 'Mdc'), (']', 'Z')],
        results_pos_tag_universal = [('Српски', 'ADJ'), ('језик', 'NOUN'), ('припада', 'VERB'), ('словенској', 'ADJ'), ('групи', 'NOUN'), ('језика', 'NOUN'), ('породице', 'NOUN'), ('индоевропских', 'ADJ'), ('језика', 'NOUN'), ('.[', 'ADP'), ('12', 'NUM'), (']', 'PUNCT')],
        results_dependency_parse = [('Српски', 'језик', 'amod', 1), ('језик', 'припада', 'nsubj', 1), ('припада', 'припада', 'root', 0), ('словенској', 'групи', 'amod', 1), ('групи', 'припада', 'obl', -2), ('језика', 'групи', 'nmod', -1), ('породице', 'језика', 'nmod', -1), ('индоевропских', 'језика', 'amod', 1), ('језика', 'породице', 'nmod', -2), ('.[', '12', 'case', 1), ('12', 'припада', 'obl', -8), (']', '12', 'punct', -1)]
    )

if __name__ == '__main__':
    test_stanza_srp_latn()
    test_stanza_srp_cyrl()
