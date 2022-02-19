# ----------------------------------------------------------------------
# Wordless: NLP - Sentence Tokenization
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

import botok
import nltk
import pythainlp
import tokenizer
import underthesea

from wl_nlp import wl_nlp_utils, wl_word_detokenization
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

    wl_nlp_utils.init_sentence_tokenizers(
        main,
        lang = lang,
        sentence_tokenizer = sentence_tokenizer
    )

    # NLTK
    if sentence_tokenizer == 'nltk_punkt':
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
    elif sentence_tokenizer.startswith('spacy_'):
        # Chinese, English, German, Portuguese
        if not lang.startswith('srp_'):
            lang = wl_conversion.remove_lang_code_suffixes(main, lang)

        nlp = main.__dict__[f'spacy_nlp_{lang}']
        doc = nlp(text)

        sentences = [sentence.text for sentence in doc.sents]
    # Chinese & Japanese
    elif sentence_tokenizer in ['wordless_zho', 'wordless_jpn']:
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
    elif sentence_tokenizer == 'tokenizer_isl':
        for sentence in tokenizer.split_into_sentences(text):
            sentences.append(wl_word_detokenization.wl_word_detokenize(
                main,
                tokens = sentence.split(),
                lang = 'isl')
            )
    # Thai
    elif sentence_tokenizer == 'pythainlp_crfcut':
        sentences = pythainlp.sent_tokenize(text)
    # Tibetan
    elif sentence_tokenizer == 'botok_bod':
        wl_nlp_utils.init_word_tokenizers(main, lang = 'bod')

        tokens = main.botok_word_tokenizer.tokenize(text)

        for sentence_tokens in botok.sentence_tokenizer(tokens):
            sentences.append(''.join([sentence_token.text
                                      for sentence_token in sentence_tokens['tokens']]))
    # Vietnamese
    elif sentence_tokenizer == 'underthesea_vie':
        sentences = underthesea.sent_tokenize(text)

    # Strip spaces
    sentences = [sentence.strip() for sentence in sentences]

    sentences = wl_nlp_utils.record_boundary_sentences(sentences, text)

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
