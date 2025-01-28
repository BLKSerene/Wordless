# ----------------------------------------------------------------------
# Utilities: Generate multilingual sentiment dictionaries for VADER
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

import math
import os
import re
import urllib

import numpy
import requests
import vaderSentiment.vaderSentiment

from tests import wl_test_init
from wordless.wl_nlp import wl_nlp_utils, wl_word_tokenization
from wordless.wl_utils import wl_conversion

def google_translate(words, lang_src, lang_tgt, chunk_size = 1000):
    results = []

    for i in range(math.ceil(len(words) / chunk_size)):
        query = '\n'.join(words[i * chunk_size : (i + 1) * chunk_size])
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={lang_src}&tl={lang_tgt}&dt=t&q={urllib.parse.quote(query)}"
        r = requests.get(url, timeout = 10)

        for item in r.json()[0]:
            results.append(re.sub(r'[\u200b-\u200d]+', '', item[0].strip()))

    assert len(words) == len(results)

    return results

def add_val_to_trs(trs, tr, val):
    if val in trs:
        trs[tr].append(val)
    else:
        trs[tr] = [val]

main = wl_test_init.Wl_Test_Main()

lexicon = [[], []]
emojis = [[], []]

booster_dict = [
    list(vaderSentiment.vaderSentiment.BOOSTER_DICT),
    list(vaderSentiment.vaderSentiment.BOOSTER_DICT.values())
]
sentiment_laden_idioms = [
    list(vaderSentiment.vaderSentiment.SENTIMENT_LADEN_IDIOMS),
    list(vaderSentiment.vaderSentiment.SENTIMENT_LADEN_IDIOMS.values())
]
special_cases = [
    list(vaderSentiment.vaderSentiment.SPECIAL_CASES),
    list(vaderSentiment.vaderSentiment.SPECIAL_CASES.values())
]

vader_dir = os.path.split(vaderSentiment.vaderSentiment.__file__)[0]

with open(f'{vader_dir}/vader_lexicon.txt', 'r', encoding = 'utf_8') as f:
    for line in f:
        items = line.strip().split('\t')
        lexicon[0].append(items[0])
        lexicon[1].append('\t'.join(items[1:]))

with open(f'{vader_dir}/emoji_utf8_lexicon.txt', 'r', encoding = 'utf_8') as f:
    for line in f:
        items = line.strip().split('\t')
        emojis[0].append(items[0])
        # Google Translate treat exclamation marks as sentence boundaries
        emojis[1].append(items[1].replace('!', ''))

os.makedirs('data/VADER', exist_ok = True)

