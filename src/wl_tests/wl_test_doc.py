#
# Wordless: Tests - Documentation
#
# Copyright (C) 2018-2021  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import re
import sys

sys.path.append('.')

import openpyxl

from wl_tests import wl_test_init

def print_acks(category, worksheet):
    acks = []

    LINE_HEADER = '&nbsp;|Name|Authors'
    LINE_HEADER_SPLITTER = '-----:|----|---------'

    print(f'### {category}')
    print()
    print(LINE_HEADER)
    print(LINE_HEADER_SPLITTER)

    for i, rows in enumerate(worksheet.rows):
        if i > 0:
            name = rows[0].value
            home_page = rows[1].value
            authors = rows[3].value.replace('\n', '<br>')

            acks.append([name, home_page, authors])

    len_names = max([len(name) + len(home_page) for name, home_page, _ in acks]) + 4

    for i, (name, home_page, authors) in enumerate(acks):
        len_name = len_names - len(name) - len(home_page) - 4

        if len_name:
            print(f"{i + 1 : <6}|[{name}]({home_page}){' ':{len_name}}|{authors}")
        else:
            print(f"{i + 1 : <6}|[{name}]({home_page})|{authors}")

    print()

def wl_test_readme_acks(main):
    workbook = openpyxl.load_workbook('wl_acks.xlsx')

    print_acks('General', workbook['General'])
    print_acks('Natural Language Processing', workbook['NLP'])
    print_acks('Language Data', workbook['Language Data'])
    print_acks('Plotting', workbook['Plotting'])
    print_acks('Miscellaneous', workbook['Miscellaneous'])

def wl_test_supported_langs(main):
    settings = main.settings_global

    langs_supported = [
        (lang_name, lang_code_639_3)
        for lang_name, (lang_code_639_3, _, _) in main.settings_global['langs'].items()
    ]

    langs_sentence_tokenizers = main.settings_global['sentence_tokenizers'].keys()
    langs_word_tokenizers = main.settings_global['word_tokenizers'].keys()
    langs_syl_tokenizers  = main.settings_global['syl_tokenizers'].keys()
    langs_word_detokenizers = main.settings_global['word_detokenizers'].keys()
    langs_pos_tagging = main.settings_global['pos_taggers'].keys()
    langs_lemmatizers = main.settings_global['lemmatizers'].keys()
    langs_stop_word_lists = main.settings_global['stop_word_lists'].keys()

    len_max_langs = max([len(lang_name) for lang_name, lang_code_639_3 in langs_supported])

    for lang_name, lang_code_639_3 in langs_supported:
        if (lang_code_639_3 in langs_sentence_tokenizers or
            lang_code_639_3 in langs_word_tokenizers or
            lang_code_639_3 in langs_syl_tokenizers or
            lang_code_639_3 in langs_word_detokenizers or
            lang_code_639_3 in langs_pos_tagging or
            lang_code_639_3 in langs_lemmatizers or
            lang_code_639_3 in langs_stop_word_lists):
            doc_supported_lang = f'{lang_name:{len_max_langs}s}'

            if lang_code_639_3 == 'other':
                doc_supported_lang += '|⭕️ |⭕️ |✖️|⭕️ |✖️|✖️|✖️'
            else:
                if lang_code_639_3 in langs_sentence_tokenizers:
                    doc_supported_lang += '|✔'
                else:
                    doc_supported_lang += '|⭕️ '

                if lang_code_639_3 in langs_word_tokenizers:
                    doc_supported_lang += '|✔'
                else:
                    doc_supported_lang += '|⭕️ '

                if lang_code_639_3 in langs_syl_tokenizers:
                    doc_supported_lang += '|✔'
                else:
                    doc_supported_lang += '|✖️'

                if lang_code_639_3 in langs_word_detokenizers:
                    doc_supported_lang += '|✔'
                else:
                    doc_supported_lang += '|⭕️ '

                if lang_code_639_3 in langs_pos_tagging:
                    doc_supported_lang += '|✔'
                else:
                    doc_supported_lang += '|✖️'

                if lang_code_639_3 in langs_lemmatizers:
                    doc_supported_lang += '|✔'
                else:
                    doc_supported_lang += '|✖️'

                if lang_code_639_3 in langs_stop_word_lists:
                    doc_supported_lang += '|✔'
                else:
                    doc_supported_lang += '|✖️'

            print(doc_supported_lang)

def wl_test_supported_encodings(main):
    langs = []
    encodings = []

    for file_encoding in main.settings_global['file_encodings']:
        lang = re.search(r'^.+(?= \()', file_encoding).group()
        encoding = file_encoding.replace(lang, r'').replace(r' (', '').replace(r')', '')

        langs.append(lang)
        encodings.append(encoding)

    len_max_langs = max([len(lang) for lang in langs])
    len_max_encodings = max([len(encoding) for encoding in encodings])

    for lang, encoding in zip(langs, encodings):
        print(f'{lang:{len_max_langs}}|{encoding:{len_max_encodings}}|✔')

if __name__ == '__main__':
    main = wl_test_init.Wl_Test_Main()

    wl_test_readme_acks(main)
    wl_test_supported_langs(main)
    wl_test_supported_encodings(main)
