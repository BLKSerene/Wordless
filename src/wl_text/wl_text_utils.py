#
# Wordless: Text - Text Utilities
#
# Copyright (C) 2018-2021  Ye Lei (叶磊)
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
import sacremoses
import spacy

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

def init_spacy_models(main, lang):
    spacy_langs = {
        'cat': 'ca_core_news_sm',
        'zho': 'zh_core_web_sm',
        'dan': 'da_core_news_sm',
        'nld': 'nl_core_news_sm',
        'eng': 'en_core_web_sm',
        'fra': 'fr_core_news_sm',
        'deu': 'de_core_news_sm',
        'ell': 'el_core_news_sm',
        'ita': 'it_core_news_sm',
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
    spacy_langs_lemmatizers = ['ben', 'cat', 'hrv', 'ces', 'hun', 'ind', 'ltz', 'fas', 'srp_cyrl', 'swe', 'tgl', 'tur', 'urd']

    # Chinese
    if lang in ['zho_cn', 'zho_tw']:
        lang = 'zho'

    if f'spacy_nlp_{lang}' not in main.__dict__:
        # Languages with models
        if lang in spacy_langs:
            model = importlib.import_module(spacy_langs[lang])

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

            if lang in spacy_langs_lemmatizers:
                main.__dict__[f'spacy_nlp_{lang}'].add_pipe('lemmatizer')

                main.__dict__[f'spacy_nlp_{lang}'].initialize()
    
def init_sentence_tokenizers(main, lang, sentence_tokenizer = 'default'):
    if lang not in main.settings_global['sentence_tokenizers']:
        lang = 'other'

    if sentence_tokenizer == 'default':
        word_tokenizer = main.settings_custom['sentence_tokenization']['sentence_tokenizers'][lang]

    # spaCy
    if 'spaCy' in sentence_tokenizer:
        init_spacy_models(main, lang)

def init_word_tokenizers(main, lang, word_tokenizer = 'default'):
    if lang not in main.settings_global['word_tokenizers']:
        lang = 'other'

    if word_tokenizer == 'default':
        word_tokenizer = main.settings_custom['word_tokenization']['word_tokenizers'][lang]

    # NLTK
    if 'NLTK' in word_tokenizer:
        if word_tokenizer == main.tr('NLTK - NIST Tokenizer'):
            if 'nltk_nist_tokenizer' not in main.__dict__:
                main.nltk_nist_tokenizer = nltk.tokenize.nist.NISTTokenizer()
        elif word_tokenizer == main.tr('NLTK - NLTK Tokenizer'):
            if 'nltk_nltk_tokenizer' not in main.__dict__:
                main.nltk_nltk_tokenizer = nltk.NLTKWordTokenizer()
        elif word_tokenizer == main.tr('NLTK - Penn Treebank Tokenizer'):
            if 'nltk_treebank_tokenizer' not in main.__dict__:
                main.nltk_treebank_tokenizer = nltk.TreebankWordTokenizer()
        elif word_tokenizer == main.tr('NLTK - Tok-tok Tokenizer'):
            if 'nltk_toktok_tokenizer' not in main.__dict__:
                main.nltk_toktok_tokenizer = nltk.ToktokTokenizer()
        elif word_tokenizer == main.tr('NLTK - Twitter Tokenizer'):
            if 'nltk_tweet_tokenizer' not in main.__dict__:
                main.nltk_tweet_tokenizer = nltk.TweetTokenizer()
    # Sacremoses
    elif 'Sacremoses' in word_tokenizer:
        if f'sacremoses_moses_tokenizer_{lang}' not in main.__dict__:
            main.__dict__[f'sacremoses_moses_tokenizer_{lang}'] = sacremoses.MosesTokenizer(lang = wl_conversion.to_iso_639_1(main, lang))
    # spaCy
    elif 'spaCy' in word_tokenizer:
        init_spacy_models(main, lang)
    # Chinese
    elif word_tokenizer == main.tr('pkuseg - Chinese Word Tokenizer'):
        if 'pkuseg_word_tokenizer' not in main.__dict__:
            main.pkuseg_word_tokenizer = pkuseg.pkuseg()
    # Chinese & Japanese
    elif 'Wordless' in word_tokenizer:
        init_spacy_models(main, 'eng')
        init_spacy_models(main, 'other')
    # Tibetan
    elif 'botok' in word_tokenizer:
        if 'botok_word_tokenizer' not in main.__dict__:
            main.botok_word_tokenizer = botok.WordTokenizer()

def init_word_detokenizers(main, lang, word_detokenizer = 'default'):
    if lang not in main.settings_global['word_detokenizers']:
        lang = 'other'

    if word_detokenizer == 'default':
        word_detokenizer = main.settings_custom['word_detokenization']['word_detokenizers'][lang]

    # English & Other Languages
    if word_detokenizer == main.tr('NLTK - Penn Treebank Detokenizer'):
        if 'nltk_treebank_detokenizer' not in main.__dict__:
            main.nltk_treebank_detokenizer = nltk.tokenize.treebank.TreebankWordDetokenizer()
    elif word_detokenizer == main.tr('Sacremoses - Moses Detokenizer'):
        if f'sacremoses_moses_detokenizer_{lang}' not in main.__dict__:
            main.__dict__[f'sacremoses_moses_detokenizer_{lang}'] = sacremoses.MosesDetokenizer(lang = wl_conversion.to_iso_639_1(main, lang))

def init_pos_taggers(main, lang, pos_tagger = 'default'):
    if pos_tagger == 'default':
        pos_tagger = main.settings_custom['pos_tagging']['pos_taggers'][lang]

    # spaCy
    if 'spaCy' in pos_tagger:
        init_spacy_models(main, lang)
    # Russian & Ukrainian
    elif pos_tagger == main.tr('pymorphy2 - Morphological Analyzer'):
        if lang == 'rus':
            if 'pymorphy2_morphological_analyzer_rus' not in main.__dict__:
                main.pymorphy2_morphological_analyzer_rus = pymorphy2.MorphAnalyzer(lang = 'ru')
        elif lang == 'ukr':
            if 'pymorphy2_morphological_analyzer_urk' not in main.__dict__:
                main.pymorphy2_morphological_analyzer_ukr = pymorphy2.MorphAnalyzer(lang = 'uk')
    # Chinese & Japanese
    elif lang in ['zho_cn', 'zho_tw', 'jpn']:
        init_spacy_models(main, 'eng')
        init_spacy_models(main, 'other')

def init_lemmatizers(main, lang, lemmatizer = 'default'):
    if lang in main.settings_global['lemmatizers']:
        if lemmatizer == 'default':
            lemmatizer = main.settings_custom['lemmatization']['lemmatizers'][lang]
    
    # spaCy
    if 'spaCy' in lemmatizer:
        init_spacy_models(main, lang)
    # Russian & Ukrainian
    elif lemmatizer == main.tr('pymorphy2 - Morphological Analyzer'):
        if lang == 'rus':
            if 'pymorphy2_morphological_analyzer_rus' not in main.__dict__:
                main.pymorphy2_morphological_analyzer_rus = pymorphy2.MorphAnalyzer(lang = 'ru')
        elif lang == 'ukr':
            if 'pymorphy2_morphological_analyzer_ukr' not in main.__dict__:
                main.pymorphy2_morphological_analyzer_ukr = pymorphy2.MorphAnalyzer(lang = 'uk')

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
    sections = []

    for i in range(len(tokens)):
        if (i + 1) % section_size == 0:
            sections.append(tokens[i + 1 - section_size : i + 1])

    if len(tokens) % section_size > 0:
        sections.append(tokens[section_size * len(sections):])

    return sections

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
