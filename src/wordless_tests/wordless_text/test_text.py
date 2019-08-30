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

def new_file(file_name, text_type):
    new_file = {}

    new_file['lang'] = 'eng'
    new_file['text_type'] = text_type
    new_file['path'] = f'wordless_tests/files/tags/{file_name}.txt'
    new_file['encoding'] = 'utf_8'

    return new_file

def test_text_untokenized_untagged():
    file = new_file(file_name = 'untokenized_untagged',
                    text_type = ('untokenized', 'untagged'))

    text_tokens_only = wordless_text.Wordless_Text(main, file,
                                                   tokens_only = True)
    text = wordless_text.Wordless_Text(main, file,
                                       tokens_only = False)

    assert text_tokens_only.tokens == ['English', 'is', 'a', 'West', 'Germanic', 'language', 'that', 'was', 'first', 'spoken', 'in', 'early', 'medieval', 'England', 'and', 'eventually', 'became', 'a', 'global', 'lingua', 'franca', '.', 'Named', 'after', 'the', 'Angles', ',', 'one', 'of', 'the', 'Germanic', 'tribes', 'that', 'migrated', 'to', 'the', 'area', 'of', 'Great', 'Britain', 'that', 'would', 'later', 'take', 'their', 'name', ',', 'England', ',', 'both', 'names', 'ultimately', 'deriving', 'from', 'the', 'Anglia', 'peninsula', 'in', 'the', 'Baltic', 'Sea', '.', 'It', 'is', 'closely', 'related', 'to', 'the', 'Frisian', 'languages', ',', 'but', 'its', 'vocabulary', 'has', 'been', 'significantly', 'influenced', 'by', 'other', 'Germanic', 'languages', ',', 'particularly', 'Norse', '(', 'a', 'North', 'Germanic', 'language', ')', ',', 'and', 'to', 'a', 'greater', 'extent', 'Latin', 'and', 'French', '.']
    assert text_tokens_only.tags_pos == [[]] * len(text_tokens_only.tokens)
    assert text_tokens_only.tags_non_pos == [[]] * len(text_tokens_only.tokens)
    assert text_tokens_only.tags_all == [[]] * len(text_tokens_only.tokens)
    assert text_tokens_only.offsets_paras == [0]
    assert text_tokens_only.offsets_sentences == [0]
    assert text_tokens_only.offsets_clauses == [0, 27, 47, 49, 71, 83, 92]

    assert (len(text_tokens_only.tokens) ==
            len(text_tokens_only.tags_pos) ==
            len(text_tokens_only.tags_non_pos) ==
            len(text_tokens_only.tags_all))
    assert len(text_tokens_only.offsets_paras) == len(text_tokens_only.tokens_sentences_paras)
    assert len(text_tokens_only.offsets_sentences) == sum([len(para)
                                                           for para in text_tokens_only.tokens_sentences_paras])

    assert text.tokens == ['English', 'is', 'a', 'West', 'Germanic', 'language', 'that', 'was', 'first', 'spoken', 'in', 'early', 'medieval', 'England', 'and', 'eventually', 'became', 'a', 'global', 'lingua', 'franca', '.', 'Named', 'after', 'the', 'Angles', ',', 'one', 'of', 'the', 'Germanic', 'tribes', 'that', 'migrated', 'to', 'the', 'area', 'of', 'Great', 'Britain', 'that', 'would', 'later', 'take', 'their', 'name', ',', 'England', ',', 'both', 'names', 'ultimately', 'deriving', 'from', 'the', 'Anglia', 'peninsula', 'in', 'the', 'Baltic', 'Sea', '.', 'It', 'is', 'closely', 'related', 'to', 'the', 'Frisian', 'languages', ',', 'but', 'its', 'vocabulary', 'has', 'been', 'significantly', 'influenced', 'by', 'other', 'Germanic', 'languages', ',', 'particularly', 'Norse', '(', 'a', 'North', 'Germanic', 'language', ')', ',', 'and', 'to', 'a', 'greater', 'extent', 'Latin', 'and', 'French', '.']
    assert text.tags_pos == [[]] * len(text.tokens)
    assert text.tags_non_pos == [[]] * len(text.tokens)
    assert text.tags_all == [[]] * len(text.tokens)
    assert text.offsets_paras == [0]
    assert text.offsets_sentences == [0, 22, 62]
    assert text.offsets_clauses == [0, 22, 27, 47, 49, 62, 71, 83, 92]

    assert (len(text.tokens) ==
            len(text.tags_pos) ==
            len(text.tags_non_pos) ==
            len(text.tags_all))
    assert len(text.offsets_paras) == len(text.tokens_sentences_paras)
    assert len(text.offsets_sentences) == sum([len(para)
                                               for para in text.tokens_sentences_paras])

