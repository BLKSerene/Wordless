# ----------------------------------------------------------------------
# Wordless: Measures - Effect size
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

# pylint: disable=unused-argument

import math

import numpy

from wordless.wl_measures import wl_measures_statistical_significance, wl_measure_utils

def get_numpy_log(main, measure_code):
    match main.settings_custom['measures']['effect_size'][measure_code]['base_log']:
        case 2:
            return wl_measure_utils.numpy_log2
        case 10:
            return wl_measure_utils.numpy_log10
        case math.e:
            return wl_measure_utils.numpy_log

# Conditional probability
# Reference: Durrant, P. (2008). High frequency collocations and second language learning [Doctoral dissertation, University of Nottingham]. Nottingham eTheses. https://eprints.nottingham.ac.uk/10622/1/final_thesis.pdf | p. 84
def conditional_probability(main, o11s, o12s, o21s, o22s):
    o1xs, _, _, _ = wl_measures_statistical_significance.get_freqs_marginal(o11s, o12s, o21s, o22s)

    return wl_measure_utils.numpy_divide(o11s, o1xs) * 100

# ΔP
# Reference: Gries, S. T. (2013). 50-something years of work on collocations: What is or should be next …. International Journal of Corpus Linguistics, 18(1), 137–165. https://doi.org/10.1075/ijcl.18.1.09gri
def delta_p(main, o11s, o12s, o21s, o22s):
    o1xs, o2xs, _, _ = wl_measures_statistical_significance.get_freqs_marginal(o11s, o12s, o21s, o22s)

    return wl_measure_utils.numpy_divide(o11s, o1xs) - wl_measure_utils.numpy_divide(o21s, o2xs)

# Dice-Sørensen coefficient
# Reference: Smadja, F., McKeown, K. R., & Hatzivassiloglou, V. (1996). Translating collocations for bilingual lexicons: A statistical approach. Computational Linguistics, 22(1), 1–38. | p. 8
def dice_sorensen_coeff(main, o11s, o12s, o21s, o22s):
    o1xs, _, ox1s, _ = wl_measures_statistical_significance.get_freqs_marginal(o11s, o12s, o21s, o22s)

    return wl_measure_utils.numpy_divide(2 * o11s, o1xs + ox1s)

# Difference coefficient
# References:
#     Hofland, K., & Johanson, S. (1982). Word frequencies in British and American English. Norwegian Computing Centre for the Humanities. | p. 14
#     Gabrielatos, C. (2018). Keyness analysis: Nature, metrics and techniques. In C. Taylor & A. Marchi (Eds.), Corpus approaches to discourse: A critical review (pp. 225–258). Routledge. | p. 236
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

# Jaccard index
# Reference: Dunning, T. E. (1998). Finding structure in text, genome and other symbolic sequences [Doctoral dissertation, University of Sheffield]. arXiv. https://arxiv.org/pdf/1207.1847 | p. 48
def jaccard_index(main, o11s, o12s, o21s, o22s):
    return wl_measure_utils.numpy_divide(o11s, o11s + o12s + o21s)

# Kilgarriff's ratio
# Reference: Kilgarriff, A. (2009). Simple maths for keywords. In M. Mahlberg, V. González-Díaz, & C. Smith (Eds.), Proceedings of the Corpus Linguistics Conference 2009 (CL2009) (Article 171). University of Liverpool.
def kilgarriffs_ratio(main, o11s, o12s, o21s, o22s):
    smoothing_param = main.settings_custom['measures']['effect_size']['kilgarriffs_ratio']['smoothing_param']

    return wl_measure_utils.numpy_divide(
        wl_measure_utils.numpy_divide(o11s, o11s + o21s) * 1000000 + smoothing_param,
        wl_measure_utils.numpy_divide(o12s, o12s + o22s) * 1000000 + smoothing_param
    )

