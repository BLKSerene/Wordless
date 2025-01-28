# ----------------------------------------------------------------------
# Wordless: Measures - Readability
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

import bisect
import copy
import math
import random
import re

import numpy
from PyQt5.QtCore import QCoreApplication

from wordless.wl_checks import wl_checks_tokens
from wordless.wl_nlp import (
    wl_lemmatization,
    wl_pos_tagging,
    wl_sentence_tokenization,
    wl_syl_tokenization,
    wl_texts
)
from wordless.wl_utils import wl_misc, wl_paths

_tr = QCoreApplication.translate

def get_nums(main, text):
    # Number of sentences
    if 'num_sentences' not in text.__dict__:
        text.words_multilevel = []

        for para in text.tokens_multilevel:
            text.words_multilevel.append([])

            for sentence in para:
                text.words_multilevel[-1].append([])

                for sentence_seg in sentence:
                    text.words_multilevel[-1][-1].append(copy.deepcopy([
                        token
                        for token in sentence_seg
                        if wl_checks_tokens.is_word_alphanumeric(token)
                    ]))

        text.sentences = [
            list(wl_misc.flatten_list(sentence))
            for para in text.words_multilevel
            for sentence in para
        ]
        text.num_sentences = len(text.sentences)

    # Number of words with at least one letter or numeral
    if 'num_words' not in text.__dict__:
        text.words_flat = list(wl_misc.flatten_list(text.words_multilevel))
        text.num_words = len(text.words_flat)
        text.num_word_types = len(set(text.words_flat))

    # Number of syllables
    if 'num_syls' not in text.__dict__ and text.lang in main.settings_global['syl_tokenizers']:
        wl_syl_tokenization.wl_syl_tokenize(main, text.words_flat, lang = text.lang)
        text.num_syls = sum((len(word.syls) for word in text.words_flat))

    # Number of characters
    if 'num_chars_all' not in text.__dict__:
        text.num_chars_all = 0
        text.num_chars_alnum = 0
        text.num_chars_alpha = 0

        for token in text.words_flat:
            for char in token:
                text.num_chars_all += 1

                if char.isalpha():
                    text.num_chars_alnum += 1
                    text.num_chars_alpha += 1
                elif char.isalnum():
                    text.num_chars_alnum += 1

    return text

def get_num_words_ltrs(words, len_min = 1, len_max = None):
    if len_max:
        return len([
            True
            for word in words
            if len_min <= len([char for char in word if char.isalpha()]) <= len_max
        ])
    else:
        return len([
            True
            for word in words
            if len([char for char in word if char.isalpha()]) >= len_min
        ])

def get_num_words_syls(words, len_min = 1, len_max = None):
    if len_max:
        return sum((
            1
            for word in words
            if len_min <= len(word.syls) <= len_max
        ))
    else:
        return sum((
            1
            for word in words
            if len(word.syls) >= len_min
        ))

def pos_tag_words(main, text):
    text.words_flat = wl_pos_tagging.wl_pos_tag_universal(main, text.words_flat, lang = text.lang, tagged = text.tagged)

def get_num_words_pos_tag(words, pos_tag):
    return sum((1 for word in words if pos_tag in word.tag_universal.split('/')))

def get_nums_words_pos_tags(words, pos_tags):
    return [
        get_num_words_pos_tag(words, pos_tag)
        for pos_tag in pos_tags
    ]

def get_num_words_outside_list(words, wordlist, use_word_types = False):
    words_inside_wordlist = set()
    num_words_outside_wordlist = 0

    # Load wordlist
    if wordlist == 'bamberger_vanecek':
        file_name = 'bamberger_vanecek_most_common_words_1000'
    elif wordlist == 'dale_769':
        file_name = 'dale_list_easy_words_769'
    elif wordlist == 'dale_3000':
        file_name = 'dale_list_easy_words_3000'
    elif wordlist == 'luong_nguyen_dinh':
        file_name = 'luong_nguyen_dinh_freq_syls_easy_1000'
    elif wordlist == 'spache':
        file_name = 'spache_word_list'

    with open(wl_paths.get_path_data(f'{file_name}.txt'), 'r', encoding = 'utf_8') as f:
        for line in f:
            word = line.strip()

            if word:
                # Ignore case
                words_inside_wordlist.add(word.lower())

    if use_word_types:
        words = set(words)
        words_inside_wordlist = set(words_inside_wordlist)

    for word in words:
        if word.lower() not in words_inside_wordlist:
            num_words_outside_wordlist += 1

    return num_words_outside_wordlist

def get_num_sentences_sample(text, sample, sample_start):
    # Calculate sentence offsets using words (punctuation marks already excluded)
    if 'offsets_sentences_words' not in text.__dict__:
        text.offsets_sentences_words = []
        num_tokens = 0

        for sentence in text.sentences:
            text.offsets_sentences_words.append(num_tokens)

            num_tokens += len(sentence)

    return (
        bisect.bisect(text.offsets_sentences_words, sample_start + len(sample))
        - bisect.bisect(text.offsets_sentences_words, sample_start)
        + 1
    )

# Al-Heeti's readability formula
# Reference: Al-Heeti, K. N. (1984). Judgment analysis technique applied to readability prediction of Arabic reading material (Publication No. 8411458) [Doctoral dissertation, University of Northern Colorado]. ProQuest Dissertations and Theses Global. | pp. 102, 104, 106
def rd(main, text):
    if text.lang == 'ara':
        text = get_nums(main, text)

        if text.num_words and text.num_sentences and text.num_word_types:
            variant = main.settings_custom['measures']['readability']['rd']['variant']

            if variant == _tr('wl_measures_readability', 'Policy One'):

                rd = (
                    4.41434307 * (text.num_chars_alpha / text.num_words)
                    - 13.46873475
                )
            elif variant == _tr('wl_measures_readability', 'Policy Two'):
                rd = (
                    0.97569509 * (text.num_chars_alpha / text.num_words)
                    + 0.37237998 * (text.num_words / text.num_sentences)
                    - 0.90451827 * (text.num_words / text.num_word_types)
                    - 1.06000414
                )
        else:
            rd = 'text_too_short'
    else:
        rd = 'no_support'

    return rd

# Automated Arabic Readability Index
# Reference: Al-Tamimi, A., Jaradat M., Aljarrah, N., & Ghanim, S. (2013). AARI: Automatic Arabic readability index. The International Arab Journal of Information Technology, 11(4), 370–378.
def aari(main, text):
    if text.lang == 'ara':
        text = get_nums(main, text)

        if text.num_words and text.num_sentences:
            aari = (
                3.28 * text.num_chars_alnum
                + 1.43 * (text.num_chars_alnum / text.num_words)
                + 1.24 * (text.num_words / text.num_sentences)
            )
        else:
            aari = 'text_too_short'
    else:
        aari = 'no_support'

    return aari

