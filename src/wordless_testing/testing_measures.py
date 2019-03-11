#
# Wordless: Testing - Measures
#
# Copyright (C) 2018-2019  Ye Lei (叶磊)
#
# This source file is licensed under GNU GPLv3.
# For details, see: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#
# All other rights reserved.
#

import sys

sys.path.append('.')

from wordless_testing import testing_init
from wordless_measures import (wordless_measures_adjusted_freq,
                               wordless_measures_bayes_factor,
                               wordless_measures_dispersion,
                               wordless_measures_effect_size,
                               wordless_measures_statistical_significance)

main = testing_init.Testing_Main()

# Dispersion
print('---------- Measures of Dispersion ----------')
# Carroll, John B. "An alternative to Juilland’s usage coefficient for lexical frequencies and a proposal for a standard frequency index." Computer Studies in the Humanities and Verbal Behaviour, vol.3, no. 2, 1970, pp. 61-65.
print('Juilland\'s D:')
print(f'\t{wordless_measures_dispersion.juillands_d([0, 4, 3, 2, 1])} (0.6464)')

# Carroll, John B. "An alternative to Juilland’s usage coefficient for lexical frequencies and a proposal for a standard frequency index." Computer Studies in the Humanities and Verbal Behaviour, vol.3, no. 2, 1970, pp. 61-65.
print('Carroll\'s D2:')
print(f'\t{wordless_measures_dispersion.carrolls_d2([2, 1, 1, 1, 0])} (0.8277)')

# Gries, Stefan Th. "Dispersions and Adjusted Frequencies in Corpora." International Journal of Corpus Linguistics, vol. 13, no. 4, 2008, p. 408.
print('Lyne\'s D3:')
print(f'\t{wordless_measures_dispersion.lynes_d3([1, 2, 3, 4, 5])} (0.944)')

# Gries, Stefan Th. "Dispersions and Adjusted Frequencies in Corpora." International Journal of Corpus Linguistics, vol. 13, no. 4, 2008, p. 407.
print('Rosengren\'s S:')
print(f'\t{wordless_measures_dispersion.rosengrens_s([1, 2, 3, 4, 5])} (0.937)')

# Gries, Stefan Th. "Dispersions and Adjusted Frequencies in Corpora." International Journal of Corpus Linguistics, vol. 13, no. 4, 2008, p. 408.
print('Zhang\'s Distributional Consistency:')
print(f'\t{wordless_measures_dispersion.zhangs_distributional_consistency([1, 2, 3, 4, 5])} (0.937)')

# Gries, Stefan Th. "Dispersions and Adjusted Frequencies in Corpora." International Journal of Corpus Linguistics, vol. 13, no. 4, 2008, p. 416.
print('Gries\'s DP:')
print(f'\t{wordless_measures_dispersion.griess_dp([3, 3, 3])} (0)')

# Lijffijt, Jefrey and Stefan Th. Gries. "Correction to Stefan Th. Gries’ “Dispersions and adjusted frequencies in corpora”" International Journal of Corpus Linguistics, vol. 17, no. 1, 2012, pp. 148.
print('Gries\'s DPnorm:')
print(f'\t{wordless_measures_dispersion.griess_dp_norm([2, 1, 0])} (0.5)')

# Adjusted Frequency
print('---------- Measures of Adjusted Frequency ----------')

# [1] Carroll, John B. "An alternative to Juilland’s usage coefficient for lexical frequencies and a proposal for a standard frequency index." Computer Studies in the Humanities and Verbal Behaviour, vol.3, no. 2, 1970, pp. 61-65.
# [2] Rosengren, Inger. "The quantitative concept of language and its relation to the structure of frequency dictionaries." Études de linguistique appliquée, no. 1, 1971, p. 115.
# [3] Engwall, Gunnel. "Fréquence Et Distribution Du Vocabulaire Dans Un Choix De Romans Français, Dissertation", Stockholm University, 1974, p. 122.
print('Juilland\'s U:')
print(f'\t[1] {wordless_measures_adjusted_freq.juillands_u([0, 4, 3, 2, 1])} (6.46)')
print(f'\t[2] {wordless_measures_adjusted_freq.juillands_u([2, 2, 2, 2, 2])} (10)')
print(f'\t[3] {wordless_measures_adjusted_freq.juillands_u([4, 2, 1, 1, 0])} (4.609)')

# [1] Carroll, John B. "An alternative to Juilland’s usage coefficient for lexical frequencies and a proposal for a standard frequency index." Computer Studies in the Humanities and Verbal Behaviour, vol.3, no. 2, 1970, pp. 61-65.
# [2] Engwall, Gunnel. "Fréquence Et Distribution Du Vocabulaire Dans Un Choix De Romans Français, Dissertation", Stockholm University, 1974, p. 122.
# [3] Gries, Stefan Th. "Dispersions and Adjusted Frequencies in Corpora." International Journal of Corpus Linguistics, vol. 13, no. 4, 2008, p. 409.
print('Carroll\'s Um:')
print(f'\t[1] {wordless_measures_adjusted_freq.carrolls_um([2, 1, 1, 1, 0])} (4.31)')
print(f'\t[2] {wordless_measures_adjusted_freq.carrolls_um([4, 2, 1, 1, 0])} (6.424)')
print(f'\t[3] {wordless_measures_adjusted_freq.carrolls_um([1, 2, 3, 4, 5])} (14.108)')

