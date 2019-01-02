#
# Wordless: Measures - Dispersion
#
# Copyright (C) 2018-2019 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import math

import numpy
import scipy.stats

# Reference:
#     Juilland, Alphonse and Eugenio Chang-Rodriguez. Frequency Dictionary of Spanish Words, Mouton, 1964.
def juillands_d(freqs):
    if sum(freqs) == 0:
        d = 0
    else:
        cv = numpy.std(freqs) / numpy.mean(freqs)
    
        d = 1 - cv / math.sqrt(len(freqs) - 1)

    return max(0, d)

# Reference:
#     Carroll, John B. "An alternative to Juilland’s usage coefficient for lexical frequencies and a proposal for a standard frequency index." Computer Studies in the Humanities and Verbal Behaviour, vol.3, no. 2, 1970, pp. 61-65.
def carrolls_d2(freqs):
    freq_total = sum(freqs)

    h = 0

    for freq in freqs:
        if freq:
            h += freq * math.log(freq, math.e)

    return ((math.log(freq_total, math.e) -
             h / freq_total) /
            math.log(len(freqs), math.e))

# Reference:
#     Lyne, A. A. "Dispersion." The Vocabulary of French Business Correspondence. Slatkine-Champion, 1985, pp. 101-24.
def lynes_d3(freqs):
    return 1 - scipy.stats.chisquare(freqs)[0] / (4 * sum(freqs))

# Reference:
#     Rosengren, Inger. "The quantitative concept of language and its relation to the structure of frequency dictionaries." Études de linguistique appliquée, no. 1, 1971, pp. 103-27.
def rosengrens_s(freqs):
    return (sum([math.sqrt(freq) for freq in freqs]) ** 2 / len(freqs) /
            sum(freqs))

# Reference:
#     Zhang Huarui, et al. "Distribution Consistency: As a General Method for Defining a Core Lexicon." Proceedings of Fourth International Conference on Language Resources and Evaluation, Lisbon, 26-28 May 2004.
def distributional_consistency(freqs):
    if sum(freqs) == 0:
        dc = 0
    else:
        number_sections = len(freqs)

        dc = ((sum([math.sqrt(freq) for freq in freqs]) / number_sections) ** 2 /
              (sum(freqs) / number_sections))

    return dc

# Reference:
#     Gries, Stefan Th. "Dispersions and Adjusted Frequencies in Corpora." International Journal of Corpus Linguistics, vol. 13, no. 4, 2008, pp. 403-37.
def griess_dp(freqs):
    pass

# Testing
if __name__ == '__main__':
    # Carroll, John B. "An alternative to Juilland’s usage coefficient for lexical frequencies and a proposal for a standard frequency index." Computer Studies in the Humanities and Verbal Behaviour, vol.3, no. 2, 1970, pp. 61-65.
    print('Juilland\'s D:\n    ', end = '')
    print(juillands_d([0, 4, 3, 2, 1])) # 0.6464

    # Carroll, John B. "An alternative to Juilland’s usage coefficient for lexical frequencies and a proposal for a standard frequency index." Computer Studies in the Humanities and Verbal Behaviour, vol.3, no. 2, 1970, pp. 61-65.
    print('Carroll\'s D2:\n    ', end = '')
    print(carrolls_d2([2, 1, 1, 1, 0])) # 0.8277

    # Gries, Stefan Th. "Dispersions and Adjusted Frequencies in Corpora." International Journal of Corpus Linguistics, vol. 13, no. 4, 2008, p. 408.
    print('Lyne\'s D3:\n    ', end = '')
    print(lynes_d3([1, 2, 3, 4, 5])) # 0.944

    # Gries, Stefan Th. "Dispersions and Adjusted Frequencies in Corpora." International Journal of Corpus Linguistics, vol. 13, no. 4, 2008, p. 407.
    print('Rosengren\'s S:\n    ', end = '')
    print(rosengrens_s([1, 2, 3, 4, 5])) # 0.937

    # Gries, Stefan Th. "Dispersions and Adjusted Frequencies in Corpora." International Journal of Corpus Linguistics, vol. 13, no. 4, 2008, p. 408.
    print('Distributional Consistency:\n    ', end = '')
    print(distributional_consistency([1, 2, 3, 4, 5])) # 0.937