# logDice
# Reference: Rychlý, P. (2008). A lexicographyer-friendly association score. In P. Sojka & A. Horák (Eds.), Proceedings of Second Workshop on Recent Advances in Slavonic Natural Languages Processing (pp. 6–9). Masaryk University
def log_dice(main, o11s, o12s, o21s, o22s):
    o1xs, _, ox1s, _ = wl_measures_statistical_significance.get_freqs_marginal(o11s, o12s, o21s, o22s)

    return wl_measure_utils.numpy_log2(wl_measure_utils.numpy_divide(2 * o11s, o1xs + ox1s), default = 14)

# Log Ratio
# Reference: Hardie, A. (2014, April 28). Log Ratio: An informal introduction. ESRC Centre for Corpus Approaches to Social Science (CASS). http://cass.lancs.ac.uk/log-ratio-an-informal-introduction/
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

# MI.log-f
# References:
#     Kilgarriff, A., & Tugwell, D. (2001). WASP-bench: An MT lexicographers' workstation supporting state-of-the-art lexical disambiguation. In B. Maegaard (Ed.), Proceedings of Machine Translation Summit VIII (pp. 187–190). European Association for Machine Translation.
#     Lexical Computing. (2015, July 8). Statistics used in Sketch Engine. Sketch Engine. https://www.sketchengine.eu/documentation/statistics-used-in-sketch-engine/ | p. 4
def mi_log_f(main, o11s, o12s, o21s, o22s):
    e11s, _, _, _ = wl_measures_statistical_significance.get_freqs_expected(o11s, o12s, o21s, o22s)

    return wl_measure_utils.numpy_log2(wl_measure_utils.numpy_divide(o11s, e11s)) * wl_measure_utils.numpy_log(o11s + 1)

# Minimum sensitivity
# Reference: Pedersen, T., & Bruce, R. (1996). What to infer from a description. In Technical report 96-CSE-04. Southern Methodist University.
def min_sensitivity(main, o11s, o12s, o21s, o22s):
    o1xs, _, ox1s, _ = wl_measures_statistical_significance.get_freqs_marginal(o11s, o12s, o21s, o22s)

    return numpy.minimum(
        wl_measure_utils.numpy_divide(o11s, o1xs),
        wl_measure_utils.numpy_divide(o11s, ox1s)
    )

# Mutual Expectation
# Reference: Dias, G., Guilloré, S., & Pereira Lopes, J. G. (1999). Language independent automatic acquisition of rigid multiword units from unrestricted text corpora. In A. Condamines, C. Fabre, & M. Péry-Woodley (Eds.), TALN'99: 6ème Conférence Annuelle Sur le Traitement Automatique des Langues Naturelles (pp. 333–339). TALN.
def me(main, o11s, o12s, o21s, o22s):
    o1xs, _, ox1s, _ = wl_measures_statistical_significance.get_freqs_marginal(o11s, o12s, o21s, o22s)

    return o11s * wl_measure_utils.numpy_divide(2 * o11s, o1xs + ox1s)

# Mutual information
# Reference: Dunning, T. E. (1998). Finding structure in text, genome and other symbolic sequences [Doctoral dissertation, University of Sheffield]. arXiv. https://arxiv.org/pdf/1207.1847 | pp. 49–52
def mi(main, o11s, o12s, o21s, o22s):
    oxxs = o11s + o12s + o21s + o22s
    e11s, e12s, e21s, e22s = wl_measures_statistical_significance.get_freqs_expected(o11s, o12s, o21s, o22s)

    numpy_log = get_numpy_log(main, 'mi')

    mi_11 = wl_measure_utils.numpy_divide(o11s, oxxs) * numpy_log(wl_measure_utils.numpy_divide(o11s, e11s))
    mi_12 = wl_measure_utils.numpy_divide(o12s, oxxs) * numpy_log(wl_measure_utils.numpy_divide(o12s, e12s))
    mi_21 = wl_measure_utils.numpy_divide(o21s, oxxs) * numpy_log(wl_measure_utils.numpy_divide(o21s, e21s))
    mi_22 = wl_measure_utils.numpy_divide(o22s, oxxs) * numpy_log(wl_measure_utils.numpy_divide(o22s, e22s))

    return mi_11 + mi_12 + mi_21 + mi_22

