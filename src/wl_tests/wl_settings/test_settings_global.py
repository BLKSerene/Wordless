#
# Wordless: Tests - Settings - Global Settings
#
# Copyright (C) 2018-2021  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import os
import pkgutil
import re
import sys

sys.path.append('.')

import pytest
import sacremoses
import spacy
import spacy_lookups_data

from wl_tests import wl_test_init
from wl_utils import wl_conversion

main = wl_test_init.Wl_Test_Main()

def check_missing_extra_langs(langs_supported, langs_global, msg):
    for lang_code in langs_supported:
        lang_code_639_3 = wl_conversion.to_iso_639_3(main, lang_code)

        if lang_code_639_3 not in langs_global:
            print(f'''Missing language code "{lang_code} / {lang_code_639_3}" found for {msg}!''')

            lang_missing = True

    for lang_code in langs_global:
        lang_code_639_1 = wl_conversion.to_iso_639_1(main, lang_code)

        if lang_code_639_1 not in langs_supported:
            print(f'''Extra language code "{lang_code} / {lang_code_639_1}" found for {msg}!''')

            lang_extra = True

def check_missing_extra_langs_default(langs, langs_default, msg):
    for lang_code in langs:
        if lang_code not in langs_default:
            print(f'Missing language code "{lang_code}" found in the default settings of {msg}!')

            lang_default_missing = True

    for lang_code_default in langs_default:
        if lang_code_default not in langs:
            print(f'Extra language code "{lang_code_default}" found in the default settings of {msg}!')

            lang_default_extra = True

