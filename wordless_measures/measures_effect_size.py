#
# Wordless: Measures - Effect Size
#
# Copyright (C) 2018-2019 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

import math

def get_marginals(c11, c12, c21, c22):
    c1x = c11 + c12
    c2x = c21 + c22
    cx1 = c11 + c21
    cx2 = c12 + c22
    cxx = c11 + c12 + c21 + c22

    return (c1x, c2x, cx1, cx2, cxx)

def get_expected(c1x, c2x, cx1, cx2, cxx):
    e11 = c1x * cx1 / cxx
    e12 = c1x * cx2 / cxx
    e21 = c2x * cx1 / cxx
    e22 = c2x * cx2 / cxx

    return (e11, e12, e21, e22)

# Reference:
#     Church, Kenneth Ward and Patrick Hanks. Word Association Norms, Mutual Information, and Lexicography. Computational Linguistics, vol. 16, no. 1, Mar. 1990, pp. 22-29.
def pmi(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)
    e11, e12, e21, e22 = get_expected(c1x, c2x, cx1, cx2, cxx)

    if c11 == 0 or e11 == 0:
        return 0
    else:
        return math.log(c11 / e11, 2)

# Reference:
#     Thanopoulos, Aristomenis, et al. "Comparative Evaluation of Collocation Extraction Metrics." Proceedings of the Third International Conference on Language Resources and Evaluation, Las Palmas, 29-31 May 2002, edited by Rodríguez, Manuel González Rodríguez and Carmen Paz Suarez Araujo, European Language Resources Association, May 2002, pp. 620-25.
def mutual_dependency(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)
    e11, e12, e21, e22 = get_expected(c1x, c2x, cx1, cx2, cxx)

    if c11 == 0 or e11 == 0:
        return 0
    else:
        return math.log(c11 ** 2 / e11, 2)

def log_freq_biased_md(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)
    e11, e12, e21, e22 = get_expected(c1x, c2x, cx1, cx2, cxx)

    if c11 == 0:
        return 0
    elif e11 == 0:
        return math.log(c11, 2)
    else:
        return math.log(c11 ** 2 / e11, 2) + math.log(c11, 2)

# Reference:
#     Daille, Béatrice. "Combined Approach for Terminology Extraction: Lexical Statistics and Linguistic Filtering." UCREL Technical Papers, vol. 5, University of Lancaster, 1995.
def cubic_association_ratio(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)
    e11, e12, e21, e22 = get_expected(c1x, c2x, cx1, cx2, cxx)

    if c11 == 0 or e11 == 0:
        return 0
    else:
        return math.log(c11 ** 3 / e11, 2)

# Reference:
#     Kilgarriff, Adam and David Tugwell. "Word Sketch: Extraction and Display of Significant Collocations for Lexicography." Proceedings of the ACL 2001 Collocations Workshop, Toulouse, 2001, pp. 32–38.
#     "Statistics used in Sketch Engine." Sketch Engine, https://www.sketchengine.eu/documentation/statistics-used-in-sketch-engine/. Accessed 26 Nov 2018.
def mi_lof_f(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)
    e11, e12, e21, e22 = get_expected(c1x, c2x, cx1, cx2, cxx)

    if c11 == 0 or e11 == 0:
        return 0
    else:
        return math.log(c11 ** 2 / e11, 2) * math.log(c11 + 1, 2)

# Reference:
#     Dunning, Ted Emerson. "Finding Structure in Text, Genome and Other Symbolic Sequences." Dissertation, U of Sheffield, 1998. arXiv, arxiv.org/pdf/1207.1847.pdf.
def mi(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)
    e11, e12, e21, e22 = get_expected(c1x, c2x, cx1, cx2, cxx)

    if c11 == 0 or e11 == 0:
        mi11 = 0
    else:
        mi11 = (c11 / cxx) * math.log(c11 / e11, 2)

    if c12 == 0 or e12 == 0:
        mi12 = 0
    else:
        mi12 = (c12 / cxx) * math.log(c12 / e12, 2)

    if c21 == 0 or e21 == 0:
        mi21 = 0
    else:
        mi21 = (c21 / cxx) * math.log(c21 / e21, 2)

    if c22 == 0 or e22 == 0:
        mi22 = 0
    else:
        mi22 = (c22 / cxx) * math.log(c22 / e22, 2)

    return mi11 + mi12 + mi21 + mi22

# Reference:
#     Church, Kenneth Ward and William A. Gale. "Concordances for Parallel Text." Using Corpora: Seventh Annual Conference of the UW Centre for the New OED and Text Research, St. Catherine's College, 29 Sept - 1 Oct 1991, UW Centre for the New OED and Text Research, 1991.
def squared_phi_coeff(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)

    if c1x == 0 or cx1 == 0:
        return 0
    else:
        return (c11 * c22 - c12 * c21) ** 2 / (c1x * c2x * cx1 * cx2)

