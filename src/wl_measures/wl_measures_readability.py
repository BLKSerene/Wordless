# ----------------------------------------------------------------------
# Wordless: Measures - Readibility
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

import math
import random

import numpy

from wl_checking import wl_checking_token
from wl_utils import wl_misc
from wl_text import wl_pos_tagging, wl_syl_tokenization

NO_SUPPORT = 'No Support'
TEXT_TOO_SHORT = 'Text is Too Short'

def get_counts(main, text):
    # Count of sentences
    if 'count_sentences' not in text.__dict__:
        text.words_multilevel = []

        for para in text.tokens_multilevel:
            text.words_multilevel.append([])

            for sentence in para:
                text.words_multilevel[-1].append([token for token in sentence if wl_checking_token.is_word_alphanumeric(token)])

        text.sentences = [sentence for para in text.words_multilevel for sentence in para]
        text.count_sentences = len(text.sentences)

    # Count of words with at least one letter or numeral
    if 'count_words' not in text.__dict__:
        text.words_flat = list(wl_misc.flatten_list(text.words_multilevel))
        text.count_words = len(text.words_flat)

    # Count of syllables
    if 'count_syls' not in text.__dict__:
        text.syls_words = wl_syl_tokenization.wl_syl_tokenize(main, text.words_flat, lang = text.lang)
        text.count_syls = sum([len(syls) for syls in text.syls_words])

    # Count of characters
    if 'count_chars_all' not in text.__dict__:
        text.count_chars_all = 0
        text.count_chars_alphanumeric = 0
        text.count_chars_alphabetic = 0

        for token in text.words_flat:
            for char in token:
                text.count_chars_all += 1

                if char.isalpha():
                    text.count_chars_alphanumeric += 1
                    text.count_chars_alphabetic += 1
                elif char.isalnum():
                    text.count_chars_alphanumeric += 1

# Calculate the number of words outside the Dale list of 3000 easy words
def get_count_difficult_words(words, num_easy_words):
    dale_list_easy_words = set()
    count_difficult_words = 0

    # Load Dale list of easy words [769, 3000]
    with open(f'wl_measures/dale_list_easy_words_{num_easy_words}.txt', 'r', encoding = 'utf_8') as f:
        for line in f:
            word = line.strip()

            if word:
                # Ignore case
                dale_list_easy_words.add(word.lower())

    for word in words:
        if word.lower() not in dale_list_easy_words:
            count_difficult_words += 1

    return count_difficult_words

# Automated Readability Index
# Reference: Smith, E. A., & Senter, R. J. (1967). Automated readability index. Aerospace Medical Research Laboratories. https://apps.dtic.mil/sti/pdfs/AD0667273.pdf
def automated_readability_index(main, text):
    get_counts(main, text)

    ari = 0.5 * (text.count_words / text.count_sentences) + 4.71 * (text.count_chars_all / text.count_words) - 21.43

    return ari

# Coleman-Liau Index
# Reference: Coleman, M., & Liau, T. L. (1975). A computer readability formula designed for machine scoring. Journal of Applied Psychology, 60(2), 283–284. https://doi.org/10.1037/h0076540
def coleman_liau_index(main, text):
    get_counts(main, text)

    est_cloze_pct = 141.8401 - 0.21459 * (text.count_chars_alphabetic / text.count_words * 100) + 1.079812 * (text.count_sentences / text.count_words * 100)
    grade_level = -27.4004 * (est_cloze_pct / 100) + 23.06395

    return grade_level

# Dale-Chall Readibility Score
# References:
#     Dale, E., & Chall, J. S. (1948). A formula for predicting readability. Educational Research Bulletin, 27(1), 11–20, 28.
#     Dale, E., & Chall, J. S. (1948). A formula for predicting readability: Instructions. Educational Research Bulletin, 27(2), 37–54.
def dale_chall_readability_score(main, text):
    if text.lang.startswith('eng'):
        get_counts(main, text)

        count_difficult_words = get_count_difficult_words(text.words_flat, 3000)
        x_c50 = 0.1579 * (count_difficult_words / text.count_words) + 0.0496 * (text.count_words / text.count_sentences) + 3.6365
    # No language support
    else:
        x_c50 = NO_SUPPORT

    return x_c50