def test_settings_global():
    settings_global = main.settings_global
    settings_default = main.settings_default

    settings_sentence_tokenizers = settings_global['sentence_tokenizers']
    settings_sentence_tokenizers_default = settings_default['sentence_tokenization']['sentence_tokenizers']

    settings_word_tokenizers = settings_global['word_tokenizers']
    settings_word_tokenizers_default = settings_default['word_tokenization']['word_tokenizers']

    settings_word_detokenizers = settings_global['word_detokenizers']
    settings_word_detokenizers_default = settings_default['word_detokenization']['word_detokenizers']

    settings_pos_taggers = settings_global['pos_taggers']
    settings_pos_taggers_default = settings_default['pos_tagging']['pos_taggers']
    settings_tagsets_default = settings_default['tagsets']['preview_pos_tagger']

    settings_lemmatizers = settings_global['lemmatizers']
    settings_lemmatizers_default = settings_default['lemmatization']['lemmatizers']

    settings_stop_word_lists = settings_global['stop_word_lists']
    settings_stop_word_lists_default = settings_default['stop_word_lists']['stop_word_lists']
    settings_stop_word_lists_default_custom = settings_default['stop_word_lists']['custom_lists']

    langs_supported_sacremoses = []
    langs_supported_spacy = []
    langs_supported_spacy_lemmatizers = []
    langs_supported_spacy_stop_words = []

    langs_sentence_tokenizers = list(settings_sentence_tokenizers.keys())
    langs_sentence_tokenizers_default = list(settings_sentence_tokenizers_default.keys())
    langs_sentence_tokenizers_spacy = []

    langs_word_tokenizers = list(settings_word_tokenizers.keys())
    langs_word_tokenizers_default = list(settings_word_tokenizers_default.keys())
    langs_word_tokenizers_nltk = []
    langs_word_tokenizers_sacremoses = []
    langs_word_tokenizers_spacy = []

    langs_word_detokenizers = list(settings_word_detokenizers.keys())
    langs_word_detokenizers_default = list(settings_word_detokenizers_default.keys())
    langs_word_detokenizers_nltk = []
    langs_word_detokenizers_sacremoses = []

    langs_pos_taggers = list(settings_pos_taggers.keys())
    langs_pos_taggers_default = list(settings_pos_taggers_default.keys())
    langs_tagsets_default = list(settings_tagsets_default.keys())

    langs_lemmatizers = list(settings_lemmatizers.keys())
    langs_lemmatizers_default = list(settings_lemmatizers_default.keys())
    langs_lemmatizers_spacy = []

    langs_stop_word_lists = list(settings_stop_word_lists.keys())
    langs_stop_word_lists_default = list(settings_stop_word_lists_default.keys())
    langs_stop_word_lists_default_custom = list(settings_stop_word_lists_default_custom.keys())
    langs_stop_word_lists_spacy = []

    lang_missing = False
    lang_extra = False
    lang_default_missing = False
    lang_default_extra = False

    # Loading languages supported by Sacremoses
    for file in os.listdir(os.path.split(sacremoses.__file__)[0] + '/data/nonbreaking_prefixes/'):
        file_ext = os.path.splitext(file)[1][1:]

        if file_ext not in ['yue', 'zh']:
            langs_supported_sacremoses.append(file_ext)

    # Loading languages supported by spaCy
    for lang in pkgutil.iter_modules(spacy.lang.__path__):
        if lang.ispkg:
            if lang.name not in ['ja', 'ko', 'sr', 'th', 'vi', 'zh', 'xx']:
                langs_supported_spacy.append(lang.name)
            # Chinese
            elif lang.name == 'zh':
                langs_supported_spacy.extend(['zh_cn', 'zh_tw'])
            # Serbian
            elif lang.name == 'sr':
                langs_supported_spacy.extend(['sr_cyrl', 'sr_latn'])

    # Lemmatizers
    for file in os.listdir(f'{spacy_lookups_data.__path__[0]}/data/'):
        if 'lemma' in file:
            lang_code = re.search(r'^([a-z]{2,3})_', file).groups()[0]
            
            # Serbian
            if lang_code == 'sr':
                langs_supported_spacy_lemmatizers.append('sr_cyrl')
            else:
                langs_supported_spacy_lemmatizers.append(lang_code)

    langs_supported_spacy_lemmatizers = sorted(set(langs_supported_spacy_lemmatizers))

    # Stop word lists
    for lang in pkgutil.iter_modules(spacy.lang.__path__):
        if lang.ispkg:
            for file in os.listdir(f'{spacy.lang.__path__[0]}/{lang.name}/'):
                if file == 'stop_words.py':
                    if lang.name not in ['sr', 'zh', 'xx', 'az']:
                        langs_supported_spacy_stop_words.append(lang.name)
                    # Chinese
                    elif lang.name == 'zh':
                        langs_supported_spacy_stop_words.extend(['zh_cn', 'zh_tw'])
                    # Serbian
                    elif lang.name == 'sr':
                        langs_supported_spacy_stop_words.extend(['sr_cyrl', 'sr_latn'])

                    break

    # Check for missing and extra languages for spaCy's sentencizer
    for lang_code, sentence_tokenizers in settings_sentence_tokenizers.items():
        if lang_code != 'other' and any(['spaCy' in sentence_tokenizer for sentence_tokenizer in sentence_tokenizers]):
            langs_sentence_tokenizers_spacy.append(lang_code)

    check_missing_extra_langs(langs_supported_spacy, langs_sentence_tokenizers_spacy, "spaCy's sentencizer")

    # Check for missing and extra languages for NLTK's word tokenizers
    for lang_code, word_tokenizers in settings_word_tokenizers.items():
        if lang_code != 'other' and any(['NLTK - NLTK Tokenizer' in word_tokenizer for word_tokenizer in word_tokenizers]):
            langs_word_tokenizers_nltk.append(lang_code)

    for lang_code in langs_word_tokenizers:
        if lang_code != 'other':
            lang_family = wl_conversion.get_lang_family(main, lang_code)

            if lang_family == 'Indo-European':
                if lang_code not in langs_word_tokenizers_nltk:
                    print(f'''Missing language code "{lang_code}" found for NLTK's tokenizers!''')

                    lang_missing = True
            else:
                if lang_code in langs_word_tokenizers_nltk:
                    print(f'''Extra language code "{lang_code}" found for NLTK's tokenizers!''')

                    lang_extra = True

    # Check for missing and extra languages for Sacremoses's Moses tokenizer
    for lang_code, word_tokenizers in settings_word_tokenizers.items():
        if lang_code != 'other' and any(['Sacremoses' in word_tokenizer for word_tokenizer in word_tokenizers]):
            langs_word_tokenizers_sacremoses.append(lang_code)

    check_missing_extra_langs(langs_supported_sacremoses, langs_word_tokenizers_sacremoses, "Sacremoses's Moses tokenizer")

    # Check for missing and extra languages for spaCy's word tokenizers
    for lang_code, word_tokenizers in settings_word_tokenizers.items():
        if lang_code != 'other' and any(['spaCy' in word_tokenizer for word_tokenizer in word_tokenizers]):
            langs_word_tokenizers_spacy.append(lang_code)

    check_missing_extra_langs(langs_supported_spacy, langs_word_tokenizers_spacy, "spaCy's word tokenizers")

    # Check for missing and extra languages for NLTK's Penn Treebank detokenizer
    for lang_code, word_detokenizers in settings_word_detokenizers.items():
        if lang_code != 'other' and any(['NLTK' in word_detokenizer for word_detokenizer in word_detokenizers]):
            langs_word_detokenizers_nltk.append(lang_code)

    for lang_code in langs_word_detokenizers:
        if lang_code != 'other':
            lang_family = wl_conversion.get_lang_family(main, lang_code)
            
            if lang_family == 'Indo-European':
                if lang_code not in langs_word_detokenizers_nltk:
                    print(f'''Missing language code "{lang_code}" found for NLTK's Penn Treebank detokenizer!''')

                    lang_missing = True
            else:
                if lang_code in langs_word_detokenizers_nltk:
                    print(f'''Extra language code "{lang_code}" found for NLTK's Penn Treebank detokenizer!''')

                    lang_extra = True

    # Check for missing and extra languages for Sacremoses's Moses detokenizer
    for lang_code, word_detokenizers in settings_word_detokenizers.items():
        if lang_code != 'other' and any(['Sacremoses' in word_detokenizer for word_detokenizer in word_detokenizers]):
            langs_word_detokenizers_sacremoses.append(lang_code)

    check_missing_extra_langs(langs_supported_sacremoses, langs_word_detokenizers_sacremoses, "Sacremoses's Moses detokenizer")

    # Check for missing and extra languages for spaCy's lemmatizers
    for lang_code, lemmatizers in settings_lemmatizers.items():
        if lang_code != 'other' and any(['spaCy' in lemmatizer for lemmatizer in lemmatizers]):
            langs_lemmatizers_spacy.append(lang_code)

    check_missing_extra_langs(langs_supported_spacy_lemmatizers, langs_lemmatizers_spacy, "spaCy's lemmatizers")

    # Check for missing and extra languages for spaCy's stop word lists
    for lang_code, stop_word_lists in settings_stop_word_lists.items():
        if lang_code != 'other' and any(['spaCy' in stop_word_list for stop_word_list in stop_word_lists]):
            langs_stop_word_lists_spacy.append(lang_code)

    check_missing_extra_langs(langs_supported_spacy_stop_words, langs_stop_word_lists_spacy, "spaCy's stop word lists")

    # Check for missing and extra languages in default settings
    check_missing_extra_langs_default(langs_sentence_tokenizers, langs_sentence_tokenizers_default, 'sentence tokenizers')
    check_missing_extra_langs_default(langs_word_tokenizers, langs_word_tokenizers_default, 'word tokenizers')
    check_missing_extra_langs_default(langs_word_detokenizers, langs_word_detokenizers_default, 'word detokenizers')
    check_missing_extra_langs_default(langs_pos_taggers, langs_pos_taggers_default, 'pos_taggers')
    check_missing_extra_langs_default(langs_pos_taggers, langs_tagsets_default, 'tagsets')
    check_missing_extra_langs_default(langs_lemmatizers, langs_lemmatizers_default, 'lemmatizers')
    check_missing_extra_langs_default(langs_stop_word_lists, langs_stop_word_lists_default, 'stop word lists')
    check_missing_extra_langs_default(langs_stop_word_lists_default, langs_stop_word_lists_default_custom, 'custom lists')

    assert not lang_missing
    assert not lang_extra
    assert not lang_default_missing
    assert not lang_default_extra

if __name__ == '__main__':
    test_settings_global()
