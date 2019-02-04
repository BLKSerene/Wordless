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
    if numpy.mean(freqs) == 0:
        d = 0
    else:
        cv = numpy.std(freqs) / numpy.mean(freqs)
    
        d = 1 - cv / math.sqrt(len(freqs) - 1)

    return max(0, d) * sum(freqs)

# Reference:
#     Carroll, John B. "An alternative to Juilland’s usage coefficient for lexical frequencies and a proposal for a standard frequency index." Computer Studies in the Humanities and Verbal Behaviour, vol.3, no. 2, 1970, pp. 61-65.
def carrolls_um(freqs):
    freq_total = sum(freqs)
    d2 = measures_dispersion.carrolls_d2(freqs)

    return freq_total * d2 + (1 - d2) * freq_total / len(freqs)

# Reference:
#     Rosengren, Inger. "The Quantitative Concept of Language and Its Relation to The Structure of Frequency Dictionaries." Études De Linguistique Appliquée, n.s.1, 1971, pp. 103-27.
def rosengrens_kf(freqs):
    return sum([math.sqrt(freq) for freq in freqs]) ** 2 / len(freqs)

# Reference:
#     Engwall, Gunnel. Fréquence Et Distribution Du Vocabulaire Dans Un Choix De Romans Français, Broché, 1974.
def engvalls_measure(freqs):
    return sum(freqs) * (len([freq for freq in freqs if freq]) / len(freqs))

# Reference:
#     Kromer, Victor. "A Usage Measure Based on Psychophysical Relations." Journal of Quatitative Linguistics, vol. 10, no. 2, 2003, pp. 177-186.
def kromers_ur(freqs):
    return sum([scipy.special.digamma(freq + 1) + C for freq in freqs])

# Testing
if __name__ == '__main__':
    # Carroll, John B. "An alternative to Juilland’s usage coefficient for lexical frequencies and a proposal for a standard frequency index." Computer Studies in the Humanities and Verbal Behaviour, vol.3, no. 2, 1970, pp. 61-65.
    print('Juilland\'s U:\n    ', end = '')
    print(juillands_u([0, 4, 3, 2, 1])) # 6.46

    # Carroll, John B. "An alternative to Juilland’s usage coefficient for lexical frequencies and a proposal for a standard frequency index." Computer Studies in the Humanities and Verbal Behaviour, vol.3, no. 2, 1970, pp. 61-65.
    print('Carroll\'s Um:\n    ', end = '')
    print(carrolls_um([2, 1, 1, 1, 0])) # 4.31

    # # Rosengren, Inger. "The quantitative concept of language and its relation to the structure of frequency dictionaries." Études de linguistique appliquée, no. 1, 1971, p. 117.
    print('Rosengren\'s KF:\n    ', end = '')
    print(rosengrens_kf([2, 2, 2, 2, 1])) # 8.86

    # Gries, Stefan Th. "Dispersions and Adjusted Frequencies in Corpora." International Journal of Corpus Linguistics, vol. 13, no. 4, 2008, p. 409.
    print('Engvall\'s Measure:\n    ', end = '')
    print(engvalls_measure([1, 2, 3, 4, 5])) # 15

    # Gries, Stefan Th. "Dispersions and Adjusted Frequencies in Corpora." International Journal of Corpus Linguistics, vol. 13, no. 4, 2008, p. 409.
    print('Kromer\'s Ur:\n    ', end = '')
    print(kromers_ur([2, 1, 1, 1, 0])) # 4.50
