# ----------------------------------------------------------------------
# Wordless: NLP - NLP utilities
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

import collections
import html
import importlib
import itertools
import os
import re
import shutil
import sys
import traceback
import zipfile

import botok
import bs4
import mecab
import nltk
import nltk.tokenize.nist
import packaging.version
import pymorphy3
import pyphen
from PyQt5.QtCore import pyqtSignal
import sacremoses
import spacy
import spacy_pkuseg
import stanza
import sudachipy

from wordless.wl_checks import wl_checks_work_area
from wordless.wl_dialogs import wl_dialogs_misc
from wordless.wl_nlp import wl_sentence_tokenization
from wordless.wl_utils import (
    wl_conversion,
    wl_misc,
    wl_paths,
    wl_threading
)

LANGS_WITHOUT_SPACES = ['mya', 'zho_cn', 'zho_tw', 'khm', 'lao', 'jpn', 'tha', 'bod']

def to_lang_util_code(main, util_type, util_text):
    return main.settings_global['mapping_lang_utils'][util_type][util_text]

def to_lang_util_codes(main, util_type, util_texts):
    return (
        main.settings_global['mapping_lang_utils'][util_type][util_text]
        for util_text in util_texts
    )

def _to_lang_util_text(main, util_type, util_code):
    for text, code in main.settings_global['mapping_lang_utils'][util_type].items():
        if code == util_code:
            return text

    return None

def to_lang_util_text(main, util_type, util_code):
    return _to_lang_util_text(main, util_type, util_code)

def to_lang_util_texts(main, util_type, util_codes):
    return (
        _to_lang_util_text(main, util_type, util_code)
        for util_code in util_codes
    )

LANGS_SPACY = {
    'cat': 'ca_core_news_trf',
    'zho': 'zh_core_web_trf',
    'hrv': 'hr_core_news_lg',
    'dan': 'da_core_news_trf',
    'nld': 'nl_core_news_lg',
    'eng': 'en_core_web_trf',
    'fin': 'fi_core_news_lg',
    'fra': 'fr_dep_news_trf',
    'deu': 'de_dep_news_trf',
    'ell': 'el_core_news_lg',
    'ita': 'it_core_news_lg',
    'jpn': 'ja_core_news_trf',
    'kor': 'ko_core_news_lg',
    'lit': 'lt_core_news_lg',
    'mkd': 'mk_core_news_lg',
    'nob': 'nb_core_news_lg',
    'pol': 'pl_core_news_lg',
    'por': 'pt_core_news_lg',
    'ron': 'ro_core_news_lg',
    'rus': 'ru_core_news_lg',
    'slv': 'sl_core_news_trf',
    'spa': 'es_dep_news_trf',
    'swe': 'sv_core_news_lg',
    'ukr': 'uk_core_news_trf',

    'other': 'en_core_web_trf'
}

def get_langs_stanza(main, util_type):
    langs_stanza = set()

    for lang_code, lang_utils in main.settings_global[util_type].items():
        if any(('stanza' in lang_util for lang_util in lang_utils)):
            langs_stanza.add(lang_code)

    return langs_stanza

