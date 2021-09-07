#
# Wordless: Checking - Token
#
# Copyright (C) 2018-2021  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

# At least one letter
def is_word_alphabetic(token):
    return any([char for char in token if char.isalpha()])

# At least one letter or numeral
def is_word_alphanumeric(token):
    return any([char for char in token if char.isalnum()])

def is_word_lowercase(token):
    return token.islower()

def is_word_uppercase(token):
    return token.isupper()

def is_word_title_case(token):
    return token.istitle()

# At least one numeral
def is_num(token):
    return any(map(str.isnumeric, token))

# All punctuation marks
def is_punc(token):
    return token and not any(map(str.isalnum, token))