# [1] Rosengren, Inger. "The quantitative concept of language and its relation to the structure of frequency dictionaries." Études de linguistique appliquée, no. 1, 1971, p. 117.
# [2] Engwall, Gunnel. "Fréquence Et Distribution Du Vocabulaire Dans Un Choix De Romans Français, Dissertation", Stockholm University, 1974, p. 122.
# [3] Gries, Stefan Th. "Dispersions and Adjusted Frequencies in Corpora." International Journal of Corpus Linguistics, vol. 13, no. 4, 2008, p. 409.
print('Rosengren\'s KF:')
print(f'\t[1] {wordless_measures_adjusted_freq.rosengrens_kf([2, 2, 2, 2, 1])} (8.86)')
print(f'\t[2] {wordless_measures_adjusted_freq.rosengrens_kf([4, 2, 1, 1, 0])} (5.863)')
print(f'\t[2] {wordless_measures_adjusted_freq.rosengrens_kf([1, 2, 3, 4, 5])} (14.053)')

# [1] Engwall, Gunnel. "Fréquence Et Distribution Du Vocabulaire Dans Un Choix De Romans Français, Dissertation", Stockholm University, 1974, p. 122.
# [2] Gries, Stefan Th. "Dispersions and Adjusted Frequencies in Corpora." International Journal of Corpus Linguistics, vol. 13, no. 4, 2008, p. 409.
print('Engwall\'s FM:')
print(f'\t[1] {wordless_measures_adjusted_freq.engwalls_fm([4, 2, 1, 1, 0])} (6.4)')
print(f'\t[2] {wordless_measures_adjusted_freq.engwalls_fm([1, 2, 3, 4, 5])} (15)')

# Gries, Stefan Th. "Dispersions and Adjusted Frequencies in Corpora." International Journal of Corpus Linguistics, vol. 13, no. 4, 2008, p. 409.
print('Kromer\'s Ur:')
print(f'\t{wordless_measures_adjusted_freq.kromers_ur([2, 1, 1, 1, 0])} (4.50)')

# Statistical Significance
print('---------- Measures of Statistical Significance ----------')

main.settings_custom['measures']['statistical_significance'] = {
    'students_t_test_two_sample': {
        'variances': 'Equal'
    },

    'pearsons_chi_squared_test': {},

    'fishers_exact_test': {},

    'mann_whitney_u_test': {
        'direction': 'Two-tailed',
        'apply_correction': True
    }
}

# Manning, Christopher D. and Hinrich Schütze. Foundations of Statistical Natural Language Processing. MIT Press, May 1999, pp. 164-165.
print('Student\'s t-test (One Sample):')
print(f'\t{wordless_measures_statistical_significance.students_t_test_one_sample(main, 8, 15828 - 8, 4675 - 8, 14307668 - 15828 - 4675 + 8)[0]} (0.999932)')

# Dunning, Ted Emerson. "Accurate Methods for the Statistics of Surprise and Coincidence." Computational Linguistics, vol. 19, no. 1, Mar. 1993, p. 73.
# Pedersen, Ted. "Fishing for Exactness." Proceedings of the South-Central SAS Users Group Conference, 27-29 Oct. 1996, Austin, p. 10.
print('Pearson\'s Chi-squared Test:')

main.settings_custom['measures']['statistical_significance']['pearsons_chi_squared_test']['apply_correction'] = False 
print(f'\t{wordless_measures_statistical_significance.pearsons_chi_squared_test(main, 3, 0, 0, 31774)[0]} (31777.00)')

main.settings_custom['measures']['statistical_significance']['pearsons_chi_squared_test']['apply_correction'] = True 
print(f'\t{wordless_measures_statistical_significance.pearsons_chi_squared_test(main, 1, 3, 3, 1)[0:2]} (0.500, 0.480) * with Yates\'s correction for continuity')

# Dunning, Ted Emerson. "Accurate Methods for the Statistics of Surprise and Coincidence." Computational Linguistics, vol. 19, no. 1, Mar. 1993, p. 72.
print('Log-likelihood Ratio Test:')
print(f'\t{wordless_measures_statistical_significance.log_likehood_ratio_test(main, 10, 0, 3, 31764)[0]} (167.23)')

# Pedersen, Ted. "Fishing for Exactness." Proceedings of the South-Central SAS Users Group Conference, 27-29 Oct. 1996, Austin, p. 10.
print('Fisher\'s Exact Test:')

main.settings_custom['measures']['statistical_significance']['fishers_exact_test']['direction'] = 'Two-tailed' 
print(f'\t{wordless_measures_statistical_significance.fishers_exact_test(main, 1, 3, 3, 1)[1]} (0.486) * Two-tailed')

main.settings_custom['measures']['statistical_significance']['fishers_exact_test']['direction'] = 'Left-tailed' 
print(f'\t{wordless_measures_statistical_significance.fishers_exact_test(main, 1, 3, 3, 1)[1]} (0.243) * Left-tailed')

