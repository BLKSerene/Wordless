#
# Wordless: Utility Functions for Distribution
#
# Copyright (C) 2018 Ye Lei
#
# For license information, see LICENSE.txt.
#

from matplotlib import pyplot
import nltk

from wordless_utils import wordless_misc, wordless_text

class Wordless_Freq_Distribution(nltk.FreqDist):
    def _cumulative_frequencies(self, samples):
        '''
        Overload to support 2-dimentional arrays
        '''
        cf = [0] * len(self[samples[0]])

        for sample in samples:
            cf = [freq_previous + freq for freq_previous, freq in zip(cf, self[sample])]
            
            yield cf

    def plot(self, files, start = 0, end = None, cumulative = False, **kwargs):
        '''
        Overload to support clipping and legend
        '''
        samples = [item for item, _ in self.most_common()][start:end]

        if cumulative:
            freqs = list(self._cumulative_frequencies(samples))
            ylabel = 'Cumulative Counts'
        else:
            freqs = [self[sample] for sample in samples]
            ylabel = 'Counts'

        for i, file in enumerate(files):
            pyplot.plot([datasets[i] for datasets in freqs], label = file.name, **kwargs)

        pyplot.xticks(range(len(samples)), samples, rotation = 90)
        pyplot.xlabel('Samples')
        pyplot.ylabel(ylabel)
        pyplot.grid(True, color = 'silver')
        pyplot.legend()
        pyplot.show()

def wordless_freq_distributions(self, files, mode):
    freq_distributions = {}

    settings = self.settings[mode]

    for i, file in enumerate(files):
        text = wordless_text.Wordless_Text(file)

        if mode == 'wordlist':
            freq_distribution = text.wordlist(settings)
        elif mode == 'ngram':
            freq_distribution = text.ngram(settings)

        # Merge frequency distributions
        for token, freq in freq_distributions.items():
            freq_distributions[token].append(0)

        for token, freq in freq_distribution.items():
            if token not in freq_distributions:
                freq_distributions[token] = [0] * (i + 1)

            freq_distributions[token][i] = freq

    freq_distributions = dict(sorted(freq_distributions.items(), key = wordless_misc.multiple_sorting))
    
    return Wordless_Freq_Distribution(freq_distributions)

def wordless_score_distributions(self, files, mode):
    score_distributions = {}

    settings = self.settings[mode]

    for i, file in enumerate(files):
        text = wordless_text.Wordless_Text(file)

        if mode == 'collocation':
            score_distribution = text.collocation(settings)

        # Merge score distributions
        for token in score_distributions:
            score_distributions[token].append(0)

        for token, score in score_distribution.items():
            if token not in score_distributions:
                score_distributions[token] = [0] * (i + 1)

            score_distributions[token][i] = score

    # Calculate the total score of all texts
    text_total = wordless_text.Wordless_Text(files)

    if mode == 'collocation':
        score_distribution_total = text_total.collocation(settings)

    # Append total scores
    for token, score in score_distribution_total.items():
        if token in score_distributions:
            score_distributions[token].append(score)

    score_distributions = dict(sorted(score_distributions.items(), key = wordless_misc.multiple_sorting))
    
    return Wordless_Freq_Distribution(score_distributions)