# Automated Readability Index
# References:
#     Smith, E. A., & Senter, R. J. (1967). Automated readability index. Aerospace Medical Research Laboratories. https://apps.dtic.mil/sti/pdfs/AD0667273.pdf | p. 8
# Navy:
#     Kincaid, J. P., Fishburne, R. P., Rogers, R. L., & Chissom, B. S. (1975). Derivation of new readability formulas (automated readability index, fog count, and Flesch reading ease formula) for Navy enlisted personnel (Report No. RBR 8-75). Naval Air Station Memphis. https://apps.dtic.mil/sti/pdfs/ADA006655.pdf | p. 14
def ari(main, text):
    text = get_nums(main, text)

    if text.num_sentences and text.num_words:
        if main.settings_custom['measures']['readability']['ari']['use_navy_variant']:
            ari = (
                0.37 * (text.num_words / text.num_sentences)
                + 5.84 * (text.num_chars_all / text.num_words)
                - 26.01
            )
        else:
            ari = (
                0.5 * (text.num_words / text.num_sentences)
                + 4.71 * (text.num_chars_all / text.num_words)
                - 21.43
            )
    else:
        ari = 'text_too_short'

    return ari

# Bormuth's cloze mean & grade placement
# Reference: Bormuth, J. R. (1969). Development of readability analyses. U.S. Department of Health, Education, and Welfare. http://files.eric.ed.gov/fulltext/ED029166.pdf | pp. 152, 160
def bormuths_cloze_mean(main, text):
    if text.lang.startswith('eng_'):
        text = get_nums(main, text)

        if text.num_sentences and text.num_words:
            ddl = get_num_words_outside_list(text.words_flat, wordlist = 'dale_3000')
            m = (
                0.886593
                - 0.083640 * (text.num_chars_alpha / text.num_words)
                + 0.161911 * ((ddl / text.num_words)**3)
                - 0.021401 * (text.num_words / text.num_sentences)
                + 0.000577 * ((text.num_words / text.num_sentences)**2)
                - 0.000005 * ((text.num_words / text.num_sentences)**3)
            )
        else:
            m = 'text_too_short'
    else:
        m = 'no_support'

    return m

def bormuths_gp(main, text):
    m = bormuths_cloze_mean(main, text)

    if m not in ['no_support', 'text_too_short']:
        c = main.settings_custom['measures']['readability']['bormuths_gp']['cloze_criterion_score'] / 100
        gp = (
            4.275 + 12.881 * m - 34.934 * (m**2) + 20.388 * (m**3)
            + 26.194 * c - 2.046 * (c**2) - 11.767 * (c**3)
            - 44.285 * (m * c) + 97.620 * ((m * c)**2) - 59.538 * ((m * c)**3)
        )
    else:
        gp = m

    return gp

# Coleman-Liau index
# Reference: Coleman, M., & Liau, T. L. (1975). A computer readability formula designed for machine scoring. Journal of Applied Psychology, 60(2), 283–284. https://doi.org/10.1037/h0076540
def coleman_liau_index(main, text):
    text = get_nums(main, text)

    if text.num_words:
        est_cloze_pct = (
            141.8401
            - 0.21459 * (text.num_chars_alpha / text.num_words * 100)
            + 1.079812 * (text.num_sentences / text.num_words * 100)
        )
        grade_level = -27.4004 * (est_cloze_pct / 100) + 23.06395
    else:
        grade_level = 'text_too_short'

    return grade_level

# Coleman's readability formula
# Reference: Liau, T. L., Bassin, C. B., Martin, C. J., & Coleman, E. B. (1976). Modification of the Coleman readability formulas. Journal of Reading Behavior, 8(4), 381–386. https://journals.sagepub.com/doi/pdf/10.1080/10862967609547193
def colemans_readability_formula(main, text):
    variant = main.settings_custom['measures']['readability']['colemans_readability_formula']['variant']

    if (
        text.lang in main.settings_global['syl_tokenizers']
        and (
            variant in ['1', '2']
            or (variant in ['3', '4'] and text.lang in main.settings_global['pos_taggers'])
        )
    ):
        text = get_nums(main, text)

        if text.num_words:
            num_words_1_syl = get_num_words_syls(text.words_flat, len_min = 1, len_max = 1)

            match variant:
                case '1':
                    cloze_pct = (
                        1.29 * (num_words_1_syl / text.num_words * 100)
                        - 38.45
                    )
                case '2':
                    cloze_pct = (
                        1.16 * (num_words_1_syl / text.num_words * 100)
                        + 1.48 * (text.num_sentences / text.num_words * 100)
                        - 37.95
                    )
                case '3':
                    pos_tag_words(main, text)
                    num_prons = get_num_words_pos_tag(
                        words = text.words_flat,
                        pos_tag = 'PRON'
                    )

                    cloze_pct = (
                        1.07 * (num_words_1_syl / text.num_words * 100)
                        + 1.18 * (text.num_sentences / text.num_words * 100)
                        + 0.76 * (num_prons / text.num_words * 100)
                        - 34.02
                    )
                case '4':
                    pos_tag_words(main, text)
                    num_prons, num_preps = get_nums_words_pos_tags(
                        words = text.words_flat,
                        pos_tags = ['PRON', 'ADP']
                    )

                    cloze_pct = (
                        1.04 * (num_words_1_syl / text.num_words * 100)
                        + 1.06 * (text.num_sentences / text.num_words * 100)
                        + 0.56 * (num_prons / text.num_words * 100)
                        - 0.36 * (num_preps / text.num_words)
                        - 26.01
                    )
        else:
            cloze_pct = 'text_too_short'
    else:
        cloze_pct = 'no_support'

    return cloze_pct

# Crawford's readability formula
# Reference: Crawford, A. N. (1985). Fórmula y gráfico para determinar la comprensibilidad de textos de nivel primario en castellano. Lectura y Vida, 6(4). http://www.lecturayvida.fahce.unlp.edu.ar/numeros/a6n4/06_04_Crawford.pdf
def crawfords_readability_formula(main, text):
    if text.lang == 'spa' and text.lang in main.settings_global['syl_tokenizers']:
        text = get_nums(main, text)

        if text.num_words:
            grade_level = (
                text.num_sentences / text.num_words * 100 * (-0.205)
                + text.num_syls / text.num_words * 100 * 0.049
                - 3.407
            )
        else:
            grade_level = 'text_too_short'
    else:
        grade_level = 'no_support'

    return grade_level

# Dale-Chall readability formula
# References:
#     Dale, E., & Chall, J. S. (1948a). A formula for predicting readability. Educational Research Bulletin, 27(1), 11–20, 28.
#     Dale, E., & Chall, J. S. (1948b). A formula for predicting readability: Instructions. Educational Research Bulletin, 27(2), 37–54.
# Powers-Sumner-Kearl:
#     Powers, R. D., Sumner, W. A., & Kearl, B. E. (1958). A recalculation of four adult readability formulas. Journal of Educational Psychology, 49(2), 99–105. https://doi.org/10.1037/h0043254
# New:
#     Chall, J. S., & Dale, E. (1995). Readability revisited: The new Dale-Chall readability formula. Brookline Books. | p. 66
def x_c50(main, text):
    if text.lang.startswith('eng_'):
        text = get_nums(main, text)
        settings = main.settings_custom['measures']['readability']['x_c50']

        if text.num_words and text.num_sentences:
            num_difficult_words = get_num_words_outside_list(text.words_flat, wordlist = 'dale_3000')

            if settings['variant'] == _tr('wl_measures_readability', 'Original'):
                x_c50 = (
                    0.1579 * (num_difficult_words / text.num_words * 100)
                    + 0.0496 * (text.num_words / text.num_sentences)
                    + 3.6365
                )
            elif settings['variant'] == 'Powers-Sumner-Kearl':
                x_c50 = (
                    3.2672
                    + 0.1155 * (num_difficult_words / text.num_words * 100)
                    + 0.0596 * (text.num_words / text.num_sentences)
                )
            elif settings['variant'] == _tr('wl_measures_readability', 'New'):
                x_c50 = (
                    64
                    - 0.95 * (num_difficult_words / text.num_words * 100)
                    - 0.69 * (text.num_words / text.num_sentences)
                )
        else:
            x_c50 = 'text_too_short'
    else:
        x_c50 = 'no_support'

    return x_c50