@wl_misc.log_time
def check_models(main, langs, lang_utils = None):
    def update_gui_stanza(main, err_msg):
        nonlocal models_ok

        models_ok = wl_checks_work_area.check_results_download_model(main, err_msg)

    models_ok = True
    langs = list(langs)

    # Check all language utilities if not specified
    if lang_utils is None:
        lang_utils = []

        for lang in langs:
            lang_utils.append([])

            for settings in [
                main.settings_custom['sentence_tokenization']['sentence_tokenizer_settings'],
                main.settings_custom['word_tokenization']['word_tokenizer_settings'],
                main.settings_custom['pos_tagging']['pos_tagger_settings']['pos_taggers'],
                main.settings_custom['lemmatization']['lemmatizer_settings'],
                main.settings_custom['dependency_parsing']['dependency_parser_settings'],
                main.settings_custom['sentiment_analysis']['sentiment_analyzer_settings']
            ]:
                if lang in settings:
                    lang_utils[-1].append(settings[lang])
                elif settings in [
                    main.settings_custom['sentence_tokenization']['sentence_tokenizer_settings'],
                    main.settings_custom['word_tokenization']['word_tokenizer_settings']
                ]:
                    lang_utils[-1].append(settings['other'])

    for lang, utils in zip(langs, lang_utils):
        for i, util in enumerate(utils):
            if util == 'default_sentence_tokenizer':
                if lang in main.settings_custom['sentence_tokenization']['sentence_tokenizer_settings']:
                    utils[i] = main.settings_custom['sentence_tokenization']['sentence_tokenizer_settings'][lang]
                else:
                    utils[i] = main.settings_custom['sentence_tokenization']['sentence_tokenizer_settings']['other']
            elif util == 'default_word_tokenizer':
                if lang in main.settings_custom['word_tokenization']['word_tokenizer_settings']:
                    utils[i] = main.settings_custom['word_tokenization']['word_tokenizer_settings'][lang]
                else:
                    utils[i] = main.settings_custom['word_tokenization']['word_tokenizer_settings']['other']
            elif util == 'default_pos_tagger':
                if lang in main.settings_custom['pos_tagging']['pos_tagger_settings']['pos_taggers']:
                    utils[i] = main.settings_custom['pos_tagging']['pos_tagger_settings']['pos_taggers'][lang]
            elif util == 'default_lemmatizer':
                if lang in main.settings_custom['lemmatization']['lemmatizer_settings']:
                    utils[i] = main.settings_custom['lemmatization']['lemmatizer_settings'][lang]
            elif util == 'default_dependency_parser':
                if lang in main.settings_custom['dependency_parsing']['dependency_parser_settings']:
                    utils[i] = main.settings_custom['dependency_parsing']['dependency_parser_settings'][lang]
            elif util == 'default_sentiment_analyzer':
                if lang in main.settings_custom['sentiment_analysis']['sentiment_analyzer_settings']:
                    utils[i] = main.settings_custom['sentiment_analysis']['sentiment_analyzer_settings'][lang]

    for lang, utils in zip(langs, lang_utils):
        if any((util.startswith('spacy_') for util in utils)):
            if lang == 'nno':
                lang_spacy = 'nob'
            else:
                lang_spacy = wl_conversion.remove_lang_code_suffixes(main, lang)

            if lang_spacy in LANGS_SPACY:
                model_name = LANGS_SPACY[lang_spacy]

                try:
                    importlib.import_module(model_name)
                except ModuleNotFoundError:
                    worker_download_model = Wl_Worker_Download_Model_Spacy(
                        main,
                        dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Download_Model(main),
                        update_gui = lambda err_msg, model_name = model_name: wl_checks_work_area.check_results_download_model(main, err_msg, model_name),
                        model_name = model_name
                    )

                    wl_threading.Wl_Thread(worker_download_model).start_worker()

                    try:
                        importlib.import_module(model_name)
                    except ModuleNotFoundError:
                        models_ok = False

        if not models_ok:
            break

        if (
            any((util.startswith('stanza_') for util in utils))
            and lang in get_langs_stanza(main, util_type = 'word_tokenizers')
        ):
            worker_download_model = Wl_Worker_Download_Model_Stanza(
                main,
                dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Download_Model(main),
                update_gui = lambda err_msg: update_gui_stanza(main, err_msg),
                lang = lang
            )

            wl_threading.Wl_Thread(worker_download_model).start_worker()

    if models_ok:
        wl_checks_work_area.wl_status_bar_msg_success_download_model(main)

    return models_ok

class Wl_Worker_Download_Model_Spacy(wl_threading.Wl_Worker):
    worker_done = pyqtSignal(str)

    def __init__(self, main, dialog_progress, update_gui, model_name):
        super().__init__(main, dialog_progress, update_gui, model_name = model_name)

        self.err_msg = ''

    def run(self):
        try:
            self.progress_updated.emit(self.tr('Fetching model information...'))

            # Clean existing models
            for file in os.listdir('.'):
                if os.path.isdir(file) and file.startswith(self.model_name):
                    shutil.rmtree(self.model_name, ignore_errors = True)

            spacy_ver = packaging.version.Version(spacy.about.__version__)
            model_ver = f'{spacy_ver.major}.{spacy_ver.minor}'

            r, err_msg = wl_misc.wl_download(self.main, spacy.about.__compatibility__)

            if not err_msg:
                model_ver = r.json()['spacy'][model_ver][self.model_name][0]
                model_file = f'{self.model_name}-{model_ver}{spacy.cli._util.WHEEL_SUFFIX}'
                model_url = f'{spacy.about.__download_url__}/{self.model_name}-{model_ver}/{model_file}'

                # Get model size
                file_size = wl_misc.wl_download_file_size(self.main, model_url)

                if file_size:
                    self.progress_updated.emit(self.tr('Downloading model ({:.2f} MB)...').format(file_size))
                else:
                    self.progress_updated.emit(self.tr('Downloading model...'))

                if getattr(sys, '_MEIPASS', False):
                    r, err_msg = wl_misc.wl_download(self.main, model_url)

                    if not err_msg:
                        with open(model_file, 'wb') as f:
                            f.write(r.content)

                        with zipfile.ZipFile(model_file) as f:
                            f.extractall(wl_paths.get_path_file(''))

                        # Clear cache
                        os.remove(model_file)
                else:
                    import pip # pylint: disable=import-outside-toplevel

                    pip.main(['install', '--no-deps', model_url])

                    # Clear cache
                    pip.main(['cache', 'purge'])
            else:
                self.err_msg = err_msg
        except Exception: # pylint: disable=broad-exception-caught
            self.err_msg = traceback.format_exc()

        self.progress_updated.emit(self.tr('Download completed successfully.'))
        self.worker_done.emit(self.err_msg)

