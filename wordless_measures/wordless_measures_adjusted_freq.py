#
# Wordless: Measures - Adjusted Frequency
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import math

import numpy
import scipy.special

# Euler-Mascheroni Constant
C = -scipy.special.digamma(1)

# Reference:
#     Juilland, Alphonse and Eugenio Chang-Rodriguez. Frequency Dictionary of Spanish Words, Mouton, 1964.
def juillands_u(freqs):
    if sum(freqs) == 0:
        d = 0
    else:
        cv = numpy.std(freqs) / numpy.mean(freqs)
    
        d = 1 - cv / math.sqrt(len(freqs) - 1)

    return max(0, d) * sum(freqs)

# Reference:
#     Carroll, John B. "An alternative to Juilland’s usage coefficient for lexical frequencies and a proposal for a standard frequency index." Computer Studies in the Humanities and Verbal Behaviour, vol.3, no. 2, 1970, pp. 61-65.
def carrolls_um(freqs):
    h = 0
    freq_total = sum(freqs)

    if freq_total == 0:
        d2 = 0
    else:
        for freq in freqs:
            if freq:
                h += freq * math.log(freq, math.e)

        d2 = (math.log(freq_total, math.e) - h / freq_total) / math.log(len(freqs), math.e)

    um = freq_total * d2 + (1 - d2) * freq_total / len(freqs)

    return um

# Reference:
#     Rosengren, Inger. "The Quantitative Concept of Language and Its Relation to The Structure of Frequency Dictionaries." Études De Linguistique Appliquée, n.s.1, 1971, pp. 103-27.
def rosengrens_kf(freqs):
    return sum([math.sqrt(freq) for freq in freqs]) ** 2 / len(freqs)

# Reference:
#     Engwall, Gunnel. "Fréquence Et Distribution Du Vocabulaire Dans Un Choix De Romans Français, Dissertation", Stockholm University, 1974.
def engwalls_fm(freqs):
    return sum(freqs) * len([freq for freq in freqs if freq]) / len(freqs)

# Reference:
#     Kromer, Victor. "A Usage Measure Based on Psychophysical Relations." Journal of Quatitative Linguistics, vol. 10, no. 2, 2003, pp. 177-186.
def kromers_ur(freqs):
    return sum([scipy.special.digamma(freq + 1) + C for freq in freqs])

# Testing
if __name__ == '__main__':
    # [1] Carroll, John B. "An alternative to Juilland’s usage coefficient for lexical frequencies and a proposal for a standard frequency index." Computer Studies in the Humanities and Verbal Behaviour, vol.3, no. 2, 1970, pp. 61-65.
    # [2] Rosengren, Inger. "The quantitative concept of language and its relation to the structure of frequency dictionaries." Études de linguistique appliquée, no. 1, 1971, p. 115.
    # [3] Engwall, Gunnel. "Fréquence Et Distribution Du Vocabulaire Dans Un Choix De Romans Français, Dissertation", Stockholm University, 1974, p. 122.
    print('Juilland\'s U:')
    print(f'\t[1] {juillands_u([0, 4, 3, 2, 1])} (6.46)')
    print(f'\t[2] {juillands_u([2, 2, 2, 2, 2])} (10)')
    print(f'\t[3] {juillands_u([4, 2, 1, 1, 0])} (4.609)')

    # [1] Carroll, John B. "An alternative to Juilland’s usage coefficient for lexical frequencies and a proposal for a standard frequency index." Computer Studies in the Humanities and Verbal Behaviour, vol.3, no. 2, 1970, pp. 61-65.
    # [2] Engwall, Gunnel. "Fréquence Et Distribution Du Vocabulaire Dans Un Choix De Romans Français, Dissertation", Stockholm University, 1974, p. 122.
    # [3] Gries, Stefan Th. "Dispersions and Adjusted Frequencies in Corpora." International Journal of Corpus Linguistics, vol. 13, no. 4, 2008, p. 409.
    print('Carroll\'s Um:')
    print(f'\t[1] {carrolls_um([2, 1, 1, 1, 0])} (4.31)')
    print(f'\t[2] {carrolls_um([4, 2, 1, 1, 0])} (6.424)')
    print(f'\t[3] {carrolls_um([1, 2, 3, 4, 5])} (14.108)')

    # [1] Rosengren, Inger. "The quantitative concept of language and its relation to the structure of frequency dictionaries." Études de linguistique appliquée, no. 1, 1971, p. 117.
    # [2] Engwall, Gunnel. "Fréquence Et Distribution Du Vocabulaire Dans Un Choix De Romans Français, Dissertation", Stockholm University, 1974, p. 122.
    # [3] Gries, Stefan Th. "Dispersions and Adjusted Frequencies in Corpora." International Journal of Corpus Linguistics, vol. 13, no. 4, 2008, p. 409.
    print('Rosengren\'s KF:')
    print(f'\t[1] {rosengrens_kf([2, 2, 2, 2, 1])} (8.86)')
    print(f'\t[2] {rosengrens_kf([4, 2, 1, 1, 0])} (5.863)')
    print(f'\t[2] {rosengrens_kf([1, 2, 3, 4, 5])} (14.053)')

    # [1] Engwall, Gunnel. "Fréquence Et Distribution Du Vocabulaire Dans Un Choix De Romans Français, Dissertation", Stockholm University, 1974, p. 122.
    # [2] Gries, Stefan Th. "Dispersions and Adjusted Frequencies in Corpora." International Journal of Corpus Linguistics, vol. 13, no. 4, 2008, p. 409.
    print('Engwall\'s FM:')
    print(f'\t[1] {engwalls_fm([4, 2, 1, 1, 0])} (6.4)')
    print(f'\t[2] {engwalls_fm([1, 2, 3, 4, 5])} (15)')

    # Gries, Stefan Th. "Dispersions and Adjusted Frequencies in Corpora." International Journal of Corpus Linguistics, vol. 13, no. 4, 2008, p. 409.
    print('Kromer\'s Ur:')
    print(f'\t{kromers_ur([2, 1, 1, 1, 0])} (4.50)')
