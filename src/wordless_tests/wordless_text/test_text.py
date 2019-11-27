#
# Wordless: Tests - Text - Text
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import sys

sys.path.append('.')

from wordless_tests import test_init
from wordless_text import wordless_text

main = test_init.Test_Main()

def new_file(text_type):
    new_file = {}

    new_file['lang'] = 'eng'
    new_file['text_type'] = text_type
    new_file['path'] = f'wordless_tests/files/wordless_text/eng.txt'
    new_file['encoding'] = 'utf_8'

    return new_file

def test_text_untokenized_untagged():
    file = new_file(text_type = ('untokenized', 'untagged'))

    text_flat_tokens = wordless_text.Wordless_Text(main, file,
                                                   flat_tokens = True)
    text = wordless_text.Wordless_Text(main, file,
                                       flat_tokens = False)

    assert text_flat_tokens.tags_pos == [[]] * len(text_flat_tokens.tokens_flat)
    assert text_flat_tokens.tags_non_pos == [[]] * len(text_flat_tokens.tokens_flat)
    assert text_flat_tokens.tags_all == [[]] * len(text_flat_tokens.tokens_flat)

    assert text_flat_tokens.offsets_paras == [0]
    assert text_flat_tokens.offsets_sentences == [0]
    assert text_flat_tokens.offsets_clauses == [0]

    assert (len(text_flat_tokens.tokens_flat) ==
            len(text_flat_tokens.tags_pos) ==
            len(text_flat_tokens.tags_non_pos) ==
            len(text_flat_tokens.tags_all))

    assert len(text_flat_tokens.offsets_paras) == len(text_flat_tokens.tokens_hierarchical)
    assert len(text_flat_tokens.offsets_sentences) == sum([len(para)
                                                           for para in text_flat_tokens.tokens_hierarchical])
    assert len(text_flat_tokens.offsets_clauses) == sum([len(sentence)
                                                         for para in text_flat_tokens.tokens_hierarchical
                                                         for sentence in para])

    assert text.tokens_flat != []
    assert text.tags_pos == [[]] * len(text.tokens_flat)
    assert text.tags_non_pos == [[]] * len(text.tokens_flat)
    assert text.tags_all == [[]] * len(text.tokens_flat)

    assert text.offsets_paras != [0]
    assert text.offsets_sentences != [0]
    assert text.offsets_clauses != [0]

    assert (len(text.tokens_flat) ==
            len(text.tags_pos) ==
            len(text.tags_non_pos) ==
            len(text.tags_all))

    assert len(text.offsets_paras) == len(text.tokens_hierarchical)
    assert len(text.offsets_sentences) == sum([len(para)
                                               for para in text.tokens_hierarchical])
    assert len(text.offsets_clauses) == sum([len(sentence)
                                             for para in text.tokens_hierarchical
                                             for sentence in para])

def test_text_untokenized_tagged_non_pos():
    file = new_file(text_type = ('untokenized', 'tagged_non_pos'))

    text_flat_tokens = wordless_text.Wordless_Text(main, file,
                                                   flat_tokens = True)
    text = wordless_text.Wordless_Text(main, file,
                                       flat_tokens = False)

    assert text_flat_tokens.tokens_flat != []
    assert text_flat_tokens.tags_pos == [[]] * len(text_flat_tokens.tokens_flat)
    assert text_flat_tokens.tags_non_pos != [[]] * len(text_flat_tokens.tokens_flat)
    assert text_flat_tokens.tags_all == text_flat_tokens.tags_non_pos

    assert text_flat_tokens.offsets_paras == [0]
    assert text_flat_tokens.offsets_sentences == [0]
    assert text_flat_tokens.offsets_clauses == [0]

    assert (len(text_flat_tokens.tokens_flat) ==
            len(text_flat_tokens.tags_pos) ==
            len(text_flat_tokens.tags_non_pos) ==
            len(text_flat_tokens.tags_all))

    assert len(text_flat_tokens.offsets_paras) == len(text_flat_tokens.tokens_hierarchical)
    assert len(text_flat_tokens.offsets_sentences) == sum([len(para)
                                                           for para in text_flat_tokens.tokens_hierarchical])
    assert len(text_flat_tokens.offsets_clauses) == sum([len(sentence)
                                                         for para in text_flat_tokens.tokens_hierarchical
                                                         for sentence in para])

    assert text.tokens_flat != []
    assert text.tags_pos == [[]] * len(text.tokens_flat)
    assert text.tags_non_pos != [[]] * len(text.tokens_flat)
    assert text.tags_all == text_flat_tokens.tags_non_pos

    assert text.offsets_paras != [0]
    assert text.offsets_sentences != [0]
    assert text.offsets_clauses != [0]

    assert (len(text.tokens_flat) ==
            len(text.tags_pos) ==
            len(text.tags_non_pos) ==
            len(text.tags_all))

    assert len(text.offsets_paras) == len(text.tokens_hierarchical)
    assert len(text.offsets_sentences) == sum([len(para)
                                               for para in text.tokens_hierarchical])
    assert len(text.offsets_clauses) == sum([len(sentence)
                                             for para in text.tokens_hierarchical
                                             for sentence in para])