def test_text_untokenized_tagged_non_pos():
    file = new_file(file_name = 'untokenized_tagged_non_pos',
                    text_type = ('untokenized', 'tagged_non_pos'))

    text_tokens_only = wordless_text.Wordless_Text(main, file,
                                                   tokens_only = True)
    text = wordless_text.Wordless_Text(main, file,
                                       tokens_only = False)

    assert text_tokens_only.tokens == ['', 'English', 'is', 'a', 'West', 'Germanic', 'language', 'that', 'was', 'first', 'spoken', 'in', 'early', 'medieval', 'England', 'and', 'eventually', 'became', 'a', 'global', 'lingua', 'franca', '.', 'Named', 'after', 'the', 'Angles', ',', 'one', 'of', 'the', 'Germanic', 'tribes', 'that', 'migrated', 'to', 'the', 'area', 'of', 'Great', 'Britain', 'that', 'would', 'later', 'take', 'their', 'name', ',', 'England', ',', 'both', 'names', 'ultimately', 'deriving', 'from', 'the', 'Anglia', 'peninsula', 'in', 'the', 'Baltic', 'Sea', '.', 'It', 'is', 'closely', 'related', 'to', 'the', 'Frisian', 'languages', ',', 'but', 'its', 'vocabulary', 'has', 'been', 'significantly', 'influenced', 'by', 'other', 'Germanic', 'languages', ',', 'particularly', 'Norse', '(', 'a', 'North', 'Germanic', 'language', ')', ',', 'and', 'to', 'a', 'greater', 'extent', 'Latin', 'and', 'French', '.']
    assert text_tokens_only.tags_pos == [[]] * len(text_tokens_only.tokens)
    assert text_tokens_only.tags_non_pos == [['<TAG1>', '<TAG2>'], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ['[4]', '[5]'], [], [], [], [], [], [], [], [], [], ['<TAG3>'], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ['<TAG3>'], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ['<TAG3>'], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ['[6]', '<TAG4>', '<TAG5>']]
    assert text_tokens_only.tags_all == text_tokens_only.tags_non_pos
    assert text_tokens_only.offsets_paras == [0]
    assert text_tokens_only.offsets_sentences == [0]
    assert text_tokens_only.offsets_clauses == [0, 28, 48, 50, 72, 84, 93]

    assert (len(text_tokens_only.tokens) ==
            len(text_tokens_only.tags_pos) ==
            len(text_tokens_only.tags_non_pos) ==
            len(text_tokens_only.tags_all))
    assert len(text_tokens_only.offsets_paras) == len(text_tokens_only.tokens_sentences_paras)
    assert len(text_tokens_only.offsets_sentences) == sum([len(para)
                                                           for para in text_tokens_only.tokens_sentences_paras])

    assert text.tokens == ['', 'English', 'is', 'a', 'West', 'Germanic', 'language', 'that', 'was', 'first', 'spoken', 'in', 'early', 'medieval', 'England', 'and', 'eventually', 'became', 'a', 'global', 'lingua', 'franca', '.', 'Named', 'after', 'the', 'Angles', ',', 'one', 'of', 'the', 'Germanic', 'tribes', 'that', 'migrated', 'to', 'the', 'area', 'of', 'Great', 'Britain', 'that', 'would', 'later', 'take', 'their', 'name', ',', 'England', ',', 'both', 'names', 'ultimately', 'deriving', 'from', 'the', 'Anglia', 'peninsula', 'in', 'the', 'Baltic', 'Sea', '.', 'It', 'is', 'closely', 'related', 'to', 'the', 'Frisian', 'languages', ',', 'but', 'its', 'vocabulary', 'has', 'been', 'significantly', 'influenced', 'by', 'other', 'Germanic', 'languages', ',', 'particularly', 'Norse', '(', 'a', 'North', 'Germanic', 'language', ')', ',', 'and', 'to', 'a', 'greater', 'extent', 'Latin', 'and', 'French', '.']
    assert text.tags_pos == [[]] * len(text.tokens)
    assert text.tags_non_pos == [['<TAG1>', '<TAG2>'], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ['[4]', '[5]'], [], [], [], [], [], [], [], [], [], ['<TAG3>'], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ['<TAG3>'], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ['<TAG3>'], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ['[6]', '<TAG4>', '<TAG5>']]
    assert text.tags_all == text_tokens_only.tags_non_pos
    assert text.offsets_paras == [0]
    assert text.offsets_sentences == [0, 23, 63]
    assert text.offsets_clauses == [0, 23, 28, 48, 50, 63, 72, 84, 93]

    assert (len(text.tokens) ==
            len(text.tags_pos) ==
            len(text.tags_non_pos) ==
            len(text.tags_all))
    assert len(text.offsets_paras) == len(text.tokens_sentences_paras)
    assert len(text.offsets_sentences) == sum([len(para)
                                               for para in text.tokens_sentences_paras])