for lang, utils in main.settings_global['sentiment_analyzers'].items():
    for util in utils:
        if (
            not lang.startswith('eng_')
            and lang not in ['fil', 'vie']
            and 'vader_' in util
        ):
            match (lang_vader := util[6:]):
                case 'zho_cn' | 'zho_tw' | 'mni_mtei':
                    lang_vader = wl_conversion.to_iso_639_1(main, lang_vader)
                case _:
                    lang_vader = wl_conversion.to_iso_639_1(main, lang_vader, no_suffix = True)

            print(f'Translating to {lang_vader}...')

            dict_path_lexicon = f'data/VADER/vader_lexicon_{lang_vader}.txt'
            dict_path_emoji = f'data/VADER/emoji_utf8_lexicon_{lang_vader}.txt'
            dict_path_exceptions = f'data/VADER/exceptions_{lang_vader}.py'

            if lang_vader == 'sr':
                dict_paths_srp = [
                    'data/VADER/vader_lexicon_sr_cyrl.txt',
                    'data/VADER/vader_lexicon_sr_latn.txt',
                    'data/VADER/emoji_utf8_lexicon_sr_cyrl.txt',
                    'data/VADER/emoji_utf8_lexicon_sr_latn.txt',
                    'data/VADER/exceptions_sr_cyrl.py',
                    'data/VADER/exceptions_sr_latn.py'
                ]

                dict_path_lexicon = dict_paths_srp[0]
                dict_path_emoji = dict_paths_srp[2]
                dict_path_exceptions = dict_paths_srp[4]

            trs_lexicon = {}
            trs_emojis = {}
            trs_negate = []
            trs_booster_dict = {}

            if not os.path.exists(dict_path_lexicon):
                for src, tr, vals in zip(lexicon[0], google_translate(lexicon[0], 'en', lang_vader), lexicon[1]):
                    # Do not translate lexical items containing only punctuation marks and/or numerals
                    if all((char.isalpha() for char in src)):
                        if lang in wl_nlp_utils.LANGS_WITHOUT_SPACES:
                            for word in wl_word_tokenization.wl_word_tokenize_flat(main, tr, lang):
                                add_val_to_trs(trs_lexicon, word, vals)
                        else:
                            for word in tr.split():
                                add_val_to_trs(trs_lexicon, word, vals)
                    else:
                        add_val_to_trs(trs_lexicon, src, vals)

                trs_lexicon_merged = {}

                for tr, vals in trs_lexicon.items():
                    measures = [float(val.split('\t')[0]) for val in vals]

                    trs_lexicon_merged[tr] = '\t'.join([str(numpy.mean(measures)), vals[-1].split('\t', maxsplit = 1)[1]])

                with open(dict_path_lexicon, 'w', encoding = 'utf_8') as f:
                    for word, vals in trs_lexicon_merged.items():
                        f.write(f'{word}\t{vals}\n')

                if lang_vader == 'sr':
                    trs_lexicon_merged = dict(zip(
                        wl_nlp_utils.to_srp_latn(list(trs_lexicon_merged)),
                        trs_lexicon_merged.values()
                    ))

                    with open(dict_paths_srp[1], 'w', encoding = 'utf_8') as f:
                        for word, vals in trs_lexicon_merged.items():
                            f.write(f'{word}\t{vals}\n')

            if not os.path.exists(dict_path_emoji):
                for emoji, tr in zip(emojis[0], google_translate(emojis[1], 'en', lang_vader, chunk_size = 300)):
                    if lang in wl_nlp_utils.LANGS_WITHOUT_SPACES:
                        trs_emojis[emoji] = ' '.join(wl_word_tokenization.wl_word_tokenize_flat(main, tr, lang))
                    else:
                        trs_emojis[emoji] = tr

                with open(dict_path_emoji, 'w', encoding = 'utf_8') as f:
                    for emoji, tr in trs_emojis.items():
                        f.write(f'{emoji}\t{tr}\n')

                if lang_vader == 'sr':
                    trs_emojis = dict(zip(
                        list(trs_emojis),
                        wl_nlp_utils.to_srp_latn(trs_emojis.values())
                    ))

                    with open(dict_paths_srp[3], 'w', encoding = 'utf_8') as f:
                        for emoji, description in trs_emojis.items():
                            f.write(f'{emoji}\t{description}\n')

            if not os.path.exists(dict_path_exceptions):
                for tr in google_translate(vaderSentiment.vaderSentiment.NEGATE, 'en', lang_vader):
                    if lang in wl_nlp_utils.LANGS_WITHOUT_SPACES:
                        trs_negate.extend(wl_word_tokenization.wl_word_tokenize_flat(main, tr, lang))
                    else:
                        for word in tr.split():
                            trs_negate.append(word)

                for tr, val in zip(google_translate(booster_dict[0], 'en', lang_vader), booster_dict[1]):
                    if lang in wl_nlp_utils.LANGS_WITHOUT_SPACES:
                        for word in wl_word_tokenization.wl_word_tokenize_flat(main, tr, lang):
                            add_val_to_trs(trs_booster_dict, word, val)
                    else:
                        for word in tr.split():
                            add_val_to_trs(trs_booster_dict, word, val)

                trs_booster_dict = {tr: numpy.mean(vals) for tr, vals in trs_booster_dict.items()}

                for i, exceptions in enumerate([sentiment_laden_idioms, special_cases]):
                    trs = google_translate(exceptions[0], 'en', lang_vader)

                    if lang in wl_nlp_utils.LANGS_WITHOUT_SPACES:
                        trs = [
                            ' '.join(wl_word_tokenization.wl_word_tokenize_flat(main, tr, lang))
                            for tr in trs
                        ]

                    trs_merged = {}

                    for tr, val in zip(trs, exceptions[1]):
                        add_val_to_trs(trs_merged, tr, val)

                    trs_merged = {tr: numpy.mean(vals) for tr, vals in trs_merged.items()}

                    match i:
                        case 0:
                            trs_sentiment_laden_idioms = trs_merged
                        case 1:
                            trs_special_cases = trs_merged

                with open(dict_path_exceptions, 'w', encoding = 'utf_8') as f:
                    f.write(f'NEGATE = {repr(list(dict.fromkeys(trs_negate)))}\n')
                    f.write(f'BOOSTER_DICT = {repr(trs_booster_dict)}\n')
                    f.write(f'SENTIMENT_LADEN_IDIOMS = {repr(trs_sentiment_laden_idioms)}\n')
                    f.write(f'SPECIAL_CASES = {repr(trs_special_cases)}\n')

                if lang_vader == 'sr':
                    trs_negate = wl_nlp_utils.to_srp_latn(trs_negate)
                    trs_booster_dict = dict(zip(
                        wl_nlp_utils.to_srp_latn(list(trs_booster_dict)),
                        trs_booster_dict.values()
                    ))
                    trs_sentiment_laden_idioms = dict(zip(
                        wl_nlp_utils.to_srp_latn(list(trs_sentiment_laden_idioms)),
                        trs_sentiment_laden_idioms.values()
                    ))
                    trs_special_cases = dict(zip(
                        wl_nlp_utils.to_srp_latn(list(trs_special_cases)),
                        trs_special_cases.values()
                    ))

                    with open(dict_paths_srp[5], 'w', encoding = 'utf_8') as f:
                        f.write(f'NEGATE = {repr(list(dict.fromkeys(trs_negate)))}\n')
                        f.write(f'BOOSTER_DICT = {repr(trs_booster_dict)}\n')
                        f.write(f'SENTIMENT_LADEN_IDIOMS = {repr(trs_sentiment_laden_idioms)}\n')
                        f.write(f'SPECIAL_CASES = {repr(trs_special_cases)}\n')