# Danielson-Bryan's readability formula
# Reference: Danielson, W. A., & Bryan, S. D. (1963). Computer automation of two readability formulas. Journalism Quarterly, 40(2), 201–206. https://doi.org/10.1177/107769906304000207
def danielson_bryans_readability_formula(main, text):
    text = get_nums(main, text)

    if text.num_words - 1 and text.num_sentences:
        variant = main.settings_custom['measures']['readability']['danielson_bryans_readability_formula']['variant']

        if variant == '1':
            danielson_bryan = (
                1.0364 * (text.num_chars_all / (text.num_words - 1))
                + 0.0194 * (text.num_chars_all / text.num_sentences)
                - 0.6059
            )
        elif variant == '2':
            danielson_bryan = (
                131.059
                - 10.364 * (text.num_chars_all / (text.num_words - 1))
                - 0.194 * (text.num_chars_all / text.num_sentences)
            )
    else:
        danielson_bryan = 'text_too_short'

    return danielson_bryan

# Dawood's readability formula
# References:
#     Dawood, B.A.K. (1977). The relationship between readability and selected language variables [Unpublished master’s thesis]. University of Baghdad.
#     Cavalli-Sforza, V., Saddiki, H., & Nassiri, N. (2018). Arabic readability research: Current state and future directions. Procedia Computer Science, 142, 38–49.
def dawoods_readability_formula(main, text):
    if text.lang == 'ara':
        text = get_nums(main, text)

        if text.num_words and text.num_sentences and text.num_word_types:
            dawood = (
                (-0.0533) * (text.num_chars_alpha / text.num_words)
                - 0.2066 * (text.num_words / text.num_sentences)
                + 5.5543 * (text.num_words / text.num_word_types)
                - 1.0801
            )
        else:
            dawood = 'text_too_short'
    else:
        dawood = 'no_support'

    return dawood

# Degrees of Reading Power
# References:
#     College Entrance Examination Board. (1981). Degrees of reading power brings the students and the text together.
#     Carver, R. P. (1985). Measuring readability using DRP units. Journal of Reading Behavior, 17(4), 303–316. https://doi.org/10.1080/10862968509547547
def drp(main, text):
    m = bormuths_cloze_mean(main, text)

    if m not in ['no_support', 'text_too_short']:
        drp = 100 - math.floor(m * 100 + 0.5)
    else:
        drp = m

    return drp

# Devereux Readability Index
# Reference: Smith, E. A. (1961). Devereaux readability index. Journal of Educational Research, 54(8), 298–303. https://doi.org/10.1080/00220671.1961.10882728
def devereux_readability_index(main, text):
    text = get_nums(main, text)

    if text.num_words and text.num_sentences:
        grade_placement = (
            1.56 * (text.num_chars_all / text.num_words)
            + 0.19 * (text.num_words / text.num_sentences)
            - 6.49
        )
    else:
        grade_placement = 'text_too_short'

    return grade_placement

# Dickes-Steiwer Handformel
# References:
#     Dickes, P. & Steiwer, L. (1977). Ausarbeitung von lesbarkeitsformeln für die deutsche sprache. Zeitschrift für Entwicklungspsychologie und Pädagogische Psychologie, 9(1), 20–28.
#     Bamberger, R., & Vanecek, E. (1984). Lesen-verstehen-lernen-schreiben: Die schwierigkeitsstufen von texten in deutscher sprache. Jugend und Volk. | p. 57
def dickes_steiwer_handformel(main, text):
    text = get_nums(main, text)

    if text.num_words and text.num_sentences:
        dickes_steiwer = (
            235.95993
            - numpy.log(text.num_chars_alpha / text.num_words + 1) * 73.021
            - numpy.log(text.num_words / text.num_sentences + 1) * 12.56438
            - text.num_word_types / text.num_words * 50.03293
        )
    else:
        dickes_steiwer = 'text_too_short'

    return dickes_steiwer

# Easy Listening Formula
# Reference: Fang, I. E. (1966). The easy listening formula. Journal of Broadcasting, 11(1), 63–68. https://doi.org/10.1080/08838156609363529
def elf(main, text):
    if text.lang in main.settings_global['syl_tokenizers']:
        text = get_nums(main, text)

        if text.num_sentences:
            elf = (text.num_syls - text.num_words) / text.num_sentences
        else:
            elf = 'text_too_short'
    else:
        elf = 'no_support'

    return elf

# Flesch-Kincaid grade level
# Reference: Kincaid, J. P., Fishburne, R. P., Rogers, R. L., & Chissom, B. S. (1975). Derivation of new readability formulas (automated readability index, fog count, and Flesch reading ease formula) for Navy enlisted personnel (Report No. RBR 8-75). Naval Air Station Memphis. https://apps.dtic.mil/sti/pdfs/ADA006655.pdf | p. 14
def gl(main, text):
    if text.lang in main.settings_global['syl_tokenizers']:
        text = get_nums(main, text)

        if text.num_sentences and text.num_words:
            gl = (
                0.39 * (text.num_words / text.num_sentences)
                + 11.8 * (text.num_syls / text.num_words)
                - 15.59
            )
        else:
            gl = 'text_too_short'
    else:
        gl = 'no_support'

    return gl

