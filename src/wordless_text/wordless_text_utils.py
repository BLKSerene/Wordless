#
# Wordless: Text - Text Utilities
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import re

from wordless_text import wordless_text
from wordless_utils import wordless_conversion

import pybo
import spacy

def check_spacy_models(main, lang, pipeline):
    if pipeline == 'word_tokenization':
        nlp_pipelines = []
        nlp_disable = ['tagger', 'parser', 'ner']
    elif pipeline == 'sentence_tokenization':
        nlp_pipelines = ['sentencizer']
        nlp_disable = ['tagger', 'parser', 'ner']
    elif pipeline in ['pos_tagging', 'lemmatization']:
        nlp_pipelines = ['tagger']
        nlp_disable = ['parser', 'ner']

    # Languages with models
    if lang in ['nld', 'eng', 'fra', 'deu', 'ell', 'ita', 'por', 'spa', 'other']:
        if f'spacy_nlp_{lang}' in main.__dict__:
            if main.__dict__[f'spacy_nlp_{lang}'].pipe_names != nlp_pipelines:
                del main.__dict__[f'spacy_nlp_{lang}']

        if f'spacy_nlp_{lang}' not in main.__dict__:
            # Dutch
            if lang == 'nld':
                import nl_core_news_sm

                main.__dict__[f'spacy_nlp_{lang}'] = nl_core_news_sm.load(disable = nlp_disable)
            # English
            elif lang == 'eng':
                import en_core_web_sm

                main.__dict__[f'spacy_nlp_{lang}'] = en_core_web_sm.load(disable = nlp_disable)
            # French
            elif lang == 'fra':
                import fr_core_news_sm

                main.__dict__[f'spacy_nlp_{lang}'] = fr_core_news_sm.load(disable = nlp_disable)
            # German
            elif lang == 'deu':
                import de_core_news_sm

                main.__dict__[f'spacy_nlp_{lang}'] = de_core_news_sm.load(disable = nlp_disable)
            # Greek (Modern)
            elif lang == 'ell':
                import el_core_news_sm

                main.__dict__[f'spacy_nlp_{lang}'] = el_core_news_sm.load(disable = nlp_disable)
            # Italian
            elif lang == 'ita':
                import it_core_news_sm
                
                main.__dict__[f'spacy_nlp_{lang}'] = it_core_news_sm.load(disable = nlp_disable)
            # Portuguese
            elif lang == 'por':
                import pt_core_news_sm
                
                main.__dict__[f'spacy_nlp_{lang}'] = pt_core_news_sm.load(disable = nlp_disable)
            # Spanish
            elif lang == 'spa':
                import es_core_news_sm
                
                main.__dict__[f'spacy_nlp_{lang}'] = es_core_news_sm.load(disable = nlp_disable)
            # Other Languages
            elif lang == 'other':
                import en_core_web_sm
                
                main.__dict__[f'spacy_nlp_{lang}'] = en_core_web_sm.load(disable = nlp_disable)
    # Languages without models
    else:
        main.__dict__[f'spacy_nlp_{lang}'] = spacy.blank(wordless_conversion.to_iso_639_1(main, lang))

    if 'sentencizer' in nlp_pipelines:
        nlp = main.__dict__[f'spacy_nlp_{lang}']

        if 'sentencizer' not in nlp.pipe_names:
            nlp.add_pipe(nlp.create_pipe('sentencizer'))

def check_pybo_tokenizers(main, word_tokenizer):
    if 'GMD' in word_tokenizer and 'pybo_tokenizer_gmd' not in main.__dict__:
        main.pybo_tokenizer_gmd = pybo.WordTokenizer('GMD')
    elif 'POS' in word_tokenizer and 'pybo_tokenizer_pos' not in main.__dict__:
        main.pybo_tokenizer_pos = pybo.WordTokenizer('POS')
    elif 'tsikchen' in word_tokenizer and 'pybo_tokenizer_tsikchen' not in main.__dict__:
        main.pybo_tokenizer_tsikchen = pybo.WordTokenizer('tsikchen')

def check_sentence_tokenizers(main, lang, sentence_tokenizer = 'default'):
    if lang not in main.settings_global['sentence_tokenizers']:
        lang = 'other'

    if sentence_tokenizer == 'default':
        word_tokenizer = main.settings_custom['sentence_tokenization']['sentence_tokenizers'][lang]

    if 'spaCy' in sentence_tokenizer:
        check_spacy_models(main, lang, pipeline = 'sentence_tokenization')

def check_word_tokenizers(main, lang, word_tokenizer = 'default'):
    if lang not in main.settings_global['word_tokenizers']:
        lang = 'other'

    if word_tokenizer == 'default':
        word_tokenizer = main.settings_custom['word_tokenization']['word_tokenizers'][lang]

    if 'spaCy' in word_tokenizer:
        check_spacy_models(main, lang, pipeline = 'word_tokenization')
    # Tibetan
    elif 'pybo' in word_tokenizer:
        check_pybo_tokenizers(main, word_tokenizer = word_tokenizer)
    # Chinese & Japanese
    elif 'Wordless' in word_tokenizer:
        check_spacy_models(main, 'eng', pipeline = 'word_tokenization')
        check_spacy_models(main, 'other', pipeline = 'word_tokenization')

def check_pos_taggers(main, lang, pos_tagger = 'default'):
    if pos_tagger == 'default':
        pos_tagger = main.settings_custom['pos_tagging']['pos_taggers'][lang]

    if 'spaCy' in pos_tagger:
        check_spacy_models(main, lang, pipeline = 'pos_tagging')

    # Chinese & Japanese
    if lang in ['zho_cn', 'zho_tw', 'jpn']:
        check_spacy_models(main, 'eng', pipeline = 'pos_tagging')
        check_spacy_models(main, 'other', pipeline = 'pos_tagging')

def check_lemmatizers(main, lang, lemmatizer = 'default'):
    if lang in main.settings_global['lemmatizers']:
        if lemmatizer == 'default':
            lemmatizer = main.settings_custom['lemmatization']['lemmatizers'][lang]

        if 'spaCy' in lemmatizer:
            check_spacy_models(main, lang, pipeline = 'lemmatization')

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

        sentences[i] = wordless_text.Wordless_Token(sentences[i], boundary = boundary)

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
