#
# Wordless: Text - Sentence Tokenization
#
# Copyright (C) 2018-2021  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import botok
import nltk
import pythainlp
import razdel
import syntok.segmenter
import tokenizer
import underthesea

from wl_text import wl_text, wl_text_utils, wl_word_detokenization
from wl_utils import wl_conversion

# Reference: https://stackoverflow.com/questions/9506869/are-there-character-collections-for-all-international-full-stop-punctuations/9508766#9508766
TERMINATORS_SENTENCE = [
    '!', '.', '?', '։', '؟', '۔', '܀', '܁', '܂', '߹',
    '।', '॥', '၊', '။', '።', '፧', '፨', '᙮', '᜵', '᜶', '᠃', '᠉', '᥄',
    '᥅', '᪨', '᪩', '᪪', '᪫', '᭚', '᭛', '᭞', '᭟', '᰻', '᰼', '᱾', '᱿',
    '‼', '‽', '⁇', '⁈', '⁉', '⸮', '⸼', '꓿', '꘎', '꘏', '꛳', '꛷', '꡶',
    '꡷', '꣎', '꣏', '꤯', '꧈', '꧉', '꩝', '꩞', '꩟', '꫰', '꫱', '꯫', '﹒',
    '﹖', '﹗', '！', '．', '？', '𐩖', '𐩗', '𑁇', '𑁈', '𑂾', '𑂿', '𑃀',
    '𑃁', '𑅁', '𑅂', '𑅃', '𑇅', '𑇆', '𑇍', '𑇞', '𑇟', '𑈸', '𑈹', '𑈻', '𑈼',
    '𑊩', '𑑋', '𑑌', '𑗂', '𑗃', '𑗉', '𑗊', '𑗋', '𑗌', '𑗍', '𑗎', '𑗏', '𑗐',
    '𑗑', '𑗒', '𑗓', '𑗔', '𑗕', '𑗖', '𑗗', '𑙁', '𑙂', '𑜼', '𑜽', '𑜾', '𑩂',
    '𑩃', '𑪛', '𑪜', '𑱁', '𑱂', '𖩮', '𖩯', '𖫵', '𖬷', '𖬸', '𖭄', '𛲟', '𝪈'
]

def wl_sentence_tokenize(main, text, lang, sentence_tokenizer = 'default'):
    sentences = []

    if lang not in main.settings_global['sentence_tokenizers']:
        lang = 'other'

    if sentence_tokenizer == 'default':
        sentence_tokenizer = main.settings_custom['sentence_tokenization']['sentence_tokenizers'][lang]

    wl_text_utils.init_sentence_tokenizers(
        main,
        lang = lang,
        sentence_tokenizer = sentence_tokenizer
    )

    # NLTK
    if sentence_tokenizer == main.tr('NLTK - Punkt Sentence Tokenizer'):
        lang_texts = {
            'ces': 'czech',
            'dan': 'danish',
            'nld': 'dutch',
            # English
            'eng_gb': 'english',
            'eng_us': 'english',
            'est': 'estonian',
            'fin': 'finnish',
            'fra': 'french',
            # German
            'deu_at': 'german',
            'deu_de': 'german',
            'deu_ch': 'german',
            'ell': 'greek',
            'ita': 'italian',
            # Norwegian
            'nob': 'norwegian',
            'nno': 'norwegian',
            'pol': 'polish',
            # Portuguese
            'por_br': 'portuguese',
            'por_pt': 'portuguese',
            'rus': 'russian',
            'slv': 'slovene',
            'spa': 'spanish',
            'swe': 'swedish',
            'tur': 'turkish',
            # Other languages
            'other': 'english'
        }

        sentences = nltk.sent_tokenize(text, language = lang_texts[lang])
    # spaCy
    elif 'spaCy' in sentence_tokenizer:
        # Chinese, English, German, Portuguese
        if lang.find('srp') == -1:
            lang = wl_conversion.remove_lang_code_suffixes(main, lang)
        
        nlp = main.__dict__[f'spacy_nlp_{lang}']
        doc = nlp(text)

        sentences = [sentence.text for sentence in doc.sents]
    # syntok
    elif sentence_tokenizer == main.tr('syntok - Sentence Segmenter'):
        for para in syntok.segmenter.analyze(text):
            for sentence in para:
                sentences.append(''.join([token.spacing + token.value for token in sentence]))
    # Chinese & Japanese
    elif sentence_tokenizer in [main.tr('Wordless - Chinese Sentence Tokenizer'),
                                main.tr('Wordless - Japanese Sentence Tokenizer')]:
        for line in text.splitlines():
            sentence_start = 0

            for i, char in enumerate(line):
                if i >= sentence_start and char in ['。', '！', '？', '!', '?']:
                    for j, char in enumerate(line):
                        if j > i and char not in ['。', '！', '？', '!', '?', '’', '”', '）', ')']:
                            sentences.append(line[sentence_start : j])

                            sentence_start = j

                            break

            if sentence_start <= len(line):
                sentences.append(line[sentence_start:])
    # Icelandic
    elif sentence_tokenizer == main.tr('Tokenizer - Icelandic Sentence Tokenizer'):
        for sentence in tokenizer.split_into_sentences(text):
            sentences.append(wl_word_detokenization.wl_word_detokenize(
                main,
                tokens = sentence.split(),
                lang = 'isl')
            )

    # Russian
    elif sentence_tokenizer == main.tr('razdel - Russian Sentenizer'):
        sentences = [sentence.text for sentence in razdel.sentenize(text)]
    # Thai
    elif sentence_tokenizer == main.tr('PyThaiNLP - CRFCut'):
        sentences = pythainlp.sent_tokenize(text)
    # Tibetan
    elif sentence_tokenizer == main.tr('botok - Tibetan Sentence Tokenizer'):
        wl_text_utils.init_word_tokenizers(main, lang = 'bod')
        
        tokens = main.botok_word_tokenizer.tokenize(text)

        for sentence_tokens in botok.sentence_tokenizer(tokens):
            sentences.append(''.join([sentence_token.text
                                      for sentence_token in sentence_tokens[1]]))
    # Vietnamese
    elif sentence_tokenizer == main.tr('Underthesea - Vietnamese Sentence Tokenizer'):
        sentences = underthesea.sent_tokenize(text)

    # Strip spaces
    sentences = [sentence.strip() for sentence in sentences]

    sentences = wl_text_utils.record_boundary_sentences(sentences, text)

    return sentences

def wl_sentence_split(main, text):
    sentences = []
    sentence_start = 0

    tokens = text.split()
    len_tokens = len(tokens)

    for i, token in enumerate(tokens):
        if token[-1] in TERMINATORS_SENTENCE or i == len_tokens - 1:
            sentences.append(' '.join(tokens[sentence_start : i + 1]))

            sentence_start = i + 1

    return sentences
