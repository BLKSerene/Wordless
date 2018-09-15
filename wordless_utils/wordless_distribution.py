#
# Wordless: Distribution
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
            pyplot.plot([datasets[i] for datasets in freqs], label = file['name'], **kwargs)

        pyplot.xticks(range(len(samples)), samples, rotation = 90)
        pyplot.xlabel('Samples')
        pyplot.ylabel(ylabel)
        pyplot.grid(True, color = 'silver')
        pyplot.legend()
        pyplot.show()
