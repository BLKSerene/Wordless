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

def wordless_distributions(self, files, mode):
    distributions = {}

    settings = self.settings[mode]

    for i, file in enumerate(files):
        text = wordless_text.Wordless_Text(file)

        if mode == 'wordlist':
            distribution = text.wordlist(settings)
        elif mode == 'ngram':
            distribution = text.ngram(settings)
        elif mode == 'collocation':
            distribution = text.collocation(settings)

        # Merge distributions
        for key in distributions:
            distributions[key].append(0)

        for key, value in distribution.items():
            if key not in distributions:
                distributions[key] = [0] * (i + 1)

            distributions[key][i] = value

    distributions = dict(sorted(distributions.items(), key = wordless_misc.multiple_sorting))
    
    return Wordless_Freq_Distribution(distributions)
