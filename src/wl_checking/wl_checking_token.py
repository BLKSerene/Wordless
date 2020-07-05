#
# Wordless: Checking - Token
#
# Copyright (C) 2018-2020  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

# At least one letter and no numerals
def is_token_word(token):
    return (any([char for char in token if char.isalnum()]) and
            all([char for char in token if not char.isnumeric()]))

def is_token_word_lowercase(token):
    return token.islower()

def is_token_word_uppercase(token):
    return token.isupper()

def is_token_word_title_case(token):
    return token.istitle()

# At least one numeral
def is_token_num(token):
    return any(map(str.isnumeric, token))

# All punctuation marks
def is_token_punc(token):
    return token and not any(map(str.isalnum, token))
