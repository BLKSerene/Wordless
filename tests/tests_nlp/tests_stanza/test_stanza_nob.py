# ----------------------------------------------------------------------
# Wordless: Tests - NLP - Stanza - Norwegian Bokmål
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

def test_stanza_nob():
    results_pos_tag = [('Bokmål', 'PROPN'), ('er', 'AUX'), ('en', 'DET'), ('varietet', 'NOUN'), ('av', 'ADP'), ('norsk', 'ADJ'), ('skriftspråk', 'NOUN'), ('.', 'PUNCT')]

    test_stanza.wl_test_stanza(
        lang = 'nob',
        results_sentence_tokenize = ['Bokmål er en varietet av norsk skriftspråk.', 'Bokmål er en av to offisielle målformer av norsk skriftspråk, hvorav den andre er nynorsk.', 'I skrift har 87,3% bokmål som hovedmål i skolen.', '[1] Etter skriftreformene av riksmål i 1987 og bokmål i 1981 og 2005 er det lite som skiller bokmål og riksmål i alminnelig bruk.'],
        results_word_tokenize = ['Bokmål', 'er', 'en', 'varietet', 'av', 'norsk', 'skriftspråk', '.'],
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_lemmatize = ['Bokmål', 'være', 'en', 'varietet', 'av', 'norsk', 'skriftspråk', '$.'],
        results_dependency_parse = [('Bokmål', 'varietet', 'nsubj', 3), ('er', 'varietet', 'cop', 2), ('en', 'varietet', 'det', 1), ('varietet', 'varietet', 'root', 0), ('av', 'skriftspråk', 'case', 2), ('norsk', 'skriftspråk', 'amod', 1), ('skriftspråk', 'varietet', 'nmod', -3), ('.', 'varietet', 'punct', -4)]
    )

if __name__ == '__main__':
    test_stanza_nob()
