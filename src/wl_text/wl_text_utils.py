#
# Wordless: Text - Text Utilities
#
# Copyright (C) 2018-2022  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import html
import importlib
import re

import botok
import bs4
import nltk
import nltk.tokenize.nist
import pkuseg
import pymorphy2
import pyphen
import sacremoses
import spacy
import sudachipy

from wl_text import wl_text
from wl_utils import wl_conversion

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

def to_lang_util_code(main, util_type, util_text):
    return main.settings_global['lang_util_mappings'][util_type][util_text]

def to_lang_util_codes(main, util_type, util_texts):
    return (main.settings_global['lang_util_mappings'][util_type][util_text] for util_text in util_texts)

def _to_lang_util_text(main, util_type, util_code):
    for text, code in main.settings_global['lang_util_mappings'][util_type].items():
        if code == util_code:
            return text

def to_lang_util_text(main, util_type, util_code):
    return _to_lang_util_text(main, util_type, util_code)

def to_lang_util_texts(main, util_type, util_codes):
    return (_to_lang_util_text(main, util_type, util_code) for util_code in util_codes)

def init_spacy_models(main, lang):
    SPACY_LANGS = {
        'cat': 'ca_core_news_sm',
        'zho': 'zh_core_web_sm',
        'dan': 'da_core_news_sm',
        'nld': 'nl_core_news_sm',
        'eng': 'en_core_web_sm',
        'fra': 'fr_core_news_sm',
        'deu': 'de_core_news_sm',
        'ell': 'el_core_news_sm',
        'ita': 'it_core_news_sm',
        'jpn': 'ja_core_news_sm',
        'lit': 'lt_core_news_sm',
        'mkd': 'mk_core_news_sm',
        'nob': 'nb_core_news_sm',
        'pol': 'pl_core_news_sm',
        'por': 'pt_core_news_sm',
        'ron': 'ro_core_news_sm',
        'rus': 'ru_core_news_sm',
        'spa': 'es_core_news_sm',
        
        'other': 'en_core_web_sm'
    }
    SPACY_LANGS_LEMMATIZERS = ['ben', 'cat', 'hrv', 'ces', 'grc', 'hun', 'ind', 'gle', 'ltz', 'fas', 'srp_cyrl', 'swe', 'tgl', 'tur', 'urd']

    # Chinese, English, German, Portuguese
    if not lang.startswith('srp_'):
        lang = wl_conversion.remove_lang_code_suffixes(main, lang)

    if f'spacy_nlp_{lang}' not in main.__dict__:
        # Languages with models
        if lang in SPACY_LANGS:
            model = importlib.import_module(SPACY_LANGS[lang])

            main.__dict__[f'spacy_nlp_{lang}'] = model.load(disable = ['parser', 'ner'])
            # Add senter
            main.__dict__[f'spacy_nlp_{lang}'].enable_pipe('senter')
        # Languages without models
        else:
            # Serbian
            if lang == 'srp_cyrl':
                main.__dict__['spacy_nlp_srp_cyrl'] = spacy.blank('sr')
            elif lang == 'srp_latn':
                main.__dict__['spacy_nlp_srp_latn'] = spacy.blank('sr')
            else:
                main.__dict__[f'spacy_nlp_{lang}'] = spacy.blank(wl_conversion.to_iso_639_1(main, lang))

            # Add sentencizer and lemmatizer
            main.__dict__[f'spacy_nlp_{lang}'].add_pipe('sentencizer')

            if lang in SPACY_LANGS_LEMMATIZERS:
                main.__dict__[f'spacy_nlp_{lang}'].add_pipe('lemmatizer')

                main.__dict__[f'spacy_nlp_{lang}'].initialize()

        # Increase 'nlp.max_length' to avoid out of memory error (Default: 1,000,000)
        main.__dict__[f'spacy_nlp_{lang}'].max_length = 1000 ** 3
    
def init_sentence_tokenizers(main, lang, sentence_tokenizer):
    # spaCy
    if sentence_tokenizer.startswith('spacy_'):
        init_spacy_models(main, lang)

def init_word_tokenizers(main, lang, word_tokenizer = 'default'):
    if lang not in main.settings_global['word_tokenizers']:
        lang = 'other'

    if word_tokenizer == 'default':
        word_tokenizer = main.settings_custom['word_tokenization']['word_tokenizers'][lang]
    
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
            main.pkuseg_word_tokenizer = pkuseg.pkuseg()
    # Chinese & Japanese
    elif word_tokenizer.startswith('wordless_'):
        init_spacy_models(main, 'eng_us')
        init_spacy_models(main, 'other')
    # Japanese
    elif word_tokenizer.startswith('sudachipy_jpn'):
        if 'sudachipy_word_tokenizer' not in main.__dict__:
            main.sudachipy_word_tokenizer = sudachipy.Dictionary().create()
    # Tibetan
    elif word_tokenizer == 'botok_bod':
        if 'botok_word_tokenizer' not in main.__dict__:
            main.botok_word_tokenizer = botok.WordTokenizer()