# Reference:
#     Smadja, Frank, et al. "Translating Collocations for Bilingual Lexicons: A Statistical Approach." Computational Linguistics, vol. 22, no. 1, 1996, pp. 1-38.
def dices_coeff(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)

    if c1x + cx1 == 0:
        return 0
    else:
        return 2 * c11 / (c1x + cx1)

# Reference:
#     Rychlý, Pavel. "A Lexicographyer-Friendly Association Score." Proceedings of Second Workshop on Recent Advances in Slavonic Natural Languages Processing, Karlova Studanka, 5-7 Dec. 2008, edited by Sojka, P. and A. Horák, Masaryk U, 2008, pp. 6-9.
def log_dice(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)

    if c1x + cx1 == 0 or c11 == 0:
        return 14
    else:
        return 14 + math.log(2 * c11 / (c1x + cx1), 2)

# Reference:
#     Dias, Gaël. "Language Independent Automatic Acquisition of Rigid Multiword Units from Unrestricted Text Corpora." Proceedings of Conférence Traitement Au-tomatique des Langues Naturelles, 12-17 July 1999, Cargèse, edited by Mitkov, Ruslan and Jong C. Park, 1999, pp. 333-39.
def mutual_expectation(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)

    if cx1 + c1x == 0:
        return 0
    else:
        return c11 * (2 * c11 / (cx1 + c1x))

# Reference:
#     Dunning, Ted Emerson. "Finding Structure in Text, Genome and Other Symbolic Sequences." Dissertation, U of Sheffield, 1998. arXiv, arxiv.org/pdf/1207.1847.pdf.
def jaccard_index(main, c11, c12, c21, c22):
    if c11 + c12 + c21 == 0:
        return 0
    else:
        return c11 / (c11 + c12 + c21)

# Reference:
#     Pedersen, Ted. "Dependent Bigram Identification." Proceedings of the Fifteenth National Conference on Artificial Intelligence, Madison, 26-30 July 1998, American Association for Artificial Intelligence, 1998, p. 1197.
def min_sensitivity(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)

    if cx1 == 0:
        s1 = 0
    else:
        s1 = c11 / cx1

    if c1x == 0:
        s2 = 0
    else:
        s2 = c11 / c1x

    return min(s1, s2)

# Reference:
#     Quasthoff, Uwe and Christian Wolff. "The Poisson Collocation Measure and Its Applications." Proceedings of 2nd International Workshop on Computational Approaches to Collocations, Wien, Austria, 2002.
def poisson_collocation_measure(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)
    e11, e12, e21, e22 = get_expected(c1x, c2x, cx1, cx2, cxx)

    return c11 * (math.log(c11 / e11) - 1) / math.log(cxx)

# Reference:
#     Kilgarriff, "Adam. Simple Maths for Keywords." Proceedings of Corpus Linguistics Conference, Liverpool, 20-23 July 2009, edited by Mahlberg, M., et al., U of Liverpool, July 2009.
def kilgarriffs_ratio(main, c11, c12, c21, c22):
    smoothing_parameter = main.settings_custom['measures']['effect_size']['kilgarriffs_ratio']['smoothing_parameter']
    
    return (c11 / (c11 + c21) * 1000000 + smoothing_parameter) / (c12 / (c12 + c22) * 1000000 + smoothing_parameter)

# Reference:
#     Pojanapunya, Punjaporn and Richard Watson Todd. "Log-likelihood and Odds Ratio Keyness Statistics for Different Purposes of Keyword Analysis." Corpus Linguistics and Lingustic Theory, vol. 15, no. 1, Jan. 2016, pp. 133-67.
def odds_ratio(main, c11, c12, c21, c22):
    if c11 == 0 and c12 > 0:
        return float('-inf')
    elif c11 > 0 and c12 == 0:
        return float('inf')
    elif c11 == 0 and c12 == 0:
        return 0
    else:
        return (c11 * c22) / (c12 * c21)

# Reference:
#     Hardie, Andrew. "Log Ratio: An Informal Introduction." The Centre for Corpus Approaches to Social Science, http://cass.lancs.ac.uk/log-ratio-an-informal-introduction/
def log_ratio(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)

    if c11 == 0 and c12 > 0:
        return float('-inf')
    elif c11 > 0 and c12 == 0:
        return float('inf')
    elif c11 == 0 and c12 == 0:
        return 0
    else:
        return math.log((c11 / cx1) / (c12 / cx2), 2)

# Reference:
#     Hofland, Knut and Stig Johansson. Word Frequencies in British and American English. Norwegian Computing Centre for the Humanities, 1982.
#     Gabrielatos, Costas. "Keyness Analysis: Nature, Metrics and Techniques." Corpus Approaches to Discourse: A Critical Review, edited by Taylor, Charlotte and Anna Marchi, Routledge, 2018.
def diff_coeff(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)

    return (c11 / cx1 - c12 / cx2) / (c11 / cx1 + c12 / cx2)