class Wl_Worker_Download_Model_Stanza(wl_threading.Wl_Worker):
    worker_done = pyqtSignal(str)

    def __init__(self, main, dialog_progress, update_gui, lang):
        super().__init__(main, dialog_progress, update_gui, lang = lang)

        self.err_msg = ''

    def run(self):
        try:
            self.progress_updated.emit(self.tr('Downloading model...'))

            # Change the directory for Stanza's downloaded models when the application is frozen
            if getattr(sys, '_MEIPASS', False):
                model_dir = wl_paths.get_path_file('stanza_resources')
            else:
                model_dir = stanza.resources.common.DEFAULT_MODEL_DIR

            processors = []

            if self.lang in get_langs_stanza(self.main, util_type = 'word_tokenizers'):
                processors.append('tokenize')
            if self.lang in get_langs_stanza(self.main, util_type = 'pos_taggers'):
                processors.append('pos')
            if self.lang in get_langs_stanza(self.main, util_type = 'lemmatizers'):
                processors.append('lemma')
            if self.lang in get_langs_stanza(self.main, util_type = 'dependency_parsers'):
                processors.append('depparse')
            if self.lang in get_langs_stanza(self.main, util_type = 'sentiment_analyzers'):
                processors.append('sentiment')

            if self.lang == 'zho_cn':
                lang_stanza = 'zh-hans'
            elif self.lang == 'zho_tw':
                lang_stanza = 'zh-hant'
            elif self.lang == 'srp_latn':
                lang_stanza = 'sr'
            elif self.lang == 'other':
                lang_stanza = 'en'
            else:
                lang_stanza = wl_conversion.to_iso_639_1(self.main, self.lang, no_suffix = True)

            stanza.download(
                lang = lang_stanza,
                model_dir = model_dir,
                package = 'default',
                processors = processors,
                proxies = wl_misc.wl_get_proxies(self.main),
                download_json = False
            )
        except Exception: # pylint: disable=broad-exception-caught
            self.err_msg = traceback.format_exc()

        self.progress_updated.emit(self.tr('Download completed successfully.'))
        self.worker_done.emit(self.err_msg)

LANGS_SPACY_LEMMATIZERS = [
    'ben', 'ces', 'grc', 'hun', 'ind', 'gle', 'ltz', 'fas', 'srp', 'tgl',
    'tur', 'urd'
]

def init_model_spacy(main, lang, sentencizer_only = False):
    sentencizer_config = {'punct_chars': list(wl_sentence_tokenization.SENTENCE_TERMINATORS)}

    # Sentencizer
    if sentencizer_only:
        if 'spacy_nlp_sentencizer' not in main.__dict__:
            main.__dict__['spacy_nlp_sentencizer'] = spacy.blank('en')
            main.__dict__['spacy_nlp_sentencizer'].add_pipe('sentencizer', config = sentencizer_config)
    else:
        lang = wl_conversion.remove_lang_code_suffixes(main, lang)

        if f'spacy_nlp_{lang}' not in main.__dict__:
            # Languages with models
            if lang in LANGS_SPACY:
                model_name = LANGS_SPACY[lang]
                model = importlib.import_module(model_name)

                # Exclude NER to boost speed
                main.__dict__[f'spacy_nlp_{lang}'] = model.load(exclude = ['ner'])

                # Transformer-based models do not have sentence recognizer
                if not model_name.endswith('_trf'):
                    main.__dict__[f'spacy_nlp_{lang}'].enable_pipe('senter')

                if lang == 'other':
                    main.__dict__[f'spacy_nlp_{lang}'].add_pipe('sentencizer', config = sentencizer_config)
            # Languages without models
            else:
                main.__dict__[f'spacy_nlp_{lang}'] = spacy.blank(wl_conversion.to_iso_639_1(main, lang))

                # Add sentencizer and lemmatizer
                main.__dict__[f'spacy_nlp_{lang}'].add_pipe('sentencizer', config = sentencizer_config)

                if lang in LANGS_SPACY_LEMMATIZERS:
                    main.__dict__[f'spacy_nlp_{lang}'].add_pipe('lemmatizer')
                    main.__dict__[f'spacy_nlp_{lang}'].initialize()