# Flesch reading ease
# References:
#     Flesch, R. (1948). A new readability yardstick. Journal of Applied Psychology, 32(3), 221–233. https://doi.org/10.1037/h0057532
# Powers-Sumner-Kearl:
#     Powers, R. D., Sumner, W. A., & Kearl, B. E. (1958). A recalculation of four adult readability formulas. Journal of Educational Psychology, 49(2), 99–105. https://doi.org/10.1037/h0043254
# Dutch (Douma):
#     Douma, W. H. (1960). De leesbaarheid van landbouwbladen: Een onderzoek naar en een toepassing van leesbaarheidsformules [Readability of Dutch farm papers: A discussion and application of readability-formulas]. Afdeling Sociologie en Sociografie van de Landbouwhogeschool Wageningen. https://edepot.wur.nl/276323 | p. 453
# Dutch (Brouwer's Leesindex A):
#     Brouwer, R. H. M. (1963). Onderzoek naar de leesmoeilijkheid van Nederlands proza. Paedagogische Studiën, 40, 454–464. https://objects.library.uu.nl/reader/index.php?obj=1874-205260&lan=en
# French:
#     Kandel, L., & Moles, A. (1958). Application de l’indice de flesch à la langue française. The Journal of Educational Research, 21, 283–287.
#     Sitbon, L., Bellot, P., & Blache, P. (2007). Eléments pour adapter les systèmes de recherche d’information aux dyslexiques. Revue TAL : traitement automatique des langues, 48(2), 123–147.
# German:
#     Amstad, T. (1978). Wie verständlich sind unsere Zeitungen? [Unpublished doctoral dissertation]. University of Zurich.
#     Bamberger, R., & Vanecek, E. (1984). Lesen-verstehen-lernen-schreiben: Die schwierigkeitsstufen von texten in deutscher sprache. Jugend und Volk. | p. 56
# Italian:
#     Franchina, V., & Vacca, R. (1986). Adaptation of Flesh readability index on a bilingual text written by the same author both in Italian and English languages. Linguaggi, 3, 47–49.
#     Garais, E. (2011). Web applications readability. Journal of Information Systems and Operations Management, 5(1), 117–121. http://www.rebe.rau.ro/RePEc/rau/jisomg/SP11/JISOM-SP11-A13.pdf
# Russian:
#     Oborneva, I. V. (2006). Автоматизированная оценка сложности учебных текстов на основе статистических параметров [Doctoral dissertation, Institute for Strategy of Education Development of the Russian Academy of Education]. Freereferats.ru. https://static.freereferats.ru/_avtoreferats/01002881899.pdf?ver=3 | p. 13
# Spanish (Fernández Huerta):
#     Fernández Huerta, J. (1959). Medidas sencillas de lecturabilidad. Consigna, 214, 29–32.
#     Garais, E. (2011). Web applications readability. Journal of Information Systems and Operations Management, 5(1), 117–121. http://www.rebe.rau.ro/RePEc/rau/jisomg/SP11/JISOM-SP11-A13.pdf
# Spanish (Szigriszt Pazos):
#     Szigriszt Pazos, F. (1993). Sistemas predictivos de legibilidad del mensaje escrito: Formula de perspicuidad [Doctoral dissertation, Complutense University of Madrid]. Biblos-e Archivo. https://repositorio.uam.es/bitstream/handle/10486/2488/3907_barrio_cantalejo_ines_maria.pdf?sequence=1&isAllowed=y | p. 247
# Ukrainian:
#     Partiko, Z. V. (2001). Zagal’ne redaguvannja. Normativni osnovi. Afiša.
#     Grzybek, P. (2010). Text difficulty and the Arens-Altmann law. In P. Grzybek, E. Kelih, & J. Mačutek (eds.), Text and language: Structures · functions · interrelations quantitative perspectives. Praesens Verlag. https://www.iqla.org/includes/basic_references/qualico_2009_proceedings_Grzybek_Kelih_Macutek_2009.pdf
def re_flesch(main, text):
    if text.lang in main.settings_global['syl_tokenizers']:
        text = get_nums(main, text)
        settings = main.settings_custom['measures']['readability']['re']

        if text.num_words and text.num_sentences:
            if settings['use_powers_sumner_kearl_variant_for_all_langs']:
                re = (
                    -2.2029
                    + 4.55 * (text.num_syls / text.num_words)
                    + 0.0778 * (text.num_words / text.num_sentences)
                )
            else:
                if text.lang == 'nld':
                    if settings['variant_nld'] == 'Douma':
                        re = (
                            206.84
                            - 77 * (text.num_syls / text.num_words)
                            - 0.93 * (text.num_words / text.num_sentences)
                        )
                    elif settings['variant_nld'] == "Brouwer's Leesindex A":
                        re = (
                            195
                            - (200 / 3) * (text.num_syls / text.num_words)
                            - 2 * (text.num_words / text.num_sentences)
                        )
                elif text.lang == 'fra':
                    re = (
                        207
                        - 73.6 * (text.num_syls / text.num_words)
                        - 1.015 * (text.num_words / text.num_sentences)
                    )
                elif text.lang.startswith('deu_'):
                    re = (
                        180
                        - 58.5 * (text.num_syls / text.num_words)
                        - (text.num_words / text.num_sentences)
                    )
                elif text.lang == 'ita':
                    re = (
                        217
                        - 60 * (text.num_syls / text.num_words)
                        - 1.3 * (text.num_words / text.num_sentences)
                    )
                elif text.lang == 'rus':
                    re = (
                        206.835
                        - 60.1 * (text.num_syls / text.num_words)
                        - 1.3 * (text.num_words / text.num_sentences)
                    )
                elif text.lang == 'spa':
                    if settings['variant_spa'] == 'Fernández Huerta':
                        re = (
                            206.84
                            - 60 * (text.num_syls / text.num_words)
                            - 1.02 * (text.num_words / text.num_sentences)
                        )
                    elif settings['variant_spa'] == 'Szigriszt Pazos':
                        re = (
                            206.84
                            - 62.3 * (text.num_syls / text.num_words)
                            - (text.num_words / text.num_sentences)
                        )
                elif text.lang == 'ukr':
                    re = (
                        206.84
                        - 28.3 * (text.num_syls / text.num_words)
                        - 5.93 * (text.num_words / text.num_sentences)
                    )
                else:
                    re = (
                        206.835
                        - 84.6 * (text.num_syls / text.num_words)
                        - 1.015 * (text.num_words / text.num_sentences)
                    )
        else:
            re = 'text_too_short'
    else:
        re = 'no_support'

    return re

# Flesch reading ease (Farr-Jenkins-Paterson)
# References:
#     Farr, J. N., Jenkins, J. J., & Paterson, D. G. (1951). Simplification of Flesch reading ease formula. Journal of Applied Psychology, 35(5), 333–337. https://doi.org/10.1037/h0062427
# Powers-Sumner-Kearl:
#     Powers, R. D., Sumner, W. A., & Kearl, B. E. (1958). A recalculation of four adult readability formulas. Journal of Educational Psychology, 49(2), 99–105. https://doi.org/10.1037/h0043254
def re_farr_jenkins_paterson(main, text):
    if text.lang in main.settings_global['syl_tokenizers']:
        text = get_nums(main, text)

        if text.num_words and text.num_sentences:
            num_words_1_syl = get_num_words_syls(text.words_flat, len_min = 1, len_max = 1)

            if main.settings_custom['measures']['readability']['re_farr_jenkins_paterson']['use_powers_sumner_kearl_variant']:
                re = (
                    8.4335
                    - 0.0648 * (num_words_1_syl / text.num_words * 100)
                    + 0.0923 * (text.num_words / text.num_sentences)
                )
            else:
                re = (
                    1.599 * (num_words_1_syl / text.num_words * 100)
                    - 1.015 * (text.num_words / text.num_sentences)
                    - 31.517
                )
        else:
            re = 'text_too_short'
    else:
        re = 'no_support'

    return re

# FORCAST
# Reference: Caylor, J. S., & Sticht, T. G. (1973). Development of a simple readability index for job reading material. Human Resource Research Organization. https://ia902703.us.archive.org/31/items/ERIC_ED076707/ERIC_ED076707.pdf | p. 3
def rgl(main, text):
    if text.lang in main.settings_global['syl_tokenizers']:
        text = get_nums(main, text)

        if text.num_words >= 150:
            sample_start = random.randint(0, text.num_words - 150)
            sample = text.words_flat[sample_start : sample_start + 150]

            num_words_1_syl = get_num_words_syls(sample, len_min = 1, len_max = 1)
            rgl = 20.43 - 0.11 * num_words_1_syl
        else:
            rgl = 'text_too_short'
    else:
        rgl = 'no_support'

    return rgl