# Devereux Readability Index
# Reference: Smith, E. A. (1961). Devereaux readability index. Journal of Educational Research, 54(8), 298–303. https://doi.org/10.1080/00220671.1961.10882728
def devereux_readability_index(main, text):
    get_counts(main, text)

    grade_placement = 1.56 * (text.count_chars_all / text.count_words) + 0.19 * (text.count_words / text.count_sentences) - 6.49

    return grade_placement

# Flesch Reading Ease
# Reference: Flesch, R. (1948). A new readability yardstick. Journal of Applied Psychology, 32(3), 221–233. https://doi.org/10.1037/h0057532
def flesch_reading_ease(main, text):
    if text.lang in main.settings_global['syl_tokenizers']:
        get_counts(main, text)

        flesch_re = 206.835 - 0.846 * (text.count_syls / text.count_words * 100) - 1.015 * (text.count_words / text.count_sentences)
    # No language support
    else:
        flesch_re = NO_SUPPORT

    return flesch_re

# Flesch Reading Ease (Simplified)
# Reference: Farr, J. N., Jenkins, J. J., & Paterson, D. G. (1951). Simplification of Flesch reading ease formula. Journal of Applied Psychology, 35(5), 333–337. https://doi.org/10.1037/h0062427
def flesch_reading_ease_simplified(main, text):
    if text.lang in main.settings_global['syl_tokenizers']:
        get_counts(main, text)

        count_words_1_syl = len([syls for syls in text.syls_words if len(syls) == 1])

        flesch_re_simplified = 1.599 * (count_words_1_syl / text.count_words * 100) - 1.015 * (text.count_words / text.count_sentences) - 31.517
    # No language support
    else:
        flesch_re_simplified = NO_SUPPORT

    return flesch_re_simplified

# Flesch-Kincaid Grade Level
# Reference: Kincaid, J. P., Fishburne, R. P., Rogers, R. L., & Chissom, B. S. (1975). Derivation of new readability formulas (automated readability index, fog count, and Flesch reading ease formula) for navy enlisted personnel. Naval Air Station Memphis. https://apps.dtic.mil/sti/pdfs/ADA006655.pdf
def flesch_kincaid_grade_level(main, text):
    if text.lang in main.settings_global['syl_tokenizers']:
        get_counts(main, text)

        gl = 0.39 * (text.count_words / text.count_sentences) + 11.8 * (text.count_syls / text.count_words) - 15.59
    # No language support
    else:
        gl = NO_SUPPORT

    return gl

# FORCAST Grade Level
# Reference: Caylor, J. S., Sticht, T. G., Fox, L. C., & Ford, J. P. (1973). Methodologies for determining reading requirements of military occupational specialties. Human Resource Research Organization. https://files.eric.ed.gov/fulltext/ED074343.pdf
def forcast_grade_level(main, text):
    if text.lang in main.settings_global['syl_tokenizers']:
        get_counts(main, text)

        if text.count_words >= 150:
            sample_start = random.randint(0, text.count_words - 150)
            sample = text.syls_words[sample_start : sample_start + 150]

            count_words_1_syl = len([syls for syls in sample if len(syls) == 1])
            rgl = 20.43 - 0.11 * count_words_1_syl
        # Text is too short
        else:
            rgl = TEXT_TOO_SHORT
    # No language support
    else:
        rgl = NO_SUPPORT

    return rgl

# Gunning Fog Index
# Reference: Gunning, R. (1968). The technique of clear writing (revised ed.). McGraw-Hill Book Company.
def gunning_fog_index(main, text):
    if text.lang.startswith('eng'):
        get_counts(main, text)

        count_hard_words = 0

        words_tagged = wl_pos_tagging.wl_pos_tag(main, text.words_flat, lang = text.lang, tagset = 'universal')

        for syls, (_, tag) in zip(text.syls_words, words_tagged):
            if tag != 'PROPN' and ((len(syls) == 3 and syls[-1] not in ['ed', 'es']) or len(syls) > 3):
                count_hard_words += 1

        fog_index = 0.4 * (text.count_words / text.count_sentences + count_hard_words / text.count_words * 100)
    # No language support
    else:
        fog_index = NO_SUPPORT

    return fog_index