def init_model_stanza(main, lang, lang_util, tokenized = False):
    if lang_util in ['sentence_tokenizer', 'word_tokenizer']:
        processors = ['tokenize']
    elif lang_util == 'pos_tagger':
        processors = ['tokenize', 'pos']
    elif lang_util == 'lemmatizer':
        processors = ['tokenize', 'pos', 'lemma']
    elif lang_util == 'dependency_parser':
        processors = ['tokenize', 'pos', 'lemma', 'depparse']
    elif lang_util == 'sentiment_analyzer':
        processors = ['tokenize', 'sentiment']

    if lang in get_langs_stanza(main, util_type = 'word_tokenizers'):
        if lang not in ['zho_cn', 'zho_tw', 'srp_latn']:
            lang = wl_conversion.remove_lang_code_suffixes(main, lang)

        if (
            f'stanza_nlp_{lang}' not in main.__dict__
            # Some language models require 'mwt' by default
            or set(processors) | {'mwt'} != set(main.__dict__[f'stanza_nlp_{lang}'].processors) | {'mwt'}
            or tokenized != main.__dict__[f'stanza_nlp_{lang}'].kwargs.get('tokenize_pretokenized', False)
        ):
            if lang == 'zho_cn':
                lang_stanza = 'zh-hans'
            elif lang == 'zho_tw':
                lang_stanza = 'zh-hant'
            elif lang == 'srp_latn':
                lang_stanza = 'sr'
            elif lang == 'other':
                lang_stanza = 'en'
            else:
                lang_stanza = wl_conversion.to_iso_639_1(main, lang, no_suffix = True)

            if getattr(sys, '_MEIPASS', False):
                model_dir = wl_paths.get_path_file('stanza_resources')
            else:
                model_dir = stanza.resources.common.DEFAULT_MODEL_DIR

            main.__dict__[f'stanza_nlp_{lang}'] = stanza.Pipeline(
                lang = lang_stanza,
                dir = model_dir,
                package = 'default',
                processors = processors,
                download_method = None,
                tokenize_pretokenized = tokenized
            )

def init_sudachipy_word_tokenizer(main):
    if 'sudachipy_word_tokenizer' not in main.__dict__:
        main.sudachipy_word_tokenizer = sudachipy.Dictionary().create()

def init_sentence_tokenizers(main, lang, sentence_tokenizer):
    # spaCy
    if sentence_tokenizer.startswith('spacy_'):
        if sentence_tokenizer == 'spacy_sentencizer':
            init_model_spacy(main, lang, sentencizer_only = True)
        else:
            init_model_spacy(main, lang)
    # Stanza
    elif sentence_tokenizer.startswith('stanza_'):
        init_model_stanza(main, lang, lang_util = 'sentence_tokenizer')

