# ----------------------------------------------------------------------
# Tests: NLP - spaCy - French
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

def test_spacy_fra():
    results_sentence_tokenize = ['Le français est une langue indo-européenne de la famille des langues romanes dont les locuteurs sont appelés « francophones ».', "Il est la cinquième langue parlée au monde après l'anglais, le mandarin, le hindi et l'espagnol."]
    results_pos_tag = [('Le', 'DET'), ('français', 'NOUN'), ('est', 'AUX'), ('une', 'DET'), ('langue', 'NOUN'), ('indo-européenne', 'ADJ'), ('de', 'ADP'), ('la', 'DET'), ('famille', 'NOUN'), ('des', 'ADP'), ('langues', 'NOUN'), ('romanes', 'ADJ'), ('dont', 'PRON'), ('les', 'DET'), ('locuteurs', 'NOUN'), ('sont', 'AUX'), ('appelés', 'VERB'), ('«', 'PUNCT'), ('francophones', 'ADJ'), ('»', 'PUNCT'), ('.', 'PUNCT')]

    test_spacy.wl_test_spacy(
        lang = 'fra',
        results_sentence_tokenize_dependency_parser = results_sentence_tokenize,
        results_sentence_tokenize_sentence_recognizer = results_sentence_tokenize,
        results_word_tokenize = ['Le', 'français', 'est', 'une', 'langue', 'indo-européenne', 'de', 'la', 'famille', 'des', 'langues', 'romanes', 'dont', 'les', 'locuteurs', 'sont', 'appelés', '«', 'francophones', '»', '.'],
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_lemmatize = ['le', 'français', 'être', 'un', 'langue', 'indo-européen', 'de', 'le', 'famille', 'de', 'langue', 'roman', 'dont', 'le', 'locuteur', 'être', 'appeler', '«', 'francophone', '»', '.'],
        results_dependency_parse = [('Le', 'français', 'det', 1), ('français', 'langue', 'nsubj', 3), ('est', 'langue', 'cop', 2), ('une', 'langue', 'det', 1), ('langue', 'langue', 'ROOT', 0), ('indo-européenne', 'langue', 'amod', -1), ('de', 'famille', 'case', 2), ('la', 'famille', 'det', 1), ('famille', 'langue', 'nmod', -4), ('des', 'langues', 'case', 1), ('langues', 'famille', 'nmod', -2), ('romanes', 'langues', 'amod', -1), ('dont', 'locuteurs', 'nmod', 2), ('les', 'locuteurs', 'det', 1), ('locuteurs', 'appelés', 'nsubj:pass', 2), ('sont', 'appelés', 'aux:pass', 1), ('appelés', 'langue', 'acl', -12), ('«', 'appelés', 'punct', -1), ('francophones', 'appelés', 'xcomp', -2), ('»', 'appelés', 'punct', -3), ('.', 'langue', 'punct', -16)]
    )

if __name__ == '__main__':
    test_spacy_fra()