# Fucks's Stilcharakteristik
# References:
#     Fucks, W. (1955). Unterschied des prosastils von dichtern und anderen schriftstellern: Ein beispiel mathematischer stilanalyse. Bouvier.
#     Briest, W. (1974). Kann man Verständlichkeit messen? STUF - Language Typology and Universals, 27(1–3), 543–563. https://doi.org/10.1524/stuf.1974.27.13.543
def fuckss_stilcharakteristik(main, text):
    if text.lang in main.settings_global['syl_tokenizers']:
        text = get_nums(main, text)

        if text.num_sentences:
            stilcharakteristik = text.num_syls / text.num_sentences
        else:
            stilcharakteristik = 'text_too_short'
    else:
        stilcharakteristik = 'no_support'

    return stilcharakteristik

# GULPEASE
# References:
#     Lucisano, P., & Emanuela Piemontese, M. (1988). GULPEASE: A formula for the prediction of the difficulty of texts in Italian. Scuola e Città, 39(3), 110–124.
#     Indice Gulpease. (2021, July 9). In Wikipedia. https://it.wikipedia.org/w/index.php?title=Indice_Gulpease&oldid=121763335.
def gulpease(main, text):
    if text.lang == 'ita':
        text = get_nums(main, text)

        if text.num_words:
            gulpease = (
                89
                + (300 * text.num_sentences - 10 * text.num_chars_alpha) / text.num_words
            )
        else:
            gulpease = 'text_too_short'
    else:
        gulpease = 'no_support'

    return gulpease

# Gunning Fog Index
# References:
#     Gunning, R. (1968). The technique of clear writing (revised ed.). McGraw-Hill Book Company. | p. 38
# Powers-Sumner-Kearl:
#     Powers, R. D., Sumner, W. A., & Kearl, B. E. (1958). A recalculation of four adult readability formulas. Journal of Educational Psychology, 49(2), 99–105. https://doi.org/10.1037/h0043254
# Navy:
#     Kincaid, J. P., Fishburne, R. P., Rogers, R. L., & Chissom, B. S. (1975). Derivation of new readability formulas (automated readability index, fog count, and Flesch reading ease formula) for Navy enlisted personnel (Report No. RBR 8-75). Naval Air Station Memphis. https://apps.dtic.mil/sti/pdfs/ADA006655.pdf | p. 14
# Polish:
#     Pisarek, W. (1969). Jak mierzyć zrozumiałość tekstu? Zeszyty Prasoznawcze, 4(42), 35–48.
def fog_index(main, text):
    if text.lang.startswith('eng_') or text.lang == 'pol':
        text = get_nums(main, text)

        if text.num_sentences and text.num_words:
            num_hard_words = 0
            variant_eng = main.settings_custom['measures']['readability']['fog_index']['variant_eng']

            if text.lang.startswith('eng_'):
                if variant_eng in [
                    _tr('wl_measures_readability', 'Original'),
                    'Powers-Sumner-Kearl'
                ]:
                    pos_tag_words(main, text)

                    for word in text.words_flat:
                        if (
                            'PROPN' not in word.tag_universal.split('/')
                            and (
                                (len(word.syls) == 3 and not word.endswith('ed') and not word.endswith('es'))
                                or len(word.syls) > 3
                            )
                        ):
                            num_hard_words += 1

                    if variant_eng == _tr('wl_measures_readability', 'Original'):
                        fog_index = (
                            0.4
                            * (text.num_words / text.num_sentences + num_hard_words / text.num_words * 100)
                        )
                    elif variant_eng == 'Powers-Sumner-Kearl':
                        fog_index = (
                            3.0680
                            + 0.0877 * (text.num_words / text.num_sentences)
                            + 0.0984 * (num_hard_words / text.num_words * 100)
                        )
                elif variant_eng == _tr('wl_measures_readability', 'Navy'):
                    num_words_3_plus_syls = get_num_words_syls(text.words_flat, len_min = 3)

                    fog_index = (
                        ((text.num_words + 2 * num_words_3_plus_syls) / text.num_sentences - 3)
                        / 2
                    )
            elif text.lang == 'pol':
                pos_tag_words(main, text)
                # Count number of syllables of word lemmas instead of original words
                wl_lemmatization.wl_lemmatize(main, text.words_flat, lang = 'pol')
                lemmas_syls = wl_syl_tokenization.wl_syl_tokenize(
                    main,
                    wl_texts.to_tokens(wl_texts.get_token_properties(text.words_flat, 'lemma'), lang = 'pol'),
                    lang = 'pol'
                )

                for word, syls in zip(text.words_flat, lemmas_syls):
                    if len(syls) > 4 and 'PROPN' not in word.tag_universal.split('/'):
                        num_hard_words += 1

                fog_index = (
                    numpy.sqrt(
                        (text.num_words / text.num_sentences) ** 2
                        + (num_hard_words / text.num_words * 100) ** 2
                    )
                    / 2
                )
        else:
            fog_index = 'text_too_short'
    else:
        fog_index = 'no_support'

    return fog_index

# Gutiérrez de Polini's readability formula
# References:
#     Gutiérrez de Polini, L. E. (1972). Investigación sobre lectura en Venezuela [Paper presentation]. Primeras Jornadas de Educación Primaria, Ministerio de Educación, Caracas, Venezuela.
#     Rodríguez Trujillo, N. (1980). Determinación de la comprensibilidad de materiales de lectura por medio de variables lingüísticas. Lectura y Vida, 1(1). http://www.lecturayvida.fahce.unlp.edu.ar/numeros/a1n1/01_01_Rodriguez.pdf
def cp(main, text):
    if text.lang == 'spa':
        text = get_nums(main, text)

        if text.num_words and text.num_sentences:
            cp = (
                95.2
                - 9.7 * (text.num_chars_alpha / text.num_words)
                - 0.35 * (text.num_words / text.num_sentences)
            )
        else:
            cp = 'text_too_short'
    else:
        cp = 'no_support'

    return cp

# Legibilidad µ
# Reference: Muñoz Baquedano, M. (2006). Legibilidad y variabilidad de los textos. Boletín de Investigación Educacional, Pontificia Universidad Católica de Chile, 21(2), 13–26.
def mu(main, text):
    if text.lang == 'spa':
        text = get_nums(main, text)

        if text.num_words >= 2:
            # Excluding numbers and punctuation marks
            lens_words_letters = numpy.array([
                len([char for char in word if char.isalpha()])
                for word in text.words_flat
            ])

            mu = (
                (text.num_words / (text.num_words - 1))
                * (numpy.mean(lens_words_letters) / numpy.var(lens_words_letters))
                * 100
            )
        else:
            mu = 'text_too_short'
    else:
        mu = 'no_support'

    return mu