def test_text_tokenized_untagged():
    file = new_file(text_type = ('tokenized', 'untagged'))

    text_flat_tokens = wordless_text.Wordless_Text(main, file,
                                                   flat_tokens = True)
    text = wordless_text.Wordless_Text(main, file,
                                       flat_tokens = False)

    assert text_flat_tokens.tokens_flat != []
    assert text_flat_tokens.tags_pos == [[]] * len(text_flat_tokens.tokens_flat)
    assert text_flat_tokens.tags_non_pos == [[]] * len(text_flat_tokens.tokens_flat)
    assert text_flat_tokens.tags_all == [[]] * len(text_flat_tokens.tokens_flat)

    assert text_flat_tokens.offsets_paras == [0]
    assert text_flat_tokens.offsets_sentences == [0]
    assert text_flat_tokens.offsets_clauses == [0]

    assert (len(text_flat_tokens.tokens_flat) ==
            len(text_flat_tokens.tags_pos) ==
            len(text_flat_tokens.tags_non_pos) ==
            len(text_flat_tokens.tags_all))

    assert len(text_flat_tokens.offsets_paras) == len(text_flat_tokens.tokens_hierarchical)
    assert len(text_flat_tokens.offsets_sentences) == sum([len(para)
                                                           for para in text_flat_tokens.tokens_hierarchical])
    assert len(text_flat_tokens.offsets_clauses) == sum([len(sentence)
                                                         for para in text_flat_tokens.tokens_hierarchical
                                                         for sentence in para])

    assert text.tokens_flat != []
    assert text.tags_pos == [[]] * len(text.tokens_flat)
    assert text.tags_non_pos == [[]] * len(text.tokens_flat)
    assert text.tags_all == [[]] * len(text.tokens_flat)

    assert text.offsets_paras != [0]
    assert text.offsets_sentences != [0]
    assert text.offsets_clauses != [0]

    assert (len(text.tokens_flat) ==
            len(text.tags_pos) ==
            len(text.tags_non_pos) ==
            len(text.tags_all))

    assert len(text.offsets_paras) == len(text.tokens_hierarchical)
    assert len(text.offsets_sentences) == sum([len(para)
                                               for para in text.tokens_hierarchical])
    assert len(text.offsets_clauses) == sum([len(sentence)
                                             for para in text.tokens_hierarchical
                                             for sentence in para])

def test_text_tokenized_tagged_pos():
    file = new_file(text_type = ('tokenized', 'tagged_pos'))

    text_flat_tokens = wordless_text.Wordless_Text(main, file,
                                                   flat_tokens = True)
    text = wordless_text.Wordless_Text(main, file,
                                       flat_tokens = False)

    assert text_flat_tokens.tokens_flat != []
    assert text_flat_tokens.tags_pos != [[]] * len(text_flat_tokens.tokens_flat)
    assert text_flat_tokens.tags_non_pos == [[]] * len(text_flat_tokens.tokens_flat)
    assert text_flat_tokens.tags_all == text_flat_tokens.tags_pos

    assert text_flat_tokens.offsets_paras == [0]
    assert text_flat_tokens.offsets_sentences == [0]
    assert text_flat_tokens.offsets_clauses == [0]

    assert (len(text_flat_tokens.tokens_flat) ==
            len(text_flat_tokens.tags_pos) ==
            len(text_flat_tokens.tags_non_pos) ==
            len(text_flat_tokens.tags_all))

    assert len(text_flat_tokens.offsets_paras) == len(text_flat_tokens.tokens_hierarchical)
    assert len(text_flat_tokens.offsets_sentences) == sum([len(para)
                                                           for para in text_flat_tokens.tokens_hierarchical])
    assert len(text_flat_tokens.offsets_clauses) == sum([len(sentence)
                                                         for para in text_flat_tokens.tokens_hierarchical
                                                         for sentence in para])

    assert text.tokens_flat != []
    assert text.tags_pos != [[]] * len(text.tokens_flat)
    assert text.tags_non_pos == [[]] * len(text.tokens_flat)
    assert text.tags_all == text.tags_pos

    assert text.offsets_paras != [0]
    assert text.offsets_sentences != [0]
    assert text.offsets_clauses != [0]

    assert (len(text.tokens_flat) ==
            len(text.tags_pos) ==
            len(text.tags_non_pos) ==
            len(text.tags_all))

    assert len(text.offsets_paras) == len(text.tokens_hierarchical)
    assert len(text.offsets_sentences) == sum([len(para)
                                               for para in text.tokens_hierarchical])
    assert len(text.offsets_clauses) == sum([len(sentence)
                                             for para in text.tokens_hierarchical
                                             for sentence in para])

