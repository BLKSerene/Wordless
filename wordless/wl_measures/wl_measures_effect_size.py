# ----------------------------------------------------------------------
# Wordless: Measures - Effect size
# Copyright (C) 2018-2024  Ye Lei (叶磊)
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

# pylint: disable=unused-argument

import numpy

from wordless.wl_measures import wl_measures_statistical_significance, wl_measure_utils

# %DIFF
# Reference: Gabrielatos, C., & Marchi, A. (2012, September 13–14). Keyness: Appropriate metrics and practical issues [Conference session]. CADS International Conference 2012, University of Bologna, Italy.
def pct_diff(main, o11s, o12s, o21s, o22s):
    _, _, ox1s, ox2s = wl_measures_statistical_significance.get_freqs_marginal(o11s, o12s, o21s, o22s)

    return numpy.where(
        (o11s == 0) & (o12s > 0),
        -numpy.inf,
        numpy.where(
            (o11s > 0) & (o12s == 0),
            numpy.inf,
            wl_measure_utils.numpy_divide(
                (wl_measure_utils.numpy_divide(o11s, ox1s) - wl_measure_utils.numpy_divide(o12s, ox2s)) * 100,
                wl_measure_utils.numpy_divide(o12s, ox2s)
            )
        )
    )

# Cubic Association Ratio
# References:
#     Daille, B. (1994). Approche mixte pour l'extraction automatique de terminologie: statistiques lexicales et filtres linguistiques [Doctoral thesis, Paris Diderot University]. Béatrice Daille. http://www.bdaille.com/index.php?option=com_docman&task=doc_download&gid=8&Itemid=
#     Daille, B. (1995). Combined approach for terminology extraction: Lexical statistics and linguistic filtering. UCREL technical papers (Vol. 5). Lancaster University.
def im3(main, o11s, o12s, o21s, o22s):
    e11s, _, _, _ = wl_measures_statistical_significance.get_freqs_expected(o11s, o12s, o21s, o22s)

    return wl_measure_utils.numpy_log2(wl_measure_utils.numpy_divide(o11s ** 3, e11s))

# Dice's Coefficient
# Reference: Smadja, F., McKeown, K. R., & Hatzivassiloglou, V. (1996). Translating collocations for bilingual lexicons: A statistical approach. Computational Linguistics, 22(1), 1–38.
def dices_coeff(main, o11s, o12s, o21s, o22s):
    o1xs, _, ox1s, _ = wl_measures_statistical_significance.get_freqs_marginal(o11s, o12s, o21s, o22s)

    return wl_measure_utils.numpy_divide(2 * o11s, o1xs + ox1s)

# Difference Coefficient
# References:
#     Hofland, K., & Johanson, S. (1982). Word frequencies in British and American English. Norwegian Computing Centre for the Humanities.
#     Gabrielatos, C. (2018). Keyness analysis: Nature, metrics and techniques. In C. Taylor & A. Marchi (Eds.), Corpus approaches to discourse: A critical review (pp. 225–258). Routledge.
def diff_coeff(main, o11s, o12s, o21s, o22s):
    _, _, ox1s, ox2s = wl_measures_statistical_significance.get_freqs_marginal(o11s, o12s, o21s, o22s)

    return numpy.where(
        (ox1s > 0) & (ox2s > 0),
        wl_measure_utils.numpy_divide(
            wl_measure_utils.numpy_divide(o11s, ox1s) - wl_measure_utils.numpy_divide(o12s, ox2s),
            wl_measure_utils.numpy_divide(o11s, ox1s) + wl_measure_utils.numpy_divide(o12s, ox2s)
        ),
        0
    )

# Jaccard Index
# Reference: Dunning, T. E. (1998). Finding structure in text, genome and other symbolic sequences [Doctoral dissertation, University of Sheffield]. arXiv. arxiv.org/pdf/1207.1847.pdf
def jaccard_index(main, o11s, o12s, o21s, o22s):
    return wl_measure_utils.numpy_divide(o11s, o11s + o12s + o21s)

# Kilgarriff's Ratio
# Reference: Kilgarriff, A. (2009). Simple maths for keywords. In M. Mahlberg, V. González-Díaz, & C. Smith (Eds.), Proceedings of the Corpus Linguistics Conference 2009 (p. 171). University of Liverpool.
def kilgarriffs_ratio(main, o11s, o12s, o21s, o22s):
    smoothing_param = main.settings_custom['measures']['effect_size']['kilgarriffs_ratio']['smoothing_param']

    return wl_measure_utils.numpy_divide(
        wl_measure_utils.numpy_divide(o11s, o11s + o21s) * 1000000 + smoothing_param,
        wl_measure_utils.numpy_divide(o12s, o12s + o22s) * 1000000 + smoothing_param
    )