# Lensear Write Formula
# Reference: O’Hayre, J. (1966). Gobbledygook has gotta go. U.S. Government Printing Office. https://www.governmentattic.org/15docs/Gobbledygook_Has_Gotta_Go_1966.pdf | p. 8
def lensear_write_formula(main, text):
    if text.lang.startswith('eng_') and text.lang in main.settings_global['syl_tokenizers']:
        text = get_nums(main, text)

        if text.num_words > 0:
            if text.num_words > 100:
                sample_start = random.randint(0, text.num_words - 100)
            else:
                sample_start = 0

            sample = text.words_flat[sample_start : sample_start + 100]

            num_words_1_syl = 0
            sysl_sample = wl_texts.get_token_properties(
                wl_syl_tokenization.wl_syl_tokenize(main, sample, lang = text.lang),
                'syls'
            )

            for syls in sysl_sample:
                if len(syls) == 1 and syls[0].lower() not in ['the', 'is', 'are', 'was', 'were']:
                    num_words_1_syl += 1

            num_sentences = get_num_sentences_sample(text, sample, sample_start)

            # Normalize counts if number of tokens is less than 100
            if text.num_words < 100:
                num_words_1_syl *= 100 / text.num_words
                num_sentences *= 100 / text.num_words

            score = num_words_1_syl + 3 * num_sentences
        else:
            score = 'text_too_short'
    else:
        score = 'no_support'

    return score

# Lix
# References:
#     Björnsson, C.-H. (1968). Läsbarhet. Liber.
#     Anderson, J. (1983). Lix and Rix: Variations on a little-known readability index. Journal of Reading, 26(6), 490–496.
def lix(main, text):
    if text.num_words and text.num_sentences:
        text = get_nums(main, text)

        num_long_words = get_num_words_ltrs(text.words_flat, len_min = 7)
        lix = text.num_words / text.num_sentences + 100 * (num_long_words / text.num_words)
    else:
        lix = 'text_too_short'

    return lix

# Lorge Readability Index
# References:
#     Lorge, I. (1944). Predicting readability. Teachers College Record, 45, 404–419.
#     Lorge, I. (1944). Predicting readability. In W. H. DuBay (Ed.), The classic readability studies (pp. 46–60). Impact Information. https://files.eric.ed.gov/fulltext/ED506404.pdf
# Corrected:
#     Lorge, I. (1948). The Lorge and Flesch readability formulae: A correction. School and Society, 67, 141–142.
#     Lorge, I. (1944). Predicting readability. In W. H. DuBay (Ed.), The classic readability studies (pp. 46–60). Impact Information. https://files.eric.ed.gov/fulltext/ED506404.pdf
def lorge_readability_index(main, text):
    if text.lang.startswith('eng_'):
        text = get_nums(main, text)

        if text.num_sentences and text.num_words:
            pos_tag_words(main, text)
            num_preps = get_num_words_pos_tag(
                words = text.words_flat,
                pos_tag = 'ADP'
            )
            num_hard_words = get_num_words_outside_list(
                text.words_flat,
                wordlist = 'dale_769',
                use_word_types = True
            )

            if main.settings_custom['measures']['readability']['lorge_readability_index']['use_corrected_formula']:
                lorge = (
                    text.num_words / text.num_sentences * 0.06
                    + num_preps / text.num_words * 0.1
                    + num_hard_words / text.num_words * 0.1
                    + 1.99
                )
            else:
                lorge = (
                    text.num_words / text.num_sentences * 0.07
                    + num_preps / text.num_words * 13.01
                    + num_hard_words / text.num_words * 10.73
                    + 1.6126
                )
        else:
            lorge = 'text_too_short'
    else:
        lorge = 'no_support'

    return lorge

# Luong-Nguyen-Dinh's readability formula
# Reference: Luong, A.-V., Nguyen, D., & Dinh, D. (2018). A new formula for Vietnamese text readability assessment. In T. M. Phuong & M. L. Nguyen (Eds.), Proceedings of 2018 10th International Conference on Knowledge and Systems Engineering (KSE) (pp. 198–202). IEEE. https://doi.org/10.1109/KSE.2018.8573379
def luong_nguyen_dinhs_readability_formula(main, text):
    if text.lang == 'vie':
        text = get_nums(main, text)

        syls = [syl.strip() for word in text.words_flat for syl in word.split()]
        num_difficult_syls = get_num_words_outside_list(words = syls, wordlist = 'luong_nguyen_dinh')

        if text.num_sentences and text.num_words:
            readability = (
                0.004 * (text.num_chars_alnum / text.num_sentences)
                + 0.1905 * (text.num_chars_alnum / text.num_words)
                + 2.7147 * num_difficult_syls / len(syls)
                - 0.7295
            )
        else:
            readability = 'text_too_short'
    else:
        readability = 'no_support'

    return readability

# McAlpine EFLAW Readability Score
# Reference: McAlpine, R. (2006). From plain English to global English. Journalism Online. Retrieved October 31, 2024, from https://www.angelfire.com/nd/nirmaldasan/journalismonline/fpetge.html
def eflaw(main, text):
    if text.lang.startswith('eng_'):
        text = get_nums(main, text)

        if text.num_sentences:
            num_mini_words = get_num_words_ltrs(text.words_flat, len_max = 3)
            eflaw = (text.num_words + num_mini_words) / text.num_sentences
        else:
            eflaw = 'text_too_short'
    else:
        eflaw = 'no_support'

    return eflaw

# neue Wiener Literaturformeln
# Reference: Bamberger, R., & Vanecek, E. (1984). Lesen-verstehen-lernen-schreiben: Die schwierigkeitsstufen von texten in deutscher sprache. Jugend und Volk. | p. 82
def nwl(main, text):
    if text.lang.startswith('deu_'):
        text = get_nums(main, text)

        if text.num_words and text.num_sentences:
            variant = main.settings_custom['measures']['readability']['nwl']['variant']

            sw = get_num_words_outside_list(text.words_flat, wordlist = 'bamberger_vanecek', use_word_types = True) / text.num_word_types * 100
            s_100 = text.num_sentences / text.num_words * 100
            ms = get_num_words_syls(text.words_flat, len_min = 3) / text.num_words * 100
            sl = text.num_words / text.num_sentences
            iw = get_num_words_ltrs(text.words_flat, len_min = 7) / text.num_words * 100

            if variant == '1':
                nwl = 0.2032 * sw - 0.1715 * s_100 + 0.1594 * ms - 0.0746 * ms - 0.145
            elif variant == '2':
                nwl = 0.2081 * sw - 0.207 * s_100 + 0.1772 * ms + 0.7498
            elif variant == '3':
                nwl = 0.2373 * ms + 0.2433 * sl + 0.1508 * iw - 3.9203
        else:
            nwl = 'text_too_short'
    else:
        nwl = 'no_support'

    return nwl

# neue Wiener Sachtextformel
# Reference: Bamberger, R., & Vanecek, E. (1984). Lesen-verstehen-lernen-schreiben: Die schwierigkeitsstufen von texten in deutscher sprache. Jugend und Volk. | pp. 83–84
def nws(main, text):
    if text.lang.startswith('deu_'):
        text = get_nums(main, text)

        if text.num_words and text.num_sentences:
            variant = main.settings_custom['measures']['readability']['nws']['variant']

            ms = get_num_words_syls(text.words_flat, len_min = 3) / text.num_words * 100
            sl = text.num_words / text.num_sentences
            iw = get_num_words_ltrs(text.words_flat, len_min = 7) / text.num_words * 100
            es = get_num_words_syls(text.words_flat, len_min = 1, len_max = 1) / text.num_words * 100

            if variant == '1':
                nws = 0.1935 * ms + 0.1672 * sl + 0.1297 * iw - 0.0327 * es - 0.875
            elif variant == '2':
                nws = 0.2007 * ms + 0.1682 * sl + 0.1373 * iw - 2.779
            elif variant == '3':
                nws = 0.2963 * ms + 0.1905 * sl - 1.1144
        else:
            nws = 'text_too_short'
    else:
        nws = 'no_support'

    return nws

