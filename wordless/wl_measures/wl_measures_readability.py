# ----------------------------------------------------------------------
# Wordless: Measures - Readability
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

import bisect
import math
import random
import re

import numpy

from wordless.wl_checks import wl_checks_tokens
from wordless.wl_nlp import wl_pos_tagging, wl_syl_tokenization
from wordless.wl_utils import wl_misc, wl_paths

def get_counts(main, text):
    # Count of sentences
    if 'count_sentences' not in text.__dict__:
        text.words_multilevel = []

        for para in text.tokens_multilevel:
            text.words_multilevel.append([])

            for sentence in para:
                text.words_multilevel[-1].append([])

                for sentence_seg in sentence:
                    text.words_multilevel[-1][-1].append([
                        token
                        for token in sentence_seg
                        if wl_checks_tokens.is_word_alphanumeric(token)
                    ])

        text.sentences = [
            list(wl_misc.flatten_list(sentence))
            for para in text.words_multilevel
            for sentence in para
        ]
        text.count_sentences = len(text.sentences)

    # Count of words with at least one letter or numeral
    if 'count_words' not in text.__dict__:
        text.words_flat = list(wl_misc.flatten_list(text.words_multilevel))
        text.count_words = len(text.words_flat)

    # Count of syllables
    if 'count_syls' not in text.__dict__ and text.lang in main.settings_global['syl_tokenizers']:
        text.syls_words = wl_syl_tokenization.wl_syl_tokenize(main, text.words_flat, lang = text.lang)
        text.count_syls = sum((len(syls) for syls in text.syls_words))

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

    return text

def get_count_words_letters(words, len_min = 1, len_max = None):
    if len_max:
        return len([
            True
            for word in words
            if  len_min <= len([char for char in word if char.isalpha()]) <= len_max
        ])
    else:
        return len([
            True
            for word in words
            if  len([char for char in word if char.isalpha()]) >= len_min
        ])

def get_count_words_syls(syls_words, len_min = 1, len_max = None):
    if len_max:
        return len([
            True
            for syls in syls_words
            if len_min <= len(syls) <= len_max
        ])
    else:
        return len([
            True
            for syls in syls_words
            if len(syls) >= len_min
        ])

def get_count_words_outside_wordlist(words, wordlist):
    easy_words = set()
    count_difficult_words = 0

    # Load wordlist
    if wordlist == 'dale_769':
        file_name = 'dale_list_easy_words_769'
    elif wordlist == 'dale_3000':
        file_name = 'dale_list_easy_words_3000'
    elif wordlist == 'spache':
        file_name = 'spache_word_list'

    with open(wl_paths.get_path_data(f'{file_name}.txt'), 'r', encoding = 'utf_8') as f:
        for line in f:
            word = line.strip()

            if word:
                # Ignore case
                easy_words.add(word.lower())

    for word in words:
        if word.lower() not in easy_words:
            count_difficult_words += 1

    return count_difficult_words

# Automated Arabic Readability Index
# Reference: Al-Tamimi, A., Jaradat M., Aljarrah, N., & Ghanim, S. (2013). AARI: Automatic Arabic readability index. The International Arab Journal of Information Technology, 11(4), pp. 370–378.
def aari(main, text):
    if text.lang == 'ara':
        text = get_counts(main, text)

        if text.count_words and text.count_sentences:
            aari = (
                3.28 * text.count_chars_alphanumeric
                + 1.43 * (text.count_chars_alphanumeric / text.count_words)
                + 1.24 * (text.count_words / text.count_sentences)
            )
        else:
            aari = 'text_too_short'
    else:
        aari = 'no_support'

    return aari

# Automated Readability Index
# Reference:
#     Smith, E. A., & Senter, R. J. (1967). Automated readability index. Aerospace Medical Research Laboratories. https://apps.dtic.mil/sti/pdfs/AD0667273.pdf
# Navy variant:
#     Kincaid, J. P., Fishburne, R. P., Rogers, R. L., & Chissom, B. S. (1975). Derivation of new readability formulas (automated readability index, fog count, and Flesch reading ease formula) for Navy enlisted personnel (Report No. RBR 8-75). Naval Air Station Memphis. https://apps.dtic.mil/sti/pdfs/ADA006655.pdf
def ari(main, text):
    text = get_counts(main, text)

    if text.count_sentences and text.count_words:
        if main.settings_custom['measures']['readability']['ari']['use_navy_variant']:
            ari = (
                0.37 * (text.count_words / text.count_sentences)
                + 5.84 * (text.count_chars_all / text.count_words)
                - 26.01
            )
        else:
            ari = (
                0.5 * (text.count_words / text.count_sentences)
                + 4.71 * (text.count_chars_all / text.count_words)
                - 21.43
            )
    else:
        ari = 'text_too_short'

    return ari