# Mutual information (normalized)
# Reference: Bouma, G. (2009). Normalized (pointwise) mutual information in collocation extraction. In C. Chiarcos, R. Eckart de Castilho, & M. Stede (Eds.), From form to meaning: processing texts automatically: Proceedings of the Biennial GSCL Conference 2009 (pp. 31–40). Gunter Narr Verlag.
def nmi(main, o11s, o12s, o21s, o22s):
    oxxs = o11s + o12s + o21s + o22s
    e11s, e12s, e21s, e22s = wl_measures_statistical_significance.get_freqs_expected(o11s, o12s, o21s, o22s)

    numpy_log = get_numpy_log(main, 'nmi')

    mi_11 = wl_measure_utils.numpy_divide(o11s, oxxs) * numpy_log(wl_measure_utils.numpy_divide(o11s, e11s))
    mi_12 = wl_measure_utils.numpy_divide(o12s, oxxs) * numpy_log(wl_measure_utils.numpy_divide(o12s, e12s))
    mi_21 = wl_measure_utils.numpy_divide(o21s, oxxs) * numpy_log(wl_measure_utils.numpy_divide(o21s, e21s))
    mi_22 = wl_measure_utils.numpy_divide(o22s, oxxs) * numpy_log(wl_measure_utils.numpy_divide(o22s, e22s))

    joint_entropy_11 = wl_measure_utils.numpy_divide(o11s, oxxs) * numpy_log(wl_measure_utils.numpy_divide(o11s, oxxs))
    joint_entropy_12 = wl_measure_utils.numpy_divide(o12s, oxxs) * numpy_log(wl_measure_utils.numpy_divide(o12s, oxxs))
    joint_entropy_21 = wl_measure_utils.numpy_divide(o21s, oxxs) * numpy_log(wl_measure_utils.numpy_divide(o21s, oxxs))
    joint_entropy_22 = wl_measure_utils.numpy_divide(o22s, oxxs) * numpy_log(wl_measure_utils.numpy_divide(o22s, oxxs))

    return wl_measure_utils.numpy_divide(
        mi_11 + mi_12 + mi_21 + mi_22,
        -(joint_entropy_11 + joint_entropy_12 + joint_entropy_21 + joint_entropy_22)
    )

# μ-value
# Reference: Evert, S. (2005). The statistics of word cooccurrences: Word pairs and collocations [Doctoral dissertation, University of Stuttgart]. OPUS - Online Publikationen der Universität Stuttgart. https://doi.org/10.18419/opus-2556 | p. 54
def mu_val(main, o11s, o12s, o21s, o22s):
    e11s, _, _, _ = wl_measures_statistical_significance.get_freqs_expected(o11s, o12s, o21s, o22s)

    return wl_measure_utils.numpy_divide(o11s, e11s)

# Odds ratio
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

# %DIFF
# Reference: Gabrielatos, C., & Marchi, A. (2011, November 5). Keyness: Matching metrics to definitions [Conference session]. Corpus Linguistics in the South 1, University of Portsmouth, United Kingdom. https://eprints.lancs.ac.uk/id/eprint/51449/4/Gabrielatos_Marchi_Keyness.pdf
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

# Pointwise mutual information
# Reference: Church, K. W., & Hanks, P. (1990). Word association norms, mutual information, and lexicography. Computational Linguistics, 16(1), 22–29.
def pmi(main, o11s, o12s, o21s, o22s):
    e11s, _, _, _ = wl_measures_statistical_significance.get_freqs_expected(o11s, o12s, o21s, o22s)

    numpy_log = get_numpy_log(main, 'pmi')

    return numpy_log(wl_measure_utils.numpy_divide(o11s, e11s))