# Estimate number of syllables in Arabic texts by counting short, long, and stress syllables
# References:
#     https://github.com/drelhaj/OsmanReadability/blob/master/src/org/project/osman/process/Syllables.java
#     https://github.com/textstat/textstat/blob/9bf37414407bcaaa45c498478ee383c8738e5d0c/textstat/textstat.py#L569
RE_STRESS = re.compile(r'[\u064B\u064C\u064D\u0651]')
RE_SHORT = re.compile(r'[\u0627\u0649\?\.\!\,\s]')

def _get_num_syls_ara(word):
    count_short = 0
    count_long = 0

    for i, char in enumerate(word):
        # Tashkeel: fatha, damma, kasra
        if char not in ('\u064E', '\u064F', '\u0650'):
            continue

        # Only if a character is a tashkeel, has a successor, and is followed by an alef, waw, or yeh
        if i + 1 < len(word):
            if word[i + 1] in ('\u0627', '\u0648', '\u064A'):
                count_long += 1
            else:
                count_short += 1
        else:
            count_short += 1

    # Stress syllables: tanween fatha, tanween damma, tanween kasra, shadda
    count_stress = len(RE_STRESS.findall(word))

    if count_short == 0:
        word = RE_SHORT.sub('', word)
        count_short = max(0, len(word) - 2)

    # Reference: https://github.com/drelhaj/OsmanReadability/blob/405b927ef3fde200fa08efe12ec2f39b8716e4be/src/org/project/osman/process/OsmanReadability.java#L259
    return count_short + 2 * (count_long + count_stress)

# OSMAN
# Reference: El-Haj, M., & Rayson, P. (2016). OSMAN: A novel Arabic readability metric. In N. Calzolari, K. Choukri, T. Declerck, S. Goggi, M. Grobelnik, B. Maegaard, J. Mariani, H. Mazo, A. Moreno, J. Odijk, & S. Piperidis (Eds.), Proceedings of the Tenth International Conference on Language Resources and Evaluation (LREC 2016) (pp. 250–255). European Language Resources Association. http://www.lrec-conf.org/proceedings/lrec2016/index.html
def osman(main, text):
    if text.lang == 'ara':
        text = get_nums(main, text)

        if text.num_sentences and text.num_words:
            nums_syls_tokens = numpy.array([_get_num_syls_ara(word) for word in text.words_flat])

            a = text.num_words
            b = text.num_sentences
            c = get_num_words_ltrs(text.words_flat, len_min = 6)
            d = numpy.sum(nums_syls_tokens)
            g = numpy.sum(nums_syls_tokens > 4)
            h = 0

            for word, num_syls in zip(text.words_flat, nums_syls_tokens):
                if (
                    num_syls > 4
                    # Faseeh letters
                    # Reference: https://github.com/drelhaj/OsmanReadability/blob/405b927ef3fde200fa08efe12ec2f39b8716e4be/src/org/project/osman/process/OsmanReadability.java#L264
                    and (
                        # Hamza (ء), yeh with hamza above (ئ), waw with hamza above (ؤ), zah (ظ), thal (ذ)
                        any((char in word for char in ['\u0621', '\u0626', '\u0624', '\u0638', '\u0630']))
                        # Waw noon (ون), waw alef (وا)
                        or word.endswith(('\u0648\u0646', '\u0648\u0627'))
                    )
                ):
                    h += 1

            osman = (
                200.791
                - 1.015 * (a / b)
                - 24.181 * ((c + d + g + h) / a)
            )
        else:
            osman = 'text_too_short'
    else:
        osman = 'no_support'

    return osman

# Rix
# Reference: Anderson, J. (1983). Lix and Rix: Variations on a little-known readability index. Journal of Reading, 26(6), 490–496.
def rix(main, text):
    text = get_nums(main, text)

    if text.num_sentences:
        num_long_words = get_num_words_ltrs(text.words_flat, len_min = 7)
        rix = num_long_words / text.num_sentences
    else:
        rix = 'text_too_short'

    return rix

# SMOG Grading
# References:
#     McLaughlin, G. H. (1969). SMOG Grading: A new readability formula. Journal of Reading, 12(8), 639–646.
# German:
#     Bamberger, R., & Vanecek, E. (1984). Lesen-verstehen-lernen-schreiben: Die schwierigkeitsstufen von texten in deutscher sprache. Jugend und Volk. | p. 78
def smog_grading(main, text):
    if text.lang in main.settings_global['syl_tokenizers']:
        text = get_nums(main, text)

        if text.num_sentences >= 30:
            # Calculate the index for the 10 sentences at the middle of the text
            sample_start_mid = text.num_sentences // 2 - 5
            sample = (
                text.sentences[:10]
                + text.sentences[sample_start_mid : sample_start_mid + 10]
                + text.sentences[-10:]
            )

            # Calculate the number of words with 3 or more syllables
            num_words_3_plus_syls = 0

            for sentence in sample:
                sentence = wl_syl_tokenization.wl_syl_tokenize(main, sentence, lang = text.lang)

                num_words_3_plus_syls += get_num_words_syls(sentence, len_min = 3)

            if text.lang.startswith('deu_'):
                g = numpy.sqrt(num_words_3_plus_syls / text.num_sentences * 30) - 2
            else:
                g = 3.1291 + 1.043 * numpy.sqrt(num_words_3_plus_syls)
        else:
            g = 'text_too_short'
    else:
        g = 'no_support'

    return g

# Spache readability formula
# References:
#     Spache, G. (1953). A new readability formula for primary-grade reading materials. Elementary School Journal, 53(7), 410–413. https://doi.org/10.1086/458513
# Revised:
#     Spache, G. (1974). Good reading for poor readers (Rev. 9th ed.). Garrard.
#     Michalke, M., Brown, E., Mirisola, A., Brulet, A., & Hauser, L. (2021, May 17). Measure readability. Documentation for package ‘koRpus’ version 0.13-8. Retrieved August 3, 2023, from https://search.r-project.org/CRAN/refmans/koRpus/html/readability-methods.html
# Spache word list:
#     Benoit, K., Watanabe, K., Wang, H., Nulty, P., Obeng, A., Müller, S., & Matsuo, A. (2020, November 17). data_char_wordlists.rda. quanteda.textstats. Retrieved August 3, 2023, from https://github.com/quanteda/quanteda.textstats/raw/master/data/data_char_wordlists.rda
def spache_readability_formula(main, text):
    if text.lang.startswith('eng_'):
        text = get_nums(main, text)

        if text.num_words >= 100:
            grade_lvls = []

            # Sample 3 times
            for _ in range(3):
                sample_start = random.randint(0, text.num_words - 100)
                sample = text.words_flat[sample_start : sample_start + 100]

                num_sentences = get_num_sentences_sample(text, sample, sample_start)

                if main.settings_custom['measures']['readability']['spache_readability_formula']['use_rev_formula']:
                    num_difficult_words = get_num_words_outside_list(sample, wordlist = 'spache')
                    grade_lvls.append(
                        0.121 * (100 / num_sentences)
                        + 0.082 * (num_difficult_words)
                        + 0.659
                    )
                else:
                    num_difficult_words = get_num_words_outside_list(sample, wordlist = 'dale_769')
                    grade_lvls.append(
                        0.141 * (100 / num_sentences)
                        + 0.086 * (num_difficult_words)
                        + 0.839
                    )

            grade_lvl = numpy.mean(grade_lvls)
        else:
            grade_lvl = 'text_too_short'
    else:
        grade_lvl = 'no_support'

    return grade_lvl