def init_word_tokenizers(main, lang, word_tokenizer = 'default'):
    if lang not in main.settings_global['word_tokenizers']:
        lang = 'other'

    if word_tokenizer == 'default':
        word_tokenizer = main.settings_custom['word_tokenization']['word_tokenizer_settings'][lang]

    # NLTK
    if word_tokenizer.startswith('nltk_'):
        if word_tokenizer == 'nltk_nist':
            if 'nltk_nist_tokenizer' not in main.__dict__:
                main.nltk_nist_tokenizer = nltk.tokenize.nist.NISTTokenizer()
        elif word_tokenizer == 'nltk_nltk':
            if 'nltk_nltk_tokenizer' not in main.__dict__:
                main.nltk_nltk_tokenizer = nltk.NLTKWordTokenizer()
        elif word_tokenizer == 'nltk_penn_treebank':
            if 'nltk_treebank_tokenizer' not in main.__dict__:
                main.nltk_treebank_tokenizer = nltk.TreebankWordTokenizer()
        elif word_tokenizer == 'nltk_regex':
            if 'nltk_regex_tokenizer' not in main.__dict__:
                main.nltk_regex_tokenizer = nltk.WordPunctTokenizer()
        elif word_tokenizer == 'nltk_tok_tok':
            if 'nltk_toktok_tokenizer' not in main.__dict__:
                main.nltk_toktok_tokenizer = nltk.ToktokTokenizer()
        elif word_tokenizer == 'nltk_twitter':
            if 'nltk_tweet_tokenizer' not in main.__dict__:
                main.nltk_tweet_tokenizer = nltk.TweetTokenizer()
    # Sacremoses
    elif word_tokenizer == 'sacremoses_moses':
        lang_sacremoses = wl_conversion.remove_lang_code_suffixes(main, wl_conversion.to_iso_639_1(main, lang))
        lang = wl_conversion.remove_lang_code_suffixes(main, lang)

        if f'sacremoses_moses_tokenizer_{lang}' not in main.__dict__:
            main.__dict__[f'sacremoses_moses_tokenizer_{lang}'] = sacremoses.MosesTokenizer(lang = lang_sacremoses)
    # spaCy
    elif word_tokenizer.startswith('spacy_'):
        init_model_spacy(main, lang)
    # Stanza
    elif word_tokenizer.startswith('stanza_'):
        init_model_stanza(main, lang, lang_util = 'word_tokenizer')
    # Chinese
    elif word_tokenizer == 'pkuseg_zho':
        if 'pkuseg_word_tokenizer' not in main.__dict__:
            main.pkuseg_word_tokenizer = spacy_pkuseg.pkuseg(model_name = 'mixed')
    # Chinese & Japanese
    elif word_tokenizer.startswith('wordless_'):
        init_model_spacy(main, 'eng_us')
        init_model_spacy(main, 'other')
    # Japanese
    elif word_tokenizer.startswith('sudachipy_jpn'):
        init_sudachipy_word_tokenizer(main)
    # Korean
    elif word_tokenizer == 'python_mecab_ko_mecab':
        if 'python_mecab_ko_mecab' not in main.__dict__:
            main.__dict__['python_mecab_ko_mecab'] = mecab.MeCab()
    # Tibetan
    elif word_tokenizer == 'botok_bod':
        if 'botok_word_tokenizer' not in main.__dict__:
            main.botok_word_tokenizer = botok.WordTokenizer()

def init_syl_tokenizers(main, lang, syl_tokenizer):
    # NLTK
    if syl_tokenizer == 'nltk_legality':
        if 'nltk_syl_tokenizer_legality' not in main.__dict__:
            main.nltk_syl_tokenizer_legality = nltk.tokenize.LegalitySyllableTokenizer(nltk.corpus.words.words())
    elif syl_tokenizer == 'nltk_sonority_sequencing':
        if 'nltk_syl_tokenizer_sonority_sequencing' not in main.__dict__:
            main.nltk_syl_tokenizer_sonority_sequencing = nltk.tokenize.SyllableTokenizer()
    # Pyphen
    elif syl_tokenizer.startswith('pyphen_'):
        if f'pyphen_syl_tokenizer_{lang}' not in main.__dict__:
            lang_pyphen = wl_conversion.to_iso_639_1(main, lang)

            main.__dict__[f'pyphen_syl_tokenizer_{lang}'] = pyphen.Pyphen(lang = lang_pyphen)

def init_word_detokenizers(main, lang):
    if lang not in ['zho_cn', 'zho_tw', 'jpn', 'tha', 'bod']:
        # Sacremoses
        lang_sacremoses = wl_conversion.remove_lang_code_suffixes(main, wl_conversion.to_iso_639_1(main, lang))
        lang = wl_conversion.remove_lang_code_suffixes(main, lang)

        if f'sacremoses_moses_detokenizer_{lang}' not in main.__dict__:
            main.__dict__[f'sacremoses_moses_detokenizer_{lang}'] = sacremoses.MosesDetokenizer(lang = lang_sacremoses)

def init_pos_taggers(main, lang, pos_tagger, tokenized = False):
    # spaCy
    if pos_tagger.startswith('spacy_'):
        init_model_spacy(main, lang)
    # Stanza
    elif pos_tagger.startswith('stanza_'):
        init_model_stanza(main, lang, lang_util = 'pos_tagger', tokenized = tokenized)
    # Japanese
    elif pos_tagger == 'sudachipy_jpn':
        init_sudachipy_word_tokenizer(main)
    # Korean
    elif pos_tagger == 'python_mecab_ko_mecab':
        init_word_tokenizers(main, lang = 'kor', word_tokenizer = 'python_mecab_ko_mecab')
    # Russian & Ukrainian
    elif pos_tagger == 'pymorphy3_morphological_analyzer':
        if lang == 'rus':
            if 'pymorphy3_morphological_analyzer_rus' not in main.__dict__:
                main.pymorphy3_morphological_analyzer_rus = pymorphy3.MorphAnalyzer(lang = 'ru')
        elif lang == 'ukr':
            if 'pymorphy3_morphological_analyzer_ukr' not in main.__dict__:
                main.pymorphy3_morphological_analyzer_ukr = pymorphy3.MorphAnalyzer(lang = 'uk')