def test_text_tokenized_untagged():
    file = new_file(file_name = 'tokenized_untagged',
                    text_type = ('tokenized', 'untagged'))

    text_tokens_only = wordless_text.Wordless_Text(main, file,
                                                   tokens_only = True)
    text = wordless_text.Wordless_Text(main, file,
                                       tokens_only = False)

    assert text_tokens_only.tokens == ['English', 'is', 'a', 'West', 'Germanic', 'language', 'that', 'was', 'first', 'spoken', 'in', 'early', 'medieval', 'England', 'and', 'eventually', 'became', 'a', 'global', 'lingua', 'franca', '.', 'Named', 'after', 'the', 'Angles', ',', 'one', 'of', 'the', 'Germanic', 'tribes', 'that', 'migrated', 'to', 'the', 'area', 'of', 'Great', 'Britain', 'that', 'would', 'later', 'take', 'their', 'name', ',', 'England', ',', 'both', 'names', 'ultimately', 'deriving', 'from', 'the', 'Anglia', 'peninsula', 'in', 'the', 'Baltic', 'Sea', '.', 'It', 'is', 'closely', 'related', 'to', 'the', 'Frisian', 'languages', ',', 'but', 'its', 'vocabulary', 'has', 'been', 'significantly', 'influenced', 'by', 'other', 'Germanic', 'languages', ',', 'particularly', 'Norse', '(', 'a', 'North', 'Germanic', 'language', ')', ',', 'and', 'to', 'a', 'greater', 'extent', 'Latin', 'and', 'French', '.']
    assert text_tokens_only.tags_pos == [[]] * len(text_tokens_only.tokens)
    assert text_tokens_only.tags_non_pos == [[]] * len(text_tokens_only.tokens)
    assert text_tokens_only.tags_all == [[]] * len(text_tokens_only.tokens)
    assert text_tokens_only.offsets_paras == [0]
    assert text_tokens_only.offsets_sentences == [0]
    assert text_tokens_only.offsets_clauses == [0, 27, 47, 49, 71, 83, 92]

    assert (len(text_tokens_only.tokens) ==
            len(text_tokens_only.tags_pos) ==
            len(text_tokens_only.tags_non_pos) ==
            len(text_tokens_only.tags_all))
    assert len(text_tokens_only.offsets_paras) == len(text_tokens_only.tokens_sentences_paras)
    assert len(text_tokens_only.offsets_sentences) == sum([len(para)
                                                           for para in text_tokens_only.tokens_sentences_paras])

    assert text.tokens == ['English', 'is', 'a', 'West', 'Germanic', 'language', 'that', 'was', 'first', 'spoken', 'in', 'early', 'medieval', 'England', 'and', 'eventually', 'became', 'a', 'global', 'lingua', 'franca', '.', 'Named', 'after', 'the', 'Angles', ',', 'one', 'of', 'the', 'Germanic', 'tribes', 'that', 'migrated', 'to', 'the', 'area', 'of', 'Great', 'Britain', 'that', 'would', 'later', 'take', 'their', 'name', ',', 'England', ',', 'both', 'names', 'ultimately', 'deriving', 'from', 'the', 'Anglia', 'peninsula', 'in', 'the', 'Baltic', 'Sea', '.', 'It', 'is', 'closely', 'related', 'to', 'the', 'Frisian', 'languages', ',', 'but', 'its', 'vocabulary', 'has', 'been', 'significantly', 'influenced', 'by', 'other', 'Germanic', 'languages', ',', 'particularly', 'Norse', '(', 'a', 'North', 'Germanic', 'language', ')', ',', 'and', 'to', 'a', 'greater', 'extent', 'Latin', 'and', 'French', '.']
    assert text.tags_pos == [[]] * len(text.tokens)
    assert text.tags_non_pos == [[]] * len(text.tokens)
    assert text.tags_all == [[]] * len(text.tokens)
    assert text.offsets_paras == [0]
    assert text.offsets_sentences == [0, 22, 62]
    assert text.offsets_clauses == [0, 22, 27, 47, 49, 62, 71, 83, 92]

    assert (len(text.tokens) ==
            len(text.tags_pos) ==
            len(text.tags_non_pos) ==
            len(text.tags_all))
    assert len(text.offsets_paras) == len(text.tokens_sentences_paras)
    assert len(text.offsets_sentences) == sum([len(para)
                                               for para in text.tokens_sentences_paras])