# Log Ratio
# Reference: Hardie, A. (2014, April 28). Log ratio: An informal introduction. ESRC Centre for Corpus Approaches to Social Science (CASS). http://cass.lancs.ac.uk/log-ratio-an-informal-introduction/
def log_ratio(main, o11s, o12s, o21s, o22s):
    _, _, ox1s, ox2s = wl_measures_statistical_significance.get_freqs_marginal(o11s, o12s, o21s, o22s)

    return numpy.where(
        (o11s == 0) & (o12s > 0),
        -numpy.inf,
        numpy.where(
            (o11s > 0) & (o12s == 0),
            numpy.inf,
            wl_measure_utils.numpy_log2(
                wl_measure_utils.numpy_divide(
                    wl_measure_utils.numpy_divide(o11s, ox1s),
                    wl_measure_utils.numpy_divide(o12s, ox2s)
                )
            )
        )
    )

# Log-Frequency Biased MD
# Reference: Thanopoulos, A., Fakotakis, N., & Kokkinakis, G. (2002). Comparative evaluation of collocation extraction metrics. In M. G. González & C. P. S. Araujo (Eds.), Proceedings of the Third International Conference on Language Resources and Evaluation (pp. 620–625). European Language Resources Association.
def lfmd(main, o11s, o12s, o21s, o22s):
    e11s, _, _, _ = wl_measures_statistical_significance.get_freqs_expected(o11s, o12s, o21s, o22s)

    return wl_measure_utils.numpy_log2(wl_measure_utils.numpy_divide(o11s ** 2, e11s)) + wl_measure_utils.numpy_log2(o11s)

# logDice
# Reference: Rychlý, P. (2008). A lexicographyer-friendly association score. In P. Sojka & A. Horák (Eds.), Proceedings of Second Workshop on Recent Advances in Slavonic Natural Languages Processing. Masaryk University
def log_dice(main, o11s, o12s, o21s, o22s):
    o1xs, _, ox1s, _ = wl_measures_statistical_significance.get_freqs_marginal(o11s, o12s, o21s, o22s)

    return wl_measure_utils.numpy_log2(wl_measure_utils.numpy_divide(2 * o11s, o1xs + ox1s), default = 14)

# MI.log-f
# References:
#     Lexical Computing. (2015, July 8). Statistics used in Sketch Engine. Sketch Engine. https://www.sketchengine.eu/documentation/statistics-used-in-sketch-engine/
#     Kilgarriff, A., & Tugwell, D. (2002). WASP-bench: An MT lexicographers' workstation supporting state-of-the-art lexical disambiguation. In Proceedings of the 8th Machine Translation Summit (pp. 187–190). European Association for Machine Translation.
def mi_log_f(main, o11s, o12s, o21s, o22s):
    e11s, _, _, _ = wl_measures_statistical_significance.get_freqs_expected(o11s, o12s, o21s, o22s)

    return wl_measure_utils.numpy_log2(wl_measure_utils.numpy_divide(o11s ** 2, e11s)) * wl_measure_utils.numpy_log(o11s + 1)

# Minimum Sensitivity
# Reference: Pedersen, T. (1998). Dependent bigram identification. In Proceedings of the Fifteenth National Conference on Artificial Intelligence (p. 1197). AAAI Press.
def min_sensitivity(main, o11s, o12s, o21s, o22s):
    o1xs, _, ox1s, _ = wl_measures_statistical_significance.get_freqs_marginal(o11s, o12s, o21s, o22s)

    return numpy.minimum(
        wl_measure_utils.numpy_divide(o11s, o1xs),
        wl_measure_utils.numpy_divide(o11s, ox1s)
    )

# Mutual Dependency
# Reference: Thanopoulos, A, Fakotakis, N., & Kokkinakis, G. (2002). Comparative evaluation of collocation extraction metrics. In M. G. González, & C. P. S. Araujo (Eds.), Proceedings of the Third International Conference on Language Resources and Evaluation (pp. 620–625). European Language Resources Association.
def md(main, o11s, o12s, o21s, o22s):
    e11s, _, _, _ = wl_measures_statistical_significance.get_freqs_expected(o11s, o12s, o21s, o22s)

    return wl_measure_utils.numpy_log2(wl_measure_utils.numpy_divide(o11s ** 2, e11s))