def init_lemmatizers(main, lang, lemmatizer, tokenized = False):
    # spaCy
    if lemmatizer.startswith('spacy_'):
        init_model_spacy(main, lang)
    # Stanza
    elif lemmatizer.startswith('stanza_'):
        init_model_stanza(main, lang, lang_util = 'lemmatizer', tokenized = tokenized)
    # Japanese
    elif lemmatizer == 'sudachipy_jpn':
        init_sudachipy_word_tokenizer(main)
    # Russian & Ukrainian
    elif lemmatizer == 'pymorphy3_morphological_analyzer':
        if lang == 'rus':
            if 'pymorphy3_morphological_analyzer_rus' not in main.__dict__:
                main.pymorphy3_morphological_analyzer_rus = pymorphy3.MorphAnalyzer(lang = 'ru')
        elif lang == 'ukr':
            if 'pymorphy3_morphological_analyzer_ukr' not in main.__dict__:
                main.pymorphy3_morphological_analyzer_ukr = pymorphy3.MorphAnalyzer(lang = 'uk')

def init_dependency_parsers(main, lang, dependency_parser, tokenized = False):
    # spaCy
    if dependency_parser.startswith('spacy_'):
        init_model_spacy(main, lang)
    # Stanza
    elif dependency_parser.startswith('stanza_'):
        init_model_stanza(main, lang, lang_util = 'dependency_parser', tokenized = tokenized)

def init_sentiment_analyzers(main, lang, sentiment_analyzer, tokenized = False):
    # Stanza
    if sentiment_analyzer.startswith('stanza_'):
        init_model_stanza(main, lang, lang_util = 'sentiment_analyzer', tokenized = tokenized)

# Make sure tokenization is not modified during NLP processing
def align_tokens(tokens_raw, tokens_processed, results, prefer_raw = False):
    results_modified = []

    tokens_raw = list(tokens_raw)

    i_raw = 0
    i_processed = 0

    len_raw = len(tokens_raw)
    len_processed = len(tokens_processed)

    while i_raw < len_raw and i_processed < len_processed:
        # Different token
        if len(tokens_raw[i_raw]) != len(tokens_processed[i_processed]):
            tokens_raw_temp = [tokens_raw[i_raw]]
            tokens_processed_temp = [tokens_processed[i_processed]]
            results_temp = [results[i_processed]]

            while i_raw < len_raw - 1 or i_processed < len_processed - 1:
                len_raw_temp = sum((len(token) for token in tokens_raw_temp))
                len_processed_temp = sum((len(token) for token in tokens_processed_temp))

                if len_raw_temp < len_processed_temp:
                    tokens_raw_temp.append(tokens_raw[i_raw + 1])

                    i_raw += 1
                elif len_raw_temp > len_processed_temp:
                    tokens_processed_temp.append(tokens_processed[i_processed + 1])
                    results_temp.append(results[i_processed + 1])

                    i_processed += 1
                elif len_raw_temp == len_processed_temp:
                    # eg. lemmatization
                    if prefer_raw:
                        # Always use original tokens
                        results_modified.extend(tokens_raw_temp)
                    # eg. POS tagging
                    else:
                        len_raw_temp_tokens = len(tokens_raw_temp)
                        len_processed_temp_tokens = len(tokens_processed_temp)

                        # Use results if one-to-one
                        if len_raw_temp_tokens == len_processed_temp_tokens:
                            results_modified.extend(results_temp)
                        # Clip results if one-to-many
                        elif len_raw_temp_tokens < len_processed_temp_tokens:
                            results_modified.extend(results_temp[:len_raw_temp_tokens])
                        # Extend results if many-to-one
                        elif len_raw_temp_tokens > len_processed_temp_tokens:
                            results_modified.extend(results_temp)
                            results_modified.extend([results_temp[-1]] * (len_raw_temp_tokens - len_processed_temp_tokens))

                    tokens_raw_temp.clear()
                    tokens_processed_temp.clear()
                    results_temp.clear()

                    break

            # If reaching end of file
            if tokens_raw_temp:
                if prefer_raw:
                    results_modified.extend(tokens_raw_temp)
                else:
                    len_raw_temp_tokens = len(tokens_raw_temp)
                    len_processed_temp_tokens = len(tokens_processed_temp)

                    if len_raw_temp_tokens == len_processed_temp_tokens:
                        results_modified.extend(results_temp)
                    elif len_raw_temp_tokens < len_processed_temp_tokens:
                        results_modified.extend(results_temp[:len_raw_temp_tokens])
                    elif len_raw_temp_tokens > len_processed_temp_tokens:
                        results_modified.extend(results_temp)
                        results_modified.extend([results_temp[-1]] * (len_raw_temp_tokens - len_processed_temp_tokens))
        else:
            results_modified.append(results[i_processed])

        i_raw += 1
        i_processed += 1

    return results_modified

