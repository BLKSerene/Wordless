# ----------------------------------------------------------------------
# Wordless: Tests - Documentation
# Copyright (C) 2018-2022  Ye Lei (叶磊)
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

import csv
import re

from wl_tests import wl_test_init

def wl_test_readme_acks(main):
    acks = []

    with open(r'wl_acks.csv', 'r', encoding = 'utf_8', newline = '') as f:
        reader = csv.reader(f)

        for row in reader:
            name = row[0]
            home_page = row[1]
            authors = row[3]

            acks.append([name, home_page, authors])

    len_names = max([len(name) + len(home_page) for name, home_page, _ in acks]) + 4

    for i, (name, home_page, authors) in enumerate(acks):
        len_name = len_names - len(name) - len(home_page) - 4

        if len_name:
            print(f"{i + 1 : <6}|[{name}]({home_page}){' ':{len_name}}|{authors}")
        else:
            print(f"{i + 1 : <6}|[{name}]({home_page})|{authors}")

def wl_test_supported_langs(main):
    langs_supported = [
        (lang_name, lang_code_639_3)
        for lang_name, (lang_code_639_3, _, _) in main.settings_global['langs'].items()
    ]

    langs_sentence_tokenizers = main.settings_global['sentence_tokenizers'].keys()
    langs_word_tokenizers = main.settings_global['word_tokenizers'].keys()
    langs_syl_tokenizers = main.settings_global['syl_tokenizers'].keys()
    langs_pos_tagging = main.settings_global['pos_taggers'].keys()
    langs_lemmatizers = main.settings_global['lemmatizers'].keys()
    langs_stop_word_lists = main.settings_global['stop_word_lists'].keys()

    len_max_langs = max([len(lang_name) for lang_name, lang_code_639_3 in langs_supported])

    for lang_name, lang_code_639_3 in langs_supported:
        if (
            lang_code_639_3 in langs_sentence_tokenizers
            or lang_code_639_3 in langs_word_tokenizers
            or lang_code_639_3 in langs_syl_tokenizers
            or lang_code_639_3 in langs_pos_tagging
            or lang_code_639_3 in langs_lemmatizers
            or lang_code_639_3 in langs_stop_word_lists
        ):
            doc_supported_lang = f'{lang_name:{len_max_langs}s}'

            if lang_code_639_3 == 'other':
                doc_supported_lang += '|⭕️ |⭕️ |✖️|✖️|✖️|✖️'
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