# Mutual Extation
# Reference: Dias, G., Guilloré, S., & Pereira Lopes, J. G. (1999). Language independent automatic acquisition of rigid multiword units from unrestricted text corpora. In A. Condamines, C. Fabre, & M. Péry-Woodley (Eds.), TALN'99: 6ème Conférence Annuelle Sur le Traitement Automatique des Langues Naturelles (pp. 333–339). TALN.
def me(main, o11s, o12s, o21s, o22s):
    o1xs, _, ox1s, _ = wl_measures_statistical_significance.get_freqs_marginal(o11s, o12s, o21s, o22s)

    return o11s * wl_measure_utils.numpy_divide(2 * o11s, o1xs + ox1s)

# Mutual Information
# Reference: Dunning, T. E. (1998). Finding structure in text, genome and other symbolic sequences [Doctoral dissertation, University of Sheffield]. arXiv. arxiv.org/pdf/1207.1847.pdf
def mi(main, o11s, o12s, o21s, o22s):
    oxxs = o11s + o12s + o21s + o22s
    e11s, e12s, e21s, e22s = wl_measures_statistical_significance.get_freqs_expected(o11s, o12s, o21s, o22s)

    mi_11 = wl_measure_utils.numpy_divide(o11s, oxxs) * wl_measure_utils.numpy_log2(wl_measure_utils.numpy_divide(o11s, e11s))
    mi_12 = wl_measure_utils.numpy_divide(o12s, oxxs) * wl_measure_utils.numpy_log2(wl_measure_utils.numpy_divide(o12s, e12s))
    mi_21 = wl_measure_utils.numpy_divide(o21s, oxxs) * wl_measure_utils.numpy_log2(wl_measure_utils.numpy_divide(o21s, e21s))
    mi_22 = wl_measure_utils.numpy_divide(o22s, oxxs) * wl_measure_utils.numpy_log2(wl_measure_utils.numpy_divide(o22s, e22s))

    return mi_11 + mi_12 + mi_21 + mi_22

# Odds Ratio
# Reference: Pojanapunya, P., & Todd, R. W. (2016). Log-likelihood and odds ratio keyness statistics for different purposes of keyword analysis. Corpus Linguistics and Linguistic Theory, 15(1), 133–167. https://doi.org/10.1515/cllt-2015-0030
def odds_ratio(main, o11s, o12s, o21s, o22s):
    return numpy.where(
        (o11s == 0) & (o12s > 0),
        -numpy.inf,
        numpy.where(
            (o11s > 0) & (o12s == 0),
            numpy.inf,
            wl_measure_utils.numpy_divide(
                o11s * o22s,
                o12s * o21s
            )
        )
    )

# Pointwise Mutual Information
# Reference: Church, K. W., & Hanks, P. (1990). Word association norms, mutual information, and lexicography. Computational Linguistics, 16(1), 22–29.
def pmi(main, o11s, o12s, o21s, o22s):
    e11s, _, _, _ = wl_measures_statistical_significance.get_freqs_expected(o11s, o12s, o21s, o22s)

    return wl_measure_utils.numpy_log2(wl_measure_utils.numpy_divide(o11s, e11s))

# Poisson Collocation Measure
# Reference: Quasthoff, U., & Wolff, C. (2002). The poisson collocation measure and its applications. Proceedings of 2nd International Workshop on Computational Approaches to Collocations. IEEE.
def poisson_collocation_measure(main, o11s, o12s, o21s, o22s):
    oxxs = o11s + o12s + o21s + o22s
    e11s, _, _, _ = wl_measures_statistical_significance.get_freqs_expected(o11s, o12s, o21s, o22s)

    return wl_measure_utils.numpy_divide(
        o11s * (wl_measure_utils.numpy_log(o11s) - wl_measure_utils.numpy_log(e11s) - 1),
        wl_measure_utils.numpy_log(oxxs)
    )

# Squared Phi Coefficient
# Reference: Church, K. W., & Gale, W. A. (1991, September 29–October 1). Concordances for parallel text [Paper presentation]. Using Corpora: Seventh Annual Conference of the UW Centre for the New OED and Text Research, St. Catherine's College, Oxford, United Kingdom.
def squared_phi_coeff(main, o11s, o12s, o21s, o22s):
    o1xs, o2xs, ox1s, ox2s = wl_measures_statistical_significance.get_freqs_marginal(o11s, o12s, o21s, o22s)

    return wl_measure_utils.numpy_divide(
        (o11s * o22s - o12s * o21s) ** 2,
        o1xs * o2xs * ox1s * ox2s
    )