# Strain Index
# References:
#     Nathaniel, W. S. (2017). A quantitative analysis of media language [Master’s thesis, Madurai Kamaraj University]. LAMBERT Academic Publishing.
#     Nirmaldasan. (2007, July). Strain Index: A new readability formula. Journalism Online. Retrieved October 31, 2024, from https://www.angelfire.com/nd/nirmaldasan/readability/si.html
def strain_index(main, text):
    if text.lang in main.settings_global['syl_tokenizers']:
        text = get_nums(main, text)

        if text.num_sentences >= 3:
            num_syls = 0

            for sentence in text.sentences[:3]:
                words_syls = wl_texts.get_token_properties(
                    wl_syl_tokenization.wl_syl_tokenize(main, sentence, lang = text.lang),
                    'syls'
                )

                num_syls += sum((len(syls) for syls in words_syls))

            strain_index = num_syls / 10
        else:
            strain_index = 'text_too_short'
    else:
        strain_index = 'no_support'

    return strain_index

# Tränkle-Bailer's readability formula
# References:
#     Tränkle, U., & Bailer, H. (1984). Kreuzvalidierung und neuberechnung von lesbarkeitsformeln für die Deutsche sprache. Zeitschrift für Entwicklungspsychologie und Pädagogische Psychologie, 16(3), 231–244.
#     Benoit, K. (2020, November 24). Calculate readability. quanteda: Quantitative Analysis of Textual Data. Retrieved August 3, 2023, from https://quanteda.io/reference/textstat_readability.html
def trankle_bailers_readability_formula(main, text):
    if text.lang in main.settings_global['pos_taggers']:
        text = get_nums(main, text)

        if text.num_words >= 100:
            pos_tag_words(main, text)

            sample_start = random.randint(0, text.num_words - 100)
            sample = text.words_flat[sample_start : sample_start + 100]

            num_chars_alnum = sum((1 for token in sample for char in token if char.isalnum()))
            num_sentences = get_num_sentences_sample(text, sample, sample_start)

            num_preps, num_cconjs, num_sconjs = get_nums_words_pos_tags( # pylint: disable=unbalanced-tuple-unpacking
                words = sample,
                pos_tags = ['ADP', 'CCONJ', 'SCONJ']
            )

            variant = main.settings_custom['measures']['readability']['trankle_bailers_readability_formula']['variant']

            if variant == '1':
                trankle_bailers = (
                    224.6814
                    - numpy.log(num_chars_alnum / 100 + 1) * 79.8304
                    - numpy.log(100 / num_sentences + 1) * 12.24032
                    - num_preps * 1.292857
                )
            elif variant == '2':
                trankle_bailers = (
                    234.1063
                    - numpy.log(num_chars_alnum / 100 + 1) * 96.11069
                    - num_preps * 2.05444
                    - (num_cconjs + num_sconjs) * 1.02805
                )
        else:
            trankle_bailers = 'text_too_short'
    else:
        trankle_bailers = 'no_support'

    return trankle_bailers

# Tuldava's readability formula
# References:
#     Tuldava, J. (1975). Ob izmerenii trudnosti tekstov. Uchenye zapiski Tartuskogo universiteta. Trudy po metodike prepodavaniya inostrannykh yazykov, 345, 102–120.
#     Grzybek, P. (2010). Text difficulty and the Arens-Altmann law. In P. Grzybek, E. Kelih, & J. Mačutek (eds.), Text and language: Structures · functions · interrelations quantitative perspectives. Praesens Verlag. https://www.iqla.org/includes/basic_references/qualico_2009_proceedings_Grzybek_Kelih_Macutek_2009.pdf
def td(main, text):
    if text.lang in main.settings_global['syl_tokenizers']:
        text = get_nums(main, text)

        if text.num_words:
            td = (
                (text.num_syls / text.num_words)
                * numpy.log(text.num_words / text.num_sentences)
            )
        else:
            td = 'text_too_short'
    else:
        td = 'no_support'

    return td

# Wheeler-Smith's readability formula
# Reference: Wheeler, L. R., & Smith, E. H. (1954). A practical readability formula for the classroom teacher in the primary grades. Elementary English, 31(7), 397–399.
UNIT_TERMINATORS = ''.join(list(wl_sentence_tokenization.SENTENCE_TERMINATORS) + list(dict.fromkeys([
    # Colons and semicolons: https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=[:name=/COLON/:]%26[:General_Category=/Punctuation/:]
    '\u003A', '\u003B',
    '\u061B',
    '\u0703', '\u0704', '\u0705', '\u0706', '\u0707', '\u0708', '\u0709',
    '\u1364', '\u1365', '\u1366',
    '\u1804',
    '\u204F', '\u205D',
    '\u2E35',
    '\uA6F4', '\uA6F6',
    '\uFE13', '\uFE14',
    '\uFE54', '\uFE55',
    '\uFF1A', '\uFF1B',
    '\U00012471', '\U00012472', '\U00012473', '\U00012474',
    '\U0001DA89', '\U0001DA8A',

    # Dashes: https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=[:Dash=Yes:]
    '\\\u002D', # The hyphen character needs to be escaped in RegEx square brackets
    '\u058A',
    '\u05BE',
    '\u1400',
    '\u1806',
    '\u2010', '\u2011', '\u2012', '\u2013', '\u2014', '\u2015', '\u2053',
    '\u207B', '\u208B',
    '\u2212',
    '\u2E17', '\u2E1A', '\u2E3A', '\u2E3B', '\u2E40', '\u2E5D',
    '\u301C', '\u3030',
    '\u30A0',
    '\uFE31', '\uFE32',
    '\uFE58', '\uFE63',
    '\uFF0D',
    '\U00010EAD'
])))

def wheeler_smiths_readability_formula(main, text):
    if text.lang in main.settings_global['syl_tokenizers']:
        text = get_nums(main, text)

        if text.num_words:
            num_units = len(wl_sentence_tokenization.wl_sentence_seg_tokenize_tokens(
                main,
                tokens = wl_misc.flatten_list(text.tokens_multilevel_with_puncs),
                terminators = UNIT_TERMINATORS
            ))
            num_words_2_syls = get_num_words_syls(text.words_flat, len_min = 2)

            wheeler_smith = (
                (text.num_words / num_units)
                * (num_words_2_syls / text.num_words)
                * 10
            )
        else:
            wheeler_smith = 'text_too_short'
    else:
        wheeler_smith = 'no_support'

    return wheeler_smith
