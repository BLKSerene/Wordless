# ----------------------------------------------------------------------
# Tests: NLP - spaCy - Catalan
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

def test_spacy_cat():
    results_pos_tag = [('Hi', 'PRON'), ('ha', 'VERB'), ('altres', 'DET'), ('glotònims', 'NOUN'), ('tradicionals', 'ADJ'), ('que', 'PRON'), ('es', 'PRON'), ('fan', 'VERB'), ('servir', 'VERB'), ('com', 'SCONJ'), ('a', 'ADP'), ('sinònim', 'NOUN'), ('de', 'ADP'), ('"', 'PUNCT'), ('català', 'NOUN'), ('"', 'PUNCT'), ('a', 'ADP'), ('l', 'DET'), ('llarg', 'NOUN'), ('d', 'ADP'), ('el', 'DET'), ('domini', 'NOUN'), ('lingüístic', 'ADJ'), ('.', 'PUNCT')]

    test_spacy.wl_test_spacy(
        lang = 'cat',
        results_sentence_tokenize_trf = ['Hi ha altres glotònims tradicionals que es fan servir com a sinònim de "català" al llarg del domini lingüístic.', "Així, per exemple, a l'Alguer se li diu alguerès, a Fraga, fragatí, a Maella, maellà i a la comarca de la Llitera, lliterà."],
        results_word_tokenize = ['Hi', 'ha', 'altres', 'glotònims', 'tradicionals', 'que', 'es', 'fan', 'servir', 'com', 'a', 'sinònim', 'de', '"', 'català', '"', 'a', 'l', 'llarg', 'd', 'el', 'domini', 'lingüístic', '.'],
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_lemmatize = ['hi', 'haver', 'altre', 'glotònim', 'tradicional', 'que', 'se', 'fer', 'servir', 'com', 'a', 'sinònim', 'de', '"', 'català', '"', 'a', 'el', 'llarg', 'de', 'el', 'domini', 'lingüístic', '.'],
        results_dependency_parse = [('Hi', 'ha', 'obj', 1), ('ha', 'ha', 'ROOT', 0), ('altres', 'glotònims', 'det', 1), ('glotònims', 'ha', 'obj', -2), ('tradicionals', 'glotònims', 'amod', -1), ('que', 'fan', 'nsubj', 2), ('es', 'fan', 'obj', 1), ('fan', 'glotònims', 'acl', -4), ('servir', 'fan', 'compound', -1), ('com', 'sinònim', 'case', 2), ('a', 'com', 'fixed', -1), ('sinònim', 'fan', 'obj', -4), ('de', 'català', 'case', 2), ('"', 'català', 'punct', 1), ('català', 'sinònim', 'nmod', -3), ('"', 'català', 'punct', -1), ('a', 'domini', 'case', 5), ('l', 'domini', 'det', 4), ('llarg', 'a', 'fixed', -2), ('d', 'a', 'case', -3), ('el', 'a', 'det', -4), ('domini', 'fan', 'obl', -14), ('lingüístic', 'domini', 'amod', -1), ('.', 'ha', 'punct', -22)]
    )

if __name__ == '__main__':
    test_spacy_cat()
