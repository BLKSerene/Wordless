#
# Wordless: Testing - Text
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

from wordless_testing import testing_init
from wordless_text import wordless_text

def new_file(file_name, text_type):
    new_file = {}

    new_file['lang'] = 'eng'
    new_file['text_type'] = text_type
    new_file['path'] = f'wordless_testing/files/tags/{file_name}'
    new_file['encoding'] = 'utf_8'

    return new_file

def print_text(title, text):
    print(f'---------- {title} ----------')

    print(f'Tokens ({len(text.tokens)}):')
    print(f'\t{text.tokens}')

    print(f'POS Tags ({len(text.tags_pos)}):')
    print(f'\t{text.tags_pos}')

    print(f'Non-POS Tags ({len(text.tags_non_pos)}):')
    print(f'\t{text.tags_non_pos}')

    print(f'All Tags ({len(text.tags_all)}):')
    print(f'\t{text.tags_all}')

main = testing_init.Testing_Main()

file_untokenized_untagged = new_file(file_name = 'untokenized_untagged.txt',
                                     text_type = ['untokenized', 'untagged'])
file_untokenized_tagged_non_pos = new_file(file_name = 'untokenized_untagged_non_pos.txt',
                                           text_type = ['untokenized', 'tagged_non_pos'])
file_tokenized_untagged = new_file(file_name = 'tokenized_untagged.txt',
                                   text_type = ['tokenized', 'untagged'])
file_tokenized_tagged_pos = new_file(file_name = 'tokenized_tagged_pos.txt',
                                     text_type = ['tokenized', 'tagged_pos'])
file_tokenized_tagged_non_pos = new_file(file_name = 'tokenized_tagged_non_pos.txt',
                                         text_type = ['tokenized', 'tagged_non_pos'])
file_tokenized_tagged_both = new_file(file_name = 'tokenized_tagged_both.txt',
                                      text_type = ['tokenized', 'tagged_both'])

text = wordless_text.Wordless_Text(main, file_untokenized_untagged)
print_text(title = 'Untokenized / Untagged', text = text)

text = wordless_text.Wordless_Text(main, file_untokenized_tagged_non_pos)
print_text(title = 'Untokenized / Tagged (Non-POS)', text = text)

text = wordless_text.Wordless_Text(main, file_tokenized_untagged)
print_text(title = 'Tokenized / Untagged', text = text)

text = wordless_text.Wordless_Text(main, file_tokenized_tagged_pos)
print_text(title = 'Tokenized / Tagged (POS)', text = text)

text = wordless_text.Wordless_Text(main, file_tokenized_tagged_non_pos)
print_text(title = 'Tokenized / Tagged (Non-POS)', text = text)

text = wordless_text.Wordless_Text(main, file_tokenized_tagged_both)
print_text(title = 'Tokenized / Tagged (Both)', text = text)