def init_syl_tokenizers(main, lang, syl_tokenizer):
    # Pyphen
    if syl_tokenizer.startswith('pyphen_'):
        if f'pyphen_syl_tokenizer_{lang}' not in main.__dict__:
            lang_pyphen = wl_conversion.to_iso_639_1(main, lang)

            if lang.find('_') > -1:
                lang_pyphen = f"{lang_pyphen.split('_')[0]}_{lang_pyphen.split('_')[1].upper()}"
            else:
                lang_pyphen = wl_conversion.to_iso_639_1(main, lang)
            
            main.__dict__[f'pyphen_syl_tokenizer_{lang}'] = pyphen.Pyphen(lang = lang_pyphen)

def init_word_detokenizers(main, lang, word_detokenizer):
    # NLTK
    if word_detokenizer == 'nltk_penn_treebank':
        if 'nltk_treebank_detokenizer' not in main.__dict__:
            main.nltk_treebank_detokenizer = nltk.tokenize.treebank.TreebankWordDetokenizer()
    # Sacremoses
    elif word_detokenizer == 'sacremoses_moses':
        if f'sacremoses_moses_detokenizer_{lang}' not in main.__dict__:
            lang_sacremoses = wl_conversion.remove_lang_code_suffixes(main, wl_conversion.to_iso_639_1(main, lang))
            lang = wl_conversion.remove_lang_code_suffixes(main, lang)

            main.__dict__[f'sacremoses_moses_detokenizer_{lang}'] = sacremoses.MosesDetokenizer(lang = lang_sacremoses)

def init_pos_taggers(main, lang, pos_tagger):
    # spaCy
    if pos_tagger.startswith('spacy_'):
        init_spacy_models(main, lang)
    # Russian & Ukrainian
    elif pos_tagger == 'pymorphy2_morphological_analyzer':
        if lang == 'rus':
            if 'pymorphy2_morphological_analyzer_rus' not in main.__dict__:
                main.pymorphy2_morphological_analyzer_rus = pymorphy2.MorphAnalyzer(lang = 'ru')
        elif lang == 'ukr':
            if 'pymorphy2_morphological_analyzer_urk' not in main.__dict__:
                main.pymorphy2_morphological_analyzer_ukr = pymorphy2.MorphAnalyzer(lang = 'uk')
    # Japanese
    elif pos_tagger == 'sudachipy_jpn':
        if 'sudachipy_word_tokenizer' not in main.__dict__:
            main.sudachipy_word_tokenizer = sudachipy.Dictionary().create()

def init_lemmatizers(main, lang, lemmatizer):
    # spaCy
    if lemmatizer.startswith('spacy_'):
        init_spacy_models(main, lang)
    # Russian & Ukrainian
    elif lemmatizer == 'pymorphy2_morphological_analyzer':
        if lang == 'rus':
            if 'pymorphy2_morphological_analyzer_rus' not in main.__dict__:
                main.pymorphy2_morphological_analyzer_rus = pymorphy2.MorphAnalyzer(lang = 'ru')
        elif lang == 'ukr':
            if 'pymorphy2_morphological_analyzer_ukr' not in main.__dict__:
                main.pymorphy2_morphological_analyzer_ukr = pymorphy2.MorphAnalyzer(lang = 'uk')
    # Japanese
    elif lemmatizer == 'sudachipy_jpn':
        if 'sudachipy_word_tokenizer' not in main.__dict__:
            main.sudachipy_word_tokenizer = sudachipy.Dictionary().create()

def record_boundary_sentences(sentences, text):
    sentence_start = 0

    text = re.sub(r'\n+', ' ', text)
    sentences = [re.sub(r'\n+', ' ', sentence) for sentence in sentences]

    for i, sentence in enumerate(sentences):
        boundary = re.search(r'^\s+', text[sentence_start + len(sentence):])

        if boundary == None:
            boundary = ''
        else:
            boundary = boundary.group()

        sentences[i] = wl_text.Wl_Token(sentences[i], boundary = boundary)

        sentence_start += len(sentence) + len(boundary)

    return sentences

def to_sections(tokens, num_sections):
    sections = []

    section_size, remainder = divmod(len(tokens), num_sections)

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

    return sections

def to_sections_unequal(tokens, section_size):
    tokens = list(tokens)
    
    for i in range(0, len(tokens), section_size):
        yield tokens[i : i + section_size]

# Serbian
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

# HTML
def text_escape(text):
    if type(text) == str:
        return html.escape(text).strip()
    elif type(text) in [list, tuple, dict]:
        return [html.escape(token).strip() for token in text]
    else:
        raise Exception('The input must be a string or a list of tokens!')

def html_to_text(text):
    # Remove tags and unescape character entities
    return bs4.BeautifulSoup(text, features = 'lxml').get_text().strip()