# SMOG Grade
# Reference: McLaughlin, G. H. (1969). SMOG grading: A new readability formula. Journal of Reading, 12(8), pp. 639–646. 
def smog_grade(main, text):
    if text.lang in main.settings_global['syl_tokenizers']:
        get_counts(main, text)

        if text.count_sentences >= 30:
            # Calculate the index for the 10 sentences at the middle of the text
            sample_start_mid = text.count_sentences // 2 - 5
            samples = text.sentences[:10] + text.sentences[sample_start_mid : sample_start_mid + 10] + text.sentences[-10:]

            # Calculate the number of words with 3 or more syllables
            count_words_polysyllabic = 0

            for sentence in samples:
                syls_words = wl_syl_tokenization.wl_syl_tokenize(main, sentence, lang = text.lang)

                count_words_polysyllabic += len([syls for syls in syls_words if len(syls) >= 3])

            g = 3.1291 + 1.043 * (count_words_polysyllabic ** 0.5)
        # Text is too short
        else:
            g = TEXT_TOO_SHORT
    # No language support
    else:
        g = NO_SUPPORT

    return g

# Spache Grade Level
# References:
#     Dale, E. (1931). A comparison of two word lists. Educational Research Bulletin, 10(18), 484–489.
#     Spache, G. (1953). A new readability formula for primary-grade reading materials. Elementary School Journal, 53(7), 410–413. https://doi.org/10.1086/458513
def spache_grade_level(main, text):
    if text.lang.startswith('eng'):
        get_counts(main, text)

        if text.count_words >= 100:
            grade_levels = []

            # Calculate the average grade level of 3 samples
            for i in range(3):
                samples = []
                i_word = 0
                count_sentences_samples = 0

                samples_start = random.randint(0, text.count_words - 100)

                for sentence in text.sentences:
                    if len(samples) < 100:
                        if i_word + len(sentence) >= samples_start:
                            count_sentences_samples += 1

                            for token in sentence:
                                if len(samples) < 100:
                                    samples.append(token)
                                else:
                                    break

                        i_word += len(sentence)
                    else:
                        break

                count_difficult_words = get_count_difficult_words(samples, 769)
                grade_levels.append(0.141 * (100 / count_sentences_samples) + 0.086 * (count_difficult_words / 100 * 100) + 0.839)

            grade_level = numpy.mean(grade_levels)
        # Text is too short
        else:
            grade_level = TEXT_TOO_SHORT
    # No language support 
    else:
        grade_level = NO_SUPPORT

    return grade_level

# Write Score
# Reference: O’Hayre, J. (1966). Gobbledygook has gotta go. U.S. Government Printing Office. https://www.governmentattic.org/15docs/Gobbledygook_Has_Gotta_Go_1966.pdf
def write_score(main, text):
    if text.lang in main.settings_global['syl_tokenizers']:
        get_counts(main, text)

        if text.count_words >= 100:
            samples = []
            i_word = 0
            count_sentences_samples = 0

            samples_start = random.randint(0, text.count_words - 100)

            for sentence in text.sentences:
                if len(samples) < 100:
                    if i_word + len(sentence) >= samples_start:
                        count_sentences_samples += 1

                        for token in sentence:
                            if len(samples) < 100:
                                samples.append(token)
                            else:
                                break

                    i_word += len(sentence)
                else:
                    break

            count_words_1_syl = 0

            samples_syls = wl_syl_tokenization.wl_syl_tokenize(main, samples, lang = text.lang)

            for syls in samples_syls:
                if len(syls) == 1 and syls[0].lower() not in ['the', 'is', 'are', 'was', 'were']:
                    count_words_1_syl += 1

            score = count_words_1_syl + 3 * count_sentences_samples
        # Text is too short
        else:
            score = TEXT_TOO_SHORT
    # No language support
    else:
        score = NO_SUPPORT

    return score