# Bormuth's Cloze Mean & Grade Placement
# Reference: Bormuth, J. R. (1969). Development of readability analyses. U.S. Department of Health, Education, and Welfare. http://files.eric.ed.gov/fulltext/ED029166.pdf
def bormuths_cloze_mean(main, text):
    if text.lang.startswith('eng_'):
        text = get_counts(main, text)

        if text.count_sentences and text.count_words:
            ddl = get_count_words_outside_wordlist(text.words_flat, wordlist = 'dale_3000')
            m = (
                0.886593
                - 0.083640 * (text.count_chars_alphabetic / text.count_words)
                + 0.161911 * ((ddl / text.count_words)**3)
                - 0.021401 * (text.count_words / text.count_sentences)
                + 0.000577 * ((text.count_words / text.count_sentences)**2)
                - 0.000005 * ((text.count_words / text.count_sentences)**3)
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

# Coleman-Liau Index
# Reference: Coleman, M., & Liau, T. L. (1975). A computer readability formula designed for machine scoring. Journal of Applied Psychology, 60(2), 283–284. https://doi.org/10.1037/h0076540
def coleman_liau_index(main, text):
    text = get_counts(main, text)

    if text.count_words:
        est_cloze_pct = (
            141.8401
            - 0.21459 * (text.count_chars_alphabetic / text.count_words * 100)
            + 1.079812 * (text.count_sentences / text.count_words * 100)
        )
        grade_level = -27.4004 * (est_cloze_pct / 100) + 23.06395
    else:
        grade_level = 'text_too_short'

    return grade_level

# Coleman's Readability Formula
# Reference: Liau, T. L., Bassin, C. B., Martin, C. J., & Coleman, E. B. (1976). Modification of the Coleman readability formulas. Journal of Reading Behavior, 8(4), 381–386. https://journals.sagepub.com/doi/pdf/10.1080/10862967609547193
def colemans_readability_formula(main, text):
    if text.lang.startswith('eng_'):
        text = get_counts(main, text)

        if text.count_words:
            variant = main.settings_custom['measures']['readability']['colemans_readability_formula']['variant']
            count_words_1_syl = get_count_words_syls(text.syls_words, len_min = 1, len_max = 1)

            if variant in ['3', '4']:
                pos_tags = wl_pos_tagging.wl_pos_tag(main, text.words_flat, lang = text.lang, tagset = 'universal')
                count_prons = sum((1 for _, pos in pos_tags if pos == 'PRON'))

                if variant == '4':
                    count_preps = sum((1 for _, pos in pos_tags if pos == 'ADP'))

            if variant == '1':
                cloze_pct = (
                    1.29 * (count_words_1_syl / text.count_words * 100)
                    - 38.45
                )
            elif variant == '2':
                cloze_pct = (
                    1.16 * (count_words_1_syl / text.count_words * 100)
                    + 1.48 * (text.count_sentences / text.count_words * 100)
                    - 37.95
                )
            elif variant == '3':
                cloze_pct = (
                    1.07 * (count_words_1_syl / text.count_words * 100)
                    + 1.18 * (text.count_sentences / text.count_words * 100)
                    + 0.76 * (count_prons / text.count_words * 100)
                    - 34.02
                )
            elif variant == '4':
                cloze_pct = (
                    1.04 * (count_words_1_syl / text.count_words * 100)
                    + 1.06 * (text.count_sentences / text.count_words * 100)
                    + 0.56 * (count_prons / text.count_words * 100)
                    - 0.36 * (count_preps / text.count_words)
                    - 26.01
                )
        else:
            cloze_pct = 'text_too_short'
    else:
        cloze_pct = 'no_support'

    return cloze_pct

# Dale-Chall Readability Formula
# References:
#     Dale, E., & Chall, J. S. (1948a). A formula for predicting readability. Educational Research Bulletin, 27(1), 11–20, 28.
#     Dale, E., & Chall, J. S. (1948b). A formula for predicting readability: Instructions. Educational Research Bulletin, 27(2), 37–54.
def dale_chall_readability_formula(main, text):
    if text.lang.startswith('eng_'):
        text = get_counts(main, text)

        if text.count_words and text.count_sentences:
            count_difficult_words = get_count_words_outside_wordlist(text.words_flat, wordlist = 'dale_3000')
            x_c50 = (
                0.1579 * (count_difficult_words / text.count_words * 100)
                + 0.0496 * (text.count_words / text.count_sentences)
                + 3.6365
            )
        else:
            x_c50 = 'text_too_short'
    else:
        x_c50 = 'no_support'

    return x_c50

# Dale-Chall Readability Formula (New)
# References:
#     Chall, J. S., & Dale, E. (1995). Readability revisited: The new Dale-Chall readability formula. Brookline Books.
#     清川英男. (1996). CHALL, J. S. and DALE, E.(1995) Readability Revisited: The New Dale-Chall Readability Formula. Brookline Books. 教育メディア研究, 3(1), 59. https://www.jstage.jst.go.jp/article/jaems/3/1/3_KJ00009004543/_pdf
def dale_chall_readability_formula_new(main, text):
    if text.lang.startswith('eng_'):
        text = get_counts(main, text)

        if text.count_words and text.count_sentences:
            count_difficult_words = get_count_words_outside_wordlist(text.words_flat, wordlist = 'dale_3000')
            x_c50 = (
                64
                - 0.95 * (count_difficult_words / text.count_words * 100)
                - 0.69 * (text.count_words / text.count_sentences)
            )
        else:
            x_c50 = 'text_too_short'
    else:
        x_c50 = 'no_support'

    return x_c50

# Danielson-Bryan's Readability Formula
# Reference: Danielson, W. A., & Bryan, S. D. (1963). Computer automation of two readability formulas. Journalism Quarterly, 40(2), 201–206. https://doi.org/10.1177/107769906304000207
def danielson_bryans_readability_formula(main, text):
    text = get_counts(main, text)

    if text.count_words - 1 and text.count_sentences:
        variant = main.settings_custom['measures']['readability']['danielson_bryans_readability_formula']['variant']

        if variant == '1':
            danielson_bryan = (
                1.0364 * (text.count_chars_all / (text.count_words - 1))
                + 0.0194 * (text.count_chars_all / text.count_sentences)
                - 0.6059
            )
        elif variant == '2':
            danielson_bryan = (
                131.059
                - 10.364 * (text.count_chars_all / (text.count_words - 1))
                - 0.194 * (text.count_chars_all / text.count_sentences)
            )
    else:
        danielson_bryan = 'text_too_short'

    return danielson_bryan

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
    text = get_counts(main, text)

    if text.count_words and text.count_sentences:
        grade_placement = (
            1.56 * (text.count_chars_all / text.count_words)
            + 0.19 * (text.count_words / text.count_sentences)
            - 6.49
        )
    else:
        grade_placement = 'text_too_short'

    return grade_placement

# Easy Listening Formula
# Reference: Fang, I. E. (1966). The easy listening formula. Journal of Broadcasting, 11(1), 63–68. https://doi.org/10.1080/08838156609363529
def elf(main, text):
    if text.lang in main.settings_global['syl_tokenizers']:
        text = get_counts(main, text)

        if text.count_sentences:
            elf = (text.count_syls - text.count_words) / text.count_sentences
        else:
            elf = 'text_too_short'
    else:
        elf = 'no_support'

    return elf

# Flesch-Kincaid Grade Level
# Reference: Kincaid, J. P., Fishburne, R. P., Rogers, R. L., & Chissom, B. S. (1975). Derivation of new readability formulas (automated readability index, fog count, and Flesch reading ease formula) for Navy enlisted personnel (Report No. RBR 8-75). Naval Air Station Memphis. https://apps.dtic.mil/sti/pdfs/ADA006655.pdf
def gl(main, text):
    if text.lang in main.settings_global['syl_tokenizers']:
        text = get_counts(main, text)

        if text.count_sentences and text.count_words:
            gl = (
                0.39 * (text.count_words / text.count_sentences)
                + 11.8 * (text.count_syls / text.count_words)
                - 15.59
            )
        else:
            gl = 'text_too_short'
    else:
        gl = 'no_support'

    return gl

# Flesch Reading Ease
# Reference:
#     Flesch, R. (1948). A new readability yardstick. Journal of Applied Psychology, 32(3), 221–233. https://doi.org/10.1037/h0057532
# Dutch variant (Douma):
#     Douma, W. H. (1960). De leesbaarheid van landbouwbladen: Een onderzoek naar en een toepassing van leesbaarheidsformules [Readability of Dutch farm papers: A discussion and application of readability-formulas]. Afdeling sociologie en sociografie van de Landbouwhogeschool Wageningen. https://edepot.wur.nl/276323
# Dutch variant (Brouwer's Leesindex A):
#     Brouwer, R. H. M. (1963). Onderzoek naar de leesmoeilijkheid van Nederlands proza. Paedagogische studiën, 40, 454–464. https://objects.library.uu.nl/reader/index.php?obj=1874-205260&lan=en
# French variant:
#     Kandel, L., & Moles A. (1958). Application de l’indice de flesch la langue francaise [applying flesch index to french language]. The Journal of Educational Research, 21, 283–287.
#     Kopient, A., & Grabar, N. (2020). Rated lexicon for the simplification of medical texts. In B.  Gersbeck-Schierholz (ed.), HEALTHINFO 2020: The fifth international conference on informatics and assistive technologies for health-care, medical support and wellbeing (pp. 11–17). IARIA. https://hal.science/hal-03095275/document
# German variant:
#     Amstad, T. (1978). Wie verständlich sind unsere Zeitungen? [Unpublished doctoral dissertation]. University of Zurich.
#     Lesbarkeitsindex. (2023, February 2). In Wikipedia. https://de.wikipedia.org/w/index.php?title=Lesbarkeitsindex&oldid=230472824
# Italian variant:
#     Franchina, V., & Vacca, R. (1986). Adaptation of Flesh readability index on a bilingual text written by the same author both in Italian and English languages. Linguaggi, 3, 47–49.
#     Garais, E. (2011). Web applications readability. Journal of Information Systems and Operations Management, 5(1), 117–121. http://www.rebe.rau.ro/RePEc/rau/jisomg/SP11/JISOM-SP11-A13.pdf
# Russian variant:
#     Oborneva, I. V. (2006). Автоматизированная оценка сложности учебных текстов на основе статистических параметров [Doctoral dissertation, Institute for Strategy of Education Development of the Russian Academy of Education]. Freereferats.ru. https://static.freereferats.ru/_avtoreferats/01002881899.pdf?ver=3
# Spanish variant (Fernández Huerta):
#     Fernández Huerta, J. (1959). Medidas sencillas de lecturabilidad. Consigna, 214, 29–32.
#     Garais, E. (2011). Web applications readability. Journal of Information Systems and Operations Management, 5(1), 117–121. http://www.rebe.rau.ro/RePEc/rau/jisomg/SP11/JISOM-SP11-A13.pdf
# Spanish variant (Szigriszt Pazos):
#     Szigriszt Pazos, F. (1993). Sistemas predictivos de legibilidad del mensaje escrito: Formula de perspicuidad [Doctoral dissertation, Complutense University of Madrid]. Biblos-e Archivo. https://repositorio.uam.es/bitstream/handle/10486/2488/3907_barrio_cantalejo_ines_maria.pdf?sequence=1&isAllowed=y
def re_flesch(main, text):
    if text.lang in main.settings_global['syl_tokenizers']:
        text = get_counts(main, text)

        if text.count_words and text.count_sentences:
            if text.lang == 'nld':
                if main.settings_custom['measures']['readability']['re']['variant_nld'] == 'Douma':
                    re = (
                        206.84
                        - 77 * (text.count_syls / text.count_words)
                        - 0.93 * (text.count_words / text.count_sentences)
                    )
                elif main.settings_custom['measures']['readability']['re']['variant_nld'] == "Brouwer's Leesindex A":
                    re = (
                        195
                        - (200 / 3) * (text.count_syls / text.count_words)
                        - 2 * (text.count_words / text.count_sentences)
                    )
            elif text.lang == 'fra':
                re = (
                    207
                    - 73.6 * (text.count_syls / text.count_words)
                    - 1.015 * (text.count_words / text.count_sentences)
                )
            elif text.lang.startswith('deu_'):
                re = (
                    180
                    - 58.5 * (text.count_syls / text.count_words)
                    - (text.count_words / text.count_sentences)
                )
            elif text.lang == 'ita':
                re = (
                    217
                    - 60 * (text.count_syls / text.count_words)
                    - 1.3 * (text.count_words / text.count_sentences)
                )
            elif text.lang == 'rus':
                re = (
                    206.835
                    - 60.1 * (text.count_syls / text.count_words)
                    - 1.3 * (text.count_words / text.count_sentences)
                )
            elif text.lang == 'spa':
                if main.settings_custom['measures']['readability']['re']['variant_spa'] == 'Fernández Huerta':
                    re = (
                        206.84
                        - 60 * (text.count_syls / text.count_words)
                        - 1.02 * (text.count_words / text.count_sentences)
                    )
                elif main.settings_custom['measures']['readability']['re']['variant_spa'] == 'Szigriszt Pazos':
                    re = (
                        206.84
                        - 62.3 * (text.count_syls / text.count_words)
                        - (text.count_words / text.count_sentences)
                    )
            else:
                re = (
                    206.835
                    - 0.846 * (text.count_syls / text.count_words * 100)
                    - 1.015 * (text.count_words / text.count_sentences)
                )
        else:
            re = 'text_too_short'
    else:
        re = 'no_support'

    return re

# Flesch Reading Ease (Simplified)
# Reference: Farr, J. N., Jenkins, J. J., & Paterson, D. G. (1951). Simplification of Flesch reading ease formula. Journal of Applied Psychology, 35(5), 333–337. https://doi.org/10.1037/h0062427
def re_simplified(main, text):
    if text.lang in main.settings_global['syl_tokenizers']:
        text = get_counts(main, text)

        if text.count_words and text.count_sentences:
            count_words_1_syl = get_count_words_syls(text.syls_words, len_min = 1, len_max = 1)

            flesch_re_simplified = (
                1.599 * (count_words_1_syl / text.count_words * 100)
                - 1.015 * (text.count_words / text.count_sentences)
                - 31.517
            )
        else:
            flesch_re_simplified = 'text_too_short'
    else:
        flesch_re_simplified = 'no_support'

    return flesch_re_simplified

# FORCAST Grade Level
# Reference: Caylor, J. S., Sticht, T. G., Fox, L. C., & Ford, J. P. (1973). Methodologies for determining reading requirements of military occupational specialties. Human Resource Research Organization. https://files.eric.ed.gov/fulltext/ED074343.pdf
def rgl(main, text):
    if text.lang in main.settings_global['syl_tokenizers']:
        text = get_counts(main, text)

        if text.count_words >= 150:
            sample_start = random.randint(0, text.count_words - 150)
            sample = text.syls_words[sample_start : sample_start + 150]

            count_words_1_syl = get_count_words_syls(sample, len_min = 1, len_max = 1)
            rgl = 20.43 - 0.11 * count_words_1_syl
        else:
            rgl = 'text_too_short'
    else:
        rgl = 'no_support'

    return rgl

# Fórmula de Comprensibilidad de Gutiérrez de Polini
# References:
#     Gutiérrez de Polini, L. E. (1972). Investigación sobre lectura en Venezuela [Paper presentation]. Primeras Jornadas de Educación Primaria, Ministerio de Educación, Caracas, Venezuela.
#     Rodríguez Trujillo, N. (1980). Determinación de la comprensibilidad de materiales de lectura por medio de variables lingüísticas. Lectura y Vida, 1(1). http://www.lecturayvida.fahce.unlp.edu.ar/numeros/a1n1/01_01_Rodriguez.pdf
def cp(main, text):
    if text.lang == 'spa':
        text = get_counts(main, text)

        if text.count_words and text.count_sentences:
            cp = (
                95.2
                - 9.7 * (text.count_chars_alphabetic / text.count_words)
                - 0.35 * (text.count_words / text.count_sentences)
            )
        else:
            cp = 'text_too_short'
    else:
        cp = 'no_support'

    return cp

# Fórmula de Crawford
# Reference: Crawford, A. N. (1985). Fórmula y gráfico para determinar la comprensibilidad de textos de nivel primario en castellano. Lectura y Vida, 6(4). http://www.lecturayvida.fahce.unlp.edu.ar/numeros/a6n4/06_04_Crawford.pdf
def formula_de_crawford(main, text):
    if text.lang == 'spa' and text.lang in main.settings_global['syl_tokenizers']:
        text = get_counts(main, text)

        if text.count_words:
            grade_level = (
                text.count_sentences / text.count_words * 100 * (-0.205)
                + text.count_syls / text.count_words * 100 * 0.049
                - 3.407
            )
        else:
            grade_level = 'text_too_short'
    else:
        grade_level = 'no_support'

    return grade_level

# Fucks's Stilcharakteristik
# References:
#     Fucks, W. (1955). Unterschied des Prosastils von Dichtern und anderen Schriftstellern: ein Beispiel mathematischer Stilanalyse. Bouvier.
#     Briest, W. (1974). Kann man Verständlichkeit messen?. STUF - Language Typology and Universals, 27(1-3), 543–563. https://doi.org/10.1524/stuf.1974.27.13.543
def fuckss_stilcharakteristik(main, text):
    if text.lang in main.settings_global['syl_tokenizers']:
        text = get_counts(main, text)

        if text.count_sentences:
            stilcharakteristik = text.count_syls / text.count_sentences
        else:
            stilcharakteristik = 'text_too_short'
    else:
        stilcharakteristik = 'no_support'

    return stilcharakteristik

# Gulpease Index
# References:
#     Lucisano, P., & Emanuela Piemontese, M. (1988). GULPEASE: A formula for the prediction of the difficulty of texts in Italian. Scuola e Città, 39(3), pp. 110–124.
#     Indice Gulpease. (2021, July 9). In Wikipedia.https://it.wikipedia.org/w/index.php?title=Indice_Gulpease&oldid=121763335.
def gulpease_index(main, text):
    if text.lang == 'ita':
        text = get_counts(main, text)

        if text.count_words:
            gulpease_index = (
                89
                + (300 * text.count_sentences - 10 * text.count_chars_alphabetic) / text.count_words
            )
        else:
            gulpease_index = 'text_too_short'
    else:
        gulpease_index = 'no_support'

    return gulpease_index

# Gunning Fog Index
# Reference:
#     Gunning, R. (1968). The technique of clear writing (revised ed.). McGraw-Hill Book Company.
# Navy variant:
#     Kincaid, J. P., Fishburne, R. P., Rogers, R. L., & Chissom, B. S. (1975). Derivation of new readability formulas (automated readability index, fog count, and Flesch reading ease formula) for Navy enlisted personnel (Report No. RBR 8-75). Naval Air Station Memphis. https://apps.dtic.mil/sti/pdfs/ADA006655.pdf
# Polish variant:
#     Pisarek, W. (1969). Jak mierzyć zrozumiałość tekstu?. Zeszyty Prasoznawcze, 4(42), 35–48.
def fog_index(main, text):
    if text.lang.startswith('eng_') or text.lang == 'pol':
        text = get_counts(main, text)

        if text.count_sentences and text.count_words:
            count_hard_words = 0

            if text.lang.startswith('eng_'):
                if main.settings_custom['measures']['readability']['fog_index']['use_navy_variant_for_eng']:
                    count_words_3_plus_syls = get_count_words_syls(text.syls_words, len_min = 3)
                else:
                    words_tagged = wl_pos_tagging.wl_pos_tag(main, text.words_flat, lang = text.lang, tagset = 'universal')

                    for syls, (word, tag) in zip(text.syls_words, words_tagged):
                        if (
                            tag != 'PROPN'
                            and (
                                (len(syls) == 3 and not word.endswith('ed') and not word.endswith('es'))
                                or len(syls) > 3
                            )
                        ):
                            count_hard_words += 1
            elif text.lang == 'pol':
                for syls in text.syls_words:
                    if len(syls) >= 4:
                        count_hard_words += 1

            if text.lang.startswith('eng_') and main.settings_custom['measures']['readability']['fog_index']['use_navy_variant_for_eng']:
                fog_index = ((text.count_words + 2 * count_words_3_plus_syls) / text.count_sentences - 3) / 2
            else:
                fog_index = (
                    0.4
                    * (text.count_words / text.count_sentences + count_hard_words / text.count_words * 100)
                )
        else:
            fog_index = 'text_too_short'
    else:
        fog_index = 'no_support'

    return fog_index

# Legibilidad µ
# Reference: Muñoz Baquedano, M. (2006). Legibilidad y variabilidad de los textos. Boletín de Investigación Educacional, Pontificia Universidad Católica de Chile, 21(2), 13–26.
def mu(main, text):
    if text.lang == 'spa':
        text = get_counts(main, text)

        if text.count_words >= 2:
            # Excluding numbers and punctuation marks
            lens_words_letters = numpy.array([
                len([char for char in word if char.isalpha()])
                for word in text.words_flat
            ])

            mu = (
                (text.count_words / (text.count_words - 1))
                * (numpy.mean(lens_words_letters) / numpy.var(lens_words_letters))
                * 100
            )
        else:
            mu = 'text_too_short'
    else:
        mu = 'no_support'

    return mu

# Lensear Write
# Reference: O’Hayre, J. (1966). Gobbledygook has gotta go. U.S. Government Printing Office. https://www.governmentattic.org/15docs/Gobbledygook_Has_Gotta_Go_1966.pdf
def lensear_write(main, text):
    if text.lang.startswith('eng_') and text.lang in main.settings_global['syl_tokenizers']:
        text = get_counts(main, text)

        if text.count_words > 0:
            if text.count_words > 100:
                sample_start = random.randint(0, text.count_words - 100)
            else:
                sample_start = 0

            sample = text.words_flat[sample_start : sample_start + 100]

            count_words_monosyllabic = 0
            sysl_sample = wl_syl_tokenization.wl_syl_tokenize(main, sample, lang = text.lang)

            for syls in sysl_sample:
                if len(syls) == 1 and syls[0].lower() not in ['the', 'is', 'are', 'was', 'were']:
                    count_words_monosyllabic += 1

            offsets_sentences = []
            offsets_sentences = []
            num_tokens = 0

            for sentence in text.sentences:
                offsets_sentences.append(num_tokens)

                num_tokens += len(sentence)

            count_sentences_sample = bisect.bisect(offsets_sentences, sample_start + 100)

            # Normalize counts if number of tokens is less than 100
            if text.count_words < 100:
                count_words_monosyllabic *= 100 / text.count_words
                count_sentences_sample *= 100 / text.count_words

            score = count_words_monosyllabic + 3 * count_sentences_sample
        else:
            score = 'text_too_short'
    else:
        score = 'no_support'

    return score

# Lix
# References:
#     Björnsson, C.-H. (1968). Läsbarhet. Liber.
#     Anderson, J. (1983). Lix and Rix: Variations on a little-known readability index. Journal of Reading, 26(6), pp. 490–496.
def lix(main, text):
    if text.count_words and text.count_sentences:
        text = get_counts(main, text)

        count_long_words = get_count_words_letters(text.words_flat, len_min = 7)
        lix = text.count_words / text.count_sentences + 100 * (count_long_words / text.count_words)
    else:
        lix = 'text_too_short'

    return lix

# McAlpine EFLAW Readability Score
# Reference: Nirmaldasan. (2009, April 30). McAlpine EFLAW readability score. Readability Monitor. Retrieved November 15, 2022, from https://strainindex.wordpress.com/2009/04/30/mcalpine-eflaw-readability-score/
def eflaw(main, text):
    if text.lang.startswith('eng_'):
        text = get_counts(main, text)

        if text.count_sentences:
            count_mini_words = get_count_words_letters(text.words_flat, len_max = 3)
            eflaw = (text.count_words + count_mini_words) / text.count_sentences
        else:
            eflaw = 'text_too_short'
    else:
        eflaw = 'no_support'

    return eflaw

# Estimate number of syllables in Arabic texts by counting short, long, and stress syllables
# Reference: https://github.com/textstat/textstat/blob/9bf37414407bcaaa45c498478ee383c8738e5d0c/textstat/textstat.py#L569
def _get_count_syls_ara(text):
    short_count = 0
    long_count = 0

    # tashkeel: fatha | damma | kasra
    tashkeel = [r'\u064E', r'\u064F', r'\u0650']
    char_list = list(re.sub(r"[^\w\s\']", '', text))

    for t in tashkeel:
        for i, c in enumerate(char_list):
            if c != t:
                continue

            # Only if a character is a tashkeel, has a successor and is followed by an alef, waw or yaaA
            if (
                i + 1 < len(char_list)
                and char_list[i + 1] in ['\u0627', '\u0648', '\u064a']
            ):
                long_count += 1
            else:
                short_count += 1

    # stress syllables: tanween fatih | tanween damm | tanween kasr | shadda
    stress_pattern = re.compile(r'[\u064B\u064C\u064D\u0651]')
    stress_count = len(stress_pattern.findall(text))

    if short_count == 0:
        text = re.sub(r'[\u0627\u0649\?\.\!\,\s*]', '', text)
        short_count = len(text) - 2

    return short_count + 2 * (long_count + stress_count)

# OSMAN
# Reference: El-Haj, M., & Rayson, P. (2016). OSMAN: A novel Arabic readability metric. In N. Calzolari, K. Choukri, T. Declerck, S. Goggi, M. Grobelnik, B. Maegaard, J. Mariani, H. Mazo, A. Moreno, J. Odijk, & S. Piperidis (Eds.), Proceedings of the Tenth International Conference on Language Resources and Evaluation (LREC 2016) (pp. 250–255). European Language Resources Association. http://www.lrec-conf.org/proceedings/lrec2016/index.html
def osman(main, text):
    if text.lang == 'ara':
        text = get_counts(main, text)

        if text.count_sentences and text.count_words:
            counts_syls_tokens = numpy.array([_get_count_syls_ara(word) for word in text.words_flat])

            a = text.count_words
            b = text.count_sentences
            c = get_count_words_letters(text.words_flat, len_min = 6)
            d = numpy.sum(counts_syls_tokens)
            g = numpy.sum(counts_syls_tokens > 4)
            h = 0

            for word, count_syls in zip(text.words_flat, counts_syls_tokens):
                if (
                    count_syls > 4
                    and (
                        any((letter in word for letter in ['ء', 'ئ', 'ؤ', 'ذ', 'ظ']))
                        or any((word.endswith(letters) for letters in ['وا', 'ون']))
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
# Reference: Anderson, J. (1983). Lix and Rix: Variations on a little-known readability index. Journal of Reading, 26(6), pp. 490–496.
def rix(main, text):
    text = get_counts(main, text)

    if text.count_sentences:
        count_long_words = get_count_words_letters(text.words_flat, len_min = 7)
        rix = count_long_words / text.count_sentences
    else:
        rix = 'text_too_short'

    return rix

# SMOG Grade
# Reference: McLaughlin, G. H. (1969). SMOG grading: A new readability formula. Journal of Reading, 12(8), pp. 639–646.
def smog_grade(main, text):
    if text.lang in main.settings_global['syl_tokenizers']:
        text = get_counts(main, text)

        if text.count_sentences >= 30:
            # Calculate the index for the 10 sentences at the middle of the text
            sample_start_mid = text.count_sentences // 2 - 5
            sample = (
                text.sentences[:10]
                + text.sentences[sample_start_mid : sample_start_mid + 10]
                + text.sentences[-10:]
            )

            # Calculate the number of words with 3 or more syllables
            count_words_3_plus_syls = 0

            for sentence in sample:
                syls_words = wl_syl_tokenization.wl_syl_tokenize(main, sentence, lang = text.lang)

                count_words_3_plus_syls += get_count_words_syls(syls_words, len_min = 3)

            g = 3.1291 + 1.043 * (count_words_3_plus_syls ** 0.5)
        else:
            g = 'text_too_short'
    else:
        g = 'no_support'

    return g

# Spache Grade Level
# References:
#     Spache, G. (1953). A new readability formula for primary-grade reading materials. Elementary School Journal, 53(7), 410–413. https://doi.org/10.1086/458513
#     Spache, G. (1974). Good reading for poor readers (Rev. 9th ed.). Garrard.
#     Michalke, M., Brown, E., Mirisola, A., Brulet, A., & Hauser, L. (2021, May 17). Measure readability. Documentation for package ‘koRpus’ version 0.13-8. Retrieved August 3, 2023, from https://search.r-project.org/CRAN/refmans/koRpus/html/readability-methods.html
# Spache word list:
#     Benoit, K., Watanabe, K., Wang, H., Nulty, P., Obeng, A., Müller, S., & Matsuo, A. (2020, November 17). data_char_wordlists.rda. quanteda.textstats. Retrieved August 3, 2023, from https://github.com/quanteda/quanteda.textstats/raw/master/data/data_char_wordlists.rda
def spache_grade_lvl(main, text):
    if text.lang.startswith('eng_'):
        text = get_counts(main, text)

        if text.count_words >= 100:
            grade_lvls = []

            # Sample 3 times
            for _ in range(3):
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

                if main.settings_custom['measures']['readability']['spache_grade_lvl']['use_rev_formula']:
                    count_difficult_words = get_count_words_outside_wordlist(samples, wordlist = 'spache')
                    grade_lvls.append(
                        0.121 * (100 / count_sentences_samples)
                        + 0.082 * (count_difficult_words)
                        + 0.659
                    )
                else:
                    count_difficult_words = get_count_words_outside_wordlist(samples, wordlist = 'dale_769')
                    grade_lvls.append(
                        0.141 * (100 / count_sentences_samples)
                        + 0.086 * (count_difficult_words)
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
#     Solomon, N. W. (2006). Qualitative analysis of media language [Unpublished doctoral dissertation]. Madurai Kamaraj University.
#     Nirmaldasan. (2007, September 25). Strain index: A new readability formula. Readability Monitor. Retrieved August 3, 2023, from https://strainindex.wordpress.com/2007/09/25/hello-world/
def strain_index(main, text):
    if text.lang in main.settings_global['syl_tokenizers']:
        text = get_counts(main, text)

        if text.count_sentences >= 3:
            count_syls = 0

            for sentence in text.sentences[:3]:
                syls_words = wl_syl_tokenization.wl_syl_tokenize(main, sentence, lang = text.lang)

                count_syls += sum((len(syls) for syls in syls_words))

            strain_index = count_syls / 10
        else:
            strain_index = 'text_too_short'
    else:
        strain_index = 'no_support'

    return strain_index

# Wiener Sachtextformel
# References:
#     Bamberger, R., & Vanecek, E. (1984). Lesen – Verstehen – Lernen – Schreiben. Jugend und Volk.
#     Lesbarkeitsindex. (2022, July 21). In Wikipedia. https://de.wikipedia.org/w/index.php?title=Lesbarkeitsindex&oldid=224664667
def wstf(main, text):
    if text.lang.startswith('deu_') and text.lang in main.settings_global['syl_tokenizers']:
        text = get_counts(main, text)

        if text.count_words and text.count_sentences:
            variant = main.settings_custom['measures']['readability']['wstf']['variant']
            ms = get_count_words_syls(text.syls_words, len_min = 3) / text.count_words
            sl = text.count_words / text.count_sentences
            iw = get_count_words_letters(text.words_flat, len_min = 7) / text.count_words
            es = get_count_words_syls(text.syls_words, len_min = 1, len_max = 1) / text.count_words

            if variant == '1':
                wstf = 0.1925 * ms + 0.1672 * sl + 0.1297 * iw - 0.0327 * es - 0.875
            elif variant == '2':
                wstf = 0.2007 * ms + 0.1682 * sl + 0.1373 * iw - 2.779
            elif variant == '3':
                wstf = 0.2963 * ms + 0.1905 * sl - 1.1144
            elif variant == '4':
                wstf = 0.2744 * ms + 0.2656 * sl - 1.693
        else:
            wstf = 'text_too_short'
    else:
        wstf = 'no_support'

    return wstf
