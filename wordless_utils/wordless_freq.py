#
# Wordless: Utility Functions for Frequency Distribution
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
#

import nltk

from wordless_utils import wordless_misc, wordless_text

class Wordless_Freq_Distribution(nltk.FreqDist):
    def _cumulative_frequencies(self, samples):
        cf = [0] * len(self[samples[0]])

        for sample in samples:
            cf = [freq_previous + freq for freq_previous, freq in zip(cf, self[sample])]
            
            yield cf

def wordless_freq_distributions(self, files, mode):
    freq_distributions = {}

    settings = self.settings[mode]

    for i, file in enumerate(files):
        for token in freq_distributions:
            freq_distributions[token].append(0)

        text = wordless_text.Wordless_Text(file)

        if mode == 'wordlist':
            freq_distribution = text.wordlist(settings)
        elif mode == 'ngram':
            freq_distribution = text.ngram(settings)
        elif mode == 'collocation':
            freq_distribution = text.collocation(settings)

        for token, freq in freq_distribution:
            if token in freq_distributions:
                freq_distributions[token][i] += freq
            else:
                freq_distributions[token] = [0] * (i + 1)
                freq_distributions[token][i] += freq

    freq_distributions = dict(sorted(freq_distributions.items(), key = wordless_misc.multiple_sorting))

    # Filter
    if settings['freq_first_min'] > 1 or settings['freq_first_max'] < float('inf'):
        freq_distributions = {token: freqs
                            for token, freqs in freq_distributions.items()
                            if settings['freq_first_min'] <= freqs[0] <= settings['freq_first_max']}

    if settings['freq_total_min'] > 1 or settings['freq_total_max'] < float('inf'):
        freq_distributions = {token: freqs
                              for token, freqs in freq_distributions.items()
                              if settings['freq_total_min'] <= sum(freqs) <= settings['freq_total_max']}

    if settings['rank_min'] > 1 or settings['rank_max'] < float('inf'):
        freq_distributions = {token: freqs
                             for i, (token, freqs) in enumerate(freq_distributions.items())
                             if settings['rank_min'] <= i + 1 <= settings['rank_max']}

    if settings['len_min'] > 1 or settings['len_max'] < float('inf'):
        freq_distributions = {token: freqs
                             for token, freqs in freq_distributions.items()
                             if settings['len_min'] <= len(token) - token.count(' ') <= settings['len_max']}

    if settings['files_min'] > 1 or settings['files_max'] < float('inf'):
        freq_distributions = {token: freqs
                              for token, freqs in freq_distributions.items()
                              if settings['files_min'] <= len([freq for freq in freqs if freq]) <= settings['files_max']}
    
    return Wordless_Freq_Distribution(freq_distributions)
