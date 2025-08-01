# ----------------------------------------------------------------------
# Tests: NLP - spaCy - English
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
from tests import wl_test_init
from wordless.wl_nlp import (
    wl_dependency_parsing,
    wl_word_tokenization
)

main = wl_test_init.Wl_Test_Main(switch_lang_utils = 'spacy')

results_word_tokenize = ['English', 'is', 'a', 'West', 'Germanic', 'language', 'in', 'the', 'Indo', '-', 'European', 'language', 'family', ',', 'whose', 'speakers', ',', 'called', 'Anglophones', ',', 'originated', 'in', 'early', 'medieval', 'England', 'on', 'the', 'island', 'of', 'Great', 'Britain.[4][5][6', ']']

def test_spacy_eng():
    test_spacy.wl_test_spacy(
        lang = 'eng_us',
        results_sentence_tokenize_trf = ['English is a West Germanic language in the Indo-European language family, whose speakers, called Anglophones, originated in early medieval England on the island of Great Britain.[4][5][6]', 'The namesake of the language is the Angles, one of the Germanic peoples that migrated to Britain after its Roman occupiers left.'],
        results_word_tokenize = results_word_tokenize,
        results_pos_tag = [('English', 'NNP'), ('is', 'VBZ'), ('a', 'DT'), ('West', 'JJ'), ('Germanic', 'JJ'), ('language', 'NN'), ('in', 'IN'), ('the', 'DT'), ('Indo', 'JJ'), ('-', 'JJ'), ('European', 'JJ'), ('language', 'NN'), ('family', 'NN'), (',', ','), ('whose', 'WP$'), ('speakers', 'NNS'), (',', ','), ('called', 'VBN'), ('Anglophones', 'NNS'), (',', ','), ('originated', 'VBD'), ('in', 'IN'), ('early', 'JJ'), ('medieval', 'JJ'), ('England', 'NNP'), ('on', 'IN'), ('the', 'DT'), ('island', 'NN'), ('of', 'IN'), ('Great', 'NNP'), ('Britain.[4][5][6', 'NFP'), (']', '-RRB-')],
        results_pos_tag_universal = [('English', 'PROPN'), ('is', 'AUX'), ('a', 'DET'), ('West', 'ADJ'), ('Germanic', 'ADJ'), ('language', 'NOUN'), ('in', 'ADP'), ('the', 'DET'), ('Indo', 'ADJ'), ('-', 'ADJ'), ('European', 'ADJ'), ('language', 'NOUN'), ('family', 'NOUN'), (',', 'PUNCT'), ('whose', 'DET'), ('speakers', 'NOUN'), (',', 'PUNCT'), ('called', 'VERB'), ('Anglophones', 'NOUN'), (',', 'PUNCT'), ('originated', 'VERB'), ('in', 'ADP'), ('early', 'ADJ'), ('medieval', 'ADJ'), ('England', 'PROPN'), ('on', 'ADP'), ('the', 'DET'), ('island', 'NOUN'), ('of', 'ADP'), ('Great', 'PROPN'), ('Britain.[4][5][6', 'PUNCT'), (']', 'PUNCT')],
        results_lemmatize = ['English', 'be', 'a', 'west', 'germanic', 'language', 'in', 'the', 'indo', '-', 'european', 'language', 'family', ',', 'whose', 'speaker', ',', 'call', 'anglophone', ',', 'originate', 'in', 'early', 'medieval', 'England', 'on', 'the', 'island', 'of', 'Great', 'Britain.[4][5][6', ']'],
        results_dependency_parse = [('English', 'is', 'nsubj', 1), ('is', 'is', 'ROOT', 0), ('a', 'language', 'det', 3), ('West', 'Germanic', 'amod', 1), ('Germanic', 'language', 'amod', 1), ('language', 'is', 'attr', -4), ('in', 'language', 'prep', -1), ('the', 'family', 'det', 5), ('Indo', 'family', 'amod', 4), ('-', 'family', 'amod', 3), ('European', 'family', 'amod', 2), ('language', 'family', 'compound', 1), ('family', 'in', 'pobj', -6), (',', 'family', 'punct', -1), ('whose', 'speakers', 'poss', 1), ('speakers', 'originated', 'nsubj', 5), (',', 'called', 'punct', 1), ('called', 'speakers', 'acl', -2), ('Anglophones', 'called', 'oprd', -1), (',', 'speakers', 'punct', -4), ('originated', 'family', 'relcl', -8), ('in', 'originated', 'prep', -1), ('early', 'England', 'amod', 2), ('medieval', 'England', 'amod', 1), ('England', 'in', 'pobj', -3), ('on', 'England', 'prep', -1), ('the', 'island', 'det', 1), ('island', 'on', 'pobj', -2), ('of', 'island', 'prep', -1), ('Great', 'of', 'pobj', -1), ('Britain.[4][5][6', 'of', 'pobj', -2), (']', 'is', 'punct', -30)]
    )

def test_spacy_other():
    test_spacy.wl_test_spacy(
        lang = 'other',
        results_sentence_tokenize_trf = ['English is a West Germanic language in the Indo-European language family, whose speakers, called Anglophones, originated in early medieval England on the island of Great Britain.[4][5][6] The namesake of the language is the Angles, one of the Germanic peoples that migrated to Britain after its Roman occupiers left.'],
        results_word_tokenize = results_word_tokenize
    )

def test_spacy_punc_marks():
    test_sentence = 'Hi, take it!'

    tokens_untokenized = wl_dependency_parsing.wl_dependency_parse(
        main,
        inputs = test_sentence,
        lang = 'eng_us'
    )

    dds_untokenized = [
        (str(token), str(token.head), token.dependency_relation, token.dd, token.dd_no_punc)
        for token in tokens_untokenized
    ]

    tokens = wl_word_tokenization.wl_word_tokenize_flat(
        main,
        text = test_sentence,
        lang = 'eng_us'
    )

    tokens_tokenized = wl_dependency_parsing.wl_dependency_parse(
        main,
        inputs = tokens,
        lang = 'eng_us'
    )

    dds_tokenized = [
        (str(token), str(token.head), token.dependency_relation, token.dd, token.dd_no_punc)
        for token in tokens_tokenized
    ]

    print('eng_us / spacy_eng:')
    print(dds_untokenized)
    print(dds_tokenized)

    assert dds_untokenized == dds_tokenized == [('Hi', 'take', 'intj', 2, 1), (',', 'take', 'punct', 1, 1), ('take', 'take', 'ROOT', 0, 0), ('it', 'take', 'dobj', -1, -1), ('!', 'take', 'punct', -2, -1)]

if __name__ == '__main__':
    test_spacy_eng()
    test_spacy_other()
    test_spacy_punc_marks()