main.settings_custom['measures']['statistical_significance']['fishers_exact_test']['direction'] = 'Right-tailed' 
print(f'\t{wordless_measures_statistical_significance.fishers_exact_test(main, 1, 3, 3, 1)[1]} (0.986) * Right-tailed')

# Kilgarriff, Adam. "Comparing Corpora." International Journal of Corpus Linguistics, vol.6, no.1, Nov. 2001, p. 238.
print('Mann-Whiteney U Test:')
print(f'''\t{5 * (5 + 1) / 2
             + wordless_measures_statistical_significance.mann_whitney_u_test(main,
                                                                              [12, 15, 18, 24, 88],
                                                                              [3, 3, 13, 27, 33])[0]} (24)''')

# Bayes Factor
print('---------- Measures of Bayes Factor ----------')

# Wilson, Andrew. "Embracing Bayes Factors for Key Item Analysis in Corpus Linguistics." New Approaches to the Study of Linguistic Variability, edited by Markus Bieswanger and Amei Koll-Stobbe, Peter Lang, 2013, p. 7.
print('Bayes Factor (Log-likelihood Ratio Test):')
print(f'\t{wordless_measures_bayes_factor.bayes_factor_log_likelihood_ratio_test(22.22, 9611 + 144925)} (10.27)')

# Effect Size
print('---------- Measures of Effect Size ----------')

main.settings_custom['measures']['effect_size'] = {
    'kilgarriffs_ratio': {
        'smoothing_parameter': 1.00,
    }
}

# Church, Kenneth Ward and Patrick Hanks. Word Association Norms, Mutual Information, and Lexicography. Computational Linguistics, vol. 16, no. 1, Mar. 1990, p. 24.
print('Pointwise Mutual Information:')
print(f'\t{wordless_measures_effect_size.pmi(main, 8, 1105 - 8, 44 - 8, 15000000 - 1105 - 44 + 8)} (11.3)')

# Church, Kenneth Ward and William A. Gale. "Concordances for Parallel Text." Using Corpora: Seventh Annual Conference of the UW Centre for the New OED and Text Research, St. Catherine's College, 29 Sept - 1 Oct 1991, UW Centre for the New OED and Text Research, 1991.
print('Squared Phi Coefficient:')
print(f'\t{wordless_measures_effect_size.squared_phi_coeff(main, 31950, 12004, 4793, 848330)} (0.62)')

# Smadja, Frank, et al. "Translating Collocations for Bilingual Lexicons: A Statistical Approach." Computational Linguistics, vol. 22, no. 1, 1996, p. 13.
print('Dice\'s Coefficient:')
print(f'\t{wordless_measures_effect_size.dices_coeff(main, 130, 3121 - 130, 143 - 130, -1)} (0.08)')

# Pedersen, Ted. "Dependent Bigram Identification." Proceedings of the Fifteenth National Conference on Artificial Intelligence, Madison, 26-30 July 1998, American Association for Artificial Intelligence, 1998, p. 1197.
print('Minimum Sensitivity:')
print(f'\t{wordless_measures_effect_size.min_sensitivity(main, 17, 240, 1001, 1298742)} (0.017)')

# "Simple maths." Sketch Engine, www.sketchengine.eu/documentation/simple-maths/. Accessed 26 Nov 2018.
print('Kilgarriff\'s Ratio:')
print(f'\t{wordless_measures_effect_size.kilgarriffs_ratio(main, 35, 263, 112289776, 1559716979)} (1.1224)')

# Pojanapunya, Punjaporn and Richard Watson Todd. "Log-likelihood and Odds Ratio Keyness Statistics for Different Purposes of Keyword Analysis." Corpus Linguistics and Lingustic Theory, vol. 15, no. 1, Jan. 2016, p 154.
print('Odd\'s Ratio:')
print(f'\t{wordless_measures_effect_size.odds_ratio(main, 16217, 735, 2796938 - 16217, 2087946 - 735)} (16.6)')

# Hardie, Andrew. "Log Ratio: An Informal Introduction." The Centre for Corpus Approaches to Social Science, cass.lancs.ac.uk/log-ratio-an-informal-introduction/
print('Log Ratio:')
print(f'\t{wordless_measures_effect_size.log_ratio(main, 1, 1, 1000000 - 1, 1000000 - 1)} (0)')

# Hofland, Knut and Stig Johansson. Word Frequencies in British and American English. Norwegian Computing Centre for the Humanities, 1982, p. 471.
print('Difference Coefficient:')
print(f'\t{wordless_measures_effect_size.diff_coeff(main, 18, 35, 1000000 - 18, 1000000 - 35)} (-0.32)')

# Gabrielatos, Costas. "Keyness Analysis: Nature, Metrics and Techniques." Corpus Approaches to Discourse: A Critical Review, edited by Taylor, Charlotte and Anna Marchi, Routledge, 2018, pp. 21-22.
print('%Diff:')
print(f'\t{wordless_measures_effect_size.pct_diff(main, 20, 1, 29954 - 20, 23691 - 1)} (1481.83)')