def test_text_tokenized_tagged_pos():
    file = new_file(file_name = 'tokenized_tagged_pos',
                    text_type = ('tokenized', 'tagged_pos'))

    text_tokens_only = wordless_text.Wordless_Text(main, file,
                                                   tokens_only = True)
    text = wordless_text.Wordless_Text(main, file,
                                       tokens_only = False)

    assert text_tokens_only.tokens == ['English', 'is', 'a', 'West', 'Germanic', 'language', 'that', 'was', 'first', 'spoken', 'in', 'early', 'medieval', 'England', 'and', 'eventually', 'became', 'a', 'global', 'lingua', 'franca', '.', 'Named', 'after', 'the', 'Angles', ',', 'one', 'of', 'the', 'Germanic', 'tribes', 'that', 'migrated', 'to', 'the', 'area', 'of', 'Great', 'Britain', 'that', 'would', 'later', 'take', 'their', 'name', ',', 'England', ',', 'both', 'names', 'ultimately', 'deriving', 'from', 'the', 'Anglia', 'peninsula', 'in', 'the', 'Baltic', 'Sea', '.', 'It', 'is', 'closely', 'related', 'to', 'the', 'Frisian', 'languages', ',', 'but', 'its', 'vocabulary', 'has', 'been', 'significantly', 'influenced', 'by', 'other', 'Germanic', 'languages', ',', 'particularly', 'Norse', '(', 'a', 'North', 'Germanic', 'language', ')', ',', 'and', 'to', 'a', 'greater', 'extent', 'Latin', 'and', 'French', '.']
    assert text_tokens_only.tags_pos == [['_JJ'], ['_VBZ'], ['_DT'], ['_JJ'], ['_JJ'], ['_NN'], ['_IN'], ['_VBD'], ['_RB'], ['_VBN'], ['_IN'], ['_RB'], ['_JJ'], ['_NN'], ['_CC'], ['_RB'], ['_VBD'], ['_DT'], ['_JJ'], ['_FW'], ['_FW'], ['_.'], ['_VBN'], ['_IN'], ['_DT'], ['_NNS'], ['_,'], ['_CD'], ['_IN'], ['_DT'], ['_JJ'], ['_NNS'], ['_IN'], ['_VBN'], ['_IN'], ['_DT'], ['_NN'], ['_IN'], ['_JJ'], ['_NNP'], ['_IN'], ['_MD'], ['_RB'], ['_VB'], ['_PRP$'], ['_NN'], ['_,'], ['_NN'], ['_,'], ['_DT'], ['_NNS'], ['_RB'], ['_VBG'], ['_IN'], ['_DT'], ['_NNP'], ['_NN'], ['_IN'], ['_DT'], ['_JJ'], ['_NNP'], ['_.'], ['_PRP'], ['_VBZ'], ['_RB'], ['_VBN'], ['_IN'], ['_DT'], ['_NNP'], ['_NNS'], ['_,'], ['_CC'], ['_PRP$'], ['_NN'], ['_VBZ'], ['_VBN'], ['_RB'], ['_VBN'], ['_IN'], ['_JJ'], ['_JJ'], ['_NNS'], ['_,'], ['_RB'], ['_NNP'], ['_-LRB-'], ['_DT'], ['_JJ'], ['_JJ'], ['_NN'], ['_-RRB-'], ['_,'], ['_CC'], ['_IN'], ['_DT'], ['_JJR'], ['_NN'], ['_JJ'], ['_CC'], ['_JJ'], ['_.']]
    assert text_tokens_only.tags_non_pos == [[]] * len(text.tokens)
    assert text_tokens_only.tags_all == text_tokens_only.tags_pos
    assert text_tokens_only.offsets_paras == [0]
    assert text_tokens_only.offsets_sentences == [0]
    assert text_tokens_only.offsets_clauses == [0, 27, 47, 49, 71, 83, 92]

    assert (len(text_tokens_only.tokens) ==
            len(text_tokens_only.tags_pos) ==
            len(text_tokens_only.tags_non_pos) ==
            len(text_tokens_only.tags_all))
    assert len(text_tokens_only.offsets_paras) == len(text_tokens_only.tokens_sentences_paras)
    assert len(text_tokens_only.offsets_sentences) == sum([len(para)
                                                           for para in text_tokens_only.tokens_sentences_paras])

    assert text.tokens == ['English', 'is', 'a', 'West', 'Germanic', 'language', 'that', 'was', 'first', 'spoken', 'in', 'early', 'medieval', 'England', 'and', 'eventually', 'became', 'a', 'global', 'lingua', 'franca', '.', 'Named', 'after', 'the', 'Angles', ',', 'one', 'of', 'the', 'Germanic', 'tribes', 'that', 'migrated', 'to', 'the', 'area', 'of', 'Great', 'Britain', 'that', 'would', 'later', 'take', 'their', 'name', ',', 'England', ',', 'both', 'names', 'ultimately', 'deriving', 'from', 'the', 'Anglia', 'peninsula', 'in', 'the', 'Baltic', 'Sea', '.', 'It', 'is', 'closely', 'related', 'to', 'the', 'Frisian', 'languages', ',', 'but', 'its', 'vocabulary', 'has', 'been', 'significantly', 'influenced', 'by', 'other', 'Germanic', 'languages', ',', 'particularly', 'Norse', '(', 'a', 'North', 'Germanic', 'language', ')', ',', 'and', 'to', 'a', 'greater', 'extent', 'Latin', 'and', 'French', '.']
    assert text.tags_pos == [['_JJ'], ['_VBZ'], ['_DT'], ['_JJ'], ['_JJ'], ['_NN'], ['_IN'], ['_VBD'], ['_RB'], ['_VBN'], ['_IN'], ['_RB'], ['_JJ'], ['_NN'], ['_CC'], ['_RB'], ['_VBD'], ['_DT'], ['_JJ'], ['_FW'], ['_FW'], ['_.'], ['_VBN'], ['_IN'], ['_DT'], ['_NNS'], ['_,'], ['_CD'], ['_IN'], ['_DT'], ['_JJ'], ['_NNS'], ['_IN'], ['_VBN'], ['_IN'], ['_DT'], ['_NN'], ['_IN'], ['_JJ'], ['_NNP'], ['_IN'], ['_MD'], ['_RB'], ['_VB'], ['_PRP$'], ['_NN'], ['_,'], ['_NN'], ['_,'], ['_DT'], ['_NNS'], ['_RB'], ['_VBG'], ['_IN'], ['_DT'], ['_NNP'], ['_NN'], ['_IN'], ['_DT'], ['_JJ'], ['_NNP'], ['_.'], ['_PRP'], ['_VBZ'], ['_RB'], ['_VBN'], ['_IN'], ['_DT'], ['_NNP'], ['_NNS'], ['_,'], ['_CC'], ['_PRP$'], ['_NN'], ['_VBZ'], ['_VBN'], ['_RB'], ['_VBN'], ['_IN'], ['_JJ'], ['_JJ'], ['_NNS'], ['_,'], ['_RB'], ['_NNP'], ['_-LRB-'], ['_DT'], ['_JJ'], ['_JJ'], ['_NN'], ['_-RRB-'], ['_,'], ['_CC'], ['_IN'], ['_DT'], ['_JJR'], ['_NN'], ['_JJ'], ['_CC'], ['_JJ'], ['_.']]
    assert text.tags_non_pos == [[]] * len(text.tokens)
    assert text.tags_all == text.tags_pos
    assert text.offsets_paras == [0]
    assert text.offsets_sentences == [0, 22, 62]
    assert text.offsets_clauses == [0, 22, 27, 47, 49, 62, 71, 83, 92]

    assert (len(text.tokens) ==
            len(text.tags_pos) ==
            len(text.tags_non_pos) ==
            len(text.tags_all))
    assert len(text.offsets_paras) == len(text.tokens_sentences_paras)
    assert len(text.offsets_sentences) == sum([len(para)
                                               for para in text.tokens_sentences_paras])