# Pointwise mutual information (cubic)
# Reference: Daille, B. (1994). Approche mixte pour l'extraction automatique de terminologie: statistiques lexicales et filtres linguistiques [Doctoral thesis, Paris Diderot University]. Béatrice Daille. http://www.bdaille.com/index.php?option=com_docman&task=doc_download&gid=8&Itemid= | p. 139
def im3(main, o11s, o12s, o21s, o22s):
    e11s, _, _, _ = wl_measures_statistical_significance.get_freqs_expected(o11s, o12s, o21s, o22s)

    numpy_log = get_numpy_log(main, 'im3')

    return numpy_log(wl_measure_utils.numpy_divide(o11s ** 3, e11s))

# Pointwise mutual information (normalized)
# Reference: Bouma, G. (2009). Normalized (pointwise) mutual information in collocation extraction. In C. Chiarcos, R. Eckart de Castilho, & M. Stede (Eds.), From form to meaning: processing texts automatically: Proceedings of the Biennial GSCL Conference 2009 (pp. 31–40). Gunter Narr Verlag.
def npmi(main, o11s, o12s, o21s, o22s):
    oxxs = o11s + o12s + o21s + o22s
    e11s, _, _, _ = wl_measures_statistical_significance.get_freqs_expected(o11s, o12s, o21s, o22s)

    numpy_log = get_numpy_log(main, 'npmi')

    return numpy.where(
        o11s > 0,
        wl_measure_utils.numpy_divide(
            numpy_log(wl_measure_utils.numpy_divide(o11s, e11s)),
            -(numpy_log(wl_measure_utils.numpy_divide(o11s, oxxs)))
        ),
        -1
    )

# Pointwise mutual information (squared)
# Reference: Daille, B. (1995). Combined approach for terminology extraction: Lexical statistics and linguistic filtering. UCREL technical papers (Vol. 5). Lancaster University. | p. 21
def im2(main, o11s, o12s, o21s, o22s):
    e11s, _, _, _ = wl_measures_statistical_significance.get_freqs_expected(o11s, o12s, o21s, o22s)

    numpy_log = get_numpy_log(main, 'im2')

    return numpy_log(wl_measure_utils.numpy_divide(o11s ** 2, e11s))

# Poisson collocation measure
# Reference: Quasthoff, U., & Wolff, C. (2002). The poisson collocation measure and its applications. Proceedings of 2nd International Workshop on Computational Approaches to Collocations. IEEE.
def poisson_collocation_measure(main, o11s, o12s, o21s, o22s):
    oxxs = o11s + o12s + o21s + o22s
    e11s, _, _, _ = wl_measures_statistical_significance.get_freqs_expected(o11s, o12s, o21s, o22s)

    return wl_measure_utils.numpy_divide(
        o11s * (wl_measure_utils.numpy_log(o11s) - wl_measure_utils.numpy_log(e11s) - 1),
        wl_measure_utils.numpy_log(oxxs)
    )

# Relative risk
# Reference: Evert, S. (2005). The statistics of word cooccurrences: Word pairs and collocations [Doctoral dissertation, University of Stuttgart]. OPUS - Online Publikationen der Universität Stuttgart. https://doi.org/10.18419/opus-2556 | p. 55
def rr(main, o11s, o12s, o21s, o22s):
    _, _, ox1s, ox2s = wl_measures_statistical_significance.get_freqs_marginal(o11s, o12s, o21s, o22s)

    return wl_measure_utils.numpy_divide(o11s * ox2s, o12s * ox1s)

# Squared phi coefficient
# Reference: Church, K. W., & Gale, W. A. (1991, September 29–October 1). Concordances for parallel text [Paper presentation]. Using Corpora: Seventh Annual Conference of the UW Centre for the New OED and Text Research, St. Catherine's College, Oxford, United Kingdom.
def squared_phi_coeff(main, o11s, o12s, o21s, o22s):
    o1xs, o2xs, ox1s, ox2s = wl_measures_statistical_significance.get_freqs_marginal(o11s, o12s, o21s, o22s)

    return wl_measure_utils.numpy_divide(
        (o11s * o22s - o12s * o21s) ** 2,
        o1xs * o2xs * ox1s * ox2s
    )