# Reference:
#     Gabrielatos, Costas and Anna Marchi. "Keyness: Appropriate Metrics and Practical Issues." Proceedings of CADS International Conference, U of Bologna, 13-14 Sept. 2012.
def pct_diff(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = get_marginals(c11, c12, c21, c22)

    if c11 == 0 and c12 > 0:
        return float('-inf')
    elif c11 > 0 and c12 == 0:
        return float('inf')
    elif c11 == 0 and c12 == 0:
        return 0
    else:
        return ((c11 / cx1 - c12 / cx2) * 100) / (c12 / cx2)

# Testing
if __name__ == '__main__':
    from PyQt5.QtCore import *

    main = QObject()
    main.settings_custom = {
        'measures': {
            'effect_size': {
                'kilgarriffs_ratio': {
                    'smoothing_parameter': 1.00,
                }
            }
        }
    }

    # Church, Kenneth Ward and Patrick Hanks. Word Association Norms, Mutual Information, and Lexicography. Computational Linguistics, vol. 16, no. 1, Mar. 1990, p. 24.
    print('Pointwise Mutual Information:\n    ', end = '')
    print(pmi(main, 8, 1105 - 8, 44 - 8, 15000000 - 1105 - 44 + 8)) # 11.3

    # Church, Kenneth Ward and William A. Gale. "Concordances for Parallel Text." Using Corpora: Seventh Annual Conference of the UW Centre for the New OED and Text Research, St. Catherine's College, 29 Sept - 1 Oct 1991, UW Centre for the New OED and Text Research, 1991.
    print('Squared Phi Coefficient:\n    ', end = '')
    print(squared_phi_coeff(main, 31950, 12004, 4793, 848330)) # 0.62

    # Smadja, Frank, et al. "Translating Collocations for Bilingual Lexicons: A Statistical Approach." Computational Linguistics, vol. 22, no. 1, 1996, p. 13.
    print('Dice\'s Coefficient:\n    ', end = '')
    print(dices_coeff(main, 130, 3121 - 130, 143 - 130, -1)) # 0.08

    # Rychlý, Pavel. "A Lexicographyer-Friendly Association Score." Proceedings of Second Workshop on Recent Advances in Slavonic Natural Languages Processing, Karlova Studanka, 5-7 Dec. 2008, edited by Sojka, P. and A. Horák, Masaryk U, 2008, p. 9.
    print('logDice:\n    ', end = '')
    print(log_dice(main, 1, 16000 - 1, 16000 - 1, 1000000 - 16000 - 16000 + 1))

    # Pedersen, Ted. "Dependent Bigram Identification." Proceedings of the Fifteenth National Conference on Artificial Intelligence, Madison, 26-30 July 1998, American Association for Artificial Intelligence, 1998, p. 1197.
    print('Minimum Sensitivity:\n    ', end = '')
    print(min_sensitivity(main, 17, 240, 1001, 1298742)) # 0.017

    # "Simple maths." Sketch Engine, www.sketchengine.eu/documentation/simple-maths/. Accessed 26 Nov 2018.
    print('Kilgarriff\'s Ratio:\n    ', end = '')
    print(kilgarriffs_ratio(main, 35, 263, 112289776, 1559716979)) # 1.1224

    # Pojanapunya, Punjaporn and Richard Watson Todd. "Log-likelihood and Odds Ratio Keyness Statistics for Different Purposes of Keyword Analysis." Corpus Linguistics and Lingustic Theory, vol. 15, no. 1, Jan. 2016, p 154.
    print('Odd\'s Ratio:\n    ', end = '')
    print(odds_ratio(main, 16217, 735, 2796938 - 16217, 2087946 - 735)) # 16.6
    
    # Hardie, Andrew. "Log Ratio: An Informal Introduction." The Centre for Corpus Approaches to Social Science, cass.lancs.ac.uk/log-ratio-an-informal-introduction/
    print('Log Ratio:\n    ', end = '')
    print(log_ratio(main, 1, 1, 1000000 - 1, 1000000 - 1)) # 0
    
    # Hofland, Knut and Stig Johansson. Word Frequencies in British and American English. Norwegian Computing Centre for the Humanities, 1982, p. 471.
    print('Difference Coefficient:\n    ', end = '')
    print(diff_coeff(main, 18, 35, 1000000 - 18, 1000000 - 35)) # -0.32

    # Gabrielatos, Costas. "Keyness Analysis: Nature, Metrics and Techniques." Corpus Approaches to Discourse: A Critical Review, edited by Taylor, Charlotte and Anna Marchi, Routledge, 2018, pp. 21-22.
    print('%Diff:\n    ', end = '')
    print(pct_diff(main, 20, 1, 29954 - 20, 23691 - 1)) # 1481.83
