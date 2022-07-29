# ----------------------------------------------------------------------
# Wordless: Measures - Effect Size
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

import numpy

from wl_measures import wl_measures_statistical_significance

# %DIFF
# Reference: Gabrielatos, C., & Marchi, A. (2012, September 13–14). Keyness: Appropriate metrics and practical issues [Conference session]. CADS International Conference 2012, University of Bologna, Italy.
def pct_diff(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = wl_measures_statistical_significance.get_marginals(c11, c12, c21, c22)

    if c11 == 0 and c12 > 0:
        return float('-inf')
    elif c11 > 0 and c12 == 0:
        return float('inf')
    elif c11 == 0 and c12 == 0:
        return 0
    else:
        return ((c11 / cx1 - c12 / cx2) * 100) / (c12 / cx2)

# Cubic Association Ratio
# References:
#     Daille, B. (1994). Approche mixte pour l'extraction automatique de terminologie: statistiques lexicales et filtres linguistiques [Doctoral thesis, Université Paris 7]. Béatrice Daille. http://www.bdaille.com/index.php?option=com_docman&task=doc_download&gid=8&Itemid=
#     Daille, B. (1995). Combined approach for terminology extraction: Lexical statistics and linguistic filtering. UCREL technical papers (Vol. 5). Lancaster University.
def im3(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = wl_measures_statistical_significance.get_marginals(c11, c12, c21, c22)
    e11, e12, e21, e22 = wl_measures_statistical_significance.get_expected(c1x, c2x, cx1, cx2, cxx)

    if c11 == 0 or e11 == 0:
        return 0
    else:
        return numpy.log2(c11 ** 3 / e11)

# Dice's Coefficient
# Reference: Smadja, F., McKeown, K. R., & Hatzivassiloglou, V. (1996). Translating collocations for bilingual lexicons: A statistical approach. Computational Linguistics, 22(1), pp. 1–38.
def dices_coeff(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = wl_measures_statistical_significance.get_marginals(c11, c12, c21, c22)

    if c1x + cx1 == 0:
        return 0
    else:
        return 2 * c11 / (c1x + cx1)

# Difference Coefficient
# References:
#     Hofland, K., & Johanson, S. (1982). Word frequencies in British and American English. Norwegian Computing Centre for the Humanities.
#     Gabrielatos, C. (2018). Keyness analysis: Nature, metrics and techniques. In C. Taylor & A. Marchi (Eds.), Corpus approaches to discourse: A critical review (pp. 225–258). Routledge.
def diff_coeff(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = wl_measures_statistical_significance.get_marginals(c11, c12, c21, c22)

    return (c11 / cx1 - c12 / cx2) / (c11 / cx1 + c12 / cx2)

# Jaccard Index
# Reference: Lexical Computing Ltd. (2015, July 8). Statistics used in Sketch Engine. Retrieved November 26, 2018 from https://www.sketchengine.eu/documentation/statistics-used-in-sketch-engine/
def jaccard_index(main, c11, c12, c21, c22):
    if c11 + c12 + c21 == 0:
        return 0
    else:
        return c11 / (c11 + c12 + c21)

# Kilgarriff's Ratio
# Reference: Kilgarriff, A. (2009). Simple maths for keywords. In M. Mahlberg, V. González-Díaz, & C. Smith (Eds.), Proceedings of the Corpus Linguistics Conference 2009 (p. 171). University of Liverpool.
def kilgarriffs_ratio(main, c11, c12, c21, c22):
    smoothing_param = main.settings_custom['measures']['effect_size']['kilgarriffs_ratio']['smoothing_param']

    if c11 + c21 == 0:
        relative_freq_observed = 0
    else:
        relative_freq_observed = c11 / (c11 + c21) * 1000000

    if c12 + c22 == 0:
        relative_freq_ref = 0
    else:
        relative_freq_ref = c12 / (c12 + c22) * 1000000

    return (relative_freq_observed + smoothing_param) / (relative_freq_ref + smoothing_param)

# Log Ratio
# Reference: Hardie, A. (2014, April 28). Log ratio: An informal introduction. ESRC Centre for Corpus Approaches to Social Science (CASS). http://cass.lancs.ac.uk/log-ratio-an-informal-introduction/.
def log_ratio(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = wl_measures_statistical_significance.get_marginals(c11, c12, c21, c22)

    if c11 == 0 and c12 > 0:
        return float('-inf')
    elif c11 > 0 and c12 == 0:
        return float('inf')
    elif c11 == 0 and c12 == 0:
        return 0
    else:
        return numpy.log2((c11 / cx1) / (c12 / cx2))

# Log-Frequency Biased MD
# Reference: Thanopoulos, A., Fakotakis, N., Kokkinakis, G. (2002). Comparative evaluation of collocation extraction metrics. In M. G. González, & C. P. S. Araujo (Eds.), Proceedings of the Third International Conference on Language Resources and Evaluation (pp. 620–625). European Language Resources Association.
def lfmd(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = wl_measures_statistical_significance.get_marginals(c11, c12, c21, c22)
    e11, e12, e21, e22 = wl_measures_statistical_significance.get_expected(c1x, c2x, cx1, cx2, cxx)

    if c11 == 0:
        return 0
    elif e11 == 0:
        return numpy.log2(c11)
    else:
        return numpy.log2(c11 ** 2 / e11) + numpy.log2(c11)

# logDice
# Reference: Rychlý, P. (2008). A lexicographyer-friendly association score. In P. Sojka, & A. Horák (Eds.), Proceedings of Second Workshop on Recent Advances in Slavonic Natural Languages Processing. Masaryk University
def log_dice(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = wl_measures_statistical_significance.get_marginals(c11, c12, c21, c22)

    if c11 == 0 or c1x + cx1 == 0:
        return 14
    else:
        return 14 + numpy.log2(2 * c11 / (c1x + cx1))

# MI.log-f
# References:
#     Lexical Computing Ltd. (2015, July 8). Statistics used in Sketch Engine. Retrieved November 26, 2018 from https://www.sketchengine.eu/documentation/statistics-used-in-sketch-engine/
#     Kilgarriff, A., & Tugwell, D. (2002). WASP-bench – an MT lexicographers' workstation supporting state-of-the-art lexical disambiguation. In Proceedings of the 8th Machine Translation Summit (pp. 187–190). European Association for Machine Translation.
def mi_log_f(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = wl_measures_statistical_significance.get_marginals(c11, c12, c21, c22)
    e11, e12, e21, e22 = wl_measures_statistical_significance.get_expected(c1x, c2x, cx1, cx2, cxx)

    if c11 == 0 or e11 == 0:
        return 0
    else:
        return numpy.log2(c11 ** 2 / e11) * numpy.log(c11 + 1)

# Minimum Sensitivity
# Reference: Pedersen, T. (1998). Dependent bigram identification. In Proceedings of the Fifteenth National Conference on Artificial Intelligence (p. 1197). AAAI Press.
def min_sensitivity(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = wl_measures_statistical_significance.get_marginals(c11, c12, c21, c22)

    if c1x == 0:
        s1 = 0
    else:
        s1 = c11 / c1x

    if cx1 == 0:
        s2 = 0
    else:
        s2 = c11 / cx1

    return min(s1, s2)

# Mutual Dependency
# Reference: Thanopoulos, A, Fakotakis, N., Kokkinakis, G. (2002). Comparative evaluation of collocation extraction metrics. In M. G. González, & C. P. S. Araujo (Eds.), Proceedings of the Third International Conference on Language Resources and Evaluation (pp. 620–625). European Language Resources Association.
def md(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = wl_measures_statistical_significance.get_marginals(c11, c12, c21, c22)
    e11, e12, e21, e22 = wl_measures_statistical_significance.get_expected(c1x, c2x, cx1, cx2, cxx)

    if c11 == 0 or e11 == 0:
        return 0
    else:
        return numpy.log2(c11 ** 2 / e11)

# Mutual Extation
# Reference: Dias, G., Guilloré, S., & Pereira Lopes, J. G. (1999). Language independent automatic acquisition of rigid multiword units from unrestricted text corpora. In A. Condamines, C. Fabre, & M. Péry-Woodley (Eds.), TALN'99: 6ème Conférence Annuelle Sur le Traitement Automatique des Langues Naturelles (pp. 333–339). TALN.
def me(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = wl_measures_statistical_significance.get_marginals(c11, c12, c21, c22)

    if cx1 + c1x == 0:
        return 0
    else:
        return c11 * (2 * c11 / (c1x + cx1))

# Mutual Information
# Reference: Dunning, T. E. (1998). Finding structure in text, genome and other symbolic sequences [Doctoral dissertation, University of Sheffield]. arXiv. arxiv.org/pdf/1207.1847.pdf
def mi(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = wl_measures_statistical_significance.get_marginals(c11, c12, c21, c22)
    e11, e12, e21, e22 = wl_measures_statistical_significance.get_expected(c1x, c2x, cx1, cx2, cxx)

    if c11 == 0 or e11 == 0:
        mi11 = 0
    else:
        mi11 = (c11 / cxx) * numpy.log2(c11 / e11)

    if c12 == 0 or e12 == 0:
        mi12 = 0
    else:
        mi12 = (c12 / cxx) * numpy.log2(c12 / e12)

    if c21 == 0 or e21 == 0:
        mi21 = 0
    else:
        mi21 = (c21 / cxx) * numpy.log2(c21 / e21)

    if c22 == 0 or e22 == 0:
        mi22 = 0
    else:
        mi22 = (c22 / cxx) * numpy.log2(c22 / e22)

    return mi11 + mi12 + mi21 + mi22

# Odds Ratio
# Reference: Pojanapunya, P., & Todd, R. W. (2016). Log-likelihood and odds ratio keyness statistics for different purposes of keyword analysis. Corpus Linguistics and Lingustic Theory, 15(1), pp. 133–167. https://doi.org/10.1515/cllt-2015-0030
def odds_ratio(main, c11, c12, c21, c22):
    if c11 == 0 and c12 > 0:
        return float('-inf')
    elif c11 > 0 and c12 == 0:
        return float('inf')
    elif c11 == 0 and c12 == 0:
        return 0
    else:
        return (c11 * c22) / (c12 * c21)

# Pointwise Mutual Information
# Reference: Church, K. W., & Hanks, P. (1990). Word association norms, mutual information, and lexicography. Computational Linguistics, 16(1), 22–29.
def pmi(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = wl_measures_statistical_significance.get_marginals(c11, c12, c21, c22)
    e11, e12, e21, e22 = wl_measures_statistical_significance.get_expected(c1x, c2x, cx1, cx2, cxx)

    if c11 == 0 or e11 == 0:
        return 0
    else:
        return numpy.log2(c11 / e11)

# Poisson Collocation Measure
# Reference: Quasthoff, U., & Wolff, C. (2002). The poisson collocation measure and its applications. Proceedings of 2nd International Workshop on Computational Approaches to Collocations. IEEE.
def poisson_collocation_measure(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = wl_measures_statistical_significance.get_marginals(c11, c12, c21, c22)
    e11, e12, e21, e22 = wl_measures_statistical_significance.get_expected(c1x, c2x, cx1, cx2, cxx)

    if c11 == 0:
        log_c11 = 0
    else:
        log_c11 = numpy.log(c11)

    if e11 == 0:
        log_e11 = 0
    else:
        log_e11 = numpy.log(e11)

    return (c11 * (log_c11 - log_e11 - 1)) / numpy.log(cxx)

# Squared Phi Coefficient
# Reference: Church, K. W., & Gale, W. A. (1991, September 29–October 1). Concordances for parallel text [Paper presentation]. Using Corpora: Seventh Annual Conference of the UW Centre for the New OED and Text Research, St. Catherine's College, Oxford, United Kingdom.
def squared_phi_coeff(main, c11, c12, c21, c22):
    c1x, c2x, cx1, cx2, cxx = wl_measures_statistical_significance.get_marginals(c11, c12, c21, c22)

    if c1x == 0 or cx1 == 0:
        return 0
    else:
        return (c11 * c22 - c12 * c21) ** 2 / (c1x * c2x * cx1 * cx2)