def to_sections(tokens, num_sections):
    len_tokens = len(tokens)

    if len_tokens >= num_sections:
        sections = []

        section_size, remainder = divmod(len_tokens, num_sections)

        for i in range(num_sections):
            if i < remainder:
                section_start = i * section_size + i
            else:
                section_start = i * section_size + remainder

            if i + 1 < remainder:
                section_stop = (i + 1) * section_size + i + 1
            else:
                section_stop = (i + 1) * section_size + remainder

            sections.append(tokens[section_start:section_stop])
    else:
        sections = [[token] for token in tokens]

    return sections

def to_sections_unequal(tokens, section_size):
    tokens = list(tokens)

    for i in range(0, len(tokens), section_size):
        yield tokens[i : i + section_size]

# Read text in chunks to avoid memory error
def split_into_chunks_text(text, section_size):
    # Split text into paragraphs excluding the last empty one
    paras = text.splitlines(keepends = True)

    for section in to_sections_unequal(paras, section_size):
        yield ''.join(section)

# Split long list of tokens
def split_token_list(main, inputs, nlp_util):
    section_size = main.settings_custom['files']['misc_settings']['read_files_in_chunks']

    # Split tokens into sub-lists as inputs of SudachiPy cannot be more than 49149 BYTES
    if nlp_util in ['spacy_jpn', 'sudachipy_jpn'] and sum((len(token) for token in inputs)) > 49149 // 4:
        # Around 6 characters per token and 4 bytes per character (≈ 49149 / 4 / 6)
        texts = to_sections_unequal(inputs, section_size = 2000)
    else:
        texts = to_sections_unequal(inputs, section_size = section_size * 100)

    return texts

# Serbian
SRP_CYRL_TO_LATN = {
    # Uppercase
    'А': 'A',
    'Б': 'B',
    'Ц': 'C',
    'Ч': 'Č',
    'Ћ': 'Ć',
    'Д': 'D',
    'Џ': 'Dž',
    'Ђ': 'Đ',
    'Е': 'E',
    'Ф': 'F',
    'Г': 'G',
    'Х': 'H',
    'И': 'I',
    'Ј': 'J',
    'К': 'K',
    'Л': 'L',
    'Љ': 'Lj',
    'М': 'M',
    'Н': 'N',
    'Њ': 'Nj',
    'О': 'O',
    'П': 'P',
    'Р': 'R',
    'С': 'S',
    'Ш': 'Š',
    'Т': 'T',
    'У': 'U',
    'В': 'V',
    'З': 'Z',
    'Ж': 'Ž',
    # Lowercase
    'а': 'a',
    'б': 'b',
    'ц': 'c',
    'ч': 'č',
    'ћ': 'ć',
    'д': 'd',
    'џ': 'dž',
    'ђ': 'đ',
    'е': 'e',
    'ф': 'f',
    'г': 'g',
    'х': 'h',
    'и': 'i',
    'ј': 'j',
    'к': 'k',
    'л': 'l',
    'љ': 'lj',
    'м': 'm',
    'н': 'n',
    'њ': 'nj',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'ш': 'š',
    'т': 't',
    'у': 'u',
    'в': 'v',
    'з': 'z',
    'ж': 'ž',
}
SRP_LATN_TO_CYRL = {
    # Uppercase
    'A': 'А',
    'B': 'Б',
    'C': 'Ц',
    'Č': 'Ч',
    'Ć': 'Ћ',
    'D': 'Д',
    'Dž': 'Џ',
    'Đ': 'Ђ',
    'E': 'Е',
    'F': 'Ф',
    'G': 'Г',
    'H': 'Х',
    'I': 'И',
    'J': 'Ј',
    'K': 'К',
    'L': 'Л',
    'Lj': 'Љ',
    'M': 'М',
    'N': 'Н',
    'Nj': 'Њ',
    'O': 'О',
    'P': 'П',
    'R': 'Р',
    'S': 'С',
    'Š': 'Ш',
    'T': 'Т',
    'U': 'У',
    'V': 'В',
    'Z': 'З',
    'Ž': 'Ж',
    # Lowercase
    'a': 'а',
    'b': 'б',
    'c': 'ц',
    'č': 'ч',
    'ć': 'ћ',
    'd': 'д',
    'dž': 'џ',
    'đ': 'ђ',
    'e': 'е',
    'f': 'ф',
    'g': 'г',
    'h': 'х',
    'i': 'и',
    'j': 'ј',
    'k': 'к',
    'l': 'л',
    'lj': 'љ',
    'm': 'м',
    'n': 'н',
    'nj': 'њ',
    'o': 'о',
    'p': 'п',
    'r': 'р',
    's': 'с',
    'š': 'ш',
    't': 'т',
    'u': 'у',
    'v': 'в',
    'z': 'з',
    'ž': 'ж'
}
SRP_LATN_TO_CYRL_DIGRAPHS = {
    'Dž': 'Џ',
    'Lj': 'Љ',
    'Nj': 'Њ',
    'dž': 'џ',
    'lj': 'љ',
    'nj': 'њ'
}

