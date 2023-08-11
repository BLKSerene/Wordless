# ----------------------------------------------------------------------
# Wordless: Tests - Documentation
# Copyright (C) 2018-2023  Ye Lei (叶磊)
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

import re

from tests import wl_test_init

def wl_test_supported_langs(main):
    langs_supported = [
        (lang_name, lang_code_639_3)
        for lang_name, (lang_code_639_3, _, _) in main.settings_global['langs'].items()
    ]
    len_max_langs = max((len(lang_name) for lang_name, lang_code_639_3 in langs_supported))

    langs_sentence_tokenizers = main.settings_global['sentence_tokenizers'].keys()
    langs_word_tokenizers = main.settings_global['word_tokenizers'].keys()
    langs_syl_tokenizers = main.settings_global['syl_tokenizers'].keys()
    langs_pos_taggers = main.settings_global['pos_taggers'].keys()
    langs_lemmatizers = main.settings_global['lemmatizers'].keys()
    langs_stop_word_lists = main.settings_global['stop_word_lists'].keys()
    langs_dependency_parsers = main.settings_global['dependency_parsers'].keys()
    langs_sentiment_analyzers = main.settings_global['sentiment_analyzers'].keys()

    langs_nlp_utils = [
        langs_sentence_tokenizers,
        langs_word_tokenizers,
        langs_syl_tokenizers,
        langs_pos_taggers,
        langs_lemmatizers,
        langs_stop_word_lists,
        langs_dependency_parsers,
        langs_sentiment_analyzers
    ]

    for lang_name, lang_code_639_3 in langs_supported:
        if any((
            lang_code_639_3 in langs
            for langs in langs_nlp_utils
        )):
            doc_supported_lang = f'{lang_name:{len_max_langs}s}'

            if lang_code_639_3 == 'other':
                doc_supported_lang += '|⭕️ |⭕️ |✖️|✖️|✖️|✖️|✖️|✖️'
            else:
                for i, langs in enumerate(langs_nlp_utils):
                    if i <= 1:
                        if lang_code_639_3 in langs:
                            doc_supported_lang += '|✔'
                        else:
                            doc_supported_lang += '|⭕️ '
                    else:
                        if lang_code_639_3 in langs:
                            doc_supported_lang += '|✔'
                        else:
                            doc_supported_lang += '|✖️'

            print(doc_supported_lang)

    print()

def wl_test_supported_encodings(main):
    langs = []
    encodings = []

    for encoding in main.settings_global['encodings']:
        lang = re.search(r'^.+(?= \()', encoding).group()
        encoding = encoding.replace(lang, r'').replace(r' (', '').replace(')', '')

        langs.append(lang)
        encodings.append(encoding)

    len_max_langs = max((len(lang) for lang in langs))
    len_max_encodings = max((len(encoding) for encoding in encodings))

    for lang, encoding in zip(langs, encodings):
        if encoding == 'UTF-8 with BOM':
            print(f'{lang:{len_max_langs}}|{encoding:{len_max_encodings}}|✖️')
        else:
            print(f'{lang:{len_max_langs}}|{encoding:{len_max_encodings}}|✔')

if __name__ == '__main__':
    main = wl_test_init.Wl_Test_Main()

    wl_test_supported_langs(main)
    wl_test_supported_encodings(main)