def test_text_tokenized_tagged_non_pos():
    file = new_file(file_name = 'tokenized_tagged_non_pos',
                    text_type = ('tokenized', 'tagged_non_pos'))

    text_tokens_only = wordless_text.Wordless_Text(main, file,
                                                   tokens_only = True)
    text = wordless_text.Wordless_Text(main, file,
                                       tokens_only = False)

    assert text_tokens_only.tokens == ['', 'English', 'is', 'a', 'West', 'Germanic', 'language', 'that', 'was', 'first', 'spoken', 'in', 'early', 'medieval', 'England', 'and', 'eventually', 'became', 'a', 'global', 'lingua', 'franca', '.', 'Named', 'after', 'the', 'Angles', ',', 'one', 'of', 'the', 'Germanic', 'tribes', 'that', 'migrated', 'to', 'the', 'area', 'of', 'Great', 'Britain', 'that', 'would', 'later', 'take', 'their', 'name', ',', 'England', ',', 'both', 'names', 'ultimately', 'deriving', 'from', 'the', 'Anglia', 'peninsula', 'in', 'the', 'Baltic', 'Sea', '.', 'It', 'is', 'closely', 'related', 'to', 'the', 'Frisian', 'languages', ',', 'but', 'its', 'vocabulary', 'has', 'been', 'significantly', 'influenced', 'by', 'other', 'Germanic', 'languages', ',', 'particularly', 'Norse', '(', 'a', 'North', 'Germanic', 'language', ')', ',', 'and', 'to', 'a', 'greater', 'extent', 'Latin', 'and', 'French', '.']
    assert text_tokens_only.tags_pos == [[]] * len(text_tokens_only.tokens)
    assert text_tokens_only.tags_non_pos == [['<TAG1>', '<TAG2>'], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ['[4]', '[5]'], [], [], [], [], [], [], [], [], [], ['<TAG3>'], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ['<TAG3>'], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ['<TAG3>'], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ['[6]', '<TAG4>', '<TAG5>']]
    assert text_tokens_only.tags_all == text_tokens_only.tags_non_pos
    assert text_tokens_only.offsets_paras == [0]
    assert text_tokens_only.offsets_sentences == [0]
    assert text_tokens_only.offsets_clauses == [0, 28, 48, 50, 72, 84, 93]

    assert (len(text_tokens_only.tokens) ==
            len(text_tokens_only.tags_pos) ==
            len(text_tokens_only.tags_non_pos) ==
            len(text_tokens_only.tags_all))
    assert len(text_tokens_only.offsets_paras) == len(text_tokens_only.tokens_sentences_paras)
    assert len(text_tokens_only.offsets_sentences) == sum([len(para)
                                                           for para in text_tokens_only.tokens_sentences_paras])

    assert text.tokens == ['', 'English', 'is', 'a', 'West', 'Germanic', 'language', 'that', 'was', 'first', 'spoken', 'in', 'early', 'medieval', 'England', 'and', 'eventually', 'became', 'a', 'global', 'lingua', 'franca', '.', 'Named', 'after', 'the', 'Angles', ',', 'one', 'of', 'the', 'Germanic', 'tribes', 'that', 'migrated', 'to', 'the', 'area', 'of', 'Great', 'Britain', 'that', 'would', 'later', 'take', 'their', 'name', ',', 'England', ',', 'both', 'names', 'ultimately', 'deriving', 'from', 'the', 'Anglia', 'peninsula', 'in', 'the', 'Baltic', 'Sea', '.', 'It', 'is', 'closely', 'related', 'to', 'the', 'Frisian', 'languages', ',', 'but', 'its', 'vocabulary', 'has', 'been', 'significantly', 'influenced', 'by', 'other', 'Germanic', 'languages', ',', 'particularly', 'Norse', '(', 'a', 'North', 'Germanic', 'language', ')', ',', 'and', 'to', 'a', 'greater', 'extent', 'Latin', 'and', 'French', '.']
    assert text.tags_pos == [[]] * len(text.tokens)
    assert text.tags_non_pos == [['<TAG1>', '<TAG2>'], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ['[4]', '[5]'], [], [], [], [], [], [], [], [], [], ['<TAG3>'], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ['<TAG3>'], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ['<TAG3>'], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ['[6]', '<TAG4>', '<TAG5>']]
    assert text.tags_all == text_tokens_only.tags_non_pos
    assert text.offsets_paras == [0]
    assert text.offsets_sentences == [0, 23, 63]
    assert text.offsets_clauses == [0, 23, 28, 48, 50, 63, 72, 84, 93]

    assert (len(text.tokens) ==
            len(text.tags_pos) ==
            len(text.tags_non_pos) ==
            len(text.tags_all))
    assert len(text.offsets_paras) == len(text.tokens_sentences_paras)
    assert len(text.offsets_sentences) == sum([len(para)
                                               for para in text.tokens_sentences_paras])