def to_srp_latn(tokens):
    tokens_latn = []

    for token in tokens:
        token_latn = ''

        for char in token:
            if char not in SRP_CYRL_TO_LATN:
                token_latn += char
            else:
                token_latn += SRP_CYRL_TO_LATN[char]

        tokens_latn.append(token_latn)

    return tokens_latn

def to_srp_cyrl(tokens):
    tokens_cyrl = []

    for token in tokens:
        token_cyrl = ''

        for char_latn, char_cyrl in SRP_LATN_TO_CYRL_DIGRAPHS.items():
            token = token.replace(char_latn, char_cyrl)

        for char in token:
            if char not in SRP_LATN_TO_CYRL:
                token_cyrl += char
            else:
                token_cyrl += SRP_LATN_TO_CYRL[char]

        tokens_cyrl.append(token_cyrl)

    return tokens_cyrl

# N-grams
# Reference: https://more-itertools.readthedocs.io/en/stable/_modules/more_itertools/recipes.html#sliding_window
def ngrams(tokens, ngram_size):
    if ngram_size == 1:
        for token in tokens:
            yield (token,)
    else:
        it = iter(tokens)
        window = collections.deque(itertools.islice(it, ngram_size), maxlen = ngram_size)

        if len(window) == ngram_size:
            yield tuple(window)

        for x in it:
            window.append(x)

            yield tuple(window)

# Reference: https://www.nltk.org/_modules/nltk/util.html#everygrams
def everygrams(tokens, ngram_size_min, ngram_size_max):
    if ngram_size_min == ngram_size_max:
        yield from ngrams(tokens, ngram_size_min)
    else:
        # Pad token list to the right
        SENTINEL = object()
        tokens = itertools.chain(tokens, (SENTINEL,) * (ngram_size_max - 1))

        for ngram in ngrams(tokens, ngram_size_max):
            for i in range(ngram_size_min, ngram_size_max + 1):
                if ngram[i - 1] is not SENTINEL:
                    yield ngram[:i]

# Reference: https://www.nltk.org/_modules/nltk/util.html#skipgrams
def skipgrams(tokens, ngram_size, num_skipped_tokens):
    if ngram_size == 1:
        yield from ngrams(tokens, ngram_size = 1)
    else:
        # Pad token list to the right
        SENTINEL = object()
        tokens = itertools.chain(tokens, (SENTINEL,) * (ngram_size - 1))

        for ngram in ngrams(tokens, ngram_size + num_skipped_tokens):
            head = ngram[:1]
            tail = ngram[1:]

            for skip_tail in itertools.combinations(tail, ngram_size - 1):
                if skip_tail[-1] is not SENTINEL:
                    yield head + skip_tail

# HTML
def escape_token(token):
    return html.escape(token).strip()

def escape_tokens(tokens):
    return [html.escape(token).strip() for token in tokens]

def html_to_text(text):
    # Remove tags and unescape character entities
    text = bs4.BeautifulSoup(text, features = 'lxml').get_text()
    text = text.replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)

    return text.strip()