def test_text_tokenized_tagged_non_pos():
    file = new_file(text_type = ('tokenized', 'tagged_non_pos'))

    text_flat_tokens = wordless_text.Wordless_Text(main, file,
                                                   flat_tokens = True)
    text = wordless_text.Wordless_Text(main, file,
                                       flat_tokens = False)

    assert text_flat_tokens.tokens_flat != []
    assert text_flat_tokens.tags_pos == [[]] * len(text_flat_tokens.tokens_flat)
    assert text_flat_tokens.tags_non_pos != [[]] * len(text_flat_tokens.tokens_flat)
    assert text_flat_tokens.tags_all == text_flat_tokens.tags_non_pos

    assert text_flat_tokens.offsets_paras == [0]
    assert text_flat_tokens.offsets_sentences == [0]
    assert text_flat_tokens.offsets_clauses == [0]

    assert (len(text_flat_tokens.tokens_flat) ==
            len(text_flat_tokens.tags_pos) ==
            len(text_flat_tokens.tags_non_pos) ==
            len(text_flat_tokens.tags_all))

    assert len(text_flat_tokens.offsets_paras) == len(text_flat_tokens.tokens_hierarchical)
    assert len(text_flat_tokens.offsets_sentences) == sum([len(para)
                                                           for para in text_flat_tokens.tokens_hierarchical])
    assert len(text_flat_tokens.offsets_clauses) == sum([len(sentence)
                                                         for para in text_flat_tokens.tokens_hierarchical
                                                         for sentence in para])

    assert text.tokens_flat != []
    assert text.tags_pos == [[]] * len(text.tokens_flat)
    assert text.tags_non_pos != [[]] * len(text.tokens_flat)
    assert text.tags_all == text.tags_non_pos

    assert text.offsets_paras != [0]
    assert text.offsets_sentences != [0]
    assert text.offsets_clauses != [0]

    assert (len(text.tokens_flat) ==
            len(text.tags_pos) ==
            len(text.tags_non_pos) ==
            len(text.tags_all))

    assert len(text.offsets_paras) == len(text.tokens_hierarchical)
    assert len(text.offsets_sentences) == sum([len(para)
                                               for para in text.tokens_hierarchical])
    assert len(text.offsets_clauses) == sum([len(sentence)
                                             for para in text.tokens_hierarchical
                                             for sentence in para])


def test_text_tokenized_tagged_both():
    file = new_file(text_type = ('tokenized', 'tagged_both'))

    text_flat_tokens = wordless_text.Wordless_Text(main, file,
                                                   flat_tokens = True)
    text = wordless_text.Wordless_Text(main, file,
                                       flat_tokens = False)

    assert text_flat_tokens.tokens_flat != []
    assert text_flat_tokens.tags_pos != [[]] * len(text_flat_tokens.tokens_flat)
    assert text_flat_tokens.tags_non_pos != [[]] * len(text_flat_tokens.tokens_flat)
    assert text_flat_tokens.tags_all != [[]] * len(text_flat_tokens.tokens_flat)

    assert text_flat_tokens.offsets_paras == [0]
    assert text_flat_tokens.offsets_sentences == [0]
    assert text_flat_tokens.offsets_clauses == [0]

    assert (len(text_flat_tokens.tokens_flat) ==
            len(text_flat_tokens.tags_pos) ==
            len(text_flat_tokens.tags_non_pos) ==
            len(text_flat_tokens.tags_all))

    assert len(text_flat_tokens.offsets_paras) == len(text_flat_tokens.tokens_hierarchical)
    assert len(text_flat_tokens.offsets_sentences) == sum([len(para)
                                                           for para in text_flat_tokens.tokens_hierarchical])
    assert len(text_flat_tokens.offsets_clauses) == sum([len(sentence)
                                                         for para in text_flat_tokens.tokens_hierarchical
                                                         for sentence in para])

    assert text.tokens_flat != []
    assert text.tags_pos != [[]] * len(text.tokens_flat)
    assert text.tags_non_pos != [[]] * len(text.tokens_flat)
    assert text.tags_all != [[]] * len(text.tokens_flat)

    assert text.offsets_paras != [0]
    assert text.offsets_sentences != [0]
    assert text.offsets_clauses != [0]

    assert (len(text.tokens_flat) ==
            len(text.tags_pos) ==
            len(text.tags_non_pos) ==
            len(text.tags_all))

    assert len(text.offsets_paras) == len(text.tokens_hierarchical)
    assert len(text.offsets_sentences) == sum([len(para)
                                               for para in text.tokens_hierarchical])
    assert len(text.offsets_clauses) == sum([len(sentence)
                                             for para in text.tokens_hierarchical
                                             for sentence in para])