def test_text_tokenized_tagged_both():
    file = new_file(file_name = 'tokenized_tagged_both',
                    text_type = ('tokenized', 'tagged_both'))

    text_tokens_only = wordless_text.Wordless_Text(main, file,
                                                   tokens_only = True)
    text = wordless_text.Wordless_Text(main, file,
                                       tokens_only = False)

    assert text_tokens_only.tokens == ['', 'English', 'is', 'a', 'West', 'Germanic', 'language', 'that', 'was', 'first', 'spoken', 'in', 'early', 'medieval', 'England', 'and', 'eventually', 'became', 'a', 'global', 'lingua', 'franca', '.', 'Named', 'after', 'the', 'Angles', ',', 'one', 'of', 'the', 'Germanic', 'tribes', 'that', 'migrated', 'to', 'the', 'area', 'of', 'Great', 'Britain', 'that', 'would', 'later', 'take', 'their', 'name', ',', 'England', ',', 'both', 'names', 'ultimately', 'deriving', 'from', 'the', 'Anglia', 'peninsula', 'in', 'the', 'Baltic', 'Sea', '.', 'It', 'is', 'closely', 'related', 'to', 'the', 'Frisian', 'languages', ',', 'but', 'its', 'vocabulary', 'has', 'been', 'significantly', 'influenced', 'by', 'other', 'Germanic', 'languages', ',', 'particularly', 'Norse', '(', 'a', 'North', 'Germanic', 'language', ')', ',', 'and', 'to', 'a', 'greater', 'extent', 'Latin', 'and', 'French', '.']
    assert text_tokens_only.tags_pos == [[], ['_JJ'], ['_VBZ'], ['_DT'], ['_JJ'], ['_JJ'], ['_NN'], ['_IN'], ['_VBD'], ['_RB'], ['_VBN'], ['_IN'], ['_RB'], ['_JJ'], ['_NN'], ['_CC'], ['_RB'], ['_VBD'], ['_DT'], ['_JJ'], ['_FW'], ['_FW'], ['_.'], ['_VBN'], ['_IN'], ['_DT'], ['_NNS'], ['_,'], ['_CD'], ['_IN'], ['_DT'], ['_JJ'], ['_NNS'], ['_IN'], ['_VBN'], ['_IN'], ['_DT'], ['_NN'], ['_IN'], ['_JJ'], ['_NNP'], ['_IN'], ['_MD'], ['_RB'], ['_VB'], ['_PRP$'], ['_NN'], ['_,'], ['_NN'], ['_,'], ['_DT'], ['_NNS'], ['_RB'], ['_VBG'], ['_IN'], ['_DT'], ['_NNP'], ['_NN'], ['_IN'], ['_DT'], ['_JJ'], ['_NNP'], ['_.'], ['_PRP'], ['_VBZ'], ['_RB'], ['_VBN'], ['_IN'], ['_DT'], ['_NNP'], ['_NNS'], ['_,'], ['_CC'], ['_PRP$'], ['_NN'], ['_VBZ'], ['_VBN'], ['_RB'], ['_VBN'], ['_IN'], ['_JJ'], ['_JJ'], ['_NNS'], ['_,'], ['_RB'], ['_NNP'], ['_-LRB-'], ['_DT'], ['_JJ'], ['_JJ'], ['_NN'], ['_-RRB-'], ['_,'], ['_CC'], ['_IN'], ['_DT'], ['_JJR'], ['_NN'], ['_JJ'], ['_CC'], ['_JJ'], ['_.']]
    assert text_tokens_only.tags_non_pos == [['<TAG1>', '<TAG2>'], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ['[4]', '[5]'], [], [], [], [], [], [], [], [], [], ['<TAG3>'], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ['<TAG3>'], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ['<TAG3>'], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ['[6]', '<TAG4>', '<TAG5>']]
    assert text_tokens_only.tags_all == [['<TAG1>', '<TAG2>'], ['_JJ'], ['_VBZ'], ['_DT'], ['_JJ'], ['_JJ'], ['_NN'], ['_IN'], ['_VBD'], ['_RB'], ['_VBN'], ['_IN'], ['_RB'], ['_JJ'], ['_NN'], ['_CC'], ['_RB'], ['_VBD'], ['_DT'], ['_JJ'], ['_FW'], ['_FW'], ['_.', '[4]', '[5]'], ['_VBN'], ['_IN'], ['_DT'], ['_NNS'], ['_,'], ['_CD'], ['_IN'], ['_DT'], ['_JJ'], ['_NNS', '<TAG3>'], ['_IN'], ['_VBN'], ['_IN'], ['_DT'], ['_NN'], ['_IN'], ['_JJ'], ['_NNP'], ['_IN'], ['_MD'], ['_RB'], ['_VB'], ['_PRP$'], ['_NN'], ['_,'], ['_NN'], ['_,'], ['_DT'], ['_NNS'], ['_RB'], ['_VBG'], ['_IN'], ['_DT'], ['_NNP'], ['_NN'], ['_IN'], ['_DT'], ['_JJ'], ['_NNP'], ['_.'], ['_PRP'], ['_VBZ'], ['_RB', '<TAG3>'], ['_VBN'], ['_IN'], ['_DT'], ['_NNP'], ['_NNS'], ['_,'], ['_CC'], ['_PRP$'], ['_NN'], ['_VBZ'], ['_VBN'], ['_RB'], ['_VBN'], ['_IN'], ['_JJ', '<TAG3>'], ['_JJ'], ['_NNS'], ['_,'], ['_RB'], ['_NNP'], ['_-LRB-'], ['_DT'], ['_JJ'], ['_JJ'], ['_NN'], ['_-RRB-'], ['_,'], ['_CC'], ['_IN'], ['_DT'], ['_JJR'], ['_NN'], ['_JJ'], ['_CC'], ['_JJ'], ['_.', '[6]', '<TAG4>', '<TAG5>']]
    assert text_tokens_only.offsets_paras == [0]
    assert text_tokens_only.offsets_sentences == [0]
    assert text_tokens_only.offsets_clauses == [0, 28, 48, 50, 72, 84, 93]

    assert (len(text_tokens_only.tokens) ==
            len(text_tokens_only.tags_pos) ==
            len(text_tokens_only.tags_non_pos) ==
            len(text_tokens_only.tags_all))
    assert len(text_tokens_only.offsets_paras) == len(text_tokens_only.tokens_sentences_paras)
    assert len(text_tokens_only.offsets_sentences) == sum([len(para)
                                                           for para in text_tokens_only.tokens_sentences_paras])

    assert text.tokens == ['', 'English', 'is', 'a', 'West', 'Germanic', 'language', 'that', 'was', 'first', 'spoken', 'in', 'early', 'medieval', 'England', 'and', 'eventually', 'became', 'a', 'global', 'lingua', 'franca', '.', 'Named', 'after', 'the', 'Angles', ',', 'one', 'of', 'the', 'Germanic', 'tribes', 'that', 'migrated', 'to', 'the', 'area', 'of', 'Great', 'Britain', 'that', 'would', 'later', 'take', 'their', 'name', ',', 'England', ',', 'both', 'names', 'ultimately', 'deriving', 'from', 'the', 'Anglia', 'peninsula', 'in', 'the', 'Baltic', 'Sea', '.', 'It', 'is', 'closely', 'related', 'to', 'the', 'Frisian', 'languages', ',', 'but', 'its', 'vocabulary', 'has', 'been', 'significantly', 'influenced', 'by', 'other', 'Germanic', 'languages', ',', 'particularly', 'Norse', '(', 'a', 'North', 'Germanic', 'language', ')', ',', 'and', 'to', 'a', 'greater', 'extent', 'Latin', 'and', 'French', '.']
    assert text.tags_pos == [[], ['_JJ'], ['_VBZ'], ['_DT'], ['_JJ'], ['_JJ'], ['_NN'], ['_IN'], ['_VBD'], ['_RB'], ['_VBN'], ['_IN'], ['_RB'], ['_JJ'], ['_NN'], ['_CC'], ['_RB'], ['_VBD'], ['_DT'], ['_JJ'], ['_FW'], ['_FW'], ['_.'], ['_VBN'], ['_IN'], ['_DT'], ['_NNS'], ['_,'], ['_CD'], ['_IN'], ['_DT'], ['_JJ'], ['_NNS'], ['_IN'], ['_VBN'], ['_IN'], ['_DT'], ['_NN'], ['_IN'], ['_JJ'], ['_NNP'], ['_IN'], ['_MD'], ['_RB'], ['_VB'], ['_PRP$'], ['_NN'], ['_,'], ['_NN'], ['_,'], ['_DT'], ['_NNS'], ['_RB'], ['_VBG'], ['_IN'], ['_DT'], ['_NNP'], ['_NN'], ['_IN'], ['_DT'], ['_JJ'], ['_NNP'], ['_.'], ['_PRP'], ['_VBZ'], ['_RB'], ['_VBN'], ['_IN'], ['_DT'], ['_NNP'], ['_NNS'], ['_,'], ['_CC'], ['_PRP$'], ['_NN'], ['_VBZ'], ['_VBN'], ['_RB'], ['_VBN'], ['_IN'], ['_JJ'], ['_JJ'], ['_NNS'], ['_,'], ['_RB'], ['_NNP'], ['_-LRB-'], ['_DT'], ['_JJ'], ['_JJ'], ['_NN'], ['_-RRB-'], ['_,'], ['_CC'], ['_IN'], ['_DT'], ['_JJR'], ['_NN'], ['_JJ'], ['_CC'], ['_JJ'], ['_.']]
    assert text.tags_non_pos == [['<TAG1>', '<TAG2>'], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ['[4]', '[5]'], [], [], [], [], [], [], [], [], [], ['<TAG3>'], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ['<TAG3>'], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ['<TAG3>'], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ['[6]', '<TAG4>', '<TAG5>']]
    assert text.tags_all == [['<TAG1>', '<TAG2>'], ['_JJ'], ['_VBZ'], ['_DT'], ['_JJ'], ['_JJ'], ['_NN'], ['_IN'], ['_VBD'], ['_RB'], ['_VBN'], ['_IN'], ['_RB'], ['_JJ'], ['_NN'], ['_CC'], ['_RB'], ['_VBD'], ['_DT'], ['_JJ'], ['_FW'], ['_FW'], ['_.', '[4]', '[5]'], ['_VBN'], ['_IN'], ['_DT'], ['_NNS'], ['_,'], ['_CD'], ['_IN'], ['_DT'], ['_JJ'], ['_NNS', '<TAG3>'], ['_IN'], ['_VBN'], ['_IN'], ['_DT'], ['_NN'], ['_IN'], ['_JJ'], ['_NNP'], ['_IN'], ['_MD'], ['_RB'], ['_VB'], ['_PRP$'], ['_NN'], ['_,'], ['_NN'], ['_,'], ['_DT'], ['_NNS'], ['_RB'], ['_VBG'], ['_IN'], ['_DT'], ['_NNP'], ['_NN'], ['_IN'], ['_DT'], ['_JJ'], ['_NNP'], ['_.'], ['_PRP'], ['_VBZ'], ['_RB', '<TAG3>'], ['_VBN'], ['_IN'], ['_DT'], ['_NNP'], ['_NNS'], ['_,'], ['_CC'], ['_PRP$'], ['_NN'], ['_VBZ'], ['_VBN'], ['_RB'], ['_VBN'], ['_IN'], ['_JJ', '<TAG3>'], ['_JJ'], ['_NNS'], ['_,'], ['_RB'], ['_NNP'], ['_-LRB-'], ['_DT'], ['_JJ'], ['_JJ'], ['_NN'], ['_-RRB-'], ['_,'], ['_CC'], ['_IN'], ['_DT'], ['_JJR'], ['_NN'], ['_JJ'], ['_CC'], ['_JJ'], ['_.', '[6]', '<TAG4>', '<TAG5>']]
    assert text.offsets_paras == [0]
    assert text.offsets_sentences == [0, 23, 63]
    assert text.offsets_clauses == [0, 23, 28, 48, 50, 63, 72, 84, 93]

    assert (len(text.tokens) ==
            len(text.tags_pos) ==
            len(text.tags_non_pos) ==
            len(text.tags_all))
    assert len(text.offsets_paras) == len(text.tokens_sentences_paras)
    assert len(text.offsets_sentences) == sum([len(para)
                                               for para in text.tokens_sentences_paras])
