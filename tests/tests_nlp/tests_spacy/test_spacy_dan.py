# ----------------------------------------------------------------------
# Tests: NLP - spaCy - Danish
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

def test_spacy_dan():
    results_pos_tag = [('Dansk', 'NOUN'), ('er', 'AUX'), ('et', 'DET'), ('østnordisk', 'ADJ'), ('sprog', 'NOUN'), ('indenfor', 'ADP'), ('den', 'DET'), ('germanske', 'ADJ'), ('gren', 'NOUN'), ('af', 'ADP'), ('den', 'DET'), ('indoeuropæiske', 'ADJ'), ('sprogfamilie', 'NOUN'), ('.', 'PUNCT')]

    test_spacy.wl_test_spacy(
        lang = 'dan',
        results_sentence_tokenize_trf = ['Dansk er et østnordisk sprog indenfor den germanske gren af den indoeuropæiske sprogfamilie.', 'Det danske sprog tales af ca. seks millioner mennesker, hovedsageligt i Danmark, men også i Sydslesvig, på Færøerne og Grønland.[1] Dansk er tæt beslægtet med norsk, svensk og islandsk, og sproghistorisk har dansk været stærkt påvirket af plattysk.'],
        results_word_tokenize = ['Dansk', 'er', 'et', 'østnordisk', 'sprog', 'indenfor', 'den', 'germanske', 'gren', 'af', 'den', 'indoeuropæiske', 'sprogfamilie', '.'],
        results_pos_tag = results_pos_tag,
        results_pos_tag_universal = results_pos_tag,
        results_lemmatize = ['dansk', 'være', 'en', 'østnordisk', 'sprog', 'indenfor', 'den', 'germansk', 'gren', 'af', 'den', 'indoeuropæisk', 'sprogfamilie', '.'],
        results_dependency_parse = [('Dansk', 'sprog', 'nsubj', 4), ('er', 'sprog', 'cop', 3), ('et', 'sprog', 'det', 2), ('østnordisk', 'sprog', 'amod', 1), ('sprog', 'sprog', 'ROOT', 0), ('indenfor', 'gren', 'case', 3), ('den', 'gren', 'det', 2), ('germanske', 'gren', 'amod', 1), ('gren', 'sprog', 'nmod', -4), ('af', 'sprogfamilie', 'case', 3), ('den', 'sprogfamilie', 'det', 2), ('indoeuropæiske', 'sprogfamilie', 'amod', 1), ('sprogfamilie', 'gren', 'nmod', -4), ('.', 'sprog', 'punct', -9)]
    )

if __name__ == '__main__':
    test_spacy_dan()
