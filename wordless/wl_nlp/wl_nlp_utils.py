# ----------------------------------------------------------------------
# Wordless: NLP - NLP Utilities
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

import collections
import html
import importlib
import itertools
import os
import re
import shutil
import sys
import traceback

import botok
import bs4
import mecab
import nltk
import nltk.tokenize.nist
import packaging.version
import pip
import pymorphy3
import pyphen
import sacremoses
import spacy
import spacy_pkuseg
import sudachipy

from wordless.wl_checks import wl_checks_work_area
from wordless.wl_dialogs import wl_dialogs_misc
from wordless.wl_utils import wl_conversion, wl_misc, wl_threading

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

SPACY_LANGS = {
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
SPACY_LANGS_LEMMATIZERS = ['ben', 'ces', 'grc', 'hun', 'ind', 'gle', 'ltz', 'fas', 'srp', 'tgl', 'tur', 'urd']

def check_models(main, langs, lang_utils = None):
    models_ok = True

    # Check all language utilities if language utility is not specified
    if lang_utils is None:
        langs_to_check = langs.copy()
        langs = []
        lang_utils = []

        for lang in langs_to_check:
            langs.extend([lang] * 5)
            lang_utils.extend([
                main.settings_custom['sentence_tokenization']['sentence_tokenizer_settings'][lang],
                main.settings_custom['word_tokenization']['word_tokenizer_settings'][lang],
                main.settings_custom['pos_tagging']['pos_tagger_settings']['pos_taggers'][lang],
                main.settings_custom['lemmatization']['lemmatizer_settings'][lang],
                main.settings_custom['dependency_parsing']['dependency_parser_settings'][lang]
            ])

    for lang, lang_util in zip(langs, lang_utils):
        if lang == 'nno':
            lang = 'nob'
        else:
            lang = wl_conversion.remove_lang_code_suffixes(main, lang)

        if lang_util.startswith('spacy_') and lang in SPACY_LANGS:
            model_name = SPACY_LANGS[lang]

            try:
                importlib.import_module(model_name)
            except ModuleNotFoundError:
                worker_download_model = Wl_Worker_Download_Spacy_Model(
                    main,
                    dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Download_Model(main),
                    update_gui = lambda err_msg, model_name = model_name: wl_checks_work_area.check_results_download_model(main, model_name, err_msg),
                    model_name = model_name
                )

                wl_threading.Wl_Thread(worker_download_model).start_worker()

                try:
                    importlib.import_module(model_name)
                except ModuleNotFoundError:
                    models_ok = False

        if not models_ok:
            break

    return models_ok

class Wl_Worker_Download_Spacy_Model(wl_threading.Wl_Worker):
    worker_done = wl_threading.wl_pyqt_signal(str)

    def __init__(self, main, dialog_progress, update_gui, model_name): # pylint: disable=unused-argument
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
                filename = f'{self.model_name}-{model_ver}/{self.model_name}-{model_ver}{spacy.cli._util.WHEEL_SUFFIX}'

                model_url = f'{spacy.about.__download_url__}/{filename}'

                # Get model size
                file_size = wl_misc.wl_download_file_size(self.main, model_url)

                if file_size:
                    self.progress_updated.emit(self.tr(f'Downloading model ({file_size:.2f} MB)...'))
                else:
                    self.progress_updated.emit(self.tr('Downloading model...'))

                if getattr(sys, '_MEIPASS', False):
                    pip.main(['install', '--target', '.', '--no-deps', model_url])
                else:
                    pip.main(['install', model_url])

                # Clear cache
                pip.main(['cache', 'purge'])
            else:
                self.err_msg = err_msg
        except Exception: # pylint: disable=broad-exception-caught
            self.err_msg = traceback.format_exc()

        self.progress_updated.emit(self.tr('Download completed successfully.'))
        self.worker_done.emit(self.err_msg)

def init_spacy_models(main, lang, sentencizer_only = False):
    if lang == 'nno':
        lang = 'nob'
    else:
        lang = wl_conversion.remove_lang_code_suffixes(main, lang)

    # Languages with models
    if lang in SPACY_LANGS:
        # Sentencizer only
        if sentencizer_only and f'spacy_nlp_{lang}_sentencizer' not in main.__dict__:
            if lang == 'other':
                main.__dict__[f'spacy_nlp_{lang}_sentencizer'] = spacy.blank('en')
            else:
                main.__dict__[f'spacy_nlp_{lang}_sentencizer'] = spacy.blank(wl_conversion.to_iso_639_1(main, lang))

            main.__dict__[f'spacy_nlp_{lang}_sentencizer'].add_pipe('sentencizer')
        elif not sentencizer_only and f'spacy_nlp_{lang}' not in main.__dict__:
            model_name = SPACY_LANGS[lang]
            model = importlib.import_module(model_name)

            # Exclude NER to boost speed
            main.__dict__[f'spacy_nlp_{lang}'] = model.load(exclude = ['ner'])

            # Transformer-based models do not have sentence recognizer
            if not model_name.endswith('_trf'):
                main.__dict__[f'spacy_nlp_{lang}'].enable_pipe('senter')

            if lang == 'other':
                main.__dict__[f'spacy_nlp_{lang}'].add_pipe('sentencizer')
    # Languages without models
    elif lang not in SPACY_LANGS and f'spacy_nlp_{lang}' not in main.__dict__:
        main.__dict__[f'spacy_nlp_{lang}'] = spacy.blank(wl_conversion.to_iso_639_1(main, lang))

        # Add sentencizer and lemmatizer
        main.__dict__[f'spacy_nlp_{lang}'].add_pipe('sentencizer')

        if lang in SPACY_LANGS_LEMMATIZERS:
            main.__dict__[f'spacy_nlp_{lang}'].add_pipe('lemmatizer')
            main.__dict__[f'spacy_nlp_{lang}'].initialize()

def init_sudachipy_word_tokenizer(main):
    if 'sudachipy_word_tokenizer' not in main.__dict__:
        main.sudachipy_word_tokenizer = sudachipy.Dictionary().create()

def init_sentence_tokenizers(main, lang, sentence_tokenizer):
    # spaCy
    if sentence_tokenizer.startswith('spacy_'):
        if sentence_tokenizer == 'spacy_sentencizer':
            init_spacy_models(main, lang, sentencizer_only = True)
        else:
            init_spacy_models(main, lang)

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
        init_spacy_models(main, lang)
    # Chinese
    elif word_tokenizer == 'pkuseg_zho':
        if 'pkuseg_word_tokenizer' not in main.__dict__:
            main.pkuseg_word_tokenizer = spacy_pkuseg.pkuseg(model_name = 'mixed')
    # Chinese & Japanese
    elif word_tokenizer.startswith('wordless_'):
        init_spacy_models(main, 'eng_us')
        init_spacy_models(main, 'other')
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

def init_pos_taggers(main, lang, pos_tagger):
    # spaCy
    if pos_tagger.startswith('spacy_'):
        init_spacy_models(main, lang)
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

def init_lemmatizers(main, lang, lemmatizer):
    # spaCy
    if lemmatizer.startswith('spacy_'):
        init_spacy_models(main, lang)
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

def init_dependency_parsers(main, lang, dependency_parser):
    # spaCy
    if dependency_parser.startswith('spacy_'):
        init_spacy_models(main, lang)

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
        texts = to_sections_unequal(inputs, section_size = section_size * 50)

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
def escape_text(text):
    return html.escape(text).strip()

def escape_tokens(tokens):
    return [html.escape(token).strip() for token in tokens]

def html_to_text(text):
    # Remove tags and unescape character entities
    text = bs4.BeautifulSoup(text, features = 'lxml').get_text()
    text = text.replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)

    return text.strip()
